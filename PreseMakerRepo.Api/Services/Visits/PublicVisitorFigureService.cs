using Microsoft.Extensions.Caching.Memory;

namespace PreseMakerRepo.Api.Services.Visits;

/// <summary>
/// The public visitor figures: the last-7-days count in the header bar of every page, and the figures on the
/// public <c>/visitors</c> page. Each is worked out at most every 10 minutes and can never break a page.
/// </summary>
public sealed class PublicVisitorFigureService
{
    /// <summary>The header bar's figure covers this many days (Ron, 2026-11-22: "weekly visitors (last 7 days)").</summary>
    public const int HeaderDays = 7;

    private readonly VisitorStatsService _stats;
    private readonly IMemoryCache _cache;
    private readonly IConfiguration _config;
    private readonly ILogger<PublicVisitorFigureService> _log;

    public PublicVisitorFigureService(VisitorStatsService stats, IMemoryCache cache, IConfiguration config,
        ILogger<PublicVisitorFigureService> log)
    {
        _stats = stats;
        _cache = cache;
        _config = config;
        _log = log;
    }

    /// <summary>Below this many visitors no figure is shown (<c>SiteSettings:PublicVisitorMinimum</c>, default 100).</summary>
    public int Minimum => _config.GetValue("SiteSettings:PublicVisitorMinimum", 100);

    /// <summary>Visitors in the last 7 days for the header, or null to show none (too few, or not worked out).</summary>
    public async Task<PublicVisitorFigure?> GetHeaderFigureAsync(CancellationToken ct = default)
    {
        const string key = "public:visitor-figure:7";
        if (_cache.TryGetValue(key, out PublicVisitorFigure? cached)) return cached;
        try
        {
            var figure = await _stats.GetPublicFigureAsync(Minimum, days: HeaderDays, ct: ct);
            // "Nothing yet" is kept only a minute (the counter saves once a minute), so the first figure shows promptly.
            _cache.Set(key, figure, TimeSpan.FromMinutes(figure is null ? 1 : 10));
            return figure;
        }
        catch (Exception ex) when (ex is not OperationCanceledException)
        {
            _log.LogWarning(ex, "Could not work out the header's visitor figure");
            return null;
        }
    }

    /// <summary>The public page's figures for one range (7, 30, 90 or 365 days), cached 10 minutes.</summary>
    public async Task<VisitorStats> GetPageStatsAsync(int days, CancellationToken ct = default)
    {
        var key = "public:visitor-stats:" + days;
        if (_cache.TryGetValue(key, out VisitorStats? cached) && cached is not null) return cached;
        var stats = await _stats.GetAsync(days, ct: ct);
        _cache.Set(key, stats, TimeSpan.FromMinutes(10));
        return stats;
    }
}
