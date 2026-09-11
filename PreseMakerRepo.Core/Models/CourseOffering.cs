namespace PreseMakerRepo.Core.Models;

/// <summary>
/// A verified offering of a course at one institution — what makes a course "exist" on the site.
/// Carries that school's own title and credit value, which is where divergence from the statewide
/// definition shows up.
/// </summary>
public class CourseOffering
{
    public string CourseId { get; set; } = string.Empty;
    public TaxonomyCourse Course { get; set; } = null!;

    public string InstitutionCode { get; set; } = string.Empty;
    public Institution Institution { get; set; } = null!;

    /// <summary>What this institution calls the course.</summary>
    public string? InstitutionTitle { get; set; }

    public decimal? Credits { get; set; }
    public int? ClockHours { get; set; }

    public bool IsActive { get; set; } = true;
    public DateTime UpdatedUtc { get; set; }
}
