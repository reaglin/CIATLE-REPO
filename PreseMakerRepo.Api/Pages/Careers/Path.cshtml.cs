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
    /// <param name="Schools">Institutions awarding a credential in the programme's CIP fields.</param>
    /// <param name="IsRoute">False when the programme is a neighbour rather than a way in.</param>
    public sealed record ProgramView(string Slug, string Name, string? Note, bool IsRoute, int Schools);

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
    /// <summary>
    /// Programmes that lead to this career. ⚠ Ron, 2026-09-17: "For programs associated with
    /// careers we want to note schools that offer the program in the career (that will be a note)."
    /// The school COUNT is derived from the programme's CIP prefixes against the award table.
    /// </summary>
    public IReadOnlyList<ProgramView> ProgramsForPath { get; set; } = [];

    /// <param name="CipTitle">The CIP group it is filed on, which is what makes it a neighbour.</param>
    public sealed record NeighbourView(string Slug, string Name, string Description, string CipTitle);

    /// <summary>The award year behind the programme school counts, so the page can say which it is.</summary>
    public int AwardYear { get; set; }

    /// <summary>
    /// Careers filed in the same CIP series as this one. ⚠ Ron, 2026-09-19: a student looking at
    /// one career does not know which others are next door — "the similarities between mechanical
    /// engineering and aerospace engineering (any similar program) should be noted as these are
    /// things students would not normally know".
    /// <para>
    /// ⚠ Matched on the PRIMARY code only. A path like Lawyer carries sixteen anchors across
    /// eleven series because that is where its applicants come FROM; matching on those would make
    /// half the site a neighbour of law.
    /// </para>
    /// </summary>
    public IReadOnlyList<NeighbourView> NearbyPaths { get; set; } = [];
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

        // ⚠ No early return here. A path with no courses placed yet still has programmes and
        // neighbours, and returning early rendered exactly the dead-end page this feature exists
        // to remove. Each block below guards itself instead.

        var ids = placed.Select(c => c.CourseId).ToList();

        var listed = await _db.TaxonomyCourses.AsNoTracking()
            .Where(c => ids.Contains(c.CourseId))
            .Select(c => new { c.CourseId, c.Title, c.StateTitle })
            .ToDictionaryAsync(c => c.CourseId);

        var withGuide = await _db.CurriculumGuides.AsNoTracking()
            .Where(g => ids.Contains(g.CourseId) && g.Title != CurriculumGuide.StubTitle)
            .Select(g => new { g.CourseId, g.Title })
            .ToDictionaryAsync(g => g.CourseId, g => g.Title);

        var progLinks = await _db.CareerPathPrograms.AsNoTracking()
            .Where(l => l.CareerPathId == path.Id)
            .Include(l => l.Program).ThenInclude(p => p!.Cips)
            .OrderBy(l => l.SortOrder)
            .ToListAsync();
        if (progLinks.Count > 0)
        {
            var awards = await _db.InstitutionAwards.AsNoTracking()
                .Select(a => new { a.UnitId, a.CipCode, a.Year }).ToListAsync();
            AwardYear = awards.Count > 0 ? awards.Max(a => a.Year) : 0;
            ProgramsForPath = progLinks.Select(l =>
            {
                var pre = l.Program!.Cips.Select(c => c.CipCode).ToList();
                var n = awards.Where(a => pre.Any(x => a.CipCode.StartsWith(x)))
                              .Select(a => a.UnitId).Distinct().Count();
                return new ProgramView(l.Program.Slug, l.Program.Name, l.Note, l.IsRoute, n);
            }).ToList();
        }

        // Neighbours: same CIP series, published, this one excluded. Two digits is the right
        // width — series 14 is engineering, so mechanical finds aerospace, materials and civil.
        var series = path.CipCode.Length >= 2 ? path.CipCode[..2] + "." : null;
        if (series is not null)
        {
            NearbyPaths = await _db.CareerPaths.AsNoTracking()
                .Where(x => x.IsPublished && x.Id != path.Id && x.CipCode.StartsWith(series))
                .OrderBy(x => x.Name)
                .Select(x => new NeighbourView(x.Slug, x.Name, x.Description,
                                               x.Cip!.Title))
                .Take(12)
                .ToListAsync();
        }

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
