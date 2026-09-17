using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Api.Helpers;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Api.Pages.Careers;

/// <summary>
/// One career path. Every course on it was placed by an author with a stated reason; nothing
/// here is derived from course codes or classification data (<see cref="CareerPathCourse"/>).
/// </summary>
public class PathModel : PageModel
{
    private readonly AppDbContext _db;
    public PathModel(AppDbContext db) => _db = db;

    /// <param name="IsListed">False when the path names a course the catalog does not carry yet.</param>
    public sealed record CourseView(
        string CourseId, string Title, string Reason, string? VariantNote,
        bool IsListed, bool HasGuide);

    public sealed record AnchorView(string Code, string Title, string? Note);

    public CareerPath Path { get; set; } = null!;
    public CipNode? Cip { get; set; }
    public CipNode? Series { get; set; }
    /// <summary>The additional CIP groups this path is filed under, with the evidence.</summary>
    public IReadOnlyList<AnchorView> Anchors { get; set; } = [];
    public IReadOnlyList<CourseView> Courses { get; set; } = [];
    public IReadOnlyList<CareerPathSource> Sources { get; set; } = [];

    public async Task<IActionResult> OnGetAsync(string slug)
    {
        var path = await _db.CareerPaths.AsNoTracking()
            .Include(p => p.Sources)
            .FirstOrDefaultAsync(p => p.Slug == slug && p.IsPublished);
        if (path is null) return NotFound();
        Path = path;
        Sources = path.Sources.OrderBy(s => s.SortOrder).ThenBy(s => s.Label).ToList();

        Cip = await _db.CipNodes.AsNoTracking().FirstOrDefaultAsync(n => n.Code == path.CipCode);
        if (Cip?.ParentCode is not null)
            Series = await _db.CipNodes.AsNoTracking().FirstOrDefaultAsync(n => n.Code == Cip.ParentCode);

        Anchors = await _db.CareerPathCips.AsNoTracking()
            .Where(c => c.CareerPathId == path.Id)
            .OrderBy(c => c.SortOrder)
            .Select(c => new AnchorView(c.CipCode, c.Cip!.Title, c.Note))
            .ToListAsync();

        var placed = await _db.CareerPathCourses.AsNoTracking()
            .Where(c => c.CareerPathId == path.Id)
            .OrderBy(c => c.SortOrder)
            .ToListAsync();

        if (placed.Count == 0) return Page();

        var ids = placed.Select(c => c.CourseId).ToList();

        var listed = await _db.TaxonomyCourses.AsNoTracking()
            .Where(c => ids.Contains(c.CourseId))
            .Select(c => new { c.CourseId, c.Title, c.StateTitle })
            .ToDictionaryAsync(c => c.CourseId);

        var withGuide = await _db.CurriculumGuides.AsNoTracking()
            .Where(g => ids.Contains(g.CourseId) && g.Title != CurriculumGuide.StubTitle)
            .Select(g => new { g.CourseId, g.Title })
            .ToDictionaryAsync(g => g.CourseId, g => g.Title);

        Courses = placed.Select(c =>
        {
            listed.TryGetValue(c.CourseId, out var course);
            withGuide.TryGetValue(c.CourseId, out var guideTitle);
            var title = course is null
                ? c.CourseId
                : CourseTitles.Display(c.CourseId, course.Title, course.StateTitle, guideTitle);
            return new CourseView(c.CourseId, title, c.Reason, c.VariantNote,
                                  course is not null, guideTitle is not null);
        }).ToList();

        return Page();
    }
}
