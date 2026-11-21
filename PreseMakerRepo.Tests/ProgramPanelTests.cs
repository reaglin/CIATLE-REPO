using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging.Abstractions;
using PreseMakerRepo.Api.Services;
using PreseMakerRepo.Api.Services.Visits;
using PreseMakerRepo.Infrastructure.Data;
using Xunit;

namespace PreseMakerRepo.Tests;

/// <summary>The home page's program panel (plan Phase 10): reading apps.json, failing quietly, counting clicks.</summary>
public class ProgramPanelTests
{
    private const string Chrome = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36";

    private static string Program(string id, string icon = "https://softwareplus.ai/images/icons/x.png",
        string page = "https://softwareplus.ai/x/", string store = "https://apps.microsoft.com/detail/9ABC") =>
        $$"""{ "id": "{{id}}", "name": "Name {{id}}", "summary": "One line.", "icon": "{{icon}}", "page": "{{page}}", "store": "{{store}}" }""";

    [Fact]
    public void The_SoftwarePlus_list_is_read_in_full()
    {
        var path = Path.Combine(AppContext.BaseDirectory, "apps.json");
        if (!File.Exists(path)) return;   // the SoftwarePlus repo is not beside this one
        var list = ProgramPanelService.Parse(File.ReadAllText(path));
        Assert.True(list.Count >= 10);
        Assert.Contains(list, p => p.Id == "gamify" && p.Name == "Gamify+");
    }

    [Fact]
    public void Good_programs_are_kept()
    {
        var list = ProgramPanelService.Parse($$"""{ "programs": [ {{Program("gamify")}}, {{Program("smada")}} ] }""");
        Assert.Equal(["gamify", "smada"], list.Select(p => p.Id));
    }

    [Theory]
    [InlineData("https://evil.example/x.png", "https://softwareplus.ai/x/", "https://apps.microsoft.com/detail/9ABC")]   // icon elsewhere
    [InlineData("https://softwareplus.ai/x.png", "javascript:alert(1)", "https://apps.microsoft.com/detail/9ABC")]     // script link
    [InlineData("https://softwareplus.ai/x.png", "http://softwareplus.ai/x/", "https://apps.microsoft.com/detail/9ABC")] // not https
    [InlineData("https://softwareplus.ai/x.png", "https://softwareplus.ai/x/", "https://apps.microsoft.com.evil.example/d")]
    public void A_program_linking_anywhere_else_is_left_out(string icon, string page, string store)
    {
        var list = ProgramPanelService.Parse($$"""{ "programs": [ {{Program("bad", icon, page, store)}}, {{Program("good")}} ] }""");
        Assert.Equal(["good"], list.Select(p => p.Id));
    }

    [Theory]
    [InlineData("not json")]
    [InlineData("{}")]
    [InlineData("""{ "programs": "none" }""")]
    [InlineData("""{ "programs": [ { "id": "Bad Id!", "name": "x" } ] }""")]
    public void A_broken_list_gives_no_programs(string json) =>
        Assert.Empty(ProgramPanelService.Parse(json));

    private sealed class FailingHandler : HttpMessageHandler
    {
        protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken ct) =>
            throw new HttpRequestException("unreachable");
    }

    private sealed class Factory(HttpMessageHandler handler) : IHttpClientFactory
    {
        public HttpClient CreateClient(string name) => new(handler, disposeHandler: false);
    }

    [Fact]
    public async Task An_unreachable_list_leaves_the_panel_out_without_an_error()
    {
        var service = new ProgramPanelService(new Factory(new FailingHandler()), new MemoryCache(new MemoryCacheOptions()),
            new ConfigurationBuilder().Build(), NullLogger<ProgramPanelService>.Instance);
        Assert.Null(await service.PickAsync());
        Assert.False(await service.IsKnownAsync("gamify"));
    }

    [Fact]
    public void Only_the_two_links_from_a_person_are_counted()
    {
        Assert.True(VisitClassifier.ShouldCountProgramClick("page", Chrome, isAdministrator: false));
        Assert.True(VisitClassifier.ShouldCountProgramClick("store", Chrome, isAdministrator: false));
        Assert.False(VisitClassifier.ShouldCountProgramClick("elsewhere", Chrome, isAdministrator: false));
        Assert.False(VisitClassifier.ShouldCountProgramClick(null, Chrome, isAdministrator: false));
        Assert.False(VisitClassifier.ShouldCountProgramClick("page", Chrome, isAdministrator: true));
        Assert.False(VisitClassifier.ShouldCountProgramClick("page", "curl/8.4.0", isAdministrator: false));
    }

    [Fact]
    public async Task Clicks_are_saved_per_day_program_and_link_and_read_back_beside_home_page_views()
    {
        var conn = new SqliteConnection("DataSource=:memory:");
        conn.Open();
        var services = new ServiceCollection();
        services.AddDbContext<AppDbContext>(o => o.UseSqlite(conn));
        using var sp = services.BuildServiceProvider();
        using (conn)
        {
            using (var scope = sp.CreateScope())
                scope.ServiceProvider.GetRequiredService<AppDbContext>().Database.EnsureCreated();

            var noon = new DateTime(2026, 11, 21, 17, 0, 0, DateTimeKind.Utc);
            var rec = new VisitRecorder(sp.GetRequiredService<IServiceScopeFactory>(), NullLogger<VisitRecorder>.Instance);
            rec.Record(new VisitHit(noon, "aaaaaaaaaaaaaaaa", "/", null));
            rec.Record(new VisitHit(noon, "bbbbbbbbbbbbbbbb", "/", null));
            rec.Record(new ProgramClickHit(noon, "gamify", "page"));
            rec.Record(new ProgramClickHit(noon, "gamify", "store"));
            Assert.Equal(4, await rec.FlushAsync());
            rec.Record(new ProgramClickHit(noon.AddMinutes(5), "gamify", "page"));   // adds to the same row
            rec.Record(new ProgramClickHit(noon.AddMinutes(5), "smada", "store"));
            Assert.Equal(2, await rec.FlushAsync());

            using var read = sp.CreateScope();
            var stats = await new VisitorStatsService(read.ServiceProvider.GetRequiredService<AppDbContext>())
                .GetAsync(7, today: new DateOnly(2026, 11, 21));
            Assert.Equal(2, stats.HomePageViews);
            var gamify = stats.ProgramClicks[0];
            Assert.Equal(("gamify", 2, 1), (gamify.ProgramId, gamify.PageClicks, gamify.StoreClicks));
            Assert.Equal(("smada", 0, 1), (stats.ProgramClicks[1].ProgramId, stats.ProgramClicks[1].PageClicks, stats.ProgramClicks[1].StoreClicks));
        }
    }
}
