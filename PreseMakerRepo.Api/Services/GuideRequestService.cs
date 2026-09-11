using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Options;
using PreseMakerRepo.Api.Models.Requests;
using PreseMakerRepo.Api.Models.Responses;
using PreseMakerRepo.Api.Options;
using PreseMakerRepo.Core.Constants;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;
using PreseMakerRepo.Infrastructure.Options;

namespace PreseMakerRepo.Api.Services;

/// <summary>
/// "Request a Curriculum Guide": shared by the REST endpoint and the web form.
/// Rate-limits per hashed IP (like content reports), refuses requests for courses that
/// already have a guide, deduplicates the same requester asking for the same course within
/// a day, and produces the per-course ranking the admin console and the queue tool use.
/// </summary>
public class GuideRequestService
{
    public enum CreateOutcome { Created, AlreadyRequested, GuideExists, RateLimited }

    public sealed record CreateResult(CreateOutcome Outcome, string CourseId, int RequestCount, bool InTaxonomy, string? TaxonomyTitle);

    private static readonly Regex CourseIdPattern = new(@"^[A-Z]{3}\d{4}[A-Z]?$", RegexOptions.Compiled);

    private readonly AppDbContext _db;
    private readonly IMemoryCache _cache;
    private readonly RepositoryOptions _repo;
    private readonly string _ipSalt;

    public GuideRequestService(AppDbContext db, IMemoryCache cache,
        IOptions<RepositoryOptions> repo, IOptions<SecurityOptions> security)
    {
        _db = db;
        _cache = cache;
        _repo = repo.Value;
        _ipSalt = security.Value.ReporterIpSalt;
    }

    /// <summary>"eet 2325c" → "EET2325C". False when the shape is not an SCNS code.</summary>
    public static bool TryNormalizeCourseId(string? raw, out string normalized)
    {
        normalized = new string((raw ?? string.Empty).Where(c => !char.IsWhiteSpace(c) && c != '-').ToArray()).ToUpperInvariant();
        return CourseIdPattern.IsMatch(normalized);
    }

    /// <summary>What the request page shows before submitting: taxonomy title, guide state, demand so far.</summary>
    public async Task<(bool InTaxonomy, string? Title, bool HasGuide, int OpenRequests)> LookupAsync(string courseId)
    {
        var course = await _db.TaxonomyCourses.AsNoTracking()
            .Where(c => c.CourseId == courseId && c.CourseId != WellKnownIds.OrphanCourseId)
            .Select(c => new { c.Title })
            .FirstOrDefaultAsync();
        var hasGuide = await _db.CurriculumGuides.AsNoTracking()
            .AnyAsync(g => g.CourseId == courseId && g.Title != CurriculumGuide.StubTitle);
        var open = await _db.GuideRequests.AsNoTracking()
            .CountAsync(r => r.CourseId == courseId && r.Status != GuideRequestStatus.Declined);
        return (course != null, course?.Title, hasGuide, open);
    }

    public async Task<CreateResult> CreateAsync(CreateGuideRequestRequest request, string ip, string? userId)
    {
        TryNormalizeCourseId(request.CourseId, out var courseId);
        var (inTaxonomy, title, hasGuide, _) = await LookupAsync(courseId);
        if (hasGuide)
            return new CreateResult(CreateOutcome.GuideExists, courseId, 0, inTaxonomy, title);

        var ipHash = HashIp(ip);
        // The same person asking again the same day counts once.
        var since = DateTime.UtcNow.AddDays(-1);
        bool duplicate = await _db.GuideRequests.AsNoTracking().AnyAsync(r =>
            r.CourseId == courseId && r.RequestedUtc >= since &&
            (r.RequesterIpHash == ipHash || (userId != null && r.RequesterUserId == userId)));
        if (duplicate)
        {
            var existing = await CountAsync(courseId);
            return new CreateResult(CreateOutcome.AlreadyRequested, courseId, existing, inTaxonomy, title);
        }

        if (!CheckRateLimit(ipHash))
            return new CreateResult(CreateOutcome.RateLimited, courseId, 0, inTaxonomy, title);

        _db.GuideRequests.Add(new GuideRequest
        {
            Id              = Guid.NewGuid(),
            CourseId        = courseId,
            CourseTitle     = (inTaxonomy && !string.IsNullOrWhiteSpace(title) ? title : request.CourseTitle).Trim(),
            Institution     = request.Institution.Trim(),
            Reason          = Clean(request.Reason),
            RequesterEmail  = Clean(request.Email)?.ToLowerInvariant(),
            RequesterIpHash = ipHash,
            RequesterUserId = userId,
            IsInTaxonomy    = inTaxonomy,
            RequestedUtc    = DateTime.UtcNow,
            Status          = GuideRequestStatus.Open
        });
        await _db.SaveChangesAsync();

        var count = await CountAsync(courseId);
        return new CreateResult(CreateOutcome.Created, courseId, count, inTaxonomy, title);
    }

    private Task<int> CountAsync(string courseId) =>
        _db.GuideRequests.AsNoTracking().CountAsync(r => r.CourseId == courseId && r.Status != GuideRequestStatus.Declined);

    /// <summary>Per-course ranking (most requested first). <paramref name="status"/> null = every status.</summary>
    public async Task<List<GuideRequestSummaryResponse>> SummaryAsync(GuideRequestStatus? status, int minCount = 1)
    {
        var query = _db.GuideRequests.AsNoTracking();
        if (status.HasValue) query = query.Where(r => r.Status == status.Value);

        var rows = await query.ToListAsync();
        var courseIds = rows.Select(r => r.CourseId).Distinct().ToList();
        var withGuide = await _db.CurriculumGuides.AsNoTracking()
            .Where(g => courseIds.Contains(g.CourseId) && g.Title != CurriculumGuide.StubTitle)
            .Select(g => g.CourseId).ToListAsync();
        var guideSet = withGuide.ToHashSet(StringComparer.OrdinalIgnoreCase);

        return rows.GroupBy(r => r.CourseId)
            .Select(g =>
            {
                var latest = g.OrderByDescending(r => r.RequestedUtc).First();
                // The group's status is the most advanced one recorded (Published > Queued > Open);
                // Declined only when every request was declined.
                var st = g.All(r => r.Status == GuideRequestStatus.Declined) ? GuideRequestStatus.Declined
                       : g.Any(r => r.Status == GuideRequestStatus.Published) ? GuideRequestStatus.Published
                       : g.Any(r => r.Status == GuideRequestStatus.Queued) ? GuideRequestStatus.Queued
                       : GuideRequestStatus.Open;
                return new GuideRequestSummaryResponse(
                    g.Key,
                    latest.CourseTitle,
                    g.Select(r => r.Institution).Where(i => i.Length > 0).Distinct(StringComparer.OrdinalIgnoreCase).OrderBy(i => i).ToList(),
                    g.Count(r => r.Status != GuideRequestStatus.Declined),
                    g.Min(r => r.RequestedUtc),
                    g.Max(r => r.RequestedUtc),
                    st.ToString(),
                    g.Any(r => r.IsInTaxonomy),
                    guideSet.Contains(g.Key),
                    g.Select(r => r.AdminNotes).LastOrDefault(n => !string.IsNullOrWhiteSpace(n)));
            })
            .Where(s => s.RequestCount >= minCount || status == GuideRequestStatus.Declined)
            .OrderByDescending(s => s.RequestCount).ThenBy(s => s.FirstRequestedUtc)
            .ToList();
    }

    /// <summary>Set the status of every request for a course. Returns the number updated.</summary>
    public async Task<int> SetStatusAsync(string courseId, GuideRequestStatus status, string? notes)
    {
        var rows = await _db.GuideRequests.Where(r => r.CourseId == courseId).ToListAsync();
        foreach (var r in rows)
        {
            r.Status = status;
            r.StatusUtc = DateTime.UtcNow;
            if (!string.IsNullOrWhiteSpace(notes)) r.AdminNotes = notes.Trim();
        }
        await _db.SaveChangesAsync();
        return rows.Count;
    }

    /// <summary>Requests whose guide has since been published but are still Open/Queued —
    /// closed automatically so the ranking only shows real gaps.</summary>
    public async Task<int> ClosePublishedAsync()
    {
        var published = await _db.GuideRequests
            .Where(r => (r.Status == GuideRequestStatus.Open || r.Status == GuideRequestStatus.Queued) &&
                        _db.CurriculumGuides.Any(g => g.CourseId == r.CourseId && g.Title != CurriculumGuide.StubTitle))
            .ToListAsync();
        foreach (var r in published) { r.Status = GuideRequestStatus.Published; r.StatusUtc = DateTime.UtcNow; }
        if (published.Count > 0) await _db.SaveChangesAsync();
        return published.Count;
    }

    /// <summary>Emails of requesters who asked to be told, for a course (distinct).</summary>
    public Task<List<string>> NotificationEmailsAsync(string courseId) =>
        _db.GuideRequests.AsNoTracking()
            .Where(r => r.CourseId == courseId && r.RequesterEmail != null)
            .Select(r => r.RequesterEmail!).Distinct().ToListAsync();

    // ── helpers ──────────────────────────────────────────────────────────────

    private bool CheckRateLimit(string ipHash)
    {
        var key = $"guide_request_rate:{ipHash}";
        var count = _cache.GetOrCreate(key, entry =>
        {
            entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromHours(1);
            return 0;
        });
        if (count >= _repo.GuideRequestRateLimitPerHour) return false;
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
