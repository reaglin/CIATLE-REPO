using Microsoft.Extensions.Caching.Memory;

namespace PreseMakerRepo.Infrastructure.Services;

/// <summary>
/// Cache keys for the figures every browse page renders (the taxonomy tree with its counts, and the
/// header totals). Both are expensive once the catalog holds tens of thousands of courses, so they
/// are cached — and dropped whenever a course or guide write changes them.
/// </summary>
public static class SiteCache
{
    public const string TaxonomyTreeKey = "taxonomy:tree";
    public const string SiteCountsKey = "sitestats:counts";

    public static void InvalidateCounts(IMemoryCache cache)
    {
        cache.Remove(TaxonomyTreeKey);
        cache.Remove(SiteCountsKey);
    }
}
