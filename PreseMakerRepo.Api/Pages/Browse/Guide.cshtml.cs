using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Core.Constants;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Api.Pages.Browse;

public class GuideModel : PageModel
{
    private readonly AppDbContext _db;
    public GuideModel(AppDbContext db) => _db = db;

    public CurriculumGuide? Guide { get; set; }
    public TaxonomyCourse? Course { get; set; }

    public async Task<IActionResult> OnGetAsync(string courseId)
    {
        var normalizedId = courseId.ToUpperInvariant();

        Course = await _db.TaxonomyCourses.AsNoTracking()
            .Include(c => c.Level3Node!)
                .ThenInclude(n => n.Parent!)
                    .ThenInclude(n => n.Parent)
            .FirstOrDefaultAsync(c => c.CourseId == normalizedId &&
                                      c.CourseId != WellKnownIds.OrphanCourseId);
        if (Course is null) return NotFound();

        Guide = await _db.CurriculumGuides.AsNoTracking()
            .FirstOrDefaultAsync(g => g.CourseId == normalizedId);
        if (Guide is null) return NotFound();

        return Page();
    }
}
