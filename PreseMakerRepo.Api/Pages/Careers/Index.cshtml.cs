using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Api.Pages.Careers;

/// <summary>
/// The Career Paths front door: the CIP taxonomy, laid out as NCES lays it out at
/// <c>nces.ed.gov/ipeds/cipcode/browse.aspx?y=55</c> — Ron's brief, 2026-09-17.
/// <para>
/// Published paths lead, because a visitor arrives wanting a profession, not a taxonomy.
/// The tree is underneath as the way in when the path they want is not written yet.
/// </para>
/// </summary>
public class IndexModel : PageModel
{
    private readonly AppDbContext _db;
    public IndexModel(AppDbContext db) => _db = db;

    public sealed record SeriesView(string Code, string Title, int GroupCount, int PathCount);
    public sealed record PathView(string Slug, string Name, string Description, string CipCode, string? CipTitle);

    public IReadOnlyList<SeriesView> Series { get; set; } = [];
    public IReadOnlyList<PathView> Paths { get; set; } = [];
    public int MappedSeriesCount { get; set; }

    public async Task OnGetAsync()
    {
        // One grouped read rather than a count per series.
        var pathsByCip = await _db.CareerPaths.AsNoTracking()
            .Where(p => p.IsPublished)
            .GroupBy(p => p.CipCode)
            .Select(g => new { CipCode = g.Key, Count = g.Count() })
            .ToListAsync();

        // A path is filed on a 4-digit group, so its series is the first two digits.
        var bySeries = pathsByCip
            .GroupBy(x => x.CipCode.Length >= 2 ? x.CipCode[..2] : x.CipCode)
            .ToDictionary(g => g.Key, g => g.Sum(x => x.Count));

        Series = await _db.CipNodes.AsNoTracking()
            .Where(n => n.Level == 2 && n.IsActive)
            .OrderBy(n => n.Code)
            .Select(n => new SeriesView(n.Code, n.Title, n.ChildCount, 0))
            .ToListAsync();

        Series = Series
            .Select(s => s with { PathCount = bySeries.TryGetValue(s.Code, out var c) ? c : 0 })
            .ToList();

        MappedSeriesCount = Series.Count(s => s.GroupCount > 0);

        Paths = await _db.CareerPaths.AsNoTracking()
            .Where(p => p.IsPublished)
            .OrderBy(p => p.SortOrder).ThenBy(p => p.Name)
            .Select(p => new PathView(p.Slug, p.Name, p.Description, p.CipCode, p.Cip!.Title))
            .ToListAsync();
    }
}
