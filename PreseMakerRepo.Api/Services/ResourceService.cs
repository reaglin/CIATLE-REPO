using System.Security.Cryptography;
using System.Text;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Options;
using PreseMakerRepo.Api.Helpers;
using PreseMakerRepo.Api.Models.Requests;
using PreseMakerRepo.Api.Models.Responses;
using PreseMakerRepo.Api.Options;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;
using PreseMakerRepo.Infrastructure.Options;

namespace PreseMakerRepo.Api.Services;

/// <summary>
/// Course resources (COURSE_CATALOG_PLAN.md phase 3; reviewer contract Tools/RESOURCE_API.md).
/// <list type="bullet">
/// <item>Visitors — or vendors suggesting a product — submit a website or YouTube link on a course's Resources
///       page: anonymous, rate-limited, deduplicated. Suggestions wait in the public review queue.</item>
/// <item>The reviewer (an AI session working to Ron's approval rules, over the admin API) approves a suggestion
///       with a title and summary for the course it was suggested for, and may list it for other courses it
///       suits — or rejects it with a short public reason. It can also list links it found itself.</item>
/// <item>Every listing belongs to one course. The same link can be listed for many courses, each with its own
///       title, summary and status; editing or removing one leaves the others alone.</item>
/// </list>
/// The server never fetches a submitted URL.
/// </summary>
public class ResourceService
{
    public const string QueuePending = "pending";
    public const string QueueDecided = "decided";
    public const string QueueAll = "all";
    public const int MaxCoursesPerCall = 100;
    public static readonly TimeSpan DecidedWindow = TimeSpan.FromDays(30);

    public static class WriteOutcomes
    {
        public const string Created = "created";
        public const string Updated = "updated";
        public const string UnknownCourse = "unknownCourse";
    }

    public enum SubmitOutcome { Submitted, AlreadySubmitted, AlreadyListed, RecentlyRejected, InvalidUrl, CourseNotFound, RateLimited }
    public sealed record SubmitResult(SubmitOutcome Outcome, Guid? SubmissionId, string Message);

    public enum ChangeOutcome { Done, NotFound, NotPending, InvalidUrl, NoListedCourses }
    public sealed record Result<T>(ChangeOutcome Outcome, T? Value, string Message);

    private readonly AppDbContext _db;
    private readonly IMemoryCache _cache;
    private readonly RepositoryOptions _repo;
    private readonly string _ipSalt;

    public ResourceService(AppDbContext db, IMemoryCache cache,
        IOptions<RepositoryOptions> repo, IOptions<SecurityOptions> security)
    {
        _db = db;
        _cache = cache;
        _repo = repo.Value;
        _ipSalt = security.Value.ReporterIpSalt;
    }

    public static string NormalizeCourseId(string? raw) =>
        new string((raw ?? string.Empty).Where(ch => !char.IsWhiteSpace(ch)).ToArray()).ToUpperInvariant();

    /// <summary>pending (default) · decided (last 30 days) · all.</summary>
    public static bool TryParseQueueFilter(string? raw, out string filter)
    {
        filter = string.IsNullOrWhiteSpace(raw) ? QueuePending : raw.Trim().ToLowerInvariant();
        return filter is QueuePending or QueueDecided or QueueAll;
    }

    public Task<bool> CourseIsListedAsync(string courseId)
    {
        var id = NormalizeCourseId(courseId);
        return _db.TaxonomyCourses.AnyAsync(c => c.CourseId == id && c.Level3Key != null);
    }

    // ── visitors ─────────────────────────────────────────────────────────────

    public async Task<SubmitResult> SubmitAsync(string courseId, SubmitResourceRequest request, string ip, string? userId)
    {
        var id = NormalizeCourseId(courseId);
        if (!await CourseIsListedAsync(id))
            return new SubmitResult(SubmitOutcome.CourseNotFound, null, $"{id} is not a listed course.");
        if (!ResourceUrls.TryParse(request.Url, out var parsed, out var error))
            return new SubmitResult(SubmitOutcome.InvalidUrl, null, error);

        if (await _db.CourseResources.AnyAsync(r => r.CourseId == id && r.Url == parsed.Url && r.Status == ResourceStatus.Active))
            return new SubmitResult(SubmitOutcome.AlreadyListed, null, $"That link is already listed for {id}.");
        if (await _db.ResourceSubmissions.AnyAsync(s => s.CourseId == id && s.Url == parsed.Url &&
                                                        s.Status == ResourceSubmissionStatus.Pending))
            return new SubmitResult(SubmitOutcome.AlreadySubmitted, null,
                "That link has already been suggested for this course and is waiting for review. Thank you.");
        var since = DateTime.UtcNow - DecidedWindow;
        if (await _db.ResourceSubmissions.AnyAsync(s => s.CourseId == id && s.Url == parsed.Url &&
                                                        s.Status == ResourceSubmissionStatus.Rejected && s.DecidedUtc >= since))
            return new SubmitResult(SubmitOutcome.RecentlyRejected, null,
                "That link was reviewed for this course recently and was not added.");

        var ipHash = HashIp(ip);
        if (!CheckRateLimit(ipHash))
            return new SubmitResult(SubmitOutcome.RateLimited, null,
                "Too many suggestions from your connection this hour. Please try again later.");

        var submission = new ResourceSubmission
        {
            Id = Guid.NewGuid(),
            CourseId = id,
            Url = parsed.Url,
            Type = parsed.Type,
            YouTubeVideoId = parsed.YouTubeVideoId,
            Description = Clean(request.Description),
            Status = ResourceSubmissionStatus.Pending,
            SubmittedUtc = DateTime.UtcNow,
            SubmitterIpHash = ipHash,
            SubmitterUserId = userId
        };
        _db.ResourceSubmissions.Add(submission);
        await _db.SaveChangesAsync();
        return new SubmitResult(SubmitOutcome.Submitted, submission.Id,
            "Thank you — your suggestion is in the review queue. Reviewed links are listed here with a short summary; the site is updated weekly.");
    }

    /// <summary>A course's active listings, newest first, each with the other courses listing the same link.</summary>
    public async Task<IReadOnlyList<CourseResourceDto>> ForCourseAsync(string courseId)
    {
        var id = NormalizeCourseId(courseId);
        var rows = await _db.CourseResources.AsNoTracking()
            .Where(r => r.CourseId == id && r.Status == ResourceStatus.Active)
            .OrderByDescending(r => r.CreatedUtc)
            .ToListAsync();
        var elsewhere = await ElsewhereAsync(rows.Select(r => r.Url).Distinct().ToList());
        return rows.Select(r => ToDto(r, elsewhere)).ToList();
    }

    public Task<int> PendingCountAsync(string courseId)
    {
        var id = NormalizeCourseId(courseId);
        return _db.ResourceSubmissions.CountAsync(s => s.CourseId == id && s.Status == ResourceSubmissionStatus.Pending);
    }

    /// <summary>The public review queue. Pending oldest first (the order to review in); decided newest first.</summary>
    public async Task<ResourceQueueResponse> QueueAsync(string filter)
    {
        var since = DateTime.UtcNow - DecidedWindow;
        var pending = await _db.ResourceSubmissions.CountAsync(s => s.Status == ResourceSubmissionStatus.Pending);
        var decided = await _db.ResourceSubmissions.CountAsync(s => s.Status != ResourceSubmissionStatus.Pending && s.DecidedUtc >= since);

        IQueryable<ResourceSubmission> query = _db.ResourceSubmissions.AsNoTracking();
        query = filter switch
        {
            QueuePending => query.Where(s => s.Status == ResourceSubmissionStatus.Pending).OrderBy(s => s.SubmittedUtc),
            QueueDecided => query.Where(s => s.Status != ResourceSubmissionStatus.Pending && s.DecidedUtc >= since)
                                 .OrderByDescending(s => s.DecidedUtc),
            _ => query.OrderByDescending(s => s.SubmittedUtc)
        };
        var rows = await query.Take(500).ToListAsync();
        var titles = await CourseTitlesAsync(rows.Select(r => r.CourseId).Distinct().ToList());

        var items = rows.Select(s => new ResourceQueueItem(s.Id, s.CourseId, titles.GetValueOrDefault(s.CourseId, s.CourseId),
                s.Url, s.Type.ToString(), ResourceUrls.DisplayHost(s.Url), s.Description, s.Status.ToString(),
                s.SubmittedUtc, s.DecidedUtc, s.DecisionNote, s.CourseResourceId))
            .ToList();
        return new ResourceQueueResponse(filter, pending, decided, items);
    }

    // ── reviewer (admin API) ─────────────────────────────────────────────────

    public async Task<Result<ResourceDecisionResponse>> ApproveAsync(Guid submissionId, ApproveResourceSubmissionRequest request)
    {
        var submission = await _db.ResourceSubmissions.FirstOrDefaultAsync(s => s.Id == submissionId);
        if (submission is null)
            return new(ChangeOutcome.NotFound, null, "Submission not found.");
        if (submission.Status != ResourceSubmissionStatus.Pending)
            return new(ChangeOutcome.NotPending, null, $"The submission is already {submission.Status}.");

        var targets = new List<ResourceCourseInput> { new(submission.CourseId, null, null) };
        targets.AddRange(request.AlsoFor ?? []);
        var now = DateTime.UtcNow;
        var results = await UpsertListingsAsync(submission.Url, submission.Type, submission.YouTubeVideoId,
            request.Title!, request.Summary!, targets, submission.CourseId, submission.Id, now);
        if (results.All(r => r.ResourceId is null))
            return new(ChangeOutcome.NoListedCourses, null, "None of those courses are listed on the site.");

        submission.Status = ResourceSubmissionStatus.Approved;
        submission.DecidedUtc = now;
        submission.CourseResourceId = results.FirstOrDefault(r => r.CourseId == submission.CourseId)?.ResourceId;
        submission.DecisionNote = Clean(request.Note);
        await _db.SaveChangesAsync();

        var listed = results.Count(r => r.ResourceId is not null);
        return new(ChangeOutcome.Done,
            new ResourceDecisionResponse(submission.Id, submission.Status.ToString(), results,
                $"Approved; listed for {listed} course(s)."),
            $"Approved; listed for {listed} course(s).");
    }

    public async Task<Result<ResourceDecisionResponse>> RejectAsync(Guid submissionId, string note)
    {
        var submission = await _db.ResourceSubmissions.FirstOrDefaultAsync(s => s.Id == submissionId);
        if (submission is null)
            return new(ChangeOutcome.NotFound, null, "Submission not found.");
        if (submission.Status != ResourceSubmissionStatus.Pending)
            return new(ChangeOutcome.NotPending, null, $"The submission is already {submission.Status}.");

        submission.Status = ResourceSubmissionStatus.Rejected;
        submission.DecidedUtc = DateTime.UtcNow;
        submission.DecisionNote = Clean(note);
        await _db.SaveChangesAsync();
        return new(ChangeOutcome.Done,
            new ResourceDecisionResponse(submission.Id, submission.Status.ToString(), [], "Rejected."), "Rejected.");
    }

    /// <summary>Puts a decided suggestion back in the queue (admin reversal). Listings it created stay — remove them separately.</summary>
    public async Task<ChangeOutcome> ReopenAsync(Guid submissionId)
    {
        var submission = await _db.ResourceSubmissions.FirstOrDefaultAsync(s => s.Id == submissionId);
        if (submission is null) return ChangeOutcome.NotFound;
        submission.Status = ResourceSubmissionStatus.Pending;
        submission.DecidedUtc = null;
        submission.DecisionNote = null;
        await _db.SaveChangesAsync();
        return ChangeOutcome.Done;
    }

    /// <summary>Lists a link directly for one or more courses — a resource the reviewer found, or more courses
    /// for a link already listed. An existing listing of the link on a course is updated and restored.</summary>
    public async Task<Result<ResourceCreateResponse>> CreateAsync(CreateResourceRequest request)
    {
        if (!ResourceUrls.TryParse(request.Url, out var parsed, out var error))
            return new(ChangeOutcome.InvalidUrl, null, error);

        var now = DateTime.UtcNow;
        var results = await UpsertListingsAsync(parsed.Url, parsed.Type, parsed.YouTubeVideoId,
            request.Title!, request.Summary!, request.Courses ?? [], null, null, now);
        if (results.All(r => r.ResourceId is null))
            return new(ChangeOutcome.NoListedCourses, null, "None of those courses are listed on the site.");

        await _db.SaveChangesAsync();
        return new(ChangeOutcome.Done, new ResourceCreateResponse(parsed.Url, parsed.Type.ToString(), results), "Listed.");
    }

    /// <summary>Edits one course's listing, or removes / restores it. Other courses' listings of the same link are untouched.</summary>
    public async Task<Result<CourseResourceDto>> UpdateAsync(Guid id, UpdateResourceRequest request)
    {
        var listing = await _db.CourseResources.FirstOrDefaultAsync(r => r.Id == id);
        if (listing is null)
            return new(ChangeOutcome.NotFound, null, "Resource not found.");

        if (request.Title is not null) listing.Title = request.Title.Trim();
        if (request.Summary is not null) listing.Summary = request.Summary.Trim();
        if (request.Status is not null)
            listing.Status = request.Status.Equals("removed", StringComparison.OrdinalIgnoreCase)
                ? ResourceStatus.Removed
                : ResourceStatus.Active;
        listing.UpdatedUtc = DateTime.UtcNow;
        await _db.SaveChangesAsync();

        var elsewhere = await ElsewhereAsync([listing.Url]);
        return new(ChangeOutcome.Done, ToDto(listing, elsewhere), "Updated.");
    }

    /// <summary>Deletes one course's listing permanently.</summary>
    public async Task<ChangeOutcome> DeleteAsync(Guid id)
    {
        var listing = await _db.CourseResources.FirstOrDefaultAsync(r => r.Id == id);
        if (listing is null) return ChangeOutcome.NotFound;
        _db.CourseResources.Remove(listing);
        await _db.SaveChangesAsync();
        return ChangeOutcome.Done;
    }

    public async Task<CourseResourceDto?> GetAsync(Guid id, bool includeRemoved)
    {
        var listing = await _db.CourseResources.AsNoTracking()
            .FirstOrDefaultAsync(r => r.Id == id && (includeRemoved || r.Status == ResourceStatus.Active));
        if (listing is null) return null;
        return ToDto(listing, await ElsewhereAsync([listing.Url]));
    }

    /// <summary>Every course listing a link (normalised first) — how the reviewer checks where a link already is.</summary>
    public async Task<Result<IReadOnlyList<CourseResourceDto>>> ForUrlAsync(string? url, bool includeRemoved)
    {
        if (!ResourceUrls.TryParse(url, out var parsed, out var error))
            return new(ChangeOutcome.InvalidUrl, null, error);
        var rows = await _db.CourseResources.AsNoTracking()
            .Where(r => r.Url == parsed.Url && (includeRemoved || r.Status == ResourceStatus.Active))
            .OrderBy(r => r.CourseId)
            .ToListAsync();
        var elsewhere = await ElsewhereAsync([parsed.Url]);
        return new(ChangeOutcome.Done, rows.Select(r => ToDto(r, elsewhere)).ToList(), "OK");
    }

    /// <summary>Admin listing: newest first, optionally filtered by title, link or course id; removed listings included.</summary>
    public async Task<List<CourseResourceDto>> AdminListAsync(string? search, int take = 300)
    {
        IQueryable<CourseResource> query = _db.CourseResources.AsNoTracking();
        if (!string.IsNullOrWhiteSpace(search))
        {
            var term = search.Trim();
            var pattern = $"%{term}%";
            var courseId = NormalizeCourseId(term);
            query = query.Where(r => r.CourseId == courseId || EF.Functions.Like(r.Title, pattern) || EF.Functions.Like(r.Url, pattern));
        }
        var rows = await query.OrderByDescending(r => r.UpdatedUtc).Take(take).ToListAsync();
        var elsewhere = await ElsewhereAsync(rows.Select(r => r.Url).Distinct().ToList());
        return rows.Select(r => ToDto(r, elsewhere)).ToList();
    }

    // ── helpers ──────────────────────────────────────────────────────────────

    private async Task<List<ResourceWriteResult>> UpsertListingsAsync(
        string url, ResourceType type, string? videoId, string defaultTitle, string defaultSummary,
        IEnumerable<ResourceCourseInput> targets, string? submittedCourseId, Guid? submissionId, DateTime now)
    {
        // Last mention of a course wins, so an AlsoFor entry can tailor the suggested course's own listing.
        var wanted = targets
            .Select(t => (Id: NormalizeCourseId(t.CourseId), t.Title, t.Summary))
            .Where(t => t.Id.Length > 0)
            .GroupBy(t => t.Id)
            .Select(g => g.Last())
            .ToList();
        var ids = wanted.Select(w => w.Id).ToList();

        var listed = (await _db.TaxonomyCourses.AsNoTracking()
                .Where(c => ids.Contains(c.CourseId) && c.Level3Key != null)
                .Select(c => c.CourseId)
                .ToListAsync())
            .ToHashSet(StringComparer.Ordinal);
        var existing = await _db.CourseResources
            .Where(r => r.Url == url && ids.Contains(r.CourseId))
            .ToDictionaryAsync(r => r.CourseId, StringComparer.Ordinal);

        var results = new List<ResourceWriteResult>(wanted.Count);
        foreach (var (courseId, title, summary) in wanted)
        {
            if (!listed.Contains(courseId))
            {
                results.Add(new ResourceWriteResult(courseId, WriteOutcomes.UnknownCourse, null));
                continue;
            }
            var listingTitle = string.IsNullOrWhiteSpace(title) ? defaultTitle.Trim() : title.Trim();
            var listingSummary = string.IsNullOrWhiteSpace(summary) ? defaultSummary.Trim() : summary.Trim();

            if (existing.TryGetValue(courseId, out var listing))
            {
                listing.Title = listingTitle;
                listing.Summary = listingSummary;
                listing.Status = ResourceStatus.Active;
                listing.UpdatedUtc = now;
                results.Add(new ResourceWriteResult(courseId, WriteOutcomes.Updated, listing.Id));
            }
            else
            {
                var submitted = courseId == submittedCourseId;
                listing = new CourseResource
                {
                    Id = Guid.NewGuid(),
                    CourseId = courseId,
                    Type = type,
                    Url = url,
                    YouTubeVideoId = videoId,
                    Title = listingTitle,
                    Summary = listingSummary,
                    Status = ResourceStatus.Active,
                    Source = submitted ? ResourceLinkSource.Submitted : ResourceLinkSource.Reviewer,
                    SubmissionId = submitted ? submissionId : null,
                    CreatedUtc = now,
                    UpdatedUtc = now
                };
                _db.CourseResources.Add(listing);
                results.Add(new ResourceWriteResult(courseId, WriteOutcomes.Created, listing.Id));
            }
        }
        return results;
    }

    /// <summary>URL → courses with an active listing of it.</summary>
    private async Task<Dictionary<string, List<string>>> ElsewhereAsync(List<string> urls)
    {
        if (urls.Count == 0) return new Dictionary<string, List<string>>(StringComparer.Ordinal);
        var rows = await _db.CourseResources.AsNoTracking()
            .Where(r => urls.Contains(r.Url) && r.Status == ResourceStatus.Active)
            .Select(r => new { r.Url, r.CourseId })
            .ToListAsync();
        return rows.GroupBy(r => r.Url, StringComparer.Ordinal)
            .ToDictionary(g => g.Key, g => g.Select(r => r.CourseId).OrderBy(c => c).ToList(), StringComparer.Ordinal);
    }

    private static CourseResourceDto ToDto(CourseResource r, Dictionary<string, List<string>> elsewhere) =>
        new(r.Id, r.CourseId, r.Type.ToString(), r.Url, r.YouTubeVideoId, r.Title, r.Summary, ResourceUrls.DisplayHost(r.Url),
            r.Status.ToString(), r.Source.ToString(),
            (elsewhere.GetValueOrDefault(r.Url) ?? []).Where(c => c != r.CourseId).ToList(),
            r.CreatedUtc, r.UpdatedUtc);

    private async Task<Dictionary<string, string>> CourseTitlesAsync(List<string> ids)
    {
        var rows = await _db.TaxonomyCourses.AsNoTracking()
            .Where(c => ids.Contains(c.CourseId))
            .Select(c => new
            {
                c.CourseId,
                c.Title,
                c.StateTitle,
                GuideTitle = _db.CurriculumGuides
                    .Where(g => g.CourseId == c.CourseId && g.Title != CurriculumGuide.StubTitle)
                    .Select(g => g.Title)
                    .FirstOrDefault()
            })
            .ToListAsync();
        return rows.ToDictionary(r => r.CourseId, r => CourseTitles.Display(r.CourseId, r.Title, r.StateTitle, r.GuideTitle),
            StringComparer.OrdinalIgnoreCase);
    }

    private bool CheckRateLimit(string ipHash)
    {
        var key = $"resource_submission_rate:{ipHash}";
        var count = _cache.GetOrCreate(key, entry =>
        {
            entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromHours(1);
            return 0;
        });
        if (count >= _repo.ResourceSubmissionRateLimitPerHour) return false;
        _cache.Set(key, count + 1, TimeSpan.FromHours(1));
        return true;
    }

    private string HashIp(string ip)
    {
        var bytes = SHA256.HashData(Encoding.UTF8.GetBytes(_ipSalt + ":" + ip));
        return Convert.ToHexString(bytes).ToLowerInvariant();
    }

    private static string? Clean(string? s) => string.IsNullOrWhiteSpace(s) ? null : s.Trim();
}
