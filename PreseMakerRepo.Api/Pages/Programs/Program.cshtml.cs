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

    public ProgramEntity Program { get; set; } = null!;
    public IReadOnlyList<SchoolView> Schools { get; set; } = [];
    public IReadOnlyList<string> AwardLevels { get; set; } = [];
    public int AwardYear { get; set; }

    public async Task<IActionResult> OnGetAsync(string slug)
    {
        var p = await _db.Programs.AsNoTracking()
            .Include(x => x.Cips)
            .FirstOrDefaultAsync(x => x.Slug == slug && x.IsPublished);
        if (p is null) return NotFound();
        Program = p;

        var prefixes = p.Cips.OrderBy(c => c.SortOrder).Select(c => c.CipCode).ToList();
        if (prefixes.Count == 0) return Page();

        var awards = await _db.InstitutionAwards.AsNoTracking().ToListAsync();
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
