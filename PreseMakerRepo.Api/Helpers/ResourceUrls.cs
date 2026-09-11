using System.Text.RegularExpressions;
using PreseMakerRepo.Core.Enums;

namespace PreseMakerRepo.Api.Helpers;

/// <summary>A suggested link after checking and normalising.</summary>
public sealed record ParsedResourceUrl(string Url, ResourceType Type, string? YouTubeVideoId, string Host);

/// <summary>
/// Checks and normalises resource links. The server never fetches a submitted URL — reviewing happens in
/// the AI session — so this is shape checking only: a public http(s) host, no credentials, no IP literals
/// or local names. Normalising (lowercase host, no fragment, no tracking parameters, one canonical form
/// per YouTube video) is what lets the same link suggested twice be recognised as one resource.
/// </summary>
public static partial class ResourceUrls
{
    public const int MaxLength = 2048;

    private static readonly HashSet<string> YouTubeHosts = new(StringComparer.OrdinalIgnoreCase)
    {
        "youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be", "youtube-nocookie.com", "www.youtube-nocookie.com"
    };

    private static readonly HashSet<string> TrackingParameters = new(StringComparer.OrdinalIgnoreCase)
    {
        "fbclid", "gclid", "msclkid", "mc_cid", "mc_eid", "igshid", "si"
    };

    private static readonly string[] LocalSuffixes = [".localhost", ".local", ".internal", ".lan", ".home", ".corp"];

    public static bool TryParse(string? raw, out ParsedResourceUrl parsed, out string error)
    {
        parsed = null!;
        error = string.Empty;

        var text = (raw ?? string.Empty).Trim();
        if (text.Length == 0) { error = "Enter the link (web address)."; return false; }
        if (text.Length > MaxLength) { error = "That link is too long."; return false; }
        if (!text.Contains("://", StringComparison.Ordinal)) text = "https://" + text;

        if (!Uri.TryCreate(text, UriKind.Absolute, out var uri) ||
            (uri.Scheme != Uri.UriSchemeHttp && uri.Scheme != Uri.UriSchemeHttps))
        {
            error = "Enter a web address starting with http:// or https://.";
            return false;
        }

        var host = uri.IdnHost.ToLowerInvariant().TrimEnd('.');
        if (uri.HostNameType != UriHostNameType.Dns || !host.Contains('.') || host == "localhost" ||
            LocalSuffixes.Any(s => host.EndsWith(s, StringComparison.Ordinal)) || uri.UserInfo.Length > 0)
        {
            error = "That link does not point to a public website.";
            return false;
        }

        if (YouTubeHosts.Contains(host))
        {
            var id = YouTubeId(uri, host);
            if (id is null)
            {
                error = "That YouTube link does not point to a single video.";
                return false;
            }
            parsed = new ParsedResourceUrl($"https://www.youtube.com/watch?v={id}", ResourceType.YouTube, id, "youtube.com");
            return true;
        }

        var builder = new UriBuilder(uri)
        {
            Scheme = uri.Scheme,
            Host = host,
            Fragment = string.Empty,
            Query = CleanQuery(uri.Query)
        };
        if ((uri.Scheme == Uri.UriSchemeHttps && builder.Port == 443) || (uri.Scheme == Uri.UriSchemeHttp && builder.Port == 80))
            builder.Port = -1;

        var url = builder.Uri.AbsoluteUri;
        if (url.Length > MaxLength) { error = "That link is too long."; return false; }
        parsed = new ParsedResourceUrl(url, ResourceType.Website, null, DisplayHost(url));
        return true;
    }

    /// <summary>"https://www.khanacademy.org/…" → "khanacademy.org".</summary>
    public static string DisplayHost(string url)
    {
        if (!Uri.TryCreate(url, UriKind.Absolute, out var uri)) return url;
        var host = uri.Host.ToLowerInvariant();
        return host.StartsWith("www.", StringComparison.Ordinal) ? host[4..] : host;
    }

    public static bool IsVideoId(string? id) => id is not null && VideoId().IsMatch(id);

    private static string? YouTubeId(Uri uri, string host)
    {
        var segments = uri.AbsolutePath.Split('/', StringSplitOptions.RemoveEmptyEntries);
        string? candidate = null;
        if (host == "youtu.be")
            candidate = segments.FirstOrDefault();
        else if (segments.Length >= 2 && segments[0] is "shorts" or "embed" or "live" or "v")
            candidate = segments[1];
        else if (segments.Length >= 1 && segments[0] == "watch")
            candidate = QueryValue(uri.Query, "v");
        return IsVideoId(candidate) ? candidate : null;
    }

    private static string? QueryValue(string query, string name)
    {
        foreach (var pair in query.TrimStart('?').Split('&', StringSplitOptions.RemoveEmptyEntries))
        {
            var eq = pair.IndexOf('=');
            var key = eq < 0 ? pair : pair[..eq];
            if (string.Equals(Uri.UnescapeDataString(key), name, StringComparison.Ordinal))
                return eq < 0 ? string.Empty : Uri.UnescapeDataString(pair[(eq + 1)..]);
        }
        return null;
    }

    /// <summary>Drops utm_* and click-id parameters, keeping the rest in order and as encoded.</summary>
    private static string CleanQuery(string query)
    {
        var kept = query.TrimStart('?')
            .Split('&', StringSplitOptions.RemoveEmptyEntries)
            .Where(pair =>
            {
                var key = Uri.UnescapeDataString(pair.Split('=', 2)[0]);
                return !key.StartsWith("utm_", StringComparison.OrdinalIgnoreCase) && !TrackingParameters.Contains(key);
            });
        return string.Join('&', kept);
    }

    [GeneratedRegex("^[A-Za-z0-9_-]{11}$")]
    private static partial Regex VideoId();
}
