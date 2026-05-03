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

    public static bool IsMimeAccepted(MaterialType type, string contentType, string[] otherAllowlist)
    {
        if (type == MaterialType.Other)
            return otherAllowlist.Contains(contentType, StringComparer.OrdinalIgnoreCase);

        return AcceptedMime.TryGetValue(type, out var accepted)
            && accepted.Contains(contentType, StringComparer.OrdinalIgnoreCase);
    }

    public static string[] AcceptedTypes(MaterialType type) =>
        AcceptedMime.TryGetValue(type, out var v) ? v : [];
}
