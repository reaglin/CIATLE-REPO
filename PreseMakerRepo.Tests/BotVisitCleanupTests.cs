using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Migrations;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;
using Xunit;

namespace PreseMakerRepo.Tests;

/// <summary>
/// Plan 16.2: the migration RemoveBotVisitsNov2026 takes out the 21–24 November 2026 scraper's visits (no referring
/// site, landing on course resources or the subject tree) and those sections' page views on those days, and nothing else.
/// </summary>
public class BotVisitCleanupTests
{
    private const string Before = "20261121233750_AddResourceSubmissionSuggestions";

    [Fact]
    public async Task The_scrapers_visits_go_and_everything_else_stays()
    {
        using var conn = new SqliteConnection("DataSource=:memory:");
        conn.Open();
        var options = new DbContextOptionsBuilder<AppDbContext>().UseSqlite(conn).Options;

        await using (var db = new AppDbContext(options))
        {
            await db.GetService<IMigrator>().MigrateAsync(Before);

            var sat = new DateOnly(2026, 11, 21);
            var tue = new DateOnly(2026, 11, 24);
            var wed = new DateOnly(2026, 11, 25);
            var fri = new DateOnly(2026, 11, 20);
            db.SiteVisits.AddRange(
                // The scraper: no referring site, a resources page or the subject tree, on the four days.
                Visit(sat, "a1", null, "/courses/EEL4205/resources"),
                Visit(tue, "a2", null, "/courses/NUR4286-SCNS/resources", views: 2),
                Visit(sat, "a3", null, "/browse/engineering"),
                // Kept: a person from Google on a resources page, a direct visit to a course page or the home page,
                // and the same kind of visit on a day outside the four.
                Visit(sat, "k1", "google.com", "/courses/EEL4205/resources"),
                Visit(sat, "k2", null, "/courses/EEL4205"),
                Visit(tue, "k3", null, "/"),
                Visit(wed, "k4", null, "/courses/EEL4205/resources"),
                Visit(fri, "k5", null, "/browse"));
            db.SitePageViews.AddRange(
                Views(sat, "/courses/EEL4205/resources", 3),
                Views(tue, "/browse", 40),
                Views(sat, "/courses/EEL4205", 1),
                Views(tue, "/", 2),
                Views(wed, "/courses/EEL4205/resources", 1),
                Views(fri, "/browse", 1));
            await db.SaveChangesAsync();

            await db.Database.MigrateAsync();
        }

        await using (var db = new AppDbContext(options))
        {
            var visits = await db.SiteVisits.Select(v => v.VisitorHash).OrderBy(h => h).ToListAsync();
            Assert.Equal(["k1", "k2", "k3", "k4", "k5"], visits);

            var pages = (await db.SitePageViews.ToListAsync())
                .Select(p => $"{p.Day:MM-dd} {p.Path}").OrderBy(p => p).ToList();
            Assert.Equal(["11-20 /browse", "11-21 /courses/EEL4205", "11-24 /", "11-25 /courses/EEL4205/resources"], pages);
        }
    }

    [Fact]
    public async Task On_an_empty_database_it_does_nothing()
    {
        using var conn = new SqliteConnection("DataSource=:memory:");
        conn.Open();
        await using var db = new AppDbContext(new DbContextOptionsBuilder<AppDbContext>().UseSqlite(conn).Options);
        await db.Database.MigrateAsync();
        Assert.Empty(await db.Database.GetPendingMigrationsAsync());
        Assert.Equal(0, await db.SiteVisits.CountAsync());
    }

    private static SiteVisit Visit(DateOnly day, string hash, string? source, string landing, int views = 1) =>
        new() { Day = day, VisitorHash = hash, Source = source, LandingPath = landing, PageViews = views };

    private static SitePageView Views(DateOnly day, string path, int views) =>
        new() { Day = day, Path = path, Views = views };
}
