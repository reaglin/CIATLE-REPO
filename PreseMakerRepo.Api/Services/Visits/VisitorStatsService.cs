using System.Globalization;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Api.Services.Visits;

public sealed record PeriodRow(string Label, DateOnly Start, int Visitors, int PageViews);
public sealed record PublicVisitorFigure(int Visitors, int Days);
/// <summary>Clicks on one program in the program panel (plan 10.4).</summary>
public sealed record ProgramClickRow(string ProgramId, int PageClicks, int StoreClicks)
{
    public int Total => PageClicks + StoreClicks;
}
public sealed record CountRow(string Name, int Count, string? Link = null, string? Detail = null);

public sealed class VisitorStats
{
    public int Days { get; init; }
    public DateOnly From { get; init; }
    public DateOnly To { get; init; }
    /// <summary>The first day the counter recorded anything, or null if it has recorded nothing yet.</summary>
    public DateOnly? CountingSince { get; init; }
    /// <summary>Days in the range the counter was running (fewer than <see cref="Days"/> just after it started).</summary>
    public int DaysCounted { get; init; }
    public int Visitors { get; init; }
    public int PageViews { get; init; }
    public double AverageVisitorsPerDay { get; init; }
    public double PagesPerVisitor { get; init; }
    public bool ByWeek { get; init; }
    public IReadOnlyList<PeriodRow> Periods { get; init; } = [];
    public IReadOnlyList<CountRow> Sections { get; init; } = [];
    public IReadOnlyList<CountRow> Courses { get; init; } = [];
    public IReadOnlyList<CountRow> Pages { get; init; } = [];
    /// <summary>Arrivals (one per visitor per day) by referring site; "direct" ones are in <see cref="DirectArrivals"/>.</summary>
    public IReadOnlyList<CountRow> Sources { get; init; } = [];
    public int DirectArrivals { get; init; }
    /// <summary>Clicks on the program panel, most first (plan 10.4).</summary>
    public IReadOnlyList<ProgramClickRow> ProgramClicks { get; init; } = [];
    /// <summary>Arrivals (one per visitor per day): the panel shows once on each, so they are the base for the click rate (plan 14.3).</summary>
    public int Arrivals { get; init; }
}

/// <summary>Reads the visitor counter's tables for <c>/admin/visitors</c> and the admin dashboard.</summary>
public sealed class VisitorStatsService
{
    public static readonly int[] Ranges = [7, 30, 90, 365];

    private readonly AppDbContext _db;
    public VisitorStatsService(AppDbContext db) => _db = db;

    public async Task<VisitorStats> GetAsync(int days, DateOnly? today = null, CancellationToken ct = default)
    {
        days = Math.Clamp(days, 1, 366);
        var to = today ?? VisitClassifier.FloridaDay(DateTime.UtcNow);
        var from = to.AddDays(-(days - 1));

        DateOnly? since = await _db.SiteVisits.AnyAsync(ct)
            ? await _db.SiteVisits.MinAsync(v => v.Day, ct)
            : null;

        var visits = await _db.SiteVisits.AsNoTracking()
            .Where(v => v.Day >= from && v.Day <= to)
            .Select(v => new { v.Day, v.VisitorHash, v.Source, v.PageViews })
            .ToListAsync(ct);

        var pageTotals = await _db.SitePageViews.AsNoTracking()
            .Where(p => p.Day >= from && p.Day <= to)
            .GroupBy(p => p.Path)
            .Select(g => new { Path = g.Key, Views = g.Sum(p => p.Views) })
            .ToListAsync(ct);

        var clicks = await _db.ProgramPanelClicks.AsNoTracking()
            .Where(c => c.Day >= from && c.Day <= to)
            .Select(c => new { c.ProgramId, c.Link, c.Clicks })
            .ToListAsync(ct);

        var start = since is { } s && s > from ? s : from;
        var daysCounted = since is null || start > to ? 0 : to.DayNumber - start.DayNumber + 1;

        var visitors = visits.Select(v => v.VisitorHash).Distinct().Count();
        var views = visits.Sum(v => v.PageViews);
        var byWeek = days > 31;

        var periods = new List<PeriodRow>();
        if (daysCounted > 0)
        {
            if (!byWeek)
            {
                for (var d = start; d <= to; d = d.AddDays(1))
                {
                    var day = visits.Where(v => v.Day == d).ToList();
                    periods.Add(new PeriodRow(d.ToString("ddd d MMM yyyy", CultureInfo.InvariantCulture) + (d == to ? " (so far)" : ""), d,
                        day.Count, day.Sum(v => v.PageViews)));
                }
            }
            else
            {
                for (var w = WeekStart(start); w <= to; w = w.AddDays(7))
                {
                    var end = w.AddDays(6);
                    var week = visits.Where(v => v.Day >= w && v.Day <= end).ToList();
                    var part = w < start || end > to ? " (part week)" : "";
                    periods.Add(new PeriodRow("Week of " + w.ToString("d MMM yyyy", CultureInfo.InvariantCulture) + part, w,
                        week.Select(v => v.VisitorHash).Distinct().Count(), week.Sum(v => v.PageViews)));
                }
            }
        }

        var courses = pageTotals
            .Select(p => new { Course = VisitClassifier.CourseOf(p.Path), p.Views })
            .Where(p => p.Course != null)
            .GroupBy(p => p.Course!)
            .Select(g => new { Id = g.Key, Views = g.Sum(p => p.Views) })
            .OrderByDescending(r => r.Views).ThenBy(r => r.Id).Take(20).ToList();
        var ids = courses.Select(c => c.Id).ToList();
        var titles = await _db.TaxonomyCourses.AsNoTracking()
            .Where(c => ids.Contains(c.CourseId))
            .Select(c => new { c.CourseId, c.Title })
            .ToDictionaryAsync(c => c.CourseId, c => c.Title, ct);

        return new VisitorStats
        {
            Days = days, From = from, To = to, CountingSince = since, DaysCounted = daysCounted,
            Visitors = visitors, PageViews = views,
            AverageVisitorsPerDay = daysCounted == 0 ? 0 : (double)visits.Count / daysCounted,
            PagesPerVisitor = visitors == 0 ? 0 : (double)views / visitors,
            ByWeek = byWeek,
            Periods = periods,
            Sections = pageTotals
                .GroupBy(p => VisitClassifier.SectionOf(p.Path))
                .Select(g => new CountRow(g.Key, g.Sum(p => p.Views)))
                .OrderByDescending(r => r.Count).ToList(),
            Courses = courses
                .Select(c => new CountRow(c.Id, c.Views, "/courses/" + c.Id, titles.GetValueOrDefault(c.Id)))
                .ToList(),
            Pages = pageTotals
                .OrderByDescending(p => p.Views).ThenBy(p => p.Path).Take(25)
                .Select(p => new CountRow(p.Path, p.Views, p.Path)).ToList(),
            Sources = visits.Where(v => v.Source != null)
                .GroupBy(v => v.Source!)
                .Select(g => new CountRow(g.Key, g.Count()))
                .OrderByDescending(r => r.Count).ThenBy(r => r.Name).Take(20).ToList(),
            DirectArrivals = visits.Count(v => v.Source == null),
            ProgramClicks = clicks
                .GroupBy(c => c.ProgramId)
                .Select(g => new ProgramClickRow(g.Key,
                    g.Where(c => c.Link == "page").Sum(c => c.Clicks),
                    g.Where(c => c.Link == "store").Sum(c => c.Clicks)))
                .OrderByDescending(r => r.Total).ThenBy(r => r.ProgramId).ToList(),
            Arrivals = visits.Count,
        };
    }

    /// <summary>Distinct visitors over the last <paramref name="days"/> days, for the dashboard card.</summary>
    public async Task<int> CountVisitorsAsync(int days, CancellationToken ct = default)
    {
        var to = VisitClassifier.FloridaDay(DateTime.UtcNow);
        var from = to.AddDays(-(days - 1));
        return await _db.SiteVisits.Where(v => v.Day >= from && v.Day <= to)
            .Select(v => v.VisitorHash).Distinct().CountAsync(ct);
    }

    /// <summary>The default span of the public figure (the admin page's "Last 30 days").</summary>
    public const int PublicFigureDays = 30;

    /// <summary>
    /// A public figure (plan 9.5; the header bar's uses 7 days, plan 13): distinct visitors over the last
    /// <paramref name="days"/> days, the same number as the admin page's matching range. While the counter has run
    /// for less than that, <c>Days</c> is the days it has run. Null below <paramref name="minimum"/> visitors (a tiny
    /// early number would say nobody uses the site), so nothing is shown.
    /// </summary>
    public async Task<PublicVisitorFigure?> GetPublicFigureAsync(int minimum, DateOnly? today = null,
        CancellationToken ct = default, int days = PublicFigureDays)
    {
        var since = await CountingSinceAsync(ct);
        if (since is null) return null;
        var to = today ?? VisitClassifier.FloridaDay(DateTime.UtcNow);
        var from = to.AddDays(-(days - 1));
        var visitors = await _db.SiteVisits.Where(v => v.Day >= from && v.Day <= to)
            .Select(v => v.VisitorHash).Distinct().CountAsync(ct);
        if (visitors == 0 || visitors < minimum) return null;
        var start = since > from ? since.Value : from;
        return new PublicVisitorFigure(visitors, to.DayNumber - start.DayNumber + 1);
    }

    /// <summary>The first day the counter recorded anything, or null.</summary>
    public async Task<DateOnly?> CountingSinceAsync(CancellationToken ct = default) =>
        await _db.SiteVisits.AnyAsync(ct) ? await _db.SiteVisits.MinAsync(v => v.Day, ct) : null;

    private static DateOnly WeekStart(DateOnly d) =>
        d.AddDays(-(((int)d.DayOfWeek + 6) % 7));   // Monday
}
