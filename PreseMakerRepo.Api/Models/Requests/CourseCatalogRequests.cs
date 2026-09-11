namespace PreseMakerRepo.Api.Models.Requests;

/// <summary>
/// Base course data, with or without a guide. Used by PUT /api/v1/courses/{courseId} (where
/// <see cref="CourseId"/> may be omitted) and by each item of POST /api/v1/courses/batch.
/// Fields left null are left unchanged on an existing course; <see cref="Title"/> is required.
/// </summary>
public record UpsertCourseRequest(
    string? CourseId,
    string? Title,
    string? StateTitle,
    int? CreditHours,
    int? ContactHours,
    string? TaxonomyKey,
    bool? IsActive,
    List<CourseOfferingInput>? Offerings,
    bool? ReplaceOfferings);

/// <summary>One institution's offering of the course.</summary>
public record CourseOfferingInput(
    string? Institution,
    string? Title,
    decimal? Credits,
    int? ClockHours,
    bool? IsActive);

public record BatchUpsertCoursesRequest(List<UpsertCourseRequest>? Courses);

public record UpsertInstitutionRequest(
    string? Code,
    string? Name,
    string? Sector,
    string? ScnsId);

public record BatchUpsertInstitutionsRequest(List<UpsertInstitutionRequest>? Institutions);
