using System.Threading.Channels;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Api.Services.Visits;

/// <summary>One counted page view, as handed from the middleware to the recorder.</summary>
public sealed record VisitHit(DateTime Utc, string VisitorHash, string Path, string? Source);

/// <summary>One counted click on the home page's program panel (plan 10.4): which program, which link.</summary>
public sealed record ProgramClickHit(DateTime Utc, string ProgramId, string Link);

/// <summary>
/// Collects counted page views in memory and writes them to the database once a minute (and when
/// the site stops), so a page view never waits on a database write. A singleton and a hosted
/// service. If the queue ever fills (50,000 waiting), further views are dropped, not blocked on.
/// </summary>
public sealed class VisitRecorder : BackgroundService
{
    private readonly Channel<VisitHit> _queue = Channel.CreateBounded<VisitHit>(
        new BoundedChannelOptions(50_000) { FullMode = BoundedChannelFullMode.DropWrite, SingleReader = true });
    private readonly Channel<ProgramClickHit> _clicks = Channel.CreateBounded<ProgramClickHit>(
        new BoundedChannelOptions(10_000) { FullMode = BoundedChannelFullMode.DropWrite, SingleReader = true });
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

    public void Record(ProgramClickHit click) => _clicks.Writer.TryWrite(click);

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

    /// <summary>Writes everything waiting. Returns how many page views and program-panel clicks were written.</summary>
    public async Task<int> FlushAsync(CancellationToken ct = default)
    {
        await _flushLock.WaitAsync(ct);
        try
        {
            var hits = new List<VisitHit>();
            while (_queue.Reader.TryRead(out var h)) hits.Add(h);
            var clicks = new List<ProgramClickHit>();
            while (_clicks.Reader.TryRead(out var c)) clicks.Add(c);
            if (hits.Count == 0 && clicks.Count == 0) return 0;

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

            foreach (var byDay in clicks.GroupBy(c => VisitClassifier.FloridaDay(c.Utc)))
            {
                var day = byDay.Key;
                var existing = await db.ProgramPanelClicks.Where(c => c.Day == day).ToListAsync(ct);
                foreach (var g in byDay.GroupBy(c => (c.ProgramId, c.Link)))
                {
                    var row = existing.FirstOrDefault(c => c.ProgramId == g.Key.ProgramId && c.Link == g.Key.Link);
                    if (row is not null) row.Clicks += g.Count();
                    else db.ProgramPanelClicks.Add(new ProgramPanelClick
                    {
                        Day = day, ProgramId = g.Key.ProgramId, Link = g.Key.Link, Clicks = g.Count()
                    });
                }
            }

            await db.SaveChangesAsync(ct);
            return hits.Count + clicks.Count;
        }
        finally
        {
            _flushLock.Release();
        }
    }
}
