namespace PreseMakerRepo.Core.Models;

public class CurriculumGuide
{
    /// <summary>
    /// Title of the placeholder guide created when modules are published for a course with no guide.
    /// A stub is not a guide: it never counts as one and never blocks a guide request.
    /// </summary>
    public const string StubTitle = "Not Completed";

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
