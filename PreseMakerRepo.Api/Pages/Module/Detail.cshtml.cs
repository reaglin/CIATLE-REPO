using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Api.Helpers;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;
using System.Text.Json;

namespace PreseMakerRepo.Api.Pages.Module;

public class DetailModel : PageModel
{
    private readonly AppDbContext _db;
    public DetailModel(AppDbContext db) => _db = db;

    public Core.Models.Module? Module { get; set; }
    public IReadOnlyList<string> Outcomes { get; set; } = [];
    public IReadOnlyList<Core.Models.Material> Materials { get; set; } = [];
    public string LicenseDisplayName { get; set; } = string.Empty;
    public string LicenseUrl { get; set; } = string.Empty;
    public string LicenseBadgeClass { get; set; } = string.Empty;

    public async Task<IActionResult> OnGetAsync(Guid moduleId)
    {
        Module = await _db.Modules.AsNoTracking()
            .Include(m => m.Contributor)
            .Include(m => m.Course)
                .ThenInclude(c => c.Level3Node!)
                    .ThenInclude(n => n.Parent!)
                        .ThenInclude(n => n.Parent)
            .FirstOrDefaultAsync(m => m.Id == moduleId && m.Status == ContentStatus.Published);

        if (Module is null) return NotFound();

        Outcomes = JsonSerializer.Deserialize<List<string>>(Module.OutcomesJson) ?? [];

        Materials = await _db.Materials.AsNoTracking()
            .Where(m => m.ModuleId == moduleId && m.Status == ContentStatus.Published)
            .OrderBy(m => m.SubmittedUtc)
            .ToListAsync();

        LicenseDisplayName = LicenseHelper.DisplayName(Module.License);
        LicenseUrl = LicenseHelper.Url(Module.License);
        LicenseBadgeClass = Module.License switch
        {
            LicenseType.CcBy40     => "badge-cc-by",
            LicenseType.CcBySa40   => "badge-cc-by-sa",
            LicenseType.CcByNc40   => "badge-cc-by-nc",
            LicenseType.CcByNcSa40 => "badge-cc-by-nc-sa",
            _                      => "bg-secondary"
        };

        return Page();
    }

    public string DownloadUrl => $"/api/v1/courses/{Module!.CourseId}/modules/{Module.Id}/download";
    public string MaterialDownloadUrl(Guid materialId) =>
        $"/api/v1/courses/{Module!.CourseId}/modules/{Module.Id}/materials/{materialId}/download";
    public string ReportEndpoint => $"/api/v1/courses/{Module!.CourseId}/modules/{Module.Id}/report";
}
