namespace PreseMakerRepo.Core.Models;

/// <summary>
/// One node of the federal CIP (Classification of Instructional Programs) taxonomy,
/// which is the browse framework for Career Paths and Programs.
/// <para>
/// Ron, 2026-09-17: career paths are "all centered on CIP codes and the CIP codes become
/// the framework for that page", laid out as at
/// <c>https://nces.ed.gov/ipeds/cipcode/browse.aspx?y=55</c>.
/// </para>
/// <para>
/// Two levels are seeded. <b>Level 2</b> (e.g. <c>51</c> Health Professions) is the complete
/// federal taxonomy minus a short list of series that are not postsecondary programmes
/// (reserved codes, adult basic skills, medical residencies). <b>Level 4</b> (e.g. <c>51.38</c>
/// Registered Nursing) is seeded only where Florida institutions have course evidence, so an
/// unpopulated series shows as an empty branch rather than disappearing.
/// </para>
/// <para>
/// ⚠ <b>Titles and definitions are NCES's own words, copied verbatim.</b> We do not paraphrase
/// the federal taxonomy. Anything we want to say ourselves goes in <see cref="EditorialNote"/>.
/// </para>
/// <para>
/// ⚠⚠ <b>Courses are never attached to a CIP node by classification data.</b> Institutions do
/// assign CIP codes to courses, and we hold 25,412 such assignments — but they disagree across
/// CIP families on 7% of multi-carrier courses, and the disagreement is worst in the broadest,
/// highest-enrolment subjects. That data is an authoring aid only. Courses reach a student
/// through a curated <see cref="CareerPath"/>, never through a derived classification.
/// </para>
/// </summary>
public class CipNode
{
    /// <summary>The CIP code itself, and the primary key: "51" or "51.38".</summary>
    public string Code { get; set; } = string.Empty;

    /// <summary>2 for a series ("51"), 4 for a group ("51.38").</summary>
    public int Level { get; set; }

    /// <summary>NCES CIPTitle, verbatim.</summary>
    public string Title { get; set; } = string.Empty;

    /// <summary>
    /// NCES CIPDefinition, verbatim. ⚠ Empty for most 4-digit groups: the federal file fills
    /// those with the placeholder "Instructional content for this group of programs is defined
    /// in codes X - Y", which tells a reader nothing. The seed drops those, so a page with no
    /// definition should show its child titles or its examples instead of an empty panel.
    /// </summary>
    public string? Definition { get; set; }

    /// <summary>NCES Examples, verbatim — illustrative programme names for a group.</summary>
    public string? Examples { get; set; }

    /// <summary>Parent code ("51" for "51.38"); null for a series.</summary>
    public string? ParentCode { get; set; }

    /// <summary>Number of seeded children, denormalised so the browse page needs no join.</summary>
    public int ChildCount { get; set; }

    /// <summary>
    /// Our own editorial text about this area in Florida — admin-edited, sanitized HTML,
    /// following <c>TaxonomyNodeDescription</c>. Kept separate from <see cref="Definition"/>
    /// so the federal text is never overwritten or confused with ours.
    /// </summary>
    public string? EditorialNote { get; set; }

    /// <summary>Hide a node from browse without deleting it.</summary>
    public bool IsActive { get; set; } = true;

    public DateTime CreatedUtc { get; set; } = DateTime.UtcNow;
    public DateTime UpdatedUtc { get; set; } = DateTime.UtcNow;

    public CipNode? Parent { get; set; }
    public ICollection<CipNode> Children { get; set; } = new List<CipNode>();
    public ICollection<CareerPath> CareerPaths { get; set; } = new List<CareerPath>();
}
