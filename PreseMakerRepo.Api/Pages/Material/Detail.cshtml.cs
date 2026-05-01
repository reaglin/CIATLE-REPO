using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Api.Helpers;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Api.Pages.Material;

public class DetailModel : PageModel
{
    private readonly AppDbContext _db;
    public DetailModel(AppDbContext db) => _db = db;

    public Core.Models.Material? Material { get; set; }
    public string LicenseDisplayName { get; set; } = string.Empty;
    public string LicenseUrl { get; set; } = string.Empty;
    public bool CanPreview { get; set; }

    public async Task<IActionResult> OnGetAsync(Guid materialId)
    {
        Material = await _db.Materials.AsNoTracking()
            .Include(m => m.Contributor)
            .Include(m => m.Module).ThenInclude(mod => mod.Course)
            .FirstOrDefaultAsync(m => m.Id == materialId && m.Status == ContentStatus.Published);

        if (Material is null) return NotFound();

        LicenseDisplayName = LicenseHelper.DisplayName(Material.License);
        LicenseUrl = LicenseHelper.Url(Material.License);
        CanPreview = Material.Type is MaterialType.Presentation or MaterialType.Image
                     || Material.ContentType.StartsWith("image/")
                     || Material.ContentType == "text/html";

        return Page();
    }

    public string DownloadUrl => Material is null ? "#"
        : $"/api/v1/courses/{Material.Module.CourseId}/modules/{Material.ModuleId}/materials/{Material.Id}/download";

    public string ReportEndpoint => Material is null ? "#"
        : $"/api/v1/courses/{Material.Module.CourseId}/modules/{Material.ModuleId}/materials/{Material.Id}/report";

    public string LicenseBadgeClass => Material?.License switch
    {
        LicenseType.CcBy40     => "badge-cc-by",
        LicenseType.CcBySa40   => "badge-cc-by-sa",
        LicenseType.CcByNc40   => "badge-cc-by-nc",
        LicenseType.CcByNcSa40 => "badge-cc-by-nc-sa",
        _                      => "bg-secondary"
    };
}
