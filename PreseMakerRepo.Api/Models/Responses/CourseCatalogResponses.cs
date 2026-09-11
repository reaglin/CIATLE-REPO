namespace PreseMakerRepo.Api.Models.Responses;

/// <summary>Outcome of one course write: "created", "updated", "unchanged" or "failed".</summary>
public record CourseUpsertResult(
    string CourseId,
    string Outcome,
    string? TaxonomyKey,
    string? ErrorCode = null,
    string? Message = null,
    IReadOnlyList<FieldError>? Fields = null);

public record BatchUpsertCoursesResponse(
    int Created,
    int Updated,
    int Unchanged,
    int Failed,
    IReadOnlyList<CourseUpsertResult> Results);

/// <summary>A course's base data as the catalog holds it — what the content pipeline reconciles against.</summary>
public record CatalogCourseDto(
    string CourseId,
    string Title,
    string? StateTitle,
    int? CreditHours,
    int? ContactHours,
    string? TaxonomyKey,
    bool IsActive,
    string Source,
    bool HasGuide,
    int OfferingCount,
    DateTime? CreatedUtc,
    DateTime? UpdatedUtc);

public record CourseOfferingDto(
    string Institution,
    string? InstitutionName,
    string? Title,
    decimal? Credits,
    int? ClockHours,
    bool IsActive);

public record CatalogCourseDetailDto(
    CatalogCourseDto Course,
    IReadOnlyList<CourseOfferingDto> Offerings);

public record InstitutionDto(
    string Code,
    string? Name,
    string? Sector,
    string? ScnsId,
    int OfferingCount);

public record InstitutionUpsertResult(
    string Code,
    string Outcome,
    string? ErrorCode = null,
    string? Message = null,
    IReadOnlyList<FieldError>? Fields = null);

public record BatchUpsertInstitutionsResponse(
    int Created,
    int Updated,
    int Unchanged,
    int Failed,
    IReadOnlyList<InstitutionUpsertResult> Results);
