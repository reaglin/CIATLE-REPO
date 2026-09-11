using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Memory;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Infrastructure.Services;

/// <summary>
/// Site-wide figures shown to visitors — currently the course count in the header strip.
///
/// Cached, because this runs on every page render of every page and the number moves a few
/// times a day at most.
/// </summary>
public class SiteStatsService
{
    private const string CoursesWithMaterialsKey = "sitestats:courses-with-materials";
    private static readonly TimeSpan CacheFor = TimeSpan.FromMinutes(30);

    private readonly AppDbContext _db;
    private readonly IMemoryCache _cache;

    public SiteStatsService(AppDbContext db, IMemoryCache cache)
    {
        _db = db;
        _cache = cache;
    }

    /// <summary>
    /// Courses that actually have something to offer: at least one published module, or a
    /// curriculum guide.
    ///
    /// This is deliberately the same predicate <see cref="TaxonomyService"/> uses for its
    /// per-leaf course counts, so the site-wide total in the header agrees with the numbers
    /// shown on Browse instead of quietly contradicting them. Courses outside the taxonomy
    /// (the _ORPHAN_COURSE container, which has no Level3Key) are excluded there and here.
    /// </summary>
    public Task<int> GetCoursesWithMaterialsAsync(CancellationToken ct = default) =>
        _cache.GetOrCreateAsync(CoursesWithMaterialsKey, entry =>
        {
            entry.AbsoluteExpirationRelativeToNow = CacheFor;
            return _db.TaxonomyCourses
                .AsNoTracking()
                .CountAsync(c => c.Level3Key != null &&
                                 (_db.Modules.Any(m => m.CourseId == c.CourseId &&
                                                       m.Status == ContentStatus.Published) ||
                                  _db.CurriculumGuides.Any(g => g.CourseId == c.CourseId)), ct);
        })!;
}
