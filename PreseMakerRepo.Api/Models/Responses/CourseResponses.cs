namespace PreseMakerRepo.Api.Models.Responses;

public record PagedResult<T>(
    IReadOnlyList<T> Items,
    int TotalCount,
    int Page,
    int PageSize,
    int TotalPages);

public record CourseListItem(
    string CourseId,
    string Title,
    int? CreditHours,
    int ModuleCount,
    int MaterialCount,
    DateTime? NewestSubmissionDate,
    string? CurriculumGuideUrl);

public record CourseDetailResponse(
    string CourseId,
    string Title,
    int? CreditHours,
    TaxonomyPathDto? TaxonomyPath,
    string? CurriculumGuideUrl,
    int ModuleCount,
    int MaterialCount,
    DateTime? NewestSubmissionDate,
    IReadOnlyList<ModuleSummaryDto> Modules);

public record ModuleSummaryDto(
    Guid ModuleId,
    string Title,
    ContributorBriefDto Contributor,
    string License,
    string LicenseDisplayName,
    string LicenseUrl,
    DateTime SubmittedUtc,
    int MaterialCount,
    IReadOnlyList<string> MaterialTypes);

public record ModuleDetailResponse(
    Guid ModuleId,
    string CourseId,
    string Title,
    string Description,
    IReadOnlyList<string> Outcomes,
    IReadOnlyList<object> TopicHierarchy,
    ContributorBriefDto Contributor,
    string License,
    string LicenseDisplayName,
    string LicenseUrl,
    DateTime SubmittedUtc,
    DateTime? UpdatedUtc,
    string Status,
    IReadOnlyList<MaterialDto> Materials,
    string DownloadAllUrl);

public record MaterialDto(
    Guid MaterialId,
    string Title,
    string Type,
    string? Description,
    string FileName,
    long FileSizeBytes,
    string ContentType,
    string DownloadUrl);

public record ContributorBriefDto(
    string Username,
    string? DisplayName,
    string? InstitutionName,
    bool IsEduVerified);

public record RecentModulesResponse(IReadOnlyList<ModuleSummaryDto> Items);

public record MaterialSummaryDto(
    Guid MaterialId,
    string Title,
    string Type,
    string? Description,
    string FileName,
    long FileSizeBytes,
    string ContentType,
    ContributorBriefDto Contributor,
    string License,
    string LicenseDisplayName,
    DateTime SubmittedUtc,
    string DownloadUrl);

public record MaterialDetailDto(
    Guid MaterialId,
    Guid ModuleId,
    string CourseId,
    string Title,
    string Type,
    string? Description,
    string FileName,
    long FileSizeBytes,
    string ContentType,
    ContributorBriefDto Contributor,
    string License,
    string LicenseDisplayName,
    string LicenseUrl,
    DateTime SubmittedUtc,
    DateTime? UpdatedUtc,
    string Status,
    string DownloadUrl);

public record SearchResultDto(
    string ResultType,       // "module" | "material"
    Guid ModuleId,
    string CourseId,
    string Title,
    string? Description,
    ContributorBriefDto Contributor,
    DateTime SubmittedUtc,
    TaxonomyPathDto? TaxonomyPath,
    // Material-only fields (null for module results)
    Guid? MaterialId,
    string? MaterialType,
    string? FileName,
    string? ModuleTitle);
