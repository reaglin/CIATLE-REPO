namespace PreseMakerRepo.Core.Models;

public class TaxonomyCourse
{
    public string CourseId { get; set; } = string.Empty;   // PK — globally unique; uppercase; immutable

    // Nullable to support the _ORPHAN_COURSE container
    public string? Level3Key { get; set; }
    public TaxonomyNode? Level3Node { get; set; }

    public string Title { get; set; } = string.Empty;
    public int? CreditHours { get; set; }
    public bool IsActive { get; set; }
    public string? CurriculumGuideUrl { get; set; }

    public ICollection<Module> Modules { get; set; } = new List<Module>();
}
