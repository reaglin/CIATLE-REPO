namespace PreseMakerRepo.Api.Models.Responses;

/// <summary>
/// A programme in a list. <see cref="SchoolCount"/> is derived from the award table by CIP
/// prefix, exactly as the /programs page derives it, so the pipeline sees the same number a
/// reader does.
/// </summary>
public record ProgramSummaryDto(
    string Slug,
    string Name,
    string Description,
    int SchoolCount,
    int CipCount,
    int CareerPathCount,
    bool IsPublished,
    DateTime UpdatedUtc);

public record ProgramDto(
    string Slug,
    string Name,
    string Description,
    string? DegreesNote,
    string? BodyHtml,
    bool IsPublished,
    int SortOrder,
    DateTime CreatedUtc,
    DateTime UpdatedUtc,
    IReadOnlyList<ProgramCipDto> Cips,
    IReadOnlyList<ProgramSchoolDto> Schools,
    IReadOnlyList<string> AwardLevels,
    int AwardYear,
    IReadOnlyList<ProgramCareerPathDto> CareerPaths,
    IReadOnlyList<ProgramRelatedDto> Related);

/// <summary>
/// A neighbouring programme. <see cref="Mutual"/> is false when the relation was authored on the
/// OTHER programme and is being shown here in reverse — the note then speaks from its side.
/// </summary>
public record ProgramRelatedDto(
    string Slug,
    string Name,
    string? Note,
    int SchoolCount,
    bool Mutual);

/// <summary>One CIP code the programme covers, with the evidence for claiming it.</summary>
public record ProgramCipDto(string CipCode, string? CipTitle, string? Note, int SchoolCount);

/// <summary>
/// A Florida institution awarding something in the programme's CIP codes. ⚠ Ordered by name,
/// never by completions — Ron: the counts are "handy, but not required", and they must not rank
/// one school above another.
/// </summary>
public record ProgramSchoolDto(
    string UnitId,
    string Name,
    string? Code,
    IReadOnlyList<string> Awards,
    int Completions);

/// <summary>A career path this programme leads to.</summary>
public record ProgramCareerPathDto(string Slug, string Name, string? Note, bool IsRoute);

/// <summary>
/// Outcome of a programme push. <see cref="UnmatchedCips"/> names codes that match no award
/// record at all — not an error (a brand-new code may simply have no completions yet), but the
/// pipeline's cue to check the code before the page tells a reader nowhere offers it.
/// </summary>
public record UpsertProgramResponse(
    string Slug,
    string Outcome,
    int CipCount,
    int SchoolCount,
    int RelatedCount,
    IReadOnlyList<string> UnmatchedCips);
