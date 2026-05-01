using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Core.Constants;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;
using ModuleEntity = PreseMakerRepo.Core.Models.Module;

namespace PreseMakerRepo.Api.Pages.Browse;

public class CourseModel : PageModel
{
    private readonly AppDbContext _db;
    public CourseModel(AppDbContext db) => _db = db;

    public TaxonomyCourse? Course { get; set; }
    public IReadOnlyList<ModuleEntity> Modules { get; set; } = [];
    public bool HasGuide { get; set; }

    public async Task<IActionResult> OnGetAsync(string courseId)
    {
        var normalizedId = courseId.ToUpperInvariant();

        Course = await _db.TaxonomyCourses.AsNoTracking()
            .Include(c => c.Level3Node).ThenInclude(n => n!.Parent).ThenInclude(n => n!.Parent)
            .FirstOrDefaultAsync(c => c.CourseId == normalizedId &&
                                      c.CourseId != WellKnownIds.OrphanCourseId);
        if (Course is null) return NotFound();

        HasGuide = await _db.CurriculumGuides.AnyAsync(g => g.CourseId == normalizedId);

        Modules = await _db.Modules.AsNoTracking()
            .Where(m => m.CourseId == normalizedId &&
                        m.Status == ContentStatus.Published &&
                        m.Id != WellKnownIds.OrphanModuleId)
            .Include(m => m.Contributor)
            .Include(m => m.Materials)
            .OrderByDescending(m => m.SubmittedUtc)
            .ToListAsync();

        return Page();
    }

    public int PublishedMaterialCount(ModuleEntity m) =>
        m.Materials.Count(mat => mat.Status == ContentStatus.Published);

    public IEnumerable<string> MaterialTypes(ModuleEntity m) =>
        m.Materials.Where(mat => mat.Status == ContentStatus.Published)
                   .Select(mat => mat.Type.ToString()).Distinct();
}
