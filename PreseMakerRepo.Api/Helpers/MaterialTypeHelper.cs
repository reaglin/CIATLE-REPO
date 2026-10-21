using PreseMakerRepo.Core.Enums;

namespace PreseMakerRepo.Api.Helpers;

public static class MaterialTypeHelper
{
    private static readonly Dictionary<MaterialType, string[]> AcceptedMime = new()
    {
        [MaterialType.Presentation] = [
            "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        ],
        [MaterialType.NarratedPresentation] = [
            "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        ],
        [MaterialType.InteractiveHTML] = [
            "text/html", "application/zip"
        ],
        [MaterialType.PrintableHTML] = [
            "text/html"
        ],
        [MaterialType.GutenbergHTML] = [
            "text/html"
        ],
        [MaterialType.Document] = [
            "text/markdown", "text/plain", "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/json", "application/xml", "text/xml", "text/csv",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ],
        [MaterialType.Image] = [
            "image/png", "image/jpeg", "image/gif", "image/svg+xml", "application/zip"
        ],
        [MaterialType.Audio] = [
            "audio/mpeg", "audio/wav", "application/zip"
        ],
        [MaterialType.Assignment] = [
            "application/pdf", "text/html", "text/markdown", "application/zip"
        ],
        // Other is validated against configurable allowlist — treated as empty here
        [MaterialType.Other] = []
    };

    public static bool TryParse(string value, out MaterialType type) =>
        Enum.TryParse(value, ignoreCase: true, out type);

    /// <summary>
    /// True when a file of <paramref name="contentType"/> may be stored as <paramref name="type"/>.
    /// The content type is compared without its parameters ("text/html; charset=utf-8" is "text/html").
    /// Other is checked against the configured allowlist, whose entries are ".ext:mime"
    /// (e.g. ".csv:text/csv"); a bare "mime" entry is accepted too. A file sent as
    /// application/octet-stream (no type known to the sender) is accepted for Other when its
    /// extension is on the list.
    /// </summary>
    public static bool IsMimeAccepted(MaterialType type, string contentType, string[] otherAllowlist,
                                      string? fileName = null)
    {
        var mime = (contentType ?? string.Empty).Split(';')[0].Trim();

        if (type == MaterialType.Other)
        {
            var ext = string.IsNullOrEmpty(fileName) ? string.Empty : Path.GetExtension(fileName);
            foreach (var entry in otherAllowlist ?? [])
            {
                var (entryExt, entryMime) = SplitAllowlistEntry(entry);
                if (entryMime.Length > 0 && string.Equals(entryMime, mime, StringComparison.OrdinalIgnoreCase))
                    return true;
                if (entryExt.Length > 0 && ext.Length > 0
                    && string.Equals(mime, "application/octet-stream", StringComparison.OrdinalIgnoreCase)
                    && string.Equals(entryExt, ext, StringComparison.OrdinalIgnoreCase))
                    return true;
            }
            return false;
        }

        return AcceptedMime.TryGetValue(type, out var accepted)
            && accepted.Contains(mime, StringComparer.OrdinalIgnoreCase);
    }

    /// <summary>Splits an allowlist entry ".ext:mime" into (".ext", "mime"); a bare "mime" gives ("", "mime").</summary>
    public static (string Ext, string Mime) SplitAllowlistEntry(string entry)
    {
        var e = (entry ?? string.Empty).Trim();
        if (e.StartsWith('.'))
        {
            var colon = e.IndexOf(':');
            return colon < 0 ? (e, string.Empty) : (e[..colon].Trim(), e[(colon + 1)..].Trim());
        }
        return (string.Empty, e);
    }

    public static string[] AcceptedTypes(MaterialType type) =>
        AcceptedMime.TryGetValue(type, out var v) ? v : [];
}
