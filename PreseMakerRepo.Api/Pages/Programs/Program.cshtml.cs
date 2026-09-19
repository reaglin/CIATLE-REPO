using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Infrastructure.Data;
using ProgramEntity = PreseMakerRepo.Core.Models.Program;

namespace PreseMakerRepo.Api.Pages.Programs;

/// <summary>
/// One programme: what it is, which degrees it encompasses, and which Florida public institutions
/// award them.
/// <para>
/// ⚠ The school list is DERIVED here, never stored — Ron, 2026-09-17: "I am going to decouple
/// programs from schools. Programs will be just information about programs." It is a cross-
/// reference computed by matching this programme's CIP prefixes against the federal award table.
/// </para>
/// </summary>
public class ProgramModel : PageModel
{
    private readonly AppDbContext _db;
    public ProgramModel(AppDbContext db) => _db = db;

    /// <param name="Awards">The award levels this school offers in the field — i.e. the majors.</param>
    public sealed record SchoolView(string Name, string? Code, IReadOnlyList<string> Awards, int Completions);

    /// <param name="Note">Why this career path names the programme, in the path's own words.</param>
    public sealed record PathView(string Slug, string Name, string Description, string? Note,
                                 bool IsRoute);

    /// <param name="Note">Why a student reading THIS programme should look at that one.</param>
    public sealed record RelatedView(string Slug, string Name, string? Note, int Schools);

    public ProgramEntity Program { get; set; } = null!;
    public IReadOnlyList<SchoolView> Schools { get; set; } = [];
    public IReadOnlyList<string> AwardLevels { get; set; } = [];
    public int AwardYear { get; set; }

    /// <summary>
    /// The careers this programme leads to. ⚠ Ron, 2026-09-19: a programme page without them
    /// is a dead end — the student arrived asking what this degree is FOR.
    /// </summary>
    public IReadOnlyList<PathView> Paths { get; set; } = [];

    /// <summary>
    /// Neighbouring programmes, read in both directions. ⚠ Ron, 2026-09-19: the similarity
    /// between mechanical and aerospace engineering is "something students would not normally
    /// know when looking at a career", so the note matters more than the link.
    /// </summary>
    public IReadOnlyList<RelatedView> Related { get; set; } = [];

    public async Task<IActionResult> OnGetAsync(string slug)
    {
        var p = await _db.Programs.AsNoTracking()
            .Include(x => x.Cips)
            .Include(x => x.CareerPaths).ThenInclude(l => l.CareerPath)
            .Include(x => x.Related).ThenInclude(r => r.RelatedProgram!).ThenInclude(rp => rp.Cips)
            .Include(x => x.RelatedFrom).ThenInclude(r => r.Program!).ThenInclude(op => op.Cips)
            .FirstOrDefaultAsync(x => x.Slug == slug && x.IsPublished);
        if (p is null) return NotFound();
        Program = p;

        Paths = p.CareerPaths
            .Where(l => l.CareerPath is not null && l.CareerPath.IsPublished)
            .OrderBy(l => l.CareerPath!.Name)
            .Select(l => new PathView(l.CareerPath!.Slug, l.CareerPath.Name,
                                      l.CareerPath.Description, l.Note, l.IsRoute))
            .ToList();

        var awards = await _db.InstitutionAwards.AsNoTracking().ToListAsync();

        // ⚠ Both directions: a connection authored on the other programme still belongs here,
        // because the student who landed on THIS page needs it just as much.
        int SchoolsFor(IEnumerable<string> prefixes2)
        {
            var list = prefixes2.ToList();
            return awards.Where(a => list.Any(x => a.CipCode.StartsWith(x)))
                         .Select(a => a.UnitId).Distinct().Count();
        }

        var seen = new HashSet<string>();
        var related = new List<RelatedView>();
        foreach (var r in p.Related.OrderBy(r => r.SortOrder))
        {
            var t = r.RelatedProgram;
            if (t is null || !t.IsPublished || !seen.Add(t.Slug)) continue;
            related.Add(new RelatedView(t.Slug, t.Name, r.Note,
                                        SchoolsFor(t.Cips.Select(c => c.CipCode))));
        }
        foreach (var r in p.RelatedFrom.OrderBy(r => r.SortOrder))
        {
            var o = r.Program;
            if (o is null || !o.IsPublished || !seen.Add(o.Slug)) continue;
            related.Add(new RelatedView(o.Slug, o.Name, r.Note,
                                        SchoolsFor(o.Cips.Select(c => c.CipCode))));
        }
        Related = related;

        var prefixes = p.Cips.OrderBy(c => c.SortOrder).Select(c => c.CipCode).ToList();
        if (prefixes.Count == 0) return Page();
        var mine = awards.Where(a => prefixes.Any(pre => a.CipCode.StartsWith(pre))).ToList();
        AwardYear = mine.Count > 0 ? mine.Max(a => a.Year) : 0;

        // ⚠⚠ Ordered by NAME, not by completions. Ron: counts are "handy, but not required" —
        // so they are shown, but they never rank one school above another.
        Schools = mine
            .GroupBy(a => a.UnitId)
            .Select(g => new SchoolView(
                g.First().InstitutionName,
                g.Select(x => x.InstitutionCode).FirstOrDefault(c => c != null),
                g.Select(x => x.AwardLevel).Distinct().OrderBy(x => x).ToList(),
                g.Sum(x => x.Completions)))
            .OrderBy(s => s.Name)
            .ToList();

        AwardLevels = mine.Select(a => a.AwardLevel).Distinct().OrderBy(x => x).ToList();
        return Page();
    }
}
