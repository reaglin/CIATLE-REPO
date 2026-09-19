namespace PreseMakerRepo.Core.Models;

/// <summary>
/// A programme of study — a major that supports a career path and is offered by a Florida school.
/// <para>
/// Ron's definition, 2026-09-17: <i>"I am going to define a program as a major that supports a
/// career path and is being offered by a Florida school. In many cases a program and a major will
/// be the same&#8230; However; Nursing AS (the major) = Nursing (the program) and Nursing BSN (the
/// major) = Nursing (the program). Nursing programs will encompass nursing degrees."</i>
/// </para>
/// <para>
/// ⚠⚠ <b>So a programme sits one level ABOVE a degree, and spans as many CIP codes as it takes.</b>
/// That is not a modelling convenience — it is forced by the second half of the ruling:
/// <i>"If a school has an LPN degree, they have a nursing program&#8230; I do not want a school to
/// be excluded from being listed because their offerings are limited."</i> LPN is CIP 51.39 and RN
/// is 51.38, so <b>Nursing must span both</b>. Measured against IPEDS: defining Nursing as 51.38
/// alone finds 39 Florida public institutions and misses 39 more — <b>every one of them a technical
/// college</b>, which is exactly the population the ruling protects. Both series together find 78.
/// </para>
/// <para>
/// ⚠⚠⚠ <b>A programme owns NO school list.</b> Ron: <i>"I am going to decouple programs from
/// schools. Programs will be just information about programs."</i> Which schools offer it is a
/// CROSS-REFERENCE, derived by matching this programme's CIP codes against
/// <see cref="InstitutionAward"/>, and it is never stored here.
/// </para>
/// </summary>
public class Program
{
    public Guid Id { get; set; }

    /// <summary>URL segment, e.g. "nursing".</summary>
    public string Slug { get; set; } = string.Empty;

    /// <summary>
    /// The student-facing name — "Nursing", not the federal "Registered Nursing, Nursing
    /// Administration, Nursing Research and Clinical Nursing". ⚠ This is the main reason a
    /// programme is its own entity rather than just a CIP node.
    /// </summary>
    public string Name { get; set; } = string.Empty;

    /// <summary>What the programme is and what studying it involves. A paragraph.</summary>
    public string Description { get; set; } = string.Empty;

    /// <summary>Sanitized HTML: the degrees it encompasses, entry points, what to expect.</summary>
    public string? BodyHtml { get; set; }

    /// <summary>
    /// ⚠ Where the degrees inside this programme are explained — "Nursing covers the LPN
    /// certificate, the A.S. leading to RN licensure, and the BSN". Rendered prominently, because
    /// the level a student enters at is the decision they actually face.
    /// </summary>
    public string? DegreesNote { get; set; }

    public bool IsPublished { get; set; }
    public int SortOrder { get; set; }
    public DateTime CreatedUtc { get; set; } = DateTime.UtcNow;
    public DateTime UpdatedUtc { get; set; } = DateTime.UtcNow;

    public ICollection<ProgramCip> Cips { get; set; } = new List<ProgramCip>();
    public ICollection<CareerPathProgram> CareerPaths { get; set; } = new List<CareerPathProgram>();

    /// <summary>Programmes this one names as close to it.</summary>
    public ICollection<ProgramRelation> Related { get; set; } = new List<ProgramRelation>();

    /// <summary>Programmes that name THIS one as close to them — the inverse of <see cref="Related"/>.</summary>
    public ICollection<ProgramRelation> RelatedFrom { get; set; } = new List<ProgramRelation>();
}

/// <summary>
/// A programme a student looking at this one should also read — with the reason, because the
/// reason is the part they do not already know.
/// <para>
/// ⚠⚠ Ron, 2026-09-19: <i>"the similarities between mechanical engineering and aerospace
/// engineering (any similar program) should be noted as these are things students would not
/// normally know when looking at a career… Just like civil, structural, transportation, etc… are
/// all very similar to civil."</i> A student choosing a major cannot see which doors a neighbouring
/// degree keeps open, and no catalogue tells them.
/// </para>
/// <para>
/// ⚠ CURATED, like everything else that makes a claim. The CIP tree already puts these
/// programmes near each other; what it cannot say is <i>aerospace employers hire large numbers of
/// mechanical engineers</i>. That sentence is the whole point of the row.
/// </para>
/// <para>
/// ⚠ Read in BOTH directions. A relation authored on one programme is shown on the other as
/// well, so a missing back-link never hides a connection — but a relation authored explicitly on
/// each side carries a note written for that side's reader, which is better.
/// </para>
/// </summary>
public class ProgramRelation
{
    public Guid Id { get; set; }
    public Guid ProgramId { get; set; }
    public Guid RelatedProgramId { get; set; }

    /// <summary>Why a student reading about this programme should look at that one.</summary>
    public string? Note { get; set; }

    public int SortOrder { get; set; }

    public Program? Program { get; set; }
    public Program? RelatedProgram { get; set; }
}

/// <summary>
/// One CIP code a programme covers. ⚠ Stored as a PREFIX match, so "51.38" covers every 6-digit
/// code beneath it and a programme does not have to enumerate them.
/// </summary>
public class ProgramCip
{
    public Guid Id { get; set; }
    public Guid ProgramId { get; set; }

    /// <summary>A 2-, 4- or 6-digit CIP code. Matched as a prefix against award records.</summary>
    public string CipCode { get; set; } = string.Empty;

    /// <summary>Why this code belongs to the programme — the evidence, as everywhere else.</summary>
    public string? Note { get; set; }

    public int SortOrder { get; set; }
    public Program? Program { get; set; }
}

/// <summary>
/// Links a career path to a programme that leads to it.
/// <para>
/// Ron: <i>"For programs associated with careers we want to note schools that offer the program in
/// the career (that will be a note)."</i> — so the career page shows, per programme, which schools
/// offer it. That note is derived through <see cref="ProgramCip"/> and <see cref="InstitutionAward"/>;
/// nothing about schools is stored on either side of this link.
/// </para>
/// </summary>
public class CareerPathProgram
{
    public Guid Id { get; set; }
    public Guid CareerPathId { get; set; }
    public Guid ProgramId { get; set; }

    /// <summary>How this programme relates to the career, in one line.</summary>
    public string? Note { get; set; }

    /// <summary>
    /// True when the programme is a ROUTE to the career; false when it is named as a neighbour
    /// a reader should know about but which does not lead there.
    /// <para>
    /// ⚠⚠ Added 2026-09-19 because the pages were asserting something their own notes denied:
    /// the Data Scientist path names Mechanical Engineering with the note <i>"Not a route into
    /// data science"</i>, and the programme page then headed it <i>"Careers this program leads
    /// to"</i>. A heading is read and small grey text is not, so the claim has to live in the
    /// structure rather than in the note.
    /// </para>
    /// </summary>
    public bool IsRoute { get; set; } = true;

    public int SortOrder { get; set; }
    public CareerPath? CareerPath { get; set; }
    public Program? Program { get; set; }
}

/// <summary>
/// One credential a Florida institution actually awarded, from the federal IPEDS completions file.
/// <para>
/// ⚠⚠ <b>This is the evidence behind every "which schools offer this" answer on the site</b>, and
/// it is the first programme-level data the project has ever held. Course offerings answer "where
/// can I take this course"; they cannot answer "who offers this major".
/// </para>
/// <para>
/// ⚠ It records what was AWARDED in a given year, which is strong evidence of what is offered but
/// lags a brand-new programme by a year or two. Pages that use it should say which year it is.
/// </para>
/// </summary>
public class InstitutionAward
{
    public Guid Id { get; set; }

    /// <summary>IPEDS UNITID — the federal institution key.</summary>
    public string UnitId { get; set; } = string.Empty;

    /// <summary>Institution name as IPEDS spells it.</summary>
    public string InstitutionName { get; set; } = string.Empty;

    /// <summary>Our own short code where the institution is one we already know; null otherwise.</summary>
    public string? InstitutionCode { get; set; }

    /// <summary>6-digit CIP, dotted, e.g. "51.3801".</summary>
    public string CipCode { get; set; } = string.Empty;

    /// <summary>The award level as a readable label — "Associate", "Bachelor's". THIS IS THE MAJOR.</summary>
    public string AwardLevel { get; set; } = string.Empty;

    /// <summary>Completions in the reference year. ⚠ First majors only; second majors double-count.</summary>
    public int Completions { get; set; }

    /// <summary>IPEDS collection year, e.g. 2023.</summary>
    public int Year { get; set; }
}
