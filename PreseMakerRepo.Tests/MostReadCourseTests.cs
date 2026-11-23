using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Memory;
using PreseMakerRepo.Api.Options;
using PreseMakerRepo.Api.Services;
using PreseMakerRepo.Api.Services.Visits;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;
using PreseMakerRepo.Infrastructure.Options;
using Xunit;
using MsOptions = Microsoft.Extensions.Options.Options;

namespace PreseMakerRepo.Tests;

/// <summary>Most-read courses (plan 15.3–15.5): their titles, the top 100, and the guide requests the site makes.</summary>
public class MostReadCourseTests : IDisposable
{
    private static readonly DateOnly Today = new(2026, 11, 20);
    private readonly SqliteConnection _conn = new("DataSource=:memory:");
    private readonly AppDbContext _db;

    public MostReadCourseTests()
    {
        _conn.Open();
        _db = new AppDbContext(new DbContextOptionsBuilder<AppDbContext>().UseSqlite(_conn).Options);
        _db.Database.EnsureCreated();
        _db.TaxonomyNodes.Add(new TaxonomyNode { Key = "CJK", Level = 3, Name = "Criminal Justice" });
        void Course(string id, string title, string? state = null) =>
            _db.TaxonomyCourses.Add(new TaxonomyCourse { CourseId = id, Level3Key = "CJK", Title = title, StateTitle = state, IsActive = true });
        Course("CJK0570", "CJK0570", "CORRECTIONAL OFFICER VOCATIONAL");   // placeholder title; the state's is real
        Course("CJK0001", "Intro to Corrections");
        Course("CJK0002", "CJK0002");                                       // only a guide has the title
        Course("CJK0003", "Declined Course");
        Course("CJK0004", "Waiting Course");
        _db.CurriculumGuides.Add(new CurriculumGuide { CourseId = "CJK0002", Title = "CJK0002: Firearms", HtmlContent = "<p/>" });
        _db.GuideRequests.Add(new GuideRequest { Id = Guid.NewGuid(), CourseId = "CJK0003", CourseTitle = "x", Status = GuideRequestStatus.Declined, RequestedUtc = DateTime.UtcNow });
        _db.GuideRequests.Add(new GuideRequest { Id = Guid.NewGuid(), CourseId = "CJK0004", CourseTitle = "x", Status = GuideRequestStatus.Held, RequestedUtc = DateTime.UtcNow });
        // Pages read: CJK0570 most, then 0001 ... and a course id that is not listed.
        var views = new (string Path, int Views)[]
        {
            ("/courses/CJK0570", 50), ("/courses/CJK0001", 40), ("/courses/CJK0002/guide", 30),
            ("/courses/CJK0003", 20), ("/courses/CJK0004", 10), ("/courses/ZZZ9999", 5),
        };
        foreach (var (path, n) in views) _db.SitePageViews.Add(new SitePageView { Day = Today, Path = path, Views = n });
        _db.SiteVisits.Add(new SiteVisit { Day = Today, VisitorHash = "aaaaaaaaaaaaaaaa", PageViews = 155 });
        _db.SaveChanges();
    }

    public void Dispose()
    {
        _db.Dispose();
        _conn.Dispose();
    }

    private GuideRequestService Requests() => new(_db, new MemoryCache(new MemoryCacheOptions()),
        MsOptions.Create(new RepositoryOptions()), MsOptions.Create(new SecurityOptions()));

    [Fact]
    public async Task Most_read_courses_show_the_title_their_own_page_shows()
    {
        var stats = await new VisitorStatsService(_db).GetAsync(7, today: Today);
        var detail = stats.Courses.ToDictionary(c => c.Name, c => c.Detail);
        Assert.Equal("Correctional Officer Vocational", detail["CJK0570"]);   // was blank: the stored title is the id
        Assert.Equal("Intro to Corrections", detail["CJK0001"]);
        Assert.Equal("Firearms", detail["CJK0002"]);
        Assert.Null(detail["ZZZ9999"]);                                     // not listed: no title to show
    }

    [Fact]
    public async Task The_list_can_be_cut_to_any_length()
    {
        var svc = new VisitorStatsService(_db);
        Assert.Equal(6, (await svc.GetAsync(7, today: Today, topCourses: 100)).Courses.Count);
        Assert.Equal(["CJK0570", "CJK0001"], (await svc.GetAsync(7, today: Today, topCourses: 2)).Courses.Select(c => c.Name));
    }

    [Fact]
    public async Task Most_read_courses_without_a_guide_are_requested_once()
    {
        var stats = await new VisitorStatsService(_db).GetAsync(7, today: Today);
        var service = Requests();
        var made = await service.RequestMostReadAsync(stats.Courses.Select(c => (c.Name, c.Count)).ToList(), 7);

        // Not 0002 (has a guide), 0003 (declined), 0004 (already waiting), or ZZZ9999 (not a listed course).
        Assert.Equal(["CJK0570", "CJK0001"], made);
        var r = await _db.GuideRequests.AsNoTracking().SingleAsync(g => g.CourseId == "CJK0570");
        Assert.Equal(GuideRequestChannel.MostRead, r.Channel);
        Assert.Equal(GuideRequestStatus.Open, r.Status);
        Assert.Equal("Correctional Officer Vocational", r.CourseTitle);
        Assert.Equal(GuideRequestService.MostReadReason(1, 50, 7), r.Reason);

        // The next hourly pass finds them already waiting and asks for nothing more.
        Assert.Empty(await service.RequestMostReadAsync(stats.Courses.Select(c => (c.Name, c.Count)).ToList(), 7));
        Assert.Equal(4, await _db.GuideRequests.CountAsync());
    }
}
