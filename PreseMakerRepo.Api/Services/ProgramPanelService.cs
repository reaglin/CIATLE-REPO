using System.Text.Json;
using System.Text.RegularExpressions;
using Microsoft.Extensions.Caching.Memory;

namespace PreseMakerRepo.Api.Services;

/// <summary>One program in SoftwarePlus.ai's apps.json.</summary>
public sealed record PanelProgram(string Id, string Name, string Summary, string Icon, string Page, string Store);

/// <summary>
/// The program panel (plan Phase 10; on the landing page since Phase 14, see <see cref="ProgramPanelPageFilter"/>): Dr. Ron Eaglin's Microsoft Store programs, read from
/// <c>https://softwareplus.ai/apps.json</c> (<c>SiteSettings:ProgramsUrl</c>) and kept for three hours.
/// The panel must never slow or break the home page: the list is fetched with a short timeout, and a
/// failure leaves the panel out (and is not retried for ten minutes).
/// </summary>
public sealed class ProgramPanelService
{
    /// <summary>
    /// The session cookie set when the panel is shown (plan 14.1): once per browser session, on the page the visitor
    /// lands on. It holds only "1".
    /// </summary>
    public const string ShownCookie = "fcr_programs_shown";

    /// <summary>The session cookie the home-page-only panel's × set (plan 10.3); still honoured. It holds only "1".</summary>
    public const string ClosedCookie = "fcr_programs_closed";

    public const string DefaultUrl = "https://softwareplus.ai/apps.json";
    public static readonly TimeSpan Keep = TimeSpan.FromHours(3);
    public static readonly TimeSpan KeepAfterFailure = TimeSpan.FromMinutes(10);
    public static readonly TimeSpan Timeout = TimeSpan.FromSeconds(3);

    private const string CacheKey = "program-panel:list";
    private static readonly Regex IdPattern = new("^[a-z0-9-]{1,40}$", RegexOptions.Compiled);

    private readonly IHttpClientFactory _http;
    private readonly IMemoryCache _cache;
    private readonly IConfiguration _config;
    private readonly ILogger<ProgramPanelService> _log;
    private readonly SemaphoreSlim _fetching = new(1, 1);

    public ProgramPanelService(IHttpClientFactory http, IMemoryCache cache, IConfiguration config, ILogger<ProgramPanelService> log)
    {
        _http = http;
        _cache = cache;
        _config = config;
        _log = log;
    }

    /// <summary>The programs, or an empty list if apps.json could not be read. Never throws.</summary>
    public async Task<IReadOnlyList<PanelProgram>> GetProgramsAsync(CancellationToken ct = default)
    {
        if (_cache.TryGetValue(CacheKey, out IReadOnlyList<PanelProgram>? list) && list is not null) return list;
        try
        {
            await _fetching.WaitAsync(ct);
        }
        catch (OperationCanceledException) { return []; }
        try
        {
            if (_cache.TryGetValue(CacheKey, out list) && list is not null) return list;
            list = await FetchAsync(ct);
            _cache.Set(CacheKey, list, list.Count == 0 ? KeepAfterFailure : Keep);
            return list;
        }
        finally
        {
            _fetching.Release();
        }
    }

    /// <summary>One program at random (repeats allowed), or null when there is none to show.</summary>
    public async Task<PanelProgram?> PickAsync(CancellationToken ct = default)
    {
        var list = await GetProgramsAsync(ct);
        return list.Count == 0 ? null : list[Random.Shared.Next(list.Count)];
    }

    /// <summary>True when <paramref name="id"/> is a program in the current list (clicks on anything else are ignored).</summary>
    public async Task<bool> IsKnownAsync(string? id, CancellationToken ct = default)
    {
        if (string.IsNullOrEmpty(id)) return false;
        var list = await GetProgramsAsync(ct);
        return list.Any(p => p.Id == id);
    }

    private async Task<IReadOnlyList<PanelProgram>> FetchAsync(CancellationToken ct)
    {
        var url = _config["SiteSettings:ProgramsUrl"];
        if (string.IsNullOrWhiteSpace(url)) url = DefaultUrl;
        try
        {
            using var timeout = CancellationTokenSource.CreateLinkedTokenSource(ct);
            timeout.CancelAfter(Timeout);
            var client = _http.CreateClient();
            client.DefaultRequestHeaders.UserAgent.ParseAdd("FloridaCourseRepo-ProgramPanel/1.0");
            var json = await client.GetStringAsync(url, timeout.Token);
            var list = Parse(json);
            if (list.Count == 0) _log.LogWarning("Program panel: {Url} has no usable programs", url);
            return list;
        }
        catch (Exception ex)
        {
            _log.LogWarning(ex, "Program panel: could not read {Url}; the panel is left out for now", url);
            return [];
        }
    }

    /// <summary>
    /// Reads apps.json. A program is kept only if every field is present, its id is short and plain, its icon
    /// and page are on https://softwareplus.ai and its Store link on https://apps.microsoft.com, so a mistake
    /// in the file can never put a link to anywhere else on this site.
    /// </summary>
    public static IReadOnlyList<PanelProgram> Parse(string json)
    {
        var result = new List<PanelProgram>();
        try
        {
            using var doc = JsonDocument.Parse(json);
            if (!doc.RootElement.TryGetProperty("programs", out var programs) || programs.ValueKind != JsonValueKind.Array)
                return result;
            foreach (var p in programs.EnumerateArray())
            {
                if (p.ValueKind != JsonValueKind.Object) continue;
                string? S(string name) => p.TryGetProperty(name, out var v) && v.ValueKind == JsonValueKind.String
                    ? v.GetString()?.Trim() : null;
                var id = S("id");
                var name = S("name");
                var summary = S("summary");
                var icon = S("icon");
                var page = S("page");
                var store = S("store");
                if (id is null || !IdPattern.IsMatch(id)) continue;
                if (string.IsNullOrEmpty(name) || name.Length > 60) continue;
                if (string.IsNullOrEmpty(summary) || summary.Length > 300) continue;
                if (!OnHost(icon, "softwareplus.ai") || !OnHost(page, "softwareplus.ai") || !OnHost(store, "apps.microsoft.com")) continue;
                if (result.Any(r => r.Id == id)) continue;
                result.Add(new PanelProgram(id, name, summary, icon!, page!, store!));
            }
        }
        catch (JsonException) { }
        return result;
    }

    private static bool OnHost(string? url, string host) =>
        Uri.TryCreate(url, UriKind.Absolute, out var u) && u.Scheme == Uri.UriSchemeHttps
        && string.Equals(u.Host, host, StringComparison.OrdinalIgnoreCase);
}
