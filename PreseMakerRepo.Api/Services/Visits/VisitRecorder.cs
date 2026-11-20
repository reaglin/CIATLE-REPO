using System.Threading.Channels;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Api.Services.Visits;

/// <summary>One counted page view, as handed from the middleware to the recorder.</summary>
public sealed record VisitHit(DateTime Utc, string VisitorHash, string Path, string? Source);

/// <summary>
/// Collects counted page views in memory and writes them to the database once a minute (and when
/// the site stops), so a page view never waits on a database write. A singleton and a hosted
/// service. If the queue ever fills (50,000 waiting), further views are dropped, not blocked on.
/// </summary>
public sealed class VisitRecorder : BackgroundService
{
    private readonly Channel<VisitHit> _queue = Channel.CreateBounded<VisitHit>(
        new BoundedChannelOptions(50_000) { FullMode = BoundedChannelFullMode.DropWrite, SingleReader = true });
    private readonly IServiceScopeFactory _scopes;
    private readonly ILogger<VisitRecorder> _log;
    private readonly SemaphoreSlim _flushLock = new(1, 1);

    public static readonly TimeSpan Interval = TimeSpan.FromMinutes(1);

    public VisitRecorder(IServiceScopeFactory scopes, ILogger<VisitRecorder> log)
    {
        _scopes = scopes;
        _log = log;
    }

    public void Record(VisitHit hit) => _queue.Writer.TryWrite(hit);

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        try
        {
            using var timer = new PeriodicTimer(Interval);
            while (await timer.WaitForNextTickAsync(stoppingToken))
                await FlushSafelyAsync(CancellationToken.None);
        }
        catch (OperationCanceledException) { }
    }

    public override async Task StopAsync(CancellationToken cancellationToken)
    {
        await base.StopAsync(cancellationToken);
        await FlushSafelyAsync(CancellationToken.None);   // keep the last minute's views
    }

    private async Task FlushSafelyAsync(CancellationToken ct)
    {
        try { await FlushAsync(ct); }
        catch (Exception ex) { _log.LogWarning(ex, "Visitor counter: could not save page views; they are dropped."); }
    }

    /// <summary>Writes everything waiting. Returns how many page views were written.</summary>
    public async Task<int> FlushAsync(CancellationToken ct = default)
    {
        await _flushLock.WaitAsync(ct);
        try
        {
            var hits = new List<VisitHit>();
            while (_queue.Reader.TryRead(out var h)) hits.Add(h);
            if (hits.Count == 0) return 0;

            using var scope = _scopes.CreateScope();
            var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();

            foreach (var byDay in hits.GroupBy(h => VisitClassifier.FloridaDay(h.Utc)))
            {
                var day = byDay.Key;

                var visitors = byDay.GroupBy(h => h.VisitorHash).ToList();
                var hashes = visitors.Select(g => g.Key).ToList();
                var existingVisits = await db.SiteVisits
                    .Where(v => v.Day == day && hashes.Contains(v.VisitorHash))
                    .ToDictionaryAsync(v => v.VisitorHash, ct);
                foreach (var g in visitors)
                {
                    if (existingVisits.TryGetValue(g.Key, out var v))
                        v.PageViews += g.Count();
                    else
                    {
                        var first = g.OrderBy(h => h.Utc).First();
                        db.SiteVisits.Add(new SiteVisit
                        {
                            Day = day, VisitorHash = g.Key, Source = first.Source,
                            LandingPath = first.Path, PageViews = g.Count()
                        });
                    }
                }

                var pages = byDay.GroupBy(h => h.Path).ToList();
                var paths = pages.Select(g => g.Key).ToList();
                var existingPages = await db.SitePageViews
                    .Where(p => p.Day == day && paths.Contains(p.Path))
                    .ToDictionaryAsync(p => p.Path, ct);
                foreach (var g in pages)
                {
                    if (existingPages.TryGetValue(g.Key, out var p)) p.Views += g.Count();
                    else db.SitePageViews.Add(new SitePageView { Day = day, Path = g.Key, Views = g.Count() });
                }
            }

            await db.SaveChangesAsync(ct);
            return hits.Count;
        }
        finally
        {
            _flushLock.Release();
        }
    }
}
