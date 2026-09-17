namespace PreseMakerRepo.Api.Models.Requests;

/// <summary>
/// A whole career path in one document: the path, the courses placed on it, and the sources
/// it rests on. PUT /api/v1/career-paths/{slug} replaces all three together, so a push is
/// idempotent and a removed course or source actually disappears.
/// </summary>
public record UpsertCareerPathRequest(
    string? Name,
    string? CipCode,
    string? Description,
    string? SocCode,
    string? CredentialNote,
    string? BodyHtml,
    bool? IsPublished,
    int? SortOrder,
    List<CareerPathCipInput>? CipCodes,
    List<CareerPathProgramInput>? Programs,
    List<CareerPathCourseInput>? Courses,
    List<CareerPathSourceInput>? Sources);

/// <summary>
/// A further CIP group the path is filed under, beyond <c>CipCode</c>. ⚠ <see cref="Note"/>
/// should carry the EVIDENCE that students actually come from this programme, with its source
/// — not a judgement that the subject looks related.
/// </summary>
/// <summary>
/// A programme that leads to this career. ⚠ <see cref="Slug"/> must name a seeded programme;
/// the schools offering it are derived from the programme, never listed here.
/// </summary>
public record CareerPathProgramInput(
    string? Slug,
    string? Note);

public record CareerPathCipInput(
    string? CipCode,
    string? Note);

/// <summary><see cref="Reason"/> is required: an unjustified course does not belong on a path.</summary>
public record CareerPathCourseInput(
    string? CourseId,
    string? Reason,
    string? VariantNote);

public record CareerPathSourceInput(
    string? Label,
    string? Url,
    string? Note);
