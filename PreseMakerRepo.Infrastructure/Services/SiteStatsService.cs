using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Memory;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Infrastructure.Services;

/// <summary>Site-wide totals for the header strip.</summary>
public sealed record SiteCounts(int Courses, int Guides);

/// <summary>
/// Site-wide figures shown to visitors — the course and guide totals in the header strip.
///
/// Cached, because this runs on every page render of every page; course and guide writes drop the
/// entry (<see cref="SiteCache.InvalidateCounts"/>) so the numbers move as soon as content does.
/// </summary>
public class SiteStatsService
{
    private static readonly TimeSpan CacheFor = TimeSpan.FromMinutes(30);

    private readonly AppDbContext _db;
    private readonly IMemoryCache _cache;

    public SiteStatsService(AppDbContext db, IMemoryCache cache)
    {
        _db = db;
        _cache = cache;
    }

    /// <summary>
    /// Courses listed on the site and, of those, courses with a published curriculum guide.
    ///
    /// Deliberately the same predicates <see cref="TaxonomyService"/> uses for its per-leaf counts, so the
    /// header agrees with the numbers shown on Browse. Courses outside the taxonomy (the _ORPHAN_COURSE
    /// container, which has no Level3Key) are excluded there and here.
    /// </summary>
    public async Task<SiteCounts> GetSiteCountsAsync(CancellationToken ct = default) =>
        (await _cache.GetOrCreateAsync(SiteCache.SiteCountsKey, async entry =>
        {
            entry.AbsoluteExpirationRelativeToNow = CacheFor;
            var courses = await _db.TaxonomyCourses
                .AsNoTracking()
                .CountAsync(c => c.Level3Key != null &&
                                 (c.IsActive ||
                                  _db.CurriculumGuides.Any(g => g.CourseId == c.CourseId && g.Title != CurriculumGuide.StubTitle) ||
                                  _db.Modules.Any(m => m.CourseId == c.CourseId && m.Status == ContentStatus.Published)), ct);
            var guides = await _db.CurriculumGuides
                .AsNoTracking()
                .CountAsync(g => g.Title != CurriculumGuide.StubTitle &&
                                 _db.TaxonomyCourses.Any(c => c.CourseId == g.CourseId && c.Level3Key != null), ct);
            return new SiteCounts(courses, guides);
        }))!;
}
