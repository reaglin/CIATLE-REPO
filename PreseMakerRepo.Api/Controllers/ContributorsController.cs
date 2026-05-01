using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
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
[Route("api/v1/contributors")]
[Authorize]
public class ContributorsController : ControllerBase
{
    private readonly AppDbContext _db;
    private readonly UserManager<Contributor> _userManager;
    private readonly RepositoryOptions _repo;

    public ContributorsController(
        AppDbContext db,
        UserManager<Contributor> userManager,
        IOptions<RepositoryOptions> repo)
    {
        _db = db;
        _userManager = userManager;
        _repo = repo.Value;
    }

    // GET /api/v1/contributors/me
    [HttpGet("me")]
    public async Task<IActionResult> GetProfile()
    {
        var userId = ClaimsHelper.GetUserId(User);
        var user = await _userManager.FindByIdAsync(userId!);
        if (user is null) return Unauthorized();

        var moduleCount = await _db.Modules.CountAsync(m =>
            m.ContributorId == userId && m.Status != ContentStatus.Removed);
        var materialCount = await _db.Materials.CountAsync(m =>
            m.ContributorId == userId && m.Status != ContentStatus.Removed);

        var profile = new
        {
            id = user.Id,
            username = user.UserName,
            displayName = user.DisplayName,
            email = user.Email,
            institutionName = user.InstitutionName,
            isEduVerified = user.IsEduVerified,
            registeredUtc = user.RegisteredUtc,
            submissionCounts = new { modules = moduleCount, materials = materialCount }
        };

        return Ok(ApiResponse<object>.Ok(profile));
    }

    // GET /api/v1/contributors/me/submissions
    [HttpGet("me/submissions")]
    public async Task<IActionResult> GetSubmissions(
        [FromQuery] string level = "all",
        [FromQuery] string sort = "newest",
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 20)
    {
        var userId = ClaimsHelper.GetUserId(User);
        pageSize = Math.Clamp(pageSize, 1, _repo.MaxPageSize);
        page = Math.Max(page, 1);

        var includeModules = level is "all" or "module";
        var includeMaterials = level is "all" or "material";

        var results = new List<object>();

        if (includeModules)
        {
            var modules = await _db.Modules
                .AsNoTracking()
                .Where(m => m.ContributorId == userId && m.Id != WellKnownIds.OrphanModuleId)
                .Include(m => m.Materials)
                .ToListAsync();

            results.AddRange(modules.Select(m => (object)new
            {
                level = "module",
                moduleId = m.Id,
                courseId = m.CourseId,
                title = m.Title,
                status = m.Status.ToString(),
                license = m.License.ToString(),
                licenseDisplayName = LicenseHelper.DisplayName(m.License),
                submittedUtc = m.SubmittedUtc,
                updatedUtc = m.UpdatedUtc,
                materialCount = m.Materials.Count(mat => mat.Status == ContentStatus.Published)
            }));
        }

        if (includeMaterials)
        {
            var materials = await _db.Materials
                .AsNoTracking()
                .Where(m => m.ContributorId == userId)
                .ToListAsync();

            results.AddRange(materials.Select(m => (object)new
            {
                level = "material",
                materialId = m.Id,
                moduleId = m.ModuleId,
                title = m.Title,
                type = m.Type.ToString(),
                status = m.Status.ToString(),
                license = m.License.ToString(),
                licenseDisplayName = LicenseHelper.DisplayName(m.License),
                fileName = m.FileName,
                fileSizeBytes = m.FileSizeBytes,
                submittedUtc = m.SubmittedUtc,
                updatedUtc = m.UpdatedUtc
            }));
        }

        var ordered = sort == "oldest"
            ? results.OrderBy(GetSubmittedUtc)
            : results.OrderByDescending(GetSubmittedUtc);

        var total = results.Count;
        var items = ordered.Skip((page - 1) * pageSize).Take(pageSize).ToList();

        return Ok(ApiResponse<PagedResult<object>>.Ok(
            new PagedResult<object>(items, total, page, pageSize,
                (int)Math.Ceiling(total / (double)pageSize))));
    }

    private static DateTime GetSubmittedUtc(object item)
    {
        var prop = item.GetType().GetProperty("submittedUtc");
        return prop?.GetValue(item) as DateTime? ?? DateTime.MinValue;
    }
}
