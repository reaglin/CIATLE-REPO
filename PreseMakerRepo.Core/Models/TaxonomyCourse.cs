using PreseMakerRepo.Core.Enums;

namespace PreseMakerRepo.Core.Models;

public class TaxonomyCourse
{
    public string CourseId { get; set; } = string.Empty;   // PK — globally unique; uppercase; immutable

    // Nullable to support the _ORPHAN_COURSE container
    public string? Level3Key { get; set; }
    public TaxonomyNode? Level3Node { get; set; }

    /// <summary>Display title. Courses created by a guide push start with the course id as a placeholder.</summary>
    public string Title { get; set; } = string.Empty;

    /// <summary>The SCNS statewide title, as supplied by the content pipeline.</summary>
    public string? StateTitle { get; set; }

    public int? CreditHours { get; set; }

    /// <summary>Clock hours, where that is the real measure (PSAV courses carry 0 credits).</summary>
    public int? ContactHours { get; set; }

    /// <summary>Listed on the site. A course that drops out of every catalog is set inactive — it stays
    /// visible anyway while it has a guide or published modules.</summary>
    public bool IsActive { get; set; }

    public string? CurriculumGuideUrl { get; set; }

    /// <summary>Active <see cref="CourseOffering"/> rows, kept in step by the catalog API for sorting and display.</summary>
    public int OfferingCount { get; set; }

    public CourseSource Source { get; set; } = CourseSource.Guide;

    /// <summary>Null for courses created before the catalog API existed.</summary>
    public DateTime? CreatedUtc { get; set; }
    public DateTime? UpdatedUtc { get; set; }

    public ICollection<Module> Modules { get; set; } = new List<Module>();
    public CurriculumGuide? Guide { get; set; }
    public ICollection<CourseOffering> Offerings { get; set; } = new List<CourseOffering>();
}
