using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Options;
using PreseMakerRepo.Api.Models.Responses;
using PreseMakerRepo.Api.Options;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;
using PreseMakerRepo.Infrastructure.Options;

namespace PreseMakerRepo.Api.Services;

/// <summary>
/// "Request a Career Path" — the career-path twin of <see cref="GuideRequestService"/> (Ron,
/// 2026-09-23: "the request driven will follow the same pattern as courses"). A reader on a CIP
/// area page presses Request beside an occupation the crosswalk lists there and no path covers yet.
/// Rate-limits per hashed IP, refuses occupations a published path already covers, deduplicates
/// the same requester asking for the same occupation within a day, and produces the public queue
/// and the admin ranking. Requests are anonymous.
/// <para>
/// ⚠ An occupation is COVERED when a published path names it as its <c>SocCode</c> or in its
/// <c>AdditionalSocCodes</c> — the second matters, because paths lump related occupations into
/// sections of one page.
/// </para>
/// </summary>
public class CareerRequestService
{
    public enum CreateOutcome { Created, AlreadyRequested, PathExists, NotListed, RateLimited, NetworkRateLimited }

    public const string QueueWaiting = "waiting";
    public const string QueuePublished = "published";
    public const string QueueDeclined = "declined";
    public const string QueueAll = "all";

    /// <param name="PerBrowser">True when the requester was identified by browser (the web button),
    /// false when only by network (the API) -- it decides how a repeat is worded.</param>
    public sealed record CreateResult(CreateOutcome Outcome, string SocCode, string SocTitle,
                                      int RequestCount, string? PathSlug, bool PerBrowser = true);

    private static readonly Regex SocPattern = new(@"^\d{2}-\d{4}$", RegexOptions.Compiled);
    private static readonly Regex CipGroupPattern = new(@"^\d{2}\.\d{2}$", RegexOptions.Compiled);

    private readonly AppDbContext _db;
    private readonly IMemoryCache _cache;
    private readonly RepositoryOptions _repo;
    private readonly string _ipSalt;

    public CareerRequestService(AppDbContext db, IMemoryCache cache,
        IOptions<RepositoryOptions> repo, IOptions<SecurityOptions> security)
    {
        _db = db;
        _cache = cache;
        _repo = repo.Value;
        _ipSalt = security.Value.ReporterIpSalt;
    }

    public static bool TryNormalizeSoc(string? raw, out string soc)
    {
        soc = (raw ?? string.Empty).Trim();
        return SocPattern.IsMatch(soc);
    }

    public static bool TryNormalizeCipGroup(string? raw, out string cip)
    {
        cip = (raw ?? string.Empty).Trim();
        return CipGroupPattern.IsMatch(cip);
    }

    /// <summary>SOC code → slug of the published path that covers it.</summary>
    public async Task<Dictionary<string, string>> CoveredSocsAsync()
    {
        var paths = await _db.CareerPaths.AsNoTracking()
            .Where(p => p.IsPublished)
            .OrderBy(p => p.SortOrder)
            .Select(p => new { p.Slug, p.SocCode, p.AdditionalSocCodes })
            .ToListAsync();

        var covered = new Dictionary<string, string>(StringComparer.Ordinal);
        foreach (var p in paths)
        {
            if (!string.IsNullOrWhiteSpace(p.SocCode)) covered.TryAdd(p.SocCode.Trim(), p.Slug);
            foreach (var s in SplitSocs(p.AdditionalSocCodes)) covered.TryAdd(s, p.Slug);
        }
        return covered;
    }

    /// <summary>"51-9161, 51-9061" → ["51-9161", "51-9061"]; malformed entries are dropped.</summary>
    public static IEnumerable<string> SplitSocs(string? csv) =>
        (csv ?? string.Empty).Split(',', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)
            .Where(s => SocPattern.IsMatch(s));

    /// <summary>
    /// The occupations listed under some CIP groups, with their coverage and waiting demand —
    /// what the area page renders. Hidden rows are left out unless <paramref name="includeHidden"/>.
    /// </summary>
    public async Task<List<CipOccupationResponse>> OccupationsAsync(IReadOnlyCollection<string> cipCodes,
        bool includeHidden = false)
    {
        var q = _db.CipOccupations.AsNoTracking().Where(o => cipCodes.Contains(o.CipCode));
        if (!includeHidden) q = q.Where(o => !o.IsHidden);
        var rows = await q.OrderBy(o => o.SocTitle).ToListAsync();
        if (rows.Count == 0) return [];

        var covered = await CoveredSocsAsync();
        var socs = rows.Select(r => r.SocCode).Distinct().ToList();
        var waiting = await _db.CareerRequests.AsNoTracking()
            .Where(r => socs.Contains(r.SocCode) &&
                        (r.Status == CareerRequestStatus.Open || r.Status == CareerRequestStatus.Queued))
            .GroupBy(r => r.SocCode)
            .Select(g => new { g.Key, N = g.Count() })
            .ToDictionaryAsync(x => x.Key, x => x.N);

        return rows.Select(r => new CipOccupationResponse(r.CipCode, r.SocCode, r.SocTitle, r.IsHidden,
                covered.GetValueOrDefault(r.SocCode), waiting.GetValueOrDefault(r.SocCode)))
            .ToList();
    }

    public sealed record CareerSearchHit(string SocCode, string SocTitle, string? PathSlug,
        IReadOnlyList<(string Code, string Title)> Fields);

    /// <summary>
    /// "Find a career" on /careers: occupations whose SOC title contains the words typed, each with the
    /// fields of study it is listed under (so a reader can go straight to the Request button) or the path
    /// that already covers it. Hidden pairings are left out.
    /// </summary>
    public async Task<List<CareerSearchHit>> SearchAsync(string q, int max = 40)
    {
        var words = q.Split(' ', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)
                     .Where(w => w.Length >= 2).Take(6).ToList();
        if (words.Count == 0) return [];

        var query = _db.CipOccupations.AsNoTracking().Where(o => !o.IsHidden);
        foreach (var w in words)
        {
            var like = "%" + w.Replace("%", "").Replace("_", "") + "%";
            query = query.Where(o => EF.Functions.Like(o.SocTitle, like));
        }
        var rows = await query.Select(o => new { o.SocCode, o.SocTitle, o.CipCode, CipTitle = o.Cip!.Title })
                              .ToListAsync();
        var covered = await CoveredSocsAsync();

        return rows.GroupBy(r => r.SocCode)
            .Select(g => new CareerSearchHit(g.Key, g.First().SocTitle, covered.GetValueOrDefault(g.Key),
                g.OrderBy(r => r.CipCode).Select(r => (r.CipCode, r.CipTitle)).ToList()))
            .OrderBy(h => h.SocTitle)
            .Take(max)
            .ToList();
    }

    /// <param name="browserId">The anonymous per-browser id from the <c>cr_vid</c> cookie, or null (API).
    /// ⚠ Repeats are counted once per BROWSER per day (Ron, 2026-09-23); without one, per network.</param>
    public async Task<CreateResult> CreateAsync(string socRaw, string cipRaw, string? reason, string ip,
        string? userId, CareerRequestChannel channel, string? browserId = null)
    {
        TryNormalizeSoc(socRaw, out var soc);
        TryNormalizeCipGroup(cipRaw, out var cip);

        var occ = await _db.CipOccupations.AsNoTracking()
            .FirstOrDefaultAsync(o => o.CipCode == cip && o.SocCode == soc && !o.IsHidden);
        if (occ is null)
            return new CreateResult(CreateOutcome.NotListed, soc, string.Empty, 0, null);

        var covered = await CoveredSocsAsync();
        if (covered.TryGetValue(soc, out var slug))
            return new CreateResult(CreateOutcome.PathExists, soc, occ.SocTitle, 0, slug);

        var ipHash = HashIp(ip);
        var browserHash = string.IsNullOrWhiteSpace(browserId) ? null : HashIp("browser:" + browserId.Trim());
        var perBrowser = browserHash is not null;
        var since = DateTime.UtcNow.AddDays(-1);
        bool duplicate = await _db.CareerRequests.AsNoTracking().AnyAsync(r =>
            r.SocCode == soc && r.RequestedUtc >= since &&
            ((perBrowser ? r.RequesterBrowserHash == browserHash
                         : r.RequesterBrowserHash == null && r.RequesterIpHash == ipHash)
             || (userId != null && r.RequesterUserId == userId)));
        if (duplicate)
            return new CreateResult(CreateOutcome.AlreadyRequested, soc, occ.SocTitle, await CountAsync(soc), null, perBrowser);

        // Two limits: one per browser, and a higher one per network so a whole classroom fits but
        // clearing cookies cannot inflate a career without bound.
        if (!CheckRateLimit("net:" + ipHash, _repo.CareerRequestNetworkRateLimitPerHour))
            return new CreateResult(CreateOutcome.NetworkRateLimited, soc, occ.SocTitle, 0, null, perBrowser);
        if (!CheckRateLimit((perBrowser ? "br:" + browserHash : "ip:" + ipHash), _repo.CareerRequestRateLimitPerHour))
            return new CreateResult(CreateOutcome.RateLimited, soc, occ.SocTitle, 0, null, perBrowser);

        _db.CareerRequests.Add(new CareerRequest
        {
            Id = Guid.NewGuid(),
            SocCode = soc,
            SocTitle = occ.SocTitle,
            CipCode = cip,
            Reason = string.IsNullOrWhiteSpace(reason) ? null : reason.Trim(),
            RequesterIpHash = ipHash,
            RequesterBrowserHash = browserHash,
            RequesterUserId = userId,
            RequestedUtc = DateTime.UtcNow,
            Status = CareerRequestStatus.Open,
            Channel = channel
        });
        await _db.SaveChangesAsync();

        return new CreateResult(CreateOutcome.Created, soc, occ.SocTitle, await CountAsync(soc), null, perBrowser);
    }

    /// <summary>The sentence the page or API shows for an outcome.</summary>
    public static string MessageFor(CreateResult r) => r.Outcome switch
    {
        CreateOutcome.PathExists => $"A career path already covers {r.SocTitle}.",
        CreateOutcome.NotListed => "That occupation is not listed here, so it cannot be requested from this page.",
        CreateOutcome.RateLimited =>
            "You have made a lot of requests in the last hour, so this one was not recorded. Please try again later.",
        CreateOutcome.NetworkRateLimited =>
            "Too many requests have come from this network in the last hour, so this one was not recorded. " +
            "On a school or library network other people may be requesting too. Please try again later.",
        // Counted per BROWSER on the web page, so "you" is true there; the API counts per network.
        CreateOutcome.AlreadyRequested => r.PerBrowser
            ? $"You already requested {r.SocTitle} today, so it was counted once. {Waiting(r.RequestCount)}"
            : $"A request for {r.SocTitle} from this network was already counted today, so this one was not added again. {Waiting(r.RequestCount)}",
        _ => $"Thank you. Your request for a career path for {r.SocTitle} has been recorded. {Waiting(r.RequestCount)}"
    };

    private static string Waiting(int n) => n <= 1
        ? "Paths are written in order of demand."
        : $"{n} requests are now waiting for it. Paths are written in order of demand.";

    /// <summary>Requests still waiting (Open or Queued) -- the same rule as the count on the area page,
    /// so the confirmation and the page never disagree.</summary>
    private Task<int> CountAsync(string soc) =>
        _db.CareerRequests.AsNoTracking().CountAsync(r => r.SocCode == soc &&
            (r.Status == CareerRequestStatus.Open || r.Status == CareerRequestStatus.Queued));

    /// <summary>waiting (default; "open" is accepted) · published · declined · all.</summary>
    public static bool TryParseQueueFilter(string? raw, out string filter)
    {
        filter = string.IsNullOrWhiteSpace(raw) ? QueueWaiting : raw.Trim().ToLowerInvariant();
        if (filter == "open") filter = QueueWaiting;
        return filter is QueueWaiting or QueuePublished or QueueDeclined or QueueAll;
    }

    /// <summary>
    /// The public career request queue: one row per requested occupation, most requested first
    /// (ties to the earliest request). An occupation a published path covers counts as Published
    /// whatever its rows say; one counts as Declined only when every request was declined.
    /// </summary>
    public async Task<PublicCareerQueueResponse> PublicQueueAsync(string filter)
    {
        var rows = await _db.CareerRequests.AsNoTracking()
            .Select(r => new { r.SocCode, r.SocTitle, r.CipCode, r.Status, r.RequestedUtc, r.PublicNote })
            .ToListAsync();
        var covered = await CoveredSocsAsync();

        var all = rows.GroupBy(r => r.SocCode).Select(g =>
            {
                var slug = covered.GetValueOrDefault(g.Key);
                var status = Rollup(g.Select(r => r.Status), slug is not null);
                var counted = g.Where(r => r.Status != CareerRequestStatus.Declined).ToList();
                var dated = counted.Count > 0 ? counted : g.ToList();
                return new PublicCareerQueueItem(0, g.Key, g.OrderByDescending(r => r.RequestedUtc).First().SocTitle,
                    g.Select(r => r.CipCode).Distinct().OrderBy(c => c).ToList(),
                    counted.Count, dated.Min(r => r.RequestedUtc), dated.Max(r => r.RequestedUtc),
                    status.ToString(), slug,
                    g.OrderByDescending(r => r.RequestedUtc).Select(r => r.PublicNote)
                     .FirstOrDefault(n => !string.IsNullOrWhiteSpace(n)));
            })
            .ToList();

        static bool IsWaiting(PublicCareerQueueItem i) =>
            i.Status is nameof(CareerRequestStatus.Open) or nameof(CareerRequestStatus.Queued);

        var selected = all.Where(i => filter switch
            {
                QueueWaiting => IsWaiting(i),
                QueuePublished => i.Status == nameof(CareerRequestStatus.Published),
                QueueDeclined => i.Status == nameof(CareerRequestStatus.Declined),
                _ => true
            })
            .OrderByDescending(i => i.RequestCount).ThenBy(i => i.FirstRequestedUtc).ThenBy(i => i.SocCode)
            .Select((i, index) => i with { Rank = index + 1 })
            .ToList();

        return new PublicCareerQueueResponse(filter,
            all.Count(IsWaiting),
            all.Count(i => i.Status == nameof(CareerRequestStatus.Published)),
            all.Count(i => i.Status == nameof(CareerRequestStatus.Declined)),
            selected);
    }

    /// <summary>Per-occupation ranking for the admin page and the Tools session. <paramref name="status"/> null = all.</summary>
    public async Task<List<CareerRequestSummaryResponse>> SummaryAsync(CareerRequestStatus? status)
    {
        var q = _db.CareerRequests.AsNoTracking();
        if (status.HasValue) q = q.Where(r => r.Status == status.Value);
        var rows = await q.ToListAsync();
        var covered = await CoveredSocsAsync();

        return rows.GroupBy(r => r.SocCode)
            .Select(g =>
            {
                var slug = covered.GetValueOrDefault(g.Key);
                return new CareerRequestSummaryResponse(
                    g.Key,
                    g.OrderByDescending(r => r.RequestedUtc).First().SocTitle,
                    g.Select(r => r.CipCode).Distinct().OrderBy(c => c).ToList(),
                    g.Count(r => r.Status != CareerRequestStatus.Declined),
                    g.Min(r => r.RequestedUtc),
                    g.Max(r => r.RequestedUtc),
                    Rollup(g.Select(r => r.Status), false).ToString(),
                    slug,
                    g.Select(r => r.Reason).Where(s => !string.IsNullOrWhiteSpace(s)).Select(s => s!).Distinct().ToList(),
                    g.Select(r => r.AdminNotes).LastOrDefault(n => !string.IsNullOrWhiteSpace(n)),
                    g.Select(r => r.PublicNote).LastOrDefault(n => !string.IsNullOrWhiteSpace(n)));
            })
            .OrderByDescending(s => s.RequestCount).ThenBy(s => s.FirstRequestedUtc)
            .ToList();
    }

    /// <summary>Set the status of every request for an occupation. Returns the number updated.</summary>
    /// <param name="publicNote">Shown to visitors on the public queue (e.g. why it was declined).
    /// A value sets it and "" clears it. Null keeps an existing one ONLY while the status stays Declined:
    /// moving to any other status clears it, so a re-opened request never shows an old decline reason
    /// (UX review 2026-09-23).</param>
    public async Task<int> SetStatusAsync(string soc, CareerRequestStatus status, string? notes,
        string? publicNote = null)
    {
        var rows = await _db.CareerRequests.Where(r => r.SocCode == soc).ToListAsync();
        foreach (var r in rows)
        {
            r.Status = status;
            r.StatusUtc = DateTime.UtcNow;
            if (!string.IsNullOrWhiteSpace(notes)) r.AdminNotes = notes.Trim();
            if (publicNote is not null) r.PublicNote = string.IsNullOrWhiteSpace(publicNote) ? null : publicNote.Trim();
            else if (status != CareerRequestStatus.Declined) r.PublicNote = null;
        }
        await _db.SaveChangesAsync();
        return rows.Count;
    }

    /// <summary>Open or queued requests for an occupation a published path now covers are marked
    /// Published, so the queue shows only real gaps. Called after a path push and on the admin page.</summary>
    public async Task<int> ClosePublishedAsync()
    {
        var covered = await CoveredSocsAsync();
        if (covered.Count == 0) return 0;
        var socs = covered.Keys.ToList();
        var rows = await _db.CareerRequests
            .Where(r => socs.Contains(r.SocCode) &&
                        (r.Status == CareerRequestStatus.Open || r.Status == CareerRequestStatus.Queued))
            .ToListAsync();
        foreach (var r in rows) { r.Status = CareerRequestStatus.Published; r.StatusUtc = DateTime.UtcNow; }
        if (rows.Count > 0) await _db.SaveChangesAsync();
        return rows.Count;
    }

    /// <summary>Hide or show one crosswalk pairing. False when the pairing does not exist.</summary>
    public async Task<bool> SetHiddenAsync(string cip, string soc, bool hidden)
    {
        var o = await _db.CipOccupations.FirstOrDefaultAsync(x => x.CipCode == cip && x.SocCode == soc);
        if (o is null) return false;
        o.IsHidden = hidden;
        o.UpdatedUtc = DateTime.UtcNow;
        await _db.SaveChangesAsync();
        return true;
    }

    // ── helpers ──────────────────────────────────────────────────────────────

    /// <summary>The group's status: Published if a path covers it or any row says so; Declined only if
    /// every row was declined; then Queued; else Open.</summary>
    private static CareerRequestStatus Rollup(IEnumerable<CareerRequestStatus> statuses, bool covered)
    {
        var list = statuses.ToList();
        return covered || list.Contains(CareerRequestStatus.Published) ? CareerRequestStatus.Published
             : list.All(s => s == CareerRequestStatus.Declined) ? CareerRequestStatus.Declined
             : list.Contains(CareerRequestStatus.Queued) ? CareerRequestStatus.Queued
             : CareerRequestStatus.Open;
    }

    private bool CheckRateLimit(string id, int limit)
    {
        var key = $"career_request_rate:{id}";
        var count = _cache.GetOrCreate(key, e =>
        {
            e.AbsoluteExpirationRelativeToNow = TimeSpan.FromHours(1);
            return 0;
        });
        if (count >= limit) return false;
        _cache.Set(key, count + 1, TimeSpan.FromHours(1));
        return true;
    }

    private string HashIp(string ip)
    {
        var bytes = SHA256.HashData(Encoding.UTF8.GetBytes(_ipSalt + ":" + ip));
        return Convert.ToHexString(bytes).ToLowerInvariant();
    }
}
