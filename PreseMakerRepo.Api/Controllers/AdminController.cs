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

namespace PreseMakerRepo.Api.Controllers;

[ApiController]
[Route("api/v1/admin")]
[Authorize(Policy = "AdminOnly")]
public class AdminController : ControllerBase
{
    private readonly AppDbContext _db;
    private readonly UserManager<Contributor> _userManager;
    private readonly IEmailService _email;
    private readonly RepositoryOptions _repo;

    public AdminController(
        AppDbContext db,
        UserManager<Contributor> userManager,
        IEmailService email,
        IOptions<RepositoryOptions> repo)
    {
        _db = db;
        _userManager = userManager;
        _email = email;
        _repo = repo.Value;
    }

    // GET /api/v1/admin/flagged
    [HttpGet("flagged")]
    public async Task<IActionResult> GetFlagged(
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 20)
    {
        pageSize = Math.Clamp(pageSize, 1, _repo.MaxPageSize);
        page = Math.Max(page, 1);

        var flags = await _db.ContentFlags
            .AsNoTracking()
            .Where(f => !f.IsResolved)
            .Include(f => f.Module).ThenInclude(m => m!.Contributor)
            .Include(f => f.Module).ThenInclude(m => m!.Course)
            .Include(f => f.Material).ThenInclude(m => m!.Contributor)
            .Include(f => f.Material).ThenInclude(m => m!.Module).ThenInclude(mod => mod.Course)
            .ToListAsync();

        var items = new List<FlaggedItemDto>();

        var moduleGroups = flags
            .Where(f => f.ModuleId.HasValue && f.Module is not null)
            .GroupBy(f => f.ModuleId!.Value);

        foreach (var g in moduleGroups)
        {
            var representative = g.OrderByDescending(f => f.FlaggedUtc).First();
            var m = representative.Module!;
            items.Add(new FlaggedItemDto(
                ContentType: "module",
                ContentId: m.Id,
                CourseId: m.CourseId,
                Title: m.Title,
                Contributor: new ContributorBriefDto(
                    m.Contributor.UserName!, m.Contributor.DisplayName,
                    m.Contributor.InstitutionName, m.Contributor.IsEduVerified),
                MostRecentFlagUtc: representative.FlaggedUtc,
                FlagReason: representative.Reason,
                FlagCount: g.Count()));
        }

        var materialGroups = flags
            .Where(f => f.MaterialId.HasValue && f.Material is not null)
            .GroupBy(f => f.MaterialId!.Value);

        foreach (var g in materialGroups)
        {
            var representative = g.OrderByDescending(f => f.FlaggedUtc).First();
            var mat = representative.Material!;
            items.Add(new FlaggedItemDto(
                ContentType: "material",
                ContentId: mat.Id,
                CourseId: mat.Module?.Course?.CourseId,
                Title: mat.Title,
                Contributor: new ContributorBriefDto(
                    mat.Contributor.UserName!, mat.Contributor.DisplayName,
                    mat.Contributor.InstitutionName, mat.Contributor.IsEduVerified),
                MostRecentFlagUtc: representative.FlaggedUtc,
                FlagReason: representative.Reason,
                FlagCount: g.Count()));
        }

        var ordered = items.OrderByDescending(i => i.MostRecentFlagUtc).ToList();
        var total = ordered.Count;
        var paged = ordered.Skip((page - 1) * pageSize).Take(pageSize).ToList();

        return Ok(ApiResponse<PagedResult<FlaggedItemDto>>.Ok(
            new PagedResult<FlaggedItemDto>(paged, total, page, pageSize,
                (int)Math.Ceiling(total / (double)pageSize))));
    }

    // POST /api/v1/admin/modules/{id}/clear-flag
    [HttpPost("modules/{id:guid}/clear-flag")]
    public async Task<IActionResult> ClearModuleFlag(Guid id, [FromBody] ClearFlagRequest request)
    {
        var module = await _db.Modules
            .FirstOrDefaultAsync(m => m.Id == id && m.Status != ContentStatus.Removed);
        if (module is null)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.ModuleNotFound, "Module not found."));

        var adminId = ClaimsHelper.GetUserId(User);
        var now = DateTime.UtcNow;

        await _db.ContentFlags
            .Where(f => f.ModuleId == id && !f.IsResolved)
            .ExecuteUpdateAsync(s => s
                .SetProperty(f => f.IsResolved, true)
                .SetProperty(f => f.ResolvedByAdminId, adminId)
                .SetProperty(f => f.ResolvedUtc, now)
                .SetProperty(f => f.ResolutionNote, request.Note));

        if (module.Status == ContentStatus.Flagged)
        {
            module.Status = ContentStatus.Published;
            await _db.SaveChangesAsync();
        }

        return Ok(ApiResponse<MessageResponse>.Ok(new MessageResponse("Flag cleared. Module re-published.")));
    }

    // DELETE /api/v1/admin/modules/{id}
    [HttpDelete("modules/{id:guid}")]
    public async Task<IActionResult> RemoveModule(Guid id, [FromBody] AdminRemoveRequest request)
    {
        var module = await _db.Modules
            .Include(m => m.Contributor)
            .FirstOrDefaultAsync(m => m.Id == id && m.Status != ContentStatus.Removed);
        if (module is null)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.ModuleNotFound, "Module not found."));

        module.Status = ContentStatus.Removed;
        module.RemovedUtc = DateTime.UtcNow;
        await _db.SaveChangesAsync();

        if (request.NotifyContributor && !string.IsNullOrEmpty(module.Contributor.Email))
        {
            _ = _email.SendContentRemovedEmailAsync(
                module.Contributor.Email, module.Contributor.UserName ?? "",
                module.Title, "module", request.Reason);
        }

        return Ok(ApiResponse<MessageResponse>.Ok(new MessageResponse("Module removed.")));
    }

    // POST /api/v1/admin/materials/{id}/clear-flag
    [HttpPost("materials/{id:guid}/clear-flag")]
    public async Task<IActionResult> ClearMaterialFlag(Guid id, [FromBody] ClearFlagRequest request)
    {
        var material = await _db.Materials
            .FirstOrDefaultAsync(m => m.Id == id && m.Status != ContentStatus.Removed);
        if (material is null)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.MaterialNotFound, "Material not found."));

        var adminId = ClaimsHelper.GetUserId(User);
        var now = DateTime.UtcNow;

        await _db.ContentFlags
            .Where(f => f.MaterialId == id && !f.IsResolved)
            .ExecuteUpdateAsync(s => s
                .SetProperty(f => f.IsResolved, true)
                .SetProperty(f => f.ResolvedByAdminId, adminId)
                .SetProperty(f => f.ResolvedUtc, now)
                .SetProperty(f => f.ResolutionNote, request.Note));

        if (material.Status == ContentStatus.Flagged)
        {
            material.Status = ContentStatus.Published;
            await _db.SaveChangesAsync();
        }

        return Ok(ApiResponse<MessageResponse>.Ok(new MessageResponse("Flag cleared. Material re-published.")));
    }

    // DELETE /api/v1/admin/materials/{id}
    [HttpDelete("materials/{id:guid}")]
    public async Task<IActionResult> RemoveMaterial(Guid id, [FromBody] AdminRemoveRequest request)
    {
        var material = await _db.Materials
            .Include(m => m.Contributor)
            .FirstOrDefaultAsync(m => m.Id == id && m.Status != ContentStatus.Removed);
        if (material is null)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.MaterialNotFound, "Material not found."));

        material.Status = ContentStatus.Removed;
        material.RemovedUtc = DateTime.UtcNow;
        await _db.SaveChangesAsync();

        if (request.NotifyContributor && !string.IsNullOrEmpty(material.Contributor.Email))
        {
            _ = _email.SendContentRemovedEmailAsync(
                material.Contributor.Email, material.Contributor.UserName ?? "",
                material.Title, "material", request.Reason);
        }

        return Ok(ApiResponse<MessageResponse>.Ok(new MessageResponse("Material removed.")));
    }

    // POST /api/v1/admin/contributors/{id}/suspend
    [HttpPost("contributors/{id}/suspend")]
    public async Task<IActionResult> SuspendContributor(string id, [FromBody] SuspendContributorRequest request)
    {
        var contributor = await _userManager.FindByIdAsync(id);
        if (contributor is null)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.Unauthorized, "Contributor not found."));

        contributor.IsSuspended = true;
        await _userManager.UpdateAsync(contributor);

        if (request.NotifyContributor && !string.IsNullOrEmpty(contributor.Email))
        {
            _ = _email.SendSuspensionEmailAsync(
                contributor.Email, contributor.UserName ?? "", request.Reason);
        }

        return Ok(ApiResponse<MessageResponse>.Ok(new MessageResponse("Contributor suspended.")));
    }

    // POST /api/v1/admin/contributors/{id}/reinstate
    [HttpPost("contributors/{id}/reinstate")]
    public async Task<IActionResult> ReinstateContributor(string id)
    {
        var contributor = await _userManager.FindByIdAsync(id);
        if (contributor is null)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.Unauthorized, "Contributor not found."));

        contributor.IsSuspended = false;
        await _userManager.UpdateAsync(contributor);

        return Ok(ApiResponse<MessageResponse>.Ok(new MessageResponse("Contributor reinstated.")));
    }

    // POST /api/v1/admin/contributors/{id}/contact
    [HttpPost("contributors/{id}/contact")]
    public async Task<IActionResult> ContactContributor(string id, [FromBody] AdminContactRequest request)
    {
        var contributor = await _userManager.FindByIdAsync(id);
        if (contributor is null)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.Unauthorized, "Contributor not found."));

        if (string.IsNullOrEmpty(contributor.Email))
            return UnprocessableEntity(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "Contributor has no email address."));

        await _email.SendAdminContactEmailAsync(contributor.Email, request.Subject, request.Body);

        return Ok(ApiResponse<MessageResponse>.Ok(new MessageResponse("Email sent.")));
    }

    // GET /api/v1/admin/stats
    [HttpGet("stats")]
    public async Task<IActionResult> GetStats()
    {
        var moduleCounts = await _db.Modules
            .AsNoTracking()
            .Where(m => m.Id != WellKnownIds.OrphanModuleId)
            .GroupBy(m => m.Status)
            .Select(g => new { Status = g.Key, Count = g.Count() })
            .ToListAsync();

        var totalModules = moduleCounts.Sum(x => x.Count);
        var publishedModules = moduleCounts.FirstOrDefault(x => x.Status == ContentStatus.Published)?.Count ?? 0;
        var flaggedModules = moduleCounts.FirstOrDefault(x => x.Status == ContentStatus.Flagged)?.Count ?? 0;
        var removedModules = moduleCounts.FirstOrDefault(x => x.Status == ContentStatus.Removed)?.Count ?? 0;

        var totalMaterials = await _db.Materials.AsNoTracking()
            .Where(m => m.Status != ContentStatus.Removed)
            .CountAsync();

        var totalContributors = await _userManager.Users.CountAsync();
        var suspendedContributors = await _userManager.Users.CountAsync(u => u.IsSuspended);

        var prefixCounts = await (
            from m in _db.Modules.AsNoTracking()
            where m.Status == ContentStatus.Published && m.Id != WellKnownIds.OrphanModuleId
            join c in _db.TaxonomyCourses on m.CourseId equals c.CourseId
            group m by c.Level3Key into g
            orderby g.Count() descending
            select new CoursePrefixCount(g.Key, g.Count())
        ).ToListAsync();

        var cutoff = DateTime.UtcNow.AddDays(-30);
        var recentModules = await _db.Modules.AsNoTracking()
            .CountAsync(m => m.Status == ContentStatus.Published &&
                             m.Id != WellKnownIds.OrphanModuleId &&
                             m.SubmittedUtc >= cutoff);

        var stats = new AdminStatsDto(
            TotalModules: totalModules,
            PublishedModules: publishedModules,
            FlaggedModules: flaggedModules,
            RemovedModules: removedModules,
            TotalMaterials: totalMaterials,
            TotalContributors: totalContributors,
            SuspendedContributors: suspendedContributors,
            ModulesByCoursePrefix: prefixCounts,
            RecentModules30Days: recentModules);

        return Ok(ApiResponse<AdminStatsDto>.Ok(stats));
    }
}
