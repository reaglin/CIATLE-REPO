namespace PreseMakerRepo.Core.Models;

public class CurriculumGuide
{
    public string CourseId { get; set; } = string.Empty;   // PK + FK to TaxonomyCourse
    public string Title { get; set; } = string.Empty;
    public string HtmlContent { get; set; } = string.Empty;
    public int? Credits { get; set; }
    public int? ContactHours { get; set; }
    public string? Prerequisites { get; set; }
    public string? Version { get; set; }
    public DateTime GeneratedUtc { get; set; }
    public DateTime UpdatedUtc { get; set; }

    public TaxonomyCourse Course { get; set; } = null!;
}
