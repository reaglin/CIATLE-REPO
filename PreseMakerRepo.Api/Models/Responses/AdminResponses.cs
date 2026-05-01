namespace PreseMakerRepo.Api.Models.Responses;

public record FlaggedItemDto(
    string ContentType,         // "module" | "material"
    Guid ContentId,
    string? CourseId,
    string Title,
    ContributorBriefDto Contributor,
    DateTime MostRecentFlagUtc,
    string? FlagReason,
    int FlagCount);

public record AdminStatsDto(
    int TotalModules,
    int PublishedModules,
    int FlaggedModules,
    int RemovedModules,
    int TotalMaterials,
    int TotalContributors,
    int SuspendedContributors,
    IReadOnlyList<CoursePrefixCount> ModulesByCoursePrefix,
    int RecentModules30Days);

public record CoursePrefixCount(string? Level3Key, int Count);
