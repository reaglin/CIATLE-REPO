using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;
using PreseMakerRepo.Api.Helpers;
using PreseMakerRepo.Api.Models;
using PreseMakerRepo.Api.Models.Responses;
using PreseMakerRepo.Core.Constants;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;
using PreseMakerRepo.Infrastructure.Options;

namespace PreseMakerRepo.Api.Controllers;

[ApiController]
public class SearchController : ControllerBase
{
    private readonly AppDbContext _db;
    private readonly RepositoryOptions _repo;

    public SearchController(AppDbContext db, IOptions<RepositoryOptions> repo)
    {
        _db = db;
        _repo = repo.Value;
    }

    // GET /api/v1/search
    [HttpGet("api/v1/search")]
    public async Task<IActionResult> Search(
        [FromQuery] string? q,
        [FromQuery] string level = "all",
        [FromQuery] string? level1 = null,
        [FromQuery] string? level2 = null,
        [FromQuery] string? level3 = null,
        [FromQuery] string? courseId = null,
        [FromQuery] string? materialType = null,
        [FromQuery] string sort = "newest",
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 20)
    {
        if (string.IsNullOrWhiteSpace(q) || q.Trim().Length < 2)
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.QueryTooShort, "Search query must be at least 2 characters."));

        pageSize = Math.Clamp(pageSize, 1, _repo.MaxPageSize);
        page = Math.Max(page, 1);

        var term = q.Trim();
        var pattern = $"%{term}%";
        var includeModules = level is "all" or "module";
        var includeMaterials = level is "all" or "material";

        // Resolve leaf taxonomy keys once — used by both module and material queries
        var leafKeys = await ResolveLeafKeysAsync(level1, level2, level3);

        // Resolve course IDs for the leaf keys (needed to filter materials through their module)
        List<string>? taxCourseIds = null;
        if (leafKeys is not null)
        {
            taxCourseIds = await _db.TaxonomyCourses
                .AsNoTracking()
                .Where(c => leafKeys.Contains(c.Level3Key!))
                .Select(c => c.CourseId)
                .ToListAsync();
        }

        var results = new List<SearchResultDto>();

        if (includeModules)
        {
            IQueryable<Module> modQuery = _db.Modules
                .AsNoTracking()
                .Where(m => m.Status == ContentStatus.Published &&
                            m.Id != WellKnownIds.OrphanModuleId &&
                            (EF.Functions.Like(m.Title, pattern) ||
                             EF.Functions.Like(m.Description, pattern) ||
                             EF.Functions.Like(m.OutcomesJson, pattern) ||
                             EF.Functions.Like(m.TopicHierarchyJson, pattern) ||
                             EF.Functions.Like(m.CourseId, pattern)))
                .Include(m => m.Contributor)
                .Include(m => m.Course)
                    .ThenInclude(c => c.Level3Node!)
                        .ThenInclude(n => n.Parent!)
                            .ThenInclude(n => n.Parent);

            if (taxCourseIds is not null)
                modQuery = modQuery.Where(m => taxCourseIds.Contains(m.CourseId));

            if (courseId is not null)
                modQuery = modQuery.Where(m => m.CourseId == courseId.ToUpperInvariant());

            var modules = await modQuery.ToListAsync();

            results.AddRange(modules.Select(m => new SearchResultDto(
                ResultType: "module",
                ModuleId: m.Id,
                CourseId: m.CourseId,
                Title: m.Title,
                Description: m.Description,
                Contributor: new ContributorBriefDto(
                    m.Contributor.UserName!, m.Contributor.DisplayName,
                    m.Contributor.InstitutionName, m.Contributor.IsEduVerified),
                SubmittedUtc: m.SubmittedUtc,
                TaxonomyPath: BuildTaxonomyPath(m.Course.Level3Node),
                MaterialId: null,
                MaterialType: null,
                FileName: null,
                ModuleTitle: null)));
        }

        if (includeMaterials)
        {
            IQueryable<Material> matQuery = _db.Materials
                .AsNoTracking()
                .Where(m => m.Status == ContentStatus.Published &&
                            (EF.Functions.Like(m.Title, pattern) ||
                             EF.Functions.Like(m.Description ?? string.Empty, pattern)))
                .Include(m => m.Contributor)
                .Include(m => m.Module)
                    .ThenInclude(mod => mod.Course)
                        .ThenInclude(c => c.Level3Node!)
                            .ThenInclude(n => n.Parent!)
                                .ThenInclude(n => n.Parent);

            if (taxCourseIds is not null)
                matQuery = matQuery.Where(m => taxCourseIds.Contains(m.Module.CourseId));

            if (courseId is not null)
                matQuery = matQuery.Where(m => m.Module.CourseId == courseId.ToUpperInvariant());

            if (materialType is not null && Enum.TryParse<MaterialType>(materialType, ignoreCase: true, out var parsedType))
                matQuery = matQuery.Where(m => m.Type == parsedType);

            var materials = await matQuery.ToListAsync();

            results.AddRange(materials.Select(m => new SearchResultDto(
                ResultType: "material",
                ModuleId: m.ModuleId,
                CourseId: m.Module.CourseId,
                Title: m.Title,
                Description: m.Description,
                Contributor: new ContributorBriefDto(
                    m.Contributor.UserName!, m.Contributor.DisplayName,
                    m.Contributor.InstitutionName, m.Contributor.IsEduVerified),
                SubmittedUtc: m.SubmittedUtc,
                TaxonomyPath: BuildTaxonomyPath(m.Module.Course.Level3Node),
                MaterialId: m.Id,
                MaterialType: m.Type.ToString(),
                FileName: m.FileName,
                ModuleTitle: m.Module.Title)));
        }

        var ordered = sort == "oldest"
            ? results.OrderBy(r => r.SubmittedUtc)
            : results.OrderByDescending(r => r.SubmittedUtc);

        var total = results.Count;
        var items = ordered.Skip((page - 1) * pageSize).Take(pageSize).ToList();

        return Ok(ApiResponse<PagedResult<SearchResultDto>>.Ok(
            new PagedResult<SearchResultDto>(items, total, page, pageSize,
                (int)Math.Ceiling(total / (double)pageSize))));
    }

    // ── Helpers ───────────────────────────────────────────────────────────────

    private async Task<List<string>?> ResolveLeafKeysAsync(string? l1, string? l2, string? l3)
    {
        if (l3 is not null) return [l3];
        if (l2 is not null) return [l2];
        if (l1 is not null)
        {
            return await _db.Set<TaxonomyNode>()
                .AsNoTracking()
                .Where(n => n.ParentKey == l1 || n.Key == l1)
                .Select(n => n.Key)
                .ToListAsync();
        }
        return null;
    }

    private static TaxonomyPathDto? BuildTaxonomyPath(TaxonomyNode? leafNode)
    {
        if (leafNode is null) return null;

        NodeParentDto? l1 = null, l2 = null, l3 = null;

        if (leafNode.Level == 3)
        {
            l3 = new NodeParentDto(leafNode.Key, leafNode.Name);
            if (leafNode.Parent is not null)
            {
                l2 = new NodeParentDto(leafNode.Parent.Key, leafNode.Parent.Name);
                if (leafNode.Parent.Parent is not null)
                    l1 = new NodeParentDto(leafNode.Parent.Parent.Key, leafNode.Parent.Parent.Name);
            }
        }
        else if (leafNode.Level == 2)
        {
            l2 = new NodeParentDto(leafNode.Key, leafNode.Name);
            if (leafNode.Parent is not null)
                l1 = new NodeParentDto(leafNode.Parent.Key, leafNode.Parent.Name);
        }

        return new TaxonomyPathDto(l1, l2, l3);
    }
}
