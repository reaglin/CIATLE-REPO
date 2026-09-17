using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Api.Pages.Programs;

/// <summary>
/// The Programs index. A programme is "a major that supports a career path and is being offered by
/// a Florida school" (Ron, 2026-09-17) and sits one level above a degree.
/// </summary>
public class IndexModel : PageModel
{
    private readonly AppDbContext _db;
    public IndexModel(AppDbContext db) => _db = db;

    public sealed record ProgramView(string Slug, string Name, string Description, int SchoolCount);

    public IReadOnlyList<ProgramView> Programs { get; set; } = [];
    public int AwardYear { get; set; }

    public async Task OnGetAsync()
    {
        var programs = await _db.Programs.AsNoTracking()
            .Where(p => p.IsPublished)
            .Include(p => p.Cips)
            .OrderBy(p => p.SortOrder).ThenBy(p => p.Name)
            .ToListAsync();

        // ⚠ One read of the award table, then matched in memory. The CIP codes on a programme are
        // PREFIXES, and a prefix match is not something EF can translate into a sensible query
        // across an arbitrary list of prefixes.
        var awards = await _db.InstitutionAwards.AsNoTracking()
            .Select(a => new { a.UnitId, a.CipCode, a.Year })
            .ToListAsync();
        AwardYear = awards.Count > 0 ? awards.Max(a => a.Year) : 0;

        Programs = programs.Select(p =>
        {
            var prefixes = p.Cips.Select(c => c.CipCode).ToList();
            var n = awards.Where(a => prefixes.Any(pre => a.CipCode.StartsWith(pre)))
                          .Select(a => a.UnitId).Distinct().Count();
            return new ProgramView(p.Slug, p.Name, p.Description, n);
        }).ToList();
    }
}
