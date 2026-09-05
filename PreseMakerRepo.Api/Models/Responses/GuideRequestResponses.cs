namespace PreseMakerRepo.Api.Models.Responses;

/// <summary>Result of creating a request: how many people (including this one) want the guide.</summary>
public sealed record GuideRequestCreatedResponse(
    string CourseId,
    int RequestCount,
    bool AlreadyRequestedByYou,
    string Message);

/// <summary>One course's requests, grouped — the admin ranking and the queue tool's input.</summary>
public sealed record GuideRequestSummaryResponse(
    string CourseId,
    string CourseTitle,
    IReadOnlyList<string> Institutions,
    int RequestCount,
    DateTime FirstRequestedUtc,
    DateTime LastRequestedUtc,
    string Status,
    bool InTaxonomy,
    bool HasGuide,
    string? AdminNotes);
