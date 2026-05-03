using FluentValidation;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;
using PreseMakerRepo.Api.Helpers;
using PreseMakerRepo.Api.Models;
using PreseMakerRepo.Api.Models.Requests;
using PreseMakerRepo.Api.Models.Responses;
using PreseMakerRepo.Core.Constants;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Core.Interfaces;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;
using PreseMakerRepo.Infrastructure.Options;
using System.Text.Json;

namespace PreseMakerRepo.Api.Controllers;

[ApiController]
[Route("api/v1/courses")]
public class CoursesController : ControllerBase
{
    private readonly AppDbContext _db;
    private readonly ITaxonomyService _taxonomy;
    private readonly IStorageService _storage;
    private readonly RepositoryOptions _repo;
    private readonly StorageOptions _storageOpts;
    private readonly UserManager<Contributor> _userManager;

    public CoursesController(
        AppDbContext db,
        ITaxonomyService taxonomy,
        IStorageService storage,
        IOptions<RepositoryOptions> repo,
        IOptions<StorageOptions> storageOpts,
        UserManager<Contributor> userManager)
    {
        _db = db;
        _taxonomy = taxonomy;
        _storage = storage;
        _repo = repo.Value;
        _storageOpts = storageOpts.Value;
        _userManager = userManager;
    }

    // GET /api/v1/courses
    [HttpGet]
    public async Task<IActionResult> ListCourses(
        [FromQuery] string? level1 = null,
        [FromQuery] string? level2 = null,
        [FromQuery] string? level3 = null,
        [FromQuery] string sort = "newest",
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 20)
    {
        pageSize = Math.Clamp(pageSize, 1, _repo.MaxPageSize);
        page = Math.Max(page, 1);

        var leafKeys = await ResolveLeafKeysAsync(level1, level2, level3);

        var query = _db.TaxonomyCourses
            .AsNoTracking()
            .Where(c => c.Level3Key != null &&
                        c.CourseId != WellKnownIds.OrphanCourseId &&
                        _db.Modules.Any(m => m.CourseId == c.CourseId && m.Status == ContentStatus.Published));

        if (leafKeys is not null)
            query = query.Where(c => leafKeys.Contains(c.Level3Key!));

        var courseIds = await query.Select(c => c.CourseId).ToListAsync();
        var total = courseIds.Count;

        var aggregates = await GetCourseAggregatesAsync(courseIds);

        var ordered = sort == "oldest"
            ? aggregates.OrderBy(a => a.NewestDate).ThenBy(a => a.CourseId)
            : aggregates.OrderByDescending(a => a.NewestDate).ThenBy(a => a.CourseId);

        var paged = ordered.Skip((page - 1) * pageSize).Take(pageSize).ToList();
        var courseDetails = await _db.TaxonomyCourses.AsNoTracking()
            .Where(c => paged.Select(p => p.CourseId).Contains(c.CourseId))
            .ToDictionaryAsync(c => c.CourseId);

        var items = paged.Select(a =>
        {
            var c = courseDetails[a.CourseId];
            return new CourseListItem(c.CourseId, c.Title, c.CreditHours,
                a.ModuleCount, a.MaterialCount, a.NewestDate, c.CurriculumGuideUrl);
        }).ToList();

        return Ok(ApiResponse<PagedResult<CourseListItem>>.Ok(
            new PagedResult<CourseListItem>(items, total, page, pageSize,
                (int)Math.Ceiling(total / (double)pageSize))));
    }

    // GET /api/v1/courses/recent
    [HttpGet("recent")]
    public async Task<IActionResult> GetRecent(
        [FromQuery] int count = 0,
        [FromQuery] string? level1 = null,
        [FromQuery] string? level2 = null,
        [FromQuery] string? level3 = null)
    {
        if (count <= 0) count = _repo.RecentModulesDefaultCount;
        count = Math.Clamp(count, 1, 50);

        var leafKeys = await ResolveLeafKeysAsync(level1, level2, level3);

        var query = _db.Modules
            .AsNoTracking()
            .Where(m => m.Status == ContentStatus.Published &&
                        m.Id != WellKnownIds.OrphanModuleId);

        if (leafKeys is not null)
        {
            var courseIdsInLeaf = await _db.TaxonomyCourses
                .AsNoTracking()
                .Where(c => leafKeys.Contains(c.Level3Key!))
                .Select(c => c.CourseId)
                .ToListAsync();
            query = query.Where(m => courseIdsInLeaf.Contains(m.CourseId));
        }

        var modules = await query
            .OrderByDescending(m => m.SubmittedUtc)
            .Take(count)
            .Include(m => m.Contributor)
            .Include(m => m.Materials)
            .ToListAsync();

        var summaries = modules.Select(m => ToModuleSummary(m, Request)).ToList();
        return Ok(ApiResponse<RecentModulesResponse>.Ok(new RecentModulesResponse(summaries)));
    }

    // GET /api/v1/courses/{courseId}
    [HttpGet("{courseId}")]
    public async Task<IActionResult> GetCourse(string courseId)
    {
        var course = await _db.TaxonomyCourses
            .AsNoTracking()
            .Include(c => c.Level3Node)
                .ThenInclude(n => n!.Parent)
                    .ThenInclude(n => n!.Parent)
            .FirstOrDefaultAsync(c => c.CourseId == courseId.ToUpperInvariant());

        if (course is null || course.CourseId == WellKnownIds.OrphanCourseId)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.CourseNotFound, "Course not found."));

        var modules = await _db.Modules
            .AsNoTracking()
            .Where(m => m.CourseId == course.CourseId && m.Status == ContentStatus.Published)
            .Include(m => m.Contributor)
            .Include(m => m.Materials)
            .OrderByDescending(m => m.SubmittedUtc)
            .ToListAsync();

        var materialCount = modules.Sum(m => m.Materials.Count(mat => mat.Status == ContentStatus.Published));
        var newestDate = modules.Any() ? modules.Max(m => m.SubmittedUtc) : (DateTime?)null;

        var path = BuildTaxonomyPath(course.Level3Node);
        var moduleDtos = modules.Select(m => ToModuleSummary(m, Request)).ToList();

        var detail = new CourseDetailResponse(
            course.CourseId, course.Title, course.CreditHours,
            path, course.CurriculumGuideUrl,
            modules.Count, materialCount, newestDate,
            moduleDtos);

        return Ok(ApiResponse<CourseDetailResponse>.Ok(detail));
    }

    // GET /api/v1/courses/{courseId}/download
    [HttpGet("{courseId}/download")]
    public async Task<IActionResult> DownloadCourse(string courseId)
    {
        var course = await _db.TaxonomyCourses.FindAsync(courseId.ToUpperInvariant());
        if (course is null || course.CourseId == WellKnownIds.OrphanCourseId)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.CourseNotFound, "Course not found."));

        var stream = await _storage.BuildCourseZipAsync(course.CourseId);
        if (stream == Stream.Null)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.CourseNotFound, "No published materials found for this course."));

        var shortId = course.CourseId[..Math.Min(course.CourseId.Length, 8)];
        return File(stream, "application/zip",
            $"{course.CourseId}_course_{shortId}.zip");
    }

    // GET /api/v1/courses/{courseId}/modules
    [HttpGet("{courseId}/modules")]
    public async Task<IActionResult> ListModules(
        string courseId,
        [FromQuery] string sort = "newest",
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 20)
    {
        pageSize = Math.Clamp(pageSize, 1, _repo.MaxPageSize);
        page = Math.Max(page, 1);

        var course = await _db.TaxonomyCourses.FindAsync(courseId.ToUpperInvariant());
        if (course is null || course.CourseId == WellKnownIds.OrphanCourseId)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.CourseNotFound, "Course not found."));

        var query = _db.Modules
            .AsNoTracking()
            .Where(m => m.CourseId == course.CourseId && m.Status == ContentStatus.Published);

        var total = await query.CountAsync();

        query = sort == "oldest"
            ? query.OrderBy(m => m.SubmittedUtc)
            : query.OrderByDescending(m => m.SubmittedUtc);

        var modules = await query
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .Include(m => m.Contributor)
            .Include(m => m.Materials)
            .ToListAsync();

        var items = modules.Select(m => ToModuleSummary(m, Request)).ToList();
        return Ok(ApiResponse<PagedResult<ModuleSummaryDto>>.Ok(
            new PagedResult<ModuleSummaryDto>(items, total, page, pageSize,
                (int)Math.Ceiling(total / (double)pageSize))));
    }

    // GET /api/v1/courses/{courseId}/modules/{moduleId}
    [HttpGet("{courseId}/modules/{moduleId:guid}")]
    public async Task<IActionResult> GetModule(string courseId, Guid moduleId)
    {
        var module = await _db.Modules
            .AsNoTracking()
            .Where(m => m.Id == moduleId &&
                        m.CourseId == courseId.ToUpperInvariant() &&
                        m.Status == ContentStatus.Published)
            .Include(m => m.Contributor)
            .Include(m => m.Materials)
            .FirstOrDefaultAsync();

        if (module is null)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.ModuleNotFound, "Module not found."));

        var outcomes = ParseJsonArray(module.OutcomesJson);
        var topicHierarchy = ParseJsonObjects(module.TopicHierarchyJson);

        var materials = module.Materials
            .Where(mat => mat.Status == ContentStatus.Published)
            .Select(mat => new MaterialDto(
                mat.Id, mat.Title, mat.Type.ToString(), mat.Description,
                mat.FileName, mat.FileSizeBytes, mat.ContentType,
                BuildMaterialDownloadUrl(Request, courseId, moduleId, mat.Id)))
            .ToList();

        var downloadAllUrl = BuildModuleDownloadUrl(Request, courseId, moduleId);

        var detail = new ModuleDetailResponse(
            module.Id, module.CourseId, module.Title, module.Description ?? string.Empty,
            outcomes, topicHierarchy,
            new ContributorBriefDto(module.Contributor.UserName!, module.Contributor.DisplayName,
                module.Contributor.InstitutionName, module.Contributor.IsEduVerified),
            module.License.ToString(),
            LicenseHelper.DisplayName(module.License),
            LicenseHelper.Url(module.License),
            module.SubmittedUtc, module.UpdatedUtc,
            module.Status.ToString(),
            materials, downloadAllUrl);

        return Ok(ApiResponse<ModuleDetailResponse>.Ok(detail));
    }

    // GET /api/v1/courses/{courseId}/modules/{moduleId}/download
    [HttpGet("{courseId}/modules/{moduleId:guid}/download")]
    public async Task<IActionResult> DownloadModule(string courseId, Guid moduleId)
    {
        var module = await _db.Modules
            .AsNoTracking()
            .FirstOrDefaultAsync(m => m.Id == moduleId &&
                                      m.CourseId == courseId.ToUpperInvariant() &&
                                      m.Status == ContentStatus.Published);

        if (module is null)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.ModuleNotFound, "Module not found."));

        var stream = await _storage.BuildModuleZipAsync(moduleId);
        if (stream == Stream.Null)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.ModuleNotFound, "No published materials found for this module."));

        return File(stream, "application/zip",
            $"{courseId}_{moduleId:N}.zip");
    }

    // GET /api/v1/courses/{courseId}/modules/{moduleId}/materials/{materialId}/download
    [HttpGet("{courseId}/modules/{moduleId:guid}/materials/{materialId:guid}/download")]
    public async Task<IActionResult> DownloadMaterial(string courseId, Guid moduleId, Guid materialId)
    {
        var material = await _db.Materials
            .AsNoTracking()
            .FirstOrDefaultAsync(m => m.Id == materialId &&
                                      m.ModuleId == moduleId &&
                                      m.Status == ContentStatus.Published);

        if (material is null)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.MaterialNotFound, "Material not found."));

        var stream = await _storage.ReadMaterialAsync(material.StoragePath);
        return File(stream, material.ContentType,
            material.FileName);
    }

    // GET /api/v1/courses/{courseId}/guide
    [HttpGet("{courseId}/guide")]
    public async Task<IActionResult> GetCurriculumGuide(string courseId)
    {
        var guide = await _db.CurriculumGuides.AsNoTracking()
            .FirstOrDefaultAsync(g => g.CourseId == courseId.ToUpperInvariant());

        if (guide is null)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.GuideNotFound, "No curriculum guide found for this course."));

        return Ok(ApiResponse<CurriculumGuideDto>.Ok(new CurriculumGuideDto(
            guide.CourseId,
            guide.Title,
            guide.HtmlContent,
            guide.Credits,
            guide.ContactHours,
            guide.Prerequisites,
            guide.Version,
            guide.GeneratedUtc,
            guide.UpdatedUtc)));
    }

    // PUT /api/v1/courses/{courseId}/guide
    [Authorize(Policy = "AdminOnly")]
    [HttpPut("{courseId}/guide")]
    public async Task<IActionResult> UpsertCurriculumGuide(
        string courseId,
        [FromBody] UpsertCurriculumGuideRequest request,
        [FromServices] IValidator<UpsertCurriculumGuideRequest> validator)
    {
        var vResult = await validator.ValidateAsync(request);
        if (!vResult.IsValid) return BadRequest(ValidationError(vResult));

        var normalizedId = courseId.ToUpperInvariant();

        // (1) Course already known — proceed directly.
        // (2) Explicit taxonomy key supplied — validate it and create the course.
        // (3) Prefix matches a taxonomy node — create the course there.
        // (4) None resolved — reject with a descriptive error.
        if (await _db.TaxonomyCourses.FindAsync(normalizedId) is null)
        {
            string? resolvedKey = null;

            if (request.TaxonomyKey is not null)
            {
                var key = request.TaxonomyKey.ToUpperInvariant();
                if (!await _db.TaxonomyNodes.AnyAsync(n => n.Key == key))
                    return UnprocessableEntity(ApiResponse<object?>.Fail(
                        ErrorCodes.TaxonomyNodeNotFound,
                        $"Taxonomy key '{request.TaxonomyKey}' does not exist."));
                resolvedKey = key;
            }
            else
            {
                var prefix = ExtractCoursePrefix(normalizedId);
                if (prefix is not null && await _db.TaxonomyNodes.AnyAsync(n => n.Key == prefix))
                    resolvedKey = prefix;
            }

            if (resolvedKey is null)
                return UnprocessableEntity(ApiResponse<object?>.Fail(
                    ErrorCodes.TaxonomyPlacementRequired,
                    "Course not found and taxonomy placement could not be determined from the course ID. " +
                    "Please specify the taxonomy node key via the 'taxonomyKey' field."));

            _db.TaxonomyCourses.Add(new TaxonomyCourse
            {
                CourseId = normalizedId,
                Title = normalizedId,
                Level3Key = resolvedKey,
                IsActive = true
            });
        }

        var existing = await _db.CurriculumGuides
            .FirstOrDefaultAsync(g => g.CourseId == normalizedId);

        var now = DateTime.UtcNow;

        if (existing is null)
        {
            _db.CurriculumGuides.Add(new Core.Models.CurriculumGuide
            {
                CourseId = normalizedId,
                Title = request.Title,
                HtmlContent = request.HtmlContent,
                Credits = request.Credits,
                ContactHours = request.ContactHours,
                Prerequisites = request.Prerequisites,
                Version = request.Version,
                GeneratedUtc = request.GeneratedUtc ?? now,
                UpdatedUtc = now
            });
        }
        else
        {
            existing.Title = request.Title;
            existing.HtmlContent = request.HtmlContent;
            existing.Credits = request.Credits;
            existing.ContactHours = request.ContactHours;
            existing.Prerequisites = request.Prerequisites;
            existing.Version = request.Version;
            existing.GeneratedUtc = request.GeneratedUtc ?? existing.GeneratedUtc;
            existing.UpdatedUtc = now;
        }

        await _db.SaveChangesAsync();
        return Ok(ApiResponse<MessageResponse>.Ok(new MessageResponse("Curriculum guide saved.")));
    }

    // ── Helpers ──────────────────────────────────────────────────────────────

    private async Task<List<string>?> ResolveLeafKeysAsync(string? level1, string? level2, string? level3)
    {
        if (level3 is not null) return [level3];
        if (level2 is not null) return [level2];
        if (level1 is not null)
        {
            return await _db.Set<Core.Models.TaxonomyNode>()
                .AsNoTracking()
                .Where(n => n.ParentKey == level1 || n.Key == level1)
                .Select(n => n.Key)
                .ToListAsync();
        }
        return null;
    }

    private async Task<List<CourseAggregate>> GetCourseAggregatesAsync(IEnumerable<string> courseIds)
    {
        return await _db.Modules
            .AsNoTracking()
            .Where(m => courseIds.Contains(m.CourseId) && m.Status == ContentStatus.Published)
            .GroupBy(m => m.CourseId)
            .Select(g => new CourseAggregate(
                g.Key,
                g.Count(),
                g.SelectMany(m => m.Materials).Count(mat => mat.Status == ContentStatus.Published),
                g.Max(m => (DateTime?)m.SubmittedUtc)))
            .ToListAsync();
    }

    private static ModuleSummaryDto ToModuleSummary(Core.Models.Module m, HttpRequest request)
    {
        var published = m.Materials.Where(mat => mat.Status == ContentStatus.Published).ToList();
        var types = published.Select(mat => mat.Type.ToString()).Distinct().ToList();
        return new ModuleSummaryDto(
            m.Id, m.Title,
            new ContributorBriefDto(m.Contributor.UserName!, m.Contributor.DisplayName,
                m.Contributor.InstitutionName, m.Contributor.IsEduVerified),
            m.License.ToString(),
            LicenseHelper.DisplayName(m.License),
            LicenseHelper.Url(m.License),
            m.SubmittedUtc,
            published.Count,
            types);
    }

    private static TaxonomyPathDto? BuildTaxonomyPath(Core.Models.TaxonomyNode? leafNode)
    {
        if (leafNode is null) return null;

        // For 2-level taxonomy: leafNode is level 2, parent is level 1
        // For 3-level taxonomy: leafNode is level 3, parent is level 2, grandparent is level 1
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

    private static string BuildMaterialDownloadUrl(HttpRequest req, string courseId, Guid moduleId, Guid materialId) =>
        $"{req.Scheme}://{req.Host}/api/v1/courses/{courseId}/modules/{moduleId}/materials/{materialId}/download";

    private static string BuildModuleDownloadUrl(HttpRequest req, string courseId, Guid moduleId) =>
        $"{req.Scheme}://{req.Host}/api/v1/courses/{courseId}/modules/{moduleId}/download";

    private static IReadOnlyList<string> ParseJsonArray(string json)
    {
        try { return JsonSerializer.Deserialize<List<string>>(json) ?? []; }
        catch { return []; }
    }

    private static IReadOnlyList<object> ParseJsonObjects(string json)
    {
        try { return JsonSerializer.Deserialize<List<object>>(json) ?? []; }
        catch { return []; }
    }

    private record CourseAggregate(string CourseId, int ModuleCount, int MaterialCount, DateTime? NewestDate);

    // ── Write Endpoints ───────────────────────────────────────────────────────

    // POST /api/v1/courses/{courseId}/publish  (bulk course-level publish)
    [Authorize(Policy = "ContributorOnly")]
    [HttpPost("{courseId}/publish")]
    [RequestSizeLimit(524_288_000)]
    public async Task<IActionResult> PublishCourse(
        string courseId,
        [FromServices] IValidator<PublishModuleRequest> moduleValidator)
    {
        var userId = ClaimsHelper.GetUserId(User);
        var contributor = await _userManager.FindByIdAsync(userId!);
        if (contributor is null) return Unauthorized();
        if (contributor.IsSuspended)
            return StatusCode(403, ApiResponse<object?>.Fail(ErrorCodes.AccountSuspended, "Account is suspended."));
        if (!contributor.EmailConfirmed)
            return StatusCode(403, ApiResponse<object?>.Fail(ErrorCodes.EmailNotConfirmed, "Email not confirmed."));

        var normalizedId = courseId.ToUpperInvariant();
        var validation = await _taxonomy.ValidateCourseIdAsync(normalizedId);
        if (!validation.IsValid)
            return UnprocessableEntity(ApiResponse<object?>.Fail(ErrorCodes.InvalidCourseId, "Course ID not found in taxonomy."));

        if (!Request.HasFormContentType)
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "Request must be multipart/form-data."));

        var form = await Request.ReadFormAsync();
        var metadataPart = form["metadata"].FirstOrDefault();
        if (metadataPart is null)
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "Missing 'metadata' form field."));

        CoursePublishRequest? courseRequest;
        try { courseRequest = JsonSerializer.Deserialize<CoursePublishRequest>(metadataPart, JsonOpts); }
        catch { return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "Invalid metadata JSON.")); }

        if (courseRequest is null || courseRequest.Modules is null || courseRequest.Modules.Count == 0)
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "At least one module is required."));

        long totalBytes = form.Files.Sum(f => f.Length);
        if (totalBytes > _storageOpts.MaxModuleSizeBytes)
            return StatusCode(413, ApiResponse<object?>.Fail(ErrorCodes.SubmissionTooLarge, "Total upload size exceeds limit."));

        int modulesPublished = 0, materialsPublished = 0;
        foreach (var moduleReq in courseRequest.Modules)
        {
            var vResult = await moduleValidator.ValidateAsync(moduleReq);
            if (!vResult.IsValid)
                return BadRequest(ValidationError(vResult));

            var (mod, matCount) = await SaveModuleAsync(normalizedId, userId!, moduleReq, form);
            modulesPublished++;
            materialsPublished += matCount;
        }

        await _db.SaveChangesAsync();

        var guideStatus = await EnsureGuideStubAsync(normalizedId);

        return StatusCode(201, ApiResponse<object>.Ok(new
        {
            courseId = normalizedId,
            modulesPublished,
            materialsPublished,
            guideStatus,
            courseUrl = $"{Request.Scheme}://{Request.Host}/courses/{normalizedId}"
        }));
    }

    // POST /api/v1/courses/{courseId}/modules
    [Authorize(Policy = "ContributorOnly")]
    [HttpPost("{courseId}/modules")]
    [RequestSizeLimit(524_288_000)]
    public async Task<IActionResult> PublishModule(
        string courseId,
        [FromServices] IValidator<PublishModuleRequest> validator)
    {
        var userId = ClaimsHelper.GetUserId(User);
        var contributor = await _userManager.FindByIdAsync(userId!);
        if (contributor is null) return Unauthorized();
        if (contributor.IsSuspended)
            return StatusCode(403, ApiResponse<object?>.Fail(ErrorCodes.AccountSuspended, "Account is suspended."));
        if (!contributor.EmailConfirmed)
            return StatusCode(403, ApiResponse<object?>.Fail(ErrorCodes.EmailNotConfirmed, "Email not confirmed."));

        var normalizedId = courseId.ToUpperInvariant();
        var courseValidation = await _taxonomy.ValidateCourseIdAsync(normalizedId);
        if (!courseValidation.IsValid)
            return UnprocessableEntity(ApiResponse<object?>.Fail(ErrorCodes.InvalidCourseId, "Course ID not found in taxonomy."));

        if (!Request.HasFormContentType)
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "Request must be multipart/form-data."));

        var form = await Request.ReadFormAsync();
        var metadataPart = form["metadata"].FirstOrDefault();
        if (metadataPart is null)
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "Missing 'metadata' form field."));

        PublishModuleRequest? req;
        try { req = JsonSerializer.Deserialize<PublishModuleRequest>(metadataPart, JsonOpts); }
        catch { return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "Invalid metadata JSON.")); }

        if (req is null) return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "Empty metadata."));

        var vResult = await validator.ValidateAsync(req);
        if (!vResult.IsValid) return BadRequest(ValidationError(vResult));

        long totalBytes = form.Files.Sum(f => f.Length);
        if (totalBytes > _storageOpts.MaxModuleSizeBytes)
            return StatusCode(413, ApiResponse<object?>.Fail(ErrorCodes.SubmissionTooLarge, "Total upload size exceeds limit."));

        var (module, _) = await SaveModuleAsync(normalizedId, userId!, req, form);
        await _db.SaveChangesAsync();

        var guideStatus = await EnsureGuideStubAsync(normalizedId);

        return StatusCode(201, ApiResponse<object>.Ok(new
        {
            moduleId = module.Id,
            courseId = normalizedId,
            materialsPublished = module.Materials.Count,
            guideStatus,
            moduleUrl = $"{Request.Scheme}://{Request.Host}/api/v1/courses/{normalizedId}/modules/{module.Id}"
        }));
    }

    // PUT /api/v1/courses/{courseId}/modules/{moduleId}
    [Authorize]
    [HttpPut("{courseId}/modules/{moduleId:guid}")]
    [RequestSizeLimit(524_288_000)]
    public async Task<IActionResult> UpdateModule(
        string courseId, Guid moduleId,
        [FromServices] IValidator<UpdateModuleRequest> validator)
    {
        var module = await _db.Modules
            .Include(m => m.Materials)
            .FirstOrDefaultAsync(m => m.Id == moduleId &&
                                      m.CourseId == courseId.ToUpperInvariant() &&
                                      m.Status != ContentStatus.Removed);
        if (module is null)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.ModuleNotFound, "Module not found."));

        var userId = ClaimsHelper.GetUserId(User);
        if (module.ContributorId != userId && !User.IsInRole("Administrator"))
            return StatusCode(403, ApiResponse<object?>.Fail(ErrorCodes.Forbidden, "You do not own this module."));

        if (!Request.HasFormContentType)
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "Request must be multipart/form-data."));

        var form = await Request.ReadFormAsync();
        var metadataPart = form["metadata"].FirstOrDefault();
        if (metadataPart is null)
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "Missing 'metadata' form field."));

        UpdateModuleRequest? req;
        try { req = JsonSerializer.Deserialize<UpdateModuleRequest>(metadataPart, JsonOpts); }
        catch { return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "Invalid metadata JSON.")); }

        if (req is null) return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "Empty metadata."));

        var vResult = await validator.ValidateAsync(req);
        if (!vResult.IsValid) return BadRequest(ValidationError(vResult));

        if (req.Title is not null) module.Title = req.Title;
        if (req.Description is not null) module.Description = req.Description;
        if (req.Outcomes is not null) module.OutcomesJson = JsonSerializer.Serialize(req.Outcomes);
        if (req.TopicHierarchy is not null) module.TopicHierarchyJson = JsonSerializer.Serialize(req.TopicHierarchy);
        if (req.License is not null && Enum.TryParse<LicenseType>(req.License, ignoreCase: true, out var lic))
            module.License = lic;
        module.UpdatedUtc = DateTime.UtcNow;

        // Replace file parts for any material whose filePartName is present
        if (req.Materials is not null)
        {
            foreach (var matMeta in req.Materials)
            {
                var file = form.Files.GetFile(matMeta.FilePartName);
                if (file is null) continue;

                var existing = module.Materials.FirstOrDefault(m =>
                    m.FileName == matMeta.FilePartName || m.Title == matMeta.Title);
                if (existing is null) continue;

                if (file.Length > _storageOpts.MaxMaterialSizeBytes)
                    return StatusCode(413, ApiResponse<object?>.Fail(ErrorCodes.MaterialTooLarge, $"File '{file.FileName}' exceeds size limit."));

                await using var stream = file.OpenReadStream();
                var path = await _storage.SaveMaterialAsync(module.Id, existing.Id, file.FileName, stream);
                existing.StoragePath = path;
                existing.FileSizeBytes = file.Length;
                existing.ContentType = file.ContentType;
                existing.FileName = file.FileName;
                existing.UpdatedUtc = DateTime.UtcNow;
            }
        }

        await _db.SaveChangesAsync();
        return Ok(ApiResponse<object>.Ok(new { moduleId = module.Id, message = "Module updated." }));
    }

    // DELETE /api/v1/courses/{courseId}/modules/{moduleId}
    [Authorize]
    [HttpDelete("{courseId}/modules/{moduleId:guid}")]
    public async Task<IActionResult> DeleteModule(string courseId, Guid moduleId)
    {
        var module = await _db.Modules
            .FirstOrDefaultAsync(m => m.Id == moduleId &&
                                      m.CourseId == courseId.ToUpperInvariant() &&
                                      m.Status != ContentStatus.Removed);
        if (module is null)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.ModuleNotFound, "Module not found."));

        var userId = ClaimsHelper.GetUserId(User);
        if (module.ContributorId != userId && !User.IsInRole("Administrator"))
            return StatusCode(403, ApiResponse<object?>.Fail(ErrorCodes.Forbidden, "You do not own this module."));

        module.Status = ContentStatus.Removed;
        module.RemovedUtc = DateTime.UtcNow;
        await _db.SaveChangesAsync();

        return Ok(ApiResponse<MessageResponse>.Ok(new MessageResponse("Module retracted.")));
    }

    // ── Private write helpers ─────────────────────────────────────────────────

    private static readonly JsonSerializerOptions JsonOpts = new() { PropertyNameCaseInsensitive = true };

    private async Task<(Module module, int materialCount)> SaveModuleAsync(
        string courseId, string userId, PublishModuleRequest req, IFormCollection form)
    {
        var course = await _db.TaxonomyCourses.FindAsync(courseId)
            ?? _db.TaxonomyCourses.Add(new TaxonomyCourse
            {
                CourseId = courseId,
                Title = courseId,
                IsActive = true
            }).Entity;

        Enum.TryParse<LicenseType>(req.License, ignoreCase: true, out var license);

        var module = new Module
        {
            Id = Guid.NewGuid(),
            CourseId = courseId,
            ContributorId = userId,
            Title = req.Title,
            Description = req.Description,
            OutcomesJson = JsonSerializer.Serialize(req.Outcomes ?? []),
            TopicHierarchyJson = JsonSerializer.Serialize(req.TopicHierarchy ?? []),
            License = license,
            Status = ContentStatus.Published,
            SubmittedUtc = DateTime.UtcNow
        };
        _db.Modules.Add(module);

        int materialCount = 0;
        foreach (var matMeta in req.Materials)
        {
            if (!MaterialTypeHelper.TryParse(matMeta.Type, out var matType)) continue;

            var file = form.Files.GetFile(matMeta.FilePartName);
            if (file is null) continue;

            Enum.TryParse<LicenseType>(req.License, ignoreCase: true, out var matLicense);
            var materialId = Guid.NewGuid();
            await using var stream = file.OpenReadStream();
            var storagePath = await _storage.SaveMaterialAsync(module.Id, materialId, file.FileName, stream);

            var material = new Material
            {
                Id = materialId,
                ModuleId = module.Id,
                ContributorId = userId,
                Title = matMeta.Title,
                Description = matMeta.Description,
                Type = matType,
                License = matLicense,
                Status = ContentStatus.Published,
                FileName = file.FileName,
                StoragePath = storagePath,
                FileSizeBytes = file.Length,
                ContentType = file.ContentType,
                SubmittedUtc = DateTime.UtcNow
            };
            _db.Materials.Add(material);
            materialCount++;
        }

        return (module, materialCount);
    }

    private static ApiResponse<object?> ValidationError(FluentValidation.Results.ValidationResult result)
    {
        var details = result.Errors
            .Select(e => new FieldError(e.PropertyName, e.ErrorMessage))
            .ToList();
        return ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "One or more validation errors occurred.", details);
    }

    // Creates a "Not Completed" stub guide if no guide exists yet.
    // Returns "exists" or "stub_created" for the publish response.
    private async Task<string> EnsureGuideStubAsync(string courseId)
    {
        var exists = await _db.CurriculumGuides.AnyAsync(g => g.CourseId == courseId);
        if (exists) return "exists";

        var now = DateTime.UtcNow;
        _db.CurriculumGuides.Add(new Core.Models.CurriculumGuide
        {
            CourseId = courseId,
            Title = "Not Completed",
            HtmlContent = "<p>Not Completed</p>",
            Credits = null,
            ContactHours = null,
            Prerequisites = null,
            Version = null,
            GeneratedUtc = now,
            UpdatedUtc = now
        });
        await _db.SaveChangesAsync();
        return "stub_created";
    }

    // Returns the alpha prefix before the first digit (e.g. "EGN" from "EGN1111C"),
    // or null if the course ID doesn't follow the prefix-digit pattern.
    private static string? ExtractCoursePrefix(string courseId)
    {
        int i = 0;
        while (i < courseId.Length && char.IsLetter(courseId[i])) i++;
        return i > 0 && i < courseId.Length && char.IsDigit(courseId[i]) ? courseId[..i] : null;
    }
}
