namespace PreseMakerRepo.Api.Models.Responses;

/// <summary>
/// One node of the CIP browse tree. <see cref="Title"/> and <see cref="Definition"/> are the
/// U.S. Department of Education's own words (CIP 2020), carried verbatim.
/// </summary>
public record CipNodeDto(
    string Code,
    int Level,
    string Title,
    string? Definition,
    string? Examples,
    string? ParentCode,
    int ChildCount);

public record CareerPathSummaryDto(
    string Slug,
    string Name,
    string CipCode,
    string? CipTitle,
    string Description,
    string? SocCode,
    int CourseCount,
    DateTime UpdatedUtc);

public record CareerPathDto(
    string Slug,
    string Name,
    string CipCode,
    string? CipTitle,
    string Description,
    string? SocCode,
    string? CredentialNote,
    string? BodyHtml,
    int SortOrder,
    DateTime CreatedUtc,
    DateTime UpdatedUtc,
    IReadOnlyList<CareerPathCipDto> CipCodes,
    IReadOnlyList<CareerPathCourseDto> Courses,
    IReadOnlyList<CareerPathSourceDto> Sources);

/// <summary>A further CIP group the path is filed under, with the evidence for it.</summary>
public record CareerPathCipDto(string CipCode, string? CipTitle, string? Note);

/// <summary><see cref="Reason"/> is never null: a course with no stated reason is not published.</summary>
public record CareerPathCourseDto(string CourseId, string Reason, string? VariantNote);

public record CareerPathSourceDto(string Label, string Url, string? Note);

/// <summary>
/// Outcome of a path push. <see cref="UnlistedCourses"/> names courses the path places that the
/// catalog does not carry yet — the pipeline's cue to send their base data, since a path must
/// never link to a page that is not there.
/// </summary>
public record UpsertCareerPathResponse(
    string Slug,
    string Outcome,
    int CipCount,
    int CourseCount,
    int SourceCount,
    IReadOnlyList<string> UnlistedCourses);
