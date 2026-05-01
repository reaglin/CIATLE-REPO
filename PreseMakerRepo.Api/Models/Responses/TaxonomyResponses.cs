namespace PreseMakerRepo.Api.Models.Responses;

public record TaxonomyTreeResponse(
    string RepositoryName,
    IReadOnlyList<LevelLabel> Levels,
    IReadOnlyList<TaxonomyNodeDto> Tree);

public record LevelLabel(int Level, string Label);

public record TaxonomyNodeDto(
    string Key,
    string Name,
    int Level,
    int CourseCount,
    int ModuleCount,
    IReadOnlyList<TaxonomyNodeDto>? Children = null,
    NodeParentDto? Parent = null);

public record NodeParentDto(string Key, string Name);

public record TaxonomyLevel2NodeDto(
    string Key,
    string Name,
    int Level,
    int CourseCount,
    int ModuleCount,
    NodeParentDto? Parent,
    IReadOnlyList<TaxonomyNodeDto>? Children);

public record ValidateCourseResponse(
    bool IsValid,
    string CourseId,
    string? Title = null,
    int? CreditHours = null,
    TaxonomyPathDto? TaxonomyPath = null,
    string? CurriculumGuideUrl = null,
    string? Reason = null);

public record TaxonomyPathDto(
    NodeParentDto? Level1,
    NodeParentDto? Level2,
    NodeParentDto? Level3);
