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
    List<CareerPathCourseInput>? Courses,
    List<CareerPathSourceInput>? Sources);

/// <summary><see cref="Reason"/> is required: an unjustified course does not belong on a path.</summary>
public record CareerPathCourseInput(
    string? CourseId,
    string? Reason,
    string? VariantNote);

public record CareerPathSourceInput(
    string? Label,
    string? Url,
    string? Note);
