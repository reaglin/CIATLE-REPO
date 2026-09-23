using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Api.Services;
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
    private readonly CareerRequestService _requests;

    public IndexModel(AppDbContext db, CareerRequestService requests)
    {
        _db = db;
        _requests = requests;
    }

    /// <summary>"Find a career" -- what the reader typed; null when the box was not used.</summary>
    [Microsoft.AspNetCore.Mvc.BindProperty(Name = "q", SupportsGet = true)] public string? Q { get; set; }
    public IReadOnlyList<CareerRequestService.CareerSearchHit> Hits { get; set; } = [];

    public sealed record SeriesView(string Code, string Title, int GroupCount, int PathCount);
    public sealed record PathView(string Slug, string Name, string Description, string CipCode, string? CipTitle);

    public IReadOnlyList<SeriesView> Series { get; set; } = [];
    public IReadOnlyList<PathView> Paths { get; set; } = [];
    public int MappedSeriesCount { get; set; }

    public async Task OnGetAsync()
    {
        Q = string.IsNullOrWhiteSpace(Q) ? null : Q.Trim()[..Math.Min(Q.Trim().Length, 80)];
        if (Q is not null)
        {
            var hits = await _requests.SearchAsync(Q);
            // A published path whose NAME matches but whose federal title does not ("Commercial and
            // Airline Pilot" for "airline") is still what the reader is looking for.
            var words = Q.Split(' ', StringSplitOptions.RemoveEmptyEntries).Where(w => w.Length >= 2).ToList();
            var named = await _db.CareerPaths.AsNoTracking().Where(p => p.IsPublished)
                .Select(p => new { p.Slug, p.Name }).ToListAsync();
            var have = hits.Where(h => h.PathSlug is not null).Select(h => h.PathSlug).ToHashSet();
            var extra = named.Where(p => !have.Contains(p.Slug) &&
                    words.All(w => p.Name.Contains(w, StringComparison.OrdinalIgnoreCase)))
                .Select(p => new CareerRequestService.CareerSearchHit("", p.Name, p.Slug, []));
            Hits = extra.Concat(hits).Take(40).ToList();
        }

        // Every (series, path) pair, from the primary node AND the additional anchors.
        // ⚠ Counted as DISTINCT paths per series: a path anchored to two groups in the
        // same series (Lawyer sits on both 45.10 and 45.11) is one path there, not two.
        var primary = await _db.CareerPaths.AsNoTracking()
            .Where(p => p.IsPublished)
            .Select(p => new { p.CipCode, p.Slug }).ToListAsync();
        var linked = await _db.CareerPathCips.AsNoTracking()
            .Where(c => c.CareerPath!.IsPublished)
            .Select(c => new { c.CipCode, c.CareerPath!.Slug }).ToListAsync();

        var bySeries = primary.Concat(linked)
            .GroupBy(x => x.CipCode.Length >= 2 ? x.CipCode[..2] : x.CipCode)
            .ToDictionary(g => g.Key, g => g.Select(x => x.Slug).Distinct().Count());

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
