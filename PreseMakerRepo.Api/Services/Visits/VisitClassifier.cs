using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;

namespace PreseMakerRepo.Api.Services.Visits;

/// <summary>
/// The rules of the visitor counter (plan Phase 9), kept apart from the middleware so they can be
/// tested: which requests are a person opening a page, how a visitor is identified (a salted hash,
/// never the address), which part of the site a page is in, and where a visitor came from.
/// The same rules as <c>Deployment/visitor_report.py</c>, so the log report and the counter agree.
/// </summary>
public static class VisitClassifier
{
    // Crawlers, bots, monitors and scripts (our own tools included). Same list as visitor_report.py.
    private static readonly Regex Bot = new(
        @"bot|crawl|spider|slurp|scrap|fetch|curl|wget|python|httpclient|http-client|okhttp|" +
        @"java/|go-http|libwww|axios|node-fetch|powershell|headless|phantom|lighthouse|" +
        @"facebookexternalhit|preview|monitor|uptime|pingdom|semrush|ahrefs|mj12|dotbot|" +
        @"bytespider|gptbot|chatgpt-user|oai-searchbot|claude|anthropic|ccbot|perplexity|" +
        @"dataforseo|petalbot|yandex|baidu|zgrab|masscan|nmap|nikto|censys|expanse|scan",
        RegexOptions.IgnoreCase | RegexOptions.Compiled);

    private static readonly Regex Course = new(
        @"^/courses/([A-Za-z]{3}\d{4}[A-Za-z]?(?:-[A-Za-z]{2,5})?)(?=/|$)",
        RegexOptions.IgnoreCase | RegexOptions.Compiled);

    private static readonly (Regex Rx, string Name)[] Sections =
    [
        (new Regex(@"^/$"), "Home page"),
        (new Regex(@"^/browse", RegexOptions.IgnoreCase), "Browse (subject tree)"),
        (new Regex(@"^/courses/[^/]+/guide$", RegexOptions.IgnoreCase), "Curriculum guides"),
        (new Regex(@"^/courses/[^/]+/resources$", RegexOptions.IgnoreCase), "Course resources"),
        (new Regex(@"^/courses/[^/]+$", RegexOptions.IgnoreCase), "Course pages"),
        (new Regex(@"^/careers", RegexOptions.IgnoreCase), "Career paths"),
        (new Regex(@"^/programs", RegexOptions.IgnoreCase), "Programmes"),
        (new Regex(@"^/queue/", RegexOptions.IgnoreCase), "Request queues"),
        (new Regex(@"^/request-guide", RegexOptions.IgnoreCase), "Request a guide"),
        (new Regex(@"^/(modules|materials)/", RegexOptions.IgnoreCase), "Modules and materials"),
        (new Regex(@"^/account/", RegexOptions.IgnoreCase), "Accounts"),
    ];

    public const int MaxPathLength = 200;

    public static bool IsBot(string? userAgent) =>
        string.IsNullOrWhiteSpace(userAgent) || Bot.IsMatch(userAgent);

    /// <summary>
    /// True when the finished request was a person opening a public page: a GET answered 200 with
    /// HTML, not the API or the admin console, not a prefetch, not a bot, not an administrator.
    /// </summary>
    public static bool ShouldCount(string method, string? path, int status, string? contentType,
        string? userAgent, bool isAdministrator, bool isPrefetch)
    {
        if (!HttpMethodsIsGet(method) || status != 200) return false;
        if (contentType is null || !contentType.StartsWith("text/html", StringComparison.OrdinalIgnoreCase)) return false;
        if (string.IsNullOrEmpty(path)) return false;
        if (path.StartsWith("/api/", StringComparison.OrdinalIgnoreCase) || path.Equals("/api", StringComparison.OrdinalIgnoreCase)) return false;
        if (path.StartsWith("/admin", StringComparison.OrdinalIgnoreCase)) return false;
        if (isAdministrator || isPrefetch) return false;
        return !IsBot(userAgent);
    }

    private static bool HttpMethodsIsGet(string method) =>
        string.Equals(method, "GET", StringComparison.OrdinalIgnoreCase);

    /// <summary>The path as stored: no trailing slash, course ids in capitals, at most 200 characters.</summary>
    public static string NormalizePath(string path)
    {
        if (path.Length > 1) path = path.TrimEnd('/');
        if (path.Length == 0) path = "/";
        var m = Course.Match(path);
        if (m.Success)
            path = path[..m.Groups[1].Index] + m.Groups[1].Value.ToUpperInvariant() + path[(m.Groups[1].Index + m.Groups[1].Length)..];
        return path.Length > MaxPathLength ? path[..MaxPathLength] : path;
    }

    public static string SectionOf(string path)
    {
        foreach (var (rx, name) in Sections)
            if (rx.IsMatch(path)) return name;
        return "Other pages";
    }

    /// <summary>The course id a page belongs to (course page, guide or resources), or null.</summary>
    public static string? CourseOf(string path)
    {
        var m = Course.Match(path);
        return m.Success ? m.Groups[1].Value.ToUpperInvariant() : null;
    }

    /// <summary>
    /// The referring site's host without "www.", or null when there is no referrer or it is this
    /// site (a visitor moving between our own pages).
    /// </summary>
    public static string? SourceOf(string? referer, string? ownHost)
    {
        if (string.IsNullOrWhiteSpace(referer)) return null;
        if (!Uri.TryCreate(referer, UriKind.Absolute, out var uri) || string.IsNullOrEmpty(uri.Host)) return null;
        var host = uri.Host.ToLowerInvariant();
        if (host.StartsWith("www.")) host = host[4..];
        var own = (ownHost ?? "").ToLowerInvariant();
        if (own.StartsWith("www.")) own = own[4..];
        if (host == own || host == "floridacourserepo.com") return null;
        return host.Length > 100 ? host[..100] : host;
    }

    /// <summary>16 hex characters of SHA-256(salt + IP + user agent). The address is not recoverable without the salt.</summary>
    public static string VisitorHash(string salt, string? ip, string? userAgent)
    {
        var bytes = SHA256.HashData(Encoding.UTF8.GetBytes($"{salt}:visit:{ip}|{userAgent}"));
        return Convert.ToHexString(bytes, 0, 8).ToLowerInvariant();
    }

    private static readonly TimeZoneInfo Florida = FindFlorida();

    private static TimeZoneInfo FindFlorida()
    {
        foreach (var id in new[] { "America/New_York", "Eastern Standard Time" })
        {
            try { return TimeZoneInfo.FindSystemTimeZoneById(id); }
            catch (TimeZoneNotFoundException) { }
            catch (InvalidTimeZoneException) { }
        }
        return TimeZoneInfo.Utc;
    }

    /// <summary>The day in Florida for a UTC time.</summary>
    public static DateOnly FloridaDay(DateTime utc) =>
        DateOnly.FromDateTime(TimeZoneInfo.ConvertTimeFromUtc(DateTime.SpecifyKind(utc, DateTimeKind.Utc), Florida));
}
