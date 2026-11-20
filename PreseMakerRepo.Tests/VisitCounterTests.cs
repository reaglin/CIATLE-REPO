using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging.Abstractions;
using PreseMakerRepo.Api.Services.Visits;
using PreseMakerRepo.Infrastructure.Data;
using Xunit;

namespace PreseMakerRepo.Tests;

/// <summary>The visitor counter (plan Phase 9): what is counted, and what the admin page reads back.</summary>
public class VisitCounterTests
{
    private const string Chrome = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36";

    [Theory]
    [InlineData("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")]
    [InlineData("python-requests/2.32")]
    [InlineData("curl/8.4.0")]
    [InlineData("Claude-User (claude-code/2.0)")]
    [InlineData("Mozilla/5.0 (Windows NT 10.0) WindowsPowerShell/5.1")]
    [InlineData("")]
    [InlineData(null)]
    public void Bots_scripts_and_empty_agents_are_not_people(string? ua) =>
        Assert.True(VisitClassifier.IsBot(ua));

    [Fact]
    public void A_browser_is_a_person() => Assert.False(VisitClassifier.IsBot(Chrome));

    [Fact]
    public void A_person_opening_a_page_is_counted() =>
        Assert.True(VisitClassifier.ShouldCount("GET", "/courses/EEL4205", 200, "text/html; charset=utf-8", Chrome, false, false));

    [Theory]
    [InlineData("POST", "/request-guide", 200, "text/html")]       // a form sent, not a page opened
    [InlineData("GET", "/courses/XYZ9999", 404, "text/html")]       // not found
    [InlineData("GET", "/api/v1/courses", 200, "text/html")]        // the API
    [InlineData("GET", "/admin/visitors", 200, "text/html")]        // the admin console
    [InlineData("GET", "/courses/EEL4205", 200, "application/json")] // not a page
    [InlineData("GET", "/lib/site.css", 200, "text/css")]
    public void Other_requests_are_not_counted(string method, string path, int status, string type) =>
        Assert.False(VisitClassifier.ShouldCount(method, path, status, type, Chrome, false, false));

    [Fact]
    public void Administrators_and_prefetches_are_not_counted()
    {
        Assert.False(VisitClassifier.ShouldCount("GET", "/", 200, "text/html", Chrome, isAdministrator: true, isPrefetch: false));
        Assert.False(VisitClassifier.ShouldCount("GET", "/", 200, "text/html", Chrome, isAdministrator: false, isPrefetch: true));
    }

    [Theory]
    [InlineData("/courses/eel4205/guide/", "/courses/EEL4205/guide")]
    [InlineData("/courses/nur4286-scns", "/courses/NUR4286-SCNS")]
    [InlineData("/", "/")]
    [InlineData("/browse/", "/browse")]
    public void Paths_are_stored_one_way(string raw, string stored) =>
        Assert.Equal(stored, VisitClassifier.NormalizePath(raw));

    [Theory]
    [InlineData("/", "Home page")]
    [InlineData("/courses/EEL4205", "Course pages")]
    [InlineData("/courses/EEL4205/guide", "Curriculum guides")]
    [InlineData("/courses/EEL4205/resources", "Course resources")]
    [InlineData("/careers/registered-nurse", "Career paths")]
    [InlineData("/queue/guides", "Request queues")]
    [InlineData("/about", "Other pages")]
    public void Pages_fall_into_parts_of_the_site(string path, string section) =>
        Assert.Equal(section, VisitClassifier.SectionOf(path));

    [Theory]
    [InlineData("https://www.google.com/search?q=x", "google.com")]
    [InlineData("https://chatgpt.com/", "chatgpt.com")]
    [InlineData("https://floridacourserepo.com/browse", null)]   // moving between our own pages
    [InlineData("", null)]
    [InlineData("not a url", null)]
    public void The_source_is_the_referring_site(string referer, string? source) =>
        Assert.Equal(source, VisitClassifier.SourceOf(referer, "floridacourserepo.com"));

    [Fact]
    public void The_visitor_code_holds_no_address_and_is_stable()
    {
        var a = VisitClassifier.VisitorHash("salt", "203.0.113.9", Chrome);
        Assert.Equal(a, VisitClassifier.VisitorHash("salt", "203.0.113.9", Chrome));
        Assert.NotEqual(a, VisitClassifier.VisitorHash("salt", "203.0.113.10", Chrome));
        Assert.NotEqual(a, VisitClassifier.VisitorHash("other-salt", "203.0.113.9", Chrome));
        Assert.Equal(16, a.Length);
        Assert.DoesNotContain("203", a);
    }

    [Fact]
    public void Days_are_Florida_days()
    {
        // 02:00 UTC on 21 Nov is 21:00 on 20 Nov in Florida (EST, UTC-5).
        Assert.Equal(new DateOnly(2026, 11, 20), VisitClassifier.FloridaDay(new DateTime(2026, 11, 21, 2, 0, 0, DateTimeKind.Utc)));
    }

    // ---- the recorder and the admin page's figures, against a real SQLite database ----------

    private static (ServiceProvider sp, SqliteConnection conn) Database()
    {
        var conn = new SqliteConnection("DataSource=:memory:");
        conn.Open();
        var services = new ServiceCollection();
        services.AddDbContext<AppDbContext>(o => o.UseSqlite(conn));
        var sp = services.BuildServiceProvider();
        using (var scope = sp.CreateScope())
            scope.ServiceProvider.GetRequiredService<AppDbContext>().Database.EnsureCreated();
        return (sp, conn);
    }

    private static DateTime FloridaNoon(int day) => new(2026, 11, day, 17, 0, 0, DateTimeKind.Utc);

    [Fact]
    public async Task Views_are_saved_per_visitor_per_day_and_per_page()
    {
        var (sp, conn) = Database();
        using (conn) using (sp)
        {
            var rec = new VisitRecorder(sp.GetRequiredService<IServiceScopeFactory>(), NullLogger<VisitRecorder>.Instance);
            // Visitor A: Google, then two more pages. Visitor B: direct. Both on 18 Nov.
            rec.Record(new VisitHit(FloridaNoon(18), "aaaaaaaaaaaaaaaa", "/courses/EEL4205", "google.com"));
            rec.Record(new VisitHit(FloridaNoon(18).AddMinutes(1), "aaaaaaaaaaaaaaaa", "/courses/EEL4205/guide", null));
            rec.Record(new VisitHit(FloridaNoon(18).AddMinutes(2), "aaaaaaaaaaaaaaaa", "/", null));
            rec.Record(new VisitHit(FloridaNoon(18), "bbbbbbbbbbbbbbbb", "/", null));
            Assert.Equal(4, await rec.FlushAsync());

            // A later flush adds to the same rows; A comes back on 20 Nov.
            rec.Record(new VisitHit(FloridaNoon(18).AddHours(1), "bbbbbbbbbbbbbbbb", "/", "bing.com"));
            rec.Record(new VisitHit(FloridaNoon(20), "aaaaaaaaaaaaaaaa", "/browse", "chatgpt.com"));
            Assert.Equal(2, await rec.FlushAsync());
            Assert.Equal(0, await rec.FlushAsync());

            using var scope = sp.CreateScope();
            var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
            var b18 = await db.SiteVisits.SingleAsync(v => v.Day == new DateOnly(2026, 11, 18) && v.VisitorHash == "bbbbbbbbbbbbbbbb");
            Assert.Equal(2, b18.PageViews);
            Assert.Null(b18.Source);                          // the first page of the day decides the source
            Assert.Equal(3, (await db.SitePageViews.SingleAsync(p => p.Path == "/" && p.Day == new DateOnly(2026, 11, 18))).Views);

            var stats = await new VisitorStatsService(db).GetAsync(7, today: new DateOnly(2026, 11, 20));
            Assert.Equal(2, stats.Visitors);                  // A counted once although they came on two days
            Assert.Equal(6, stats.PageViews);
            Assert.Equal(new DateOnly(2026, 11, 18), stats.CountingSince);
            Assert.Equal(3, stats.DaysCounted);               // started on the 18th, not 7 days ago
            Assert.Equal(1.0, stats.AverageVisitorsPerDay);   // 3 visitor-days over 3 days
            Assert.Equal(3, stats.Periods.Count);
            Assert.Equal(0, stats.Periods[1].Visitors);       // 19 Nov, nobody
            Assert.EndsWith("(so far)", stats.Periods[2].Label);   // today is not a whole day yet

            var weeks = await new VisitorStatsService(db).GetAsync(90, today: new DateOnly(2026, 11, 20));
            Assert.True(weeks.ByWeek);
            Assert.Single(weeks.Periods);                     // Mon 16 Nov to today
            Assert.EndsWith("(part week)", weeks.Periods[0].Label);
            Assert.Equal(2, weeks.Periods[0].Visitors);
            Assert.Equal("EEL4205", stats.Courses.Single().Name);
            Assert.Equal(2, stats.Courses.Single().Count);    // course page + guide
            Assert.Equal(1, stats.DirectArrivals);            // B on the 18th
            Assert.Contains(stats.Sources, r => r.Name == "google.com" && r.Count == 1);
            Assert.Contains(stats.Sources, r => r.Name == "chatgpt.com" && r.Count == 1);
            Assert.Contains(stats.Sections, r => r.Name == "Home page" && r.Count == 3);
        }
    }

    [Fact]
    public async Task An_empty_counter_says_so()
    {
        var (sp, conn) = Database();
        using (conn) using (sp)
        {
            using var scope = sp.CreateScope();
            var stats = await new VisitorStatsService(scope.ServiceProvider.GetRequiredService<AppDbContext>())
                .GetAsync(30, today: new DateOnly(2026, 11, 20));
            Assert.Null(stats.CountingSince);
            Assert.Equal(0, stats.Visitors);
            Assert.Empty(stats.Periods);
        }
    }
}
