namespace PreseMakerRepo.Api.Services.Visits;

/// <summary>
/// Once an hour, requests a guide for every course in the top 20 most-read courses of the last 7 days that has none
/// (plan 15.3; Ron, 2026-11-23). The list is the one on <c>/visitors?days=7</c>; the requests join the ordinary queue
/// (<c>/queue/guides</c>) marked as made by the site. <c>SiteSettings:AutoRequestTopCourses</c> sets how many of the
/// top courses count (default 20; 0 turns it off). It can never stop the site: a failure is logged and tried next hour.
/// </summary>
public sealed class MostReadGuideRequester : BackgroundService
{
    public const int Days = 7;
    private static readonly TimeSpan Every = TimeSpan.FromHours(1);
    private static readonly TimeSpan FirstRun = TimeSpan.FromMinutes(5);

    private readonly IServiceScopeFactory _scopes;
    private readonly IConfiguration _config;
    private readonly ILogger<MostReadGuideRequester> _log;

    public MostReadGuideRequester(IServiceScopeFactory scopes, IConfiguration config, ILogger<MostReadGuideRequester> log)
    {
        _scopes = scopes;
        _config = config;
        _log = log;
    }

    public int Top => Math.Max(0, _config.GetValue("SiteSettings:AutoRequestTopCourses", 20));

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        try { await Task.Delay(FirstRun, stoppingToken); }
        catch (OperationCanceledException) { return; }

        while (!stoppingToken.IsCancellationRequested)
        {
            try { await RunOnceAsync(stoppingToken); }
            catch (OperationCanceledException) when (stoppingToken.IsCancellationRequested) { return; }
            catch (Exception ex) { _log.LogWarning(ex, "Could not request guides for the most-read courses"); }

            try { await Task.Delay(Every, stoppingToken); }
            catch (OperationCanceledException) { return; }
        }
    }

    /// <summary>One pass: the courses requested (empty when none needed one, or the feature is off).</summary>
    public async Task<List<string>> RunOnceAsync(CancellationToken ct = default)
    {
        if (Top == 0) return [];
        using var scope = _scopes.CreateScope();
        var stats = await scope.ServiceProvider.GetRequiredService<VisitorStatsService>()
            .GetAsync(Days, ct: ct, topCourses: Top);
        var made = await scope.ServiceProvider.GetRequiredService<GuideRequestService>()
            .RequestMostReadAsync(stats.Courses.Select(c => (c.Name, c.Count)).ToList(), Days, ct);
        if (made.Count > 0)
            _log.LogInformation("Requested guides for {Count} most-read courses: {Courses}", made.Count, string.Join(", ", made));
        return made;
    }
}
