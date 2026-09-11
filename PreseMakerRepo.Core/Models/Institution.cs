namespace PreseMakerRepo.Core.Models;

/// <summary>
/// A school that offers courses (UCF, DSC, PESC…). Keyed by the short code the SCNS inventory uses.
/// Filled over the API by the content pipeline; an offering that names an unknown code creates a
/// code-only row, and the name arrives later.
/// </summary>
public class Institution
{
    /// <summary>Uppercase short code, e.g. "UCF". Primary key.</summary>
    public string Code { get; set; } = string.Empty;

    public string? Name { get; set; }

    /// <summary>Free text for now: "FCS", "SUS", "private", "other".</summary>
    public string? Sector { get; set; }

    /// <summary>The institution's numeric id on flscns.fldoe.org, when known.</summary>
    public string? ScnsId { get; set; }

    public DateTime UpdatedUtc { get; set; }

    public ICollection<CourseOffering> Offerings { get; set; } = new List<CourseOffering>();
}
