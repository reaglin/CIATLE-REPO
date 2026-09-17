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
    /// <param name="Offered">How many of this path's courses the institution offers.</param>
    public sealed record SchoolView(string Code, string? Name, string? Sector, int Offered);

    public CareerPath Path { get; set; } = null!;
    public CipNode? Cip { get; set; }
    public CipNode? Series { get; set; }
    /// <summary>The additional CIP groups this path is filed under, with the evidence.</summary>
    public IReadOnlyList<AnchorView> Anchors { get; set; } = [];
    /// <summary>
    /// Institutions that teach the courses on this path, most coverage first. ⚠ Derived from
    /// COURSE OFFERINGS, not from programme data — so it says "you can take these courses here",
    /// which is true, and never "this school offers this degree", which we do not know.
    /// </summary>
    public IReadOnlyList<SchoolView> Schools { get; set; } = [];
    /// <summary>Courses on the path the catalog actually carries — the denominator for Schools.</summary>
    public int CoursesListed { get; set; }
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

        // ⚠ Ron, 2026-09-17, on what a career page should carry: "Schools represented in repo
        // offering this path (note the path may or may not be a specific degree)." Derived live
        // from offerings so it cannot go stale, and counted per institution so the reader can see
        // WHO COVERS MOST OF THE PATH rather than a flat list.
        var offerings = await _db.CourseOfferings.AsNoTracking()
            .Where(o => ids.Contains(o.CourseId) && o.IsActive)
            .Select(o => new { o.CourseId, o.InstitutionCode, o.Institution.Name, o.Institution.Sector })
            .ToListAsync();

        CoursesListed = offerings.Select(o => o.CourseId).Distinct().Count();
        Schools = offerings
            .GroupBy(o => o.InstitutionCode)
            .Select(g => new SchoolView(g.Key, g.First().Name, g.First().Sector,
                                        g.Select(x => x.CourseId).Distinct().Count()))
            .OrderByDescending(s => s.Offered).ThenBy(s => s.Name ?? s.Code)
            .ToList();

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
