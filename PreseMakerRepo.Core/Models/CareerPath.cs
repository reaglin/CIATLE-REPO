namespace PreseMakerRepo.Core.Models;

/// <summary>
/// A documented route from study to an occupation, hung off a <see cref="CipNode"/>.
/// <para>
/// Shape settled by Ron (2026-09-11, <c>COURSE_CATALOG_PLAN.md</c> §14): "not a tremendous
/// amount of information: career path name, short description, associated courses; not all,
/// but courses that are specific to a career path and areas that might be important, like
/// math is to engineering. Programs that can lead to that career path should be listed."
/// A path is held together by <b>its sources</b> — licensing boards, BLS/O*NET, FLDOE,
/// professional associations — not by our own assertions.
/// </para>
/// <para>
/// ⚠⚠⚠ <b>Paths are curated content, never derived data.</b> Every course is placed by an
/// author and identified by exact course id. No prerequisite-text parsing, no inference from
/// course-code arithmetic, no classification lookup. This is the first principle of
/// <c>CAREER_PATHS_PLAN.md</c> and it exists because two hundred batches of guide work
/// established that a course number does not identify a course.
/// </para>
/// </summary>
public class CareerPath
{
    public Guid Id { get; set; }

    /// <summary>URL segment, e.g. "registered-nurse". Unique.</summary>
    public string Slug { get; set; } = string.Empty;

    /// <summary>The occupation as a student would name it, e.g. "Registered Nurse".</summary>
    public string Name { get; set; } = string.Empty;

    /// <summary>
    /// The CIP group this path sits under, e.g. "51.38". ⚠ A CIP code classifies a
    /// <i>programme of instruction</i>, not an occupation, so this is where the path is
    /// filed for browsing — it is not a claim that the code means the job.
    /// </summary>
    public string CipCode { get; set; } = string.Empty;

    /// <summary>Short plain description of the profession. A paragraph, not an essay.</summary>
    public string Description { get; set; } = string.Empty;

    /// <summary>
    /// Standard Occupational Classification code where one applies, e.g. "29-1141".
    /// ⚠ Optional, and deliberately so: some real destinations have no clean SOC code, and
    /// some SOC codes cover several distinct jobs. Where it exists it is the honest link to
    /// federal wage and outlook data; where it does not, the path still stands.
    /// </summary>
    public string? SocCode { get; set; }

    /// <summary>
    /// ⚠⚠ What the law or an accreditor requires beyond coursework — licensure, a programme
    /// approved by a named accreditor, an examination. Rendered prominently, because guide
    /// work repeatedly found that <b>accreditation outranks credit</b>: a student can hold
    /// credit for every course and still not qualify. Null where nothing is required.
    /// </summary>
    public string? CredentialNote { get; set; }

    /// <summary>Sanitized HTML; the substantive body where one is warranted.</summary>
    public string? BodyHtml { get; set; }

    public bool IsPublished { get; set; }
    public int SortOrder { get; set; }
    public DateTime CreatedUtc { get; set; } = DateTime.UtcNow;
    public DateTime UpdatedUtc { get; set; } = DateTime.UtcNow;

    public CipNode? Cip { get; set; }
    public ICollection<CareerPathCourse> Courses { get; set; } = new List<CareerPathCourse>();
    public ICollection<CareerPathSource> Sources { get; set; } = new List<CareerPathSource>();
}

/// <summary>
/// One course an author has placed on a path, with the reason it is there.
/// <para>
/// ⚠ <b>Selective, not exhaustive</b> (Ron, 2026-09-11): the courses specific to the path,
/// plus the foundations that decide whether someone can follow it — "like math is to
/// engineering". A complete course list would be a catalogue, which the site already has.
/// </para>
/// </summary>
public class CareerPathCourse
{
    public Guid Id { get; set; }
    public Guid CareerPathId { get; set; }

    /// <summary>Exact SCNS course id, e.g. "NUR3125". Links to the guide, or to a request.</summary>
    public string CourseId { get; set; } = string.Empty;

    /// <summary>
    /// ⚠ <b>Required.</b> Why this course is on this path, in one line — "the mathematics the
    /// whole engineering sequence is built on". A course with no stated reason is a course the
    /// author has not justified, and the reason is what makes the list useful rather than long.
    /// </summary>
    public string Reason { get; set; } = string.Empty;

    /// <summary>
    /// ⚠⚠ Where the same number carries a different subject somewhere in Florida, or a
    /// carrier diverges in a way that matters to this path. This is where the guide work's
    /// divergence findings reach a path page. Null when the number is clean.
    /// </summary>
    public string? VariantNote { get; set; }

    public int SortOrder { get; set; }
    public CareerPath? CareerPath { get; set; }
}

/// <summary>
/// An external authority a path rests on. ⚠ Ron: a path is "grounded in links to the detailed
/// sources that support it" — licensing boards, BLS/O*NET, FLDOE, professional associations.
/// A path with no sources is an assertion, and this project does not publish assertions.
/// </summary>
public class CareerPathSource
{
    public Guid Id { get; set; }
    public Guid CareerPathId { get; set; }

    /// <summary>Who it is, e.g. "Florida Board of Nursing".</summary>
    public string Label { get; set; } = string.Empty;

    public string Url { get; set; } = string.Empty;

    /// <summary>What this source establishes, so a reader knows why to follow it.</summary>
    public string? Note { get; set; }

    public int SortOrder { get; set; }
    public CareerPath? CareerPath { get; set; }
}
