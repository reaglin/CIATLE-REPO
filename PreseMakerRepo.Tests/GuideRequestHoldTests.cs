using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Memory;
using PreseMakerRepo.Api.Models.Requests;
using PreseMakerRepo.Api.Options;
using PreseMakerRepo.Api.Services;
using PreseMakerRepo.Api.Validators;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;
using PreseMakerRepo.Infrastructure.Options;
using Xunit;
using MsOptions = Microsoft.Extensions.Options.Options;

namespace PreseMakerRepo.Tests;

/// <summary>A request the pipeline cannot write is held with a public reason, declined with it, and can be asked for again.</summary>
public class GuideRequestHoldTests : IDisposable
{
    private const string Reason = "Florida Poly, the only college that offers it, publishes no description or syllabus.";
    private readonly SqliteConnection _conn = new("DataSource=:memory:");
    private readonly AppDbContext _db;
    private readonly GuideRequestService _service;

    public GuideRequestHoldTests()
    {
        _conn.Open();
        _db = new AppDbContext(new DbContextOptionsBuilder<AppDbContext>().UseSqlite(_conn).Options);
        _db.Database.EnsureCreated();
        _db.TaxonomyNodes.Add(new TaxonomyNode { Key = "EEL", Level = 3, Name = "Electrical Engineering" });
        _db.TaxonomyCourses.Add(new TaxonomyCourse { CourseId = "EEL4448", Level3Key = "EEL", Title = "Optoelectronics", IsActive = true });
        _db.SaveChanges();
        _service = new GuideRequestService(_db, new MemoryCache(new MemoryCacheOptions()),
            MsOptions.Create(new RepositoryOptions()), MsOptions.Create(new SecurityOptions()));
    }

    public void Dispose()
    {
        _db.Dispose();
        _conn.Dispose();
    }

    private Task<GuideRequestService.CreateResult> Ask(string ip, string? reason = null) =>
        _service.CreateAsync(new CreateGuideRequestRequest("EEL4448", null, null, reason, null), ip, null);

    private async Task<PreseMakerRepo.Api.Models.Responses.PublicGuideQueueItem> Public() =>
        Assert.Single((await _service.PublicQueueAsync(GuideRequestService.QueueAll)).Items);

    [Fact]
    public async Task Held_then_declined_shows_the_reason_and_can_be_asked_again()
    {
        await Ask("203.0.113.1");
        await _service.SetStatusAsync("EEL4448", GuideRequestStatus.Held, Reason);

        var held = await Public();
        Assert.Equal("Held", held.Status);
        Assert.Null(held.Note);                       // a hold's reason is not public yet
        Assert.Equal(1, (await _service.PublicQueueAsync(GuideRequestService.QueueWaiting)).Waiting);

        // A second visitor joins the hold rather than reopening the course.
        await Ask("203.0.113.2");
        Assert.All(_db.GuideRequests.AsNoTracking(), r => Assert.Equal(GuideRequestStatus.Held, r.Status));

        Assert.Equal(["EEL4448"], await _service.DeclineHeldAsync());
        var declined = await Public();
        Assert.Equal("Declined", declined.Status);
        Assert.Equal(Reason, declined.Note);
        Assert.Equal(Reason, await _service.DeclineReasonAsync("EEL4448"));

        // Asked again, saying what changed: the course reopens and the reviewer sees both.
        var again = await Ask("203.0.113.3", "UCF now offers it; syllabus at https://example.edu/eel4448");
        Assert.Equal(GuideRequestService.CreateOutcome.Created, again.Outcome);
        Assert.Equal("Open", (await Public()).Status);
        Assert.Null(await _service.DeclineReasonAsync("EEL4448"));
        var summary = Assert.Single(await _service.SummaryAsync(null));
        Assert.Equal(Reason, summary.AdminNotes);
        Assert.Contains("UCF now offers it; syllabus at https://example.edu/eel4448", summary.RequesterNotes!);
    }

    [Fact]
    public async Task Declining_held_leaves_other_courses_alone()
    {
        await Ask("203.0.113.1");
        Assert.Empty(await _service.DeclineHeldAsync());          // nothing on hold
        Assert.Equal("Open", (await Public()).Status);
    }

    [Fact]
    public void A_hold_needs_its_reason()
    {
        var v = new SetGuideRequestStatusRequestValidator();
        Assert.False(v.Validate(new SetGuideRequestStatusRequest("Held", null)).IsValid);
        Assert.True(v.Validate(new SetGuideRequestStatusRequest("held", Reason)).IsValid);
        Assert.True(v.Validate(new SetGuideRequestStatusRequest("Declined", null)).IsValid);
    }

    [Fact]
    public void Group_status_orders_held_between_queued_and_open()
    {
        Assert.Equal(GuideRequestStatus.Held, GuideRequestService.GroupStatus([GuideRequestStatus.Held, GuideRequestStatus.Open], false));
        Assert.Equal(GuideRequestStatus.Queued, GuideRequestService.GroupStatus([GuideRequestStatus.Held, GuideRequestStatus.Queued], false));
        Assert.Equal(GuideRequestStatus.Open, GuideRequestService.GroupStatus([GuideRequestStatus.Declined, GuideRequestStatus.Open], false));
        Assert.Equal(GuideRequestStatus.Published, GuideRequestService.GroupStatus([GuideRequestStatus.Held], true));
    }
}
