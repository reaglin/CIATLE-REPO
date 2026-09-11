using System.Text.RegularExpressions;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Api.Helpers;

/// <summary>
/// The title a visitor sees for a course. Courses created by a guide push carry the course id as a
/// placeholder title, and SCNS supplies titles in capitals, so the stored value is not always
/// presentable: pick the first real title available and make an all-capitals one readable.
/// Stored data is never changed here — site reviews correct titles through the API.
/// </summary>
public static partial class CourseTitles
{
    public static string Display(string courseId, string? title, string? stateTitle = null, string? guideTitle = null)
    {
        var pick = IsReal(courseId, title) ? title
                 : IsReal(courseId, stateTitle) ? stateTitle
                 : IsReal(courseId, guideTitle) ? guideTitle
                 : null;
        return pick is null ? courseId : Readable(pick.Trim());
    }

    /// <summary>False for empty, the course-id placeholder, and the "Not Completed" guide stub.</summary>
    public static bool IsReal(string courseId, string? title) =>
        !string.IsNullOrWhiteSpace(title) &&
        !string.Equals(title.Trim(), courseId, StringComparison.OrdinalIgnoreCase) &&
        !string.Equals(title.Trim(), CurriculumGuide.StubTitle, StringComparison.OrdinalIgnoreCase);

    /// <summary>"INTRO TO CAD/CAM II" → "Intro to CAD/CAM II". Titles with any lower case are left alone.</summary>
    public static string Readable(string title)
    {
        if (title.Any(char.IsLower)) return title;
        var first = true;
        return Word().Replace(title, m =>
        {
            var w = m.Value;
            var isFirst = first;
            first = false;
            if (RomanNumeral().IsMatch(w) || Acronyms.Contains(w)) return w;
            var lower = w.ToLowerInvariant();
            if (!isFirst && SmallWords.Contains(lower)) return lower;
            return char.ToUpperInvariant(lower[0]) + lower[1..];
        });
    }

    [GeneratedRegex(@"[A-Za-z][A-Za-z']*")]
    private static partial Regex Word();

    [GeneratedRegex(@"^(I|II|III|IV|V|VI|VII|VIII|IX|X)$")]
    private static partial Regex RomanNumeral();

    private static readonly HashSet<string> SmallWords = new(StringComparer.Ordinal)
    {
        "a", "an", "and", "as", "at", "but", "by", "for", "from", "in", "into", "nor", "of", "on", "or",
        "per", "the", "to", "via", "vs", "with"
    };

    private static readonly HashSet<string> Acronyms = new(StringComparer.Ordinal)
    {
        "AC", "ADA", "ADN", "AI", "AIDS", "API", "ASE", "ASL", "AWS", "BSN", "CAD", "CAM", "CNA", "CNC", "CPA",
        "CPR", "CPT", "CSS", "DC", "DNA", "ECG", "EEG", "EHR", "EKG", "ELL", "EMR", "EMS", "EMT", "ESE", "ESL",
        "ESOL", "GIS", "GPS", "HIV", "HTML", "HVAC", "HVACR", "ICD", "IEP", "IT", "LAN", "LPN", "MLS", "MRI",
        "NCLEX", "OSHA", "PC", "PLC", "RF", "RN", "RNA", "ROTC", "SQL", "STEM", "TESOL", "TV", "UAS", "UAV",
        "UI", "UNIX", "US", "USA", "UX", "WAN"
    };
}
