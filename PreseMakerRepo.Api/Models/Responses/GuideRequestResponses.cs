namespace PreseMakerRepo.Api.Models.Responses;

/// <summary>Result of creating a request: how many people (including this one) want the guide.</summary>
public sealed record GuideRequestCreatedResponse(
    string CourseId,
    int RequestCount,
    bool AlreadyRequestedByYou,
    string Message);

/// <summary>
/// One course in the public guide request queue. Carries nothing about who asked — no schools typed by
/// requesters, reasons, notes or hashes. <see cref="Status"/>: Open · Queued · Published · Declined.
/// </summary>
public sealed record PublicGuideQueueItem(
    int Rank,
    string CourseId,
    string Title,
    int RequestCount,
    DateTime FirstRequestedUtc,
    DateTime LastRequestedUtc,
    string Status,
    bool HasGuide,
    bool IsListed);

/// <summary>The public queue for one filter, with the size of each filter for the page tabs.</summary>
public sealed record PublicGuideQueueResponse(
    string Filter,
    int Waiting,
    int Published,
    int Declined,
    IReadOnlyList<PublicGuideQueueItem> Items);

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
