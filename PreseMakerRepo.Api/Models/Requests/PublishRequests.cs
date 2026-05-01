namespace PreseMakerRepo.Api.Models.Requests;

public record MaterialMetadataItem(
    string Title,
    string Type,
    string? Description,
    string FilePartName);

public record PublishModuleRequest(
    string Title,
    string Description,
    IReadOnlyList<string>? Outcomes,
    IReadOnlyList<object>? TopicHierarchy,
    string License,
    IReadOnlyList<MaterialMetadataItem> Materials);

public record UpdateModuleRequest(
    string? Title,
    string? Description,
    IReadOnlyList<string>? Outcomes,
    IReadOnlyList<object>? TopicHierarchy,
    string? License,
    IReadOnlyList<MaterialMetadataItem>? Materials);

public record PublishMaterialRequest(
    string Title,
    string Type,
    string? Description,
    string License);

public record UpdateMaterialRequest(
    string? Title,
    string? Type,
    string? Description,
    string? License);

public record CoursePublishRequest(
    string CourseId,
    IReadOnlyList<PublishModuleRequest> Modules);

public record ReportRequest(string? Reason);

public record UpsertCurriculumGuideRequest(
    string Title,
    string HtmlContent,
    int? Credits,
    int? ContactHours,
    string? Prerequisites,
    string? Version,
    DateTime? GeneratedUtc);
