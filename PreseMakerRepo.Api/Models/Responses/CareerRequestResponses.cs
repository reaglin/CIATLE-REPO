namespace PreseMakerRepo.Api.Models.Responses;

/// <summary>Result of a career-path request: how many people (including this one) want the path.</summary>
public sealed record CareerRequestCreatedResponse(
    string SocCode,
    string SocTitle,
    int RequestCount,
    bool AlreadyRequestedByYou,
    string Message);

/// <summary>
/// One occupation in the public career request queue. Carries nothing about who asked.
/// <see cref="Status"/>: Open · Queued · Published · Declined. <see cref="PathSlug"/> is set once a
/// published path covers the occupation.
/// </summary>
public sealed record PublicCareerQueueItem(
    int Rank,
    string SocCode,
    string SocTitle,
    IReadOnlyList<string> CipCodes,
    int RequestCount,
    DateTime FirstRequestedUtc,
    DateTime LastRequestedUtc,
    string Status,
    string? PathSlug,
    /// <summary>A reason shown to visitors, typically why a request was declined. Null when none was given.</summary>
    string? PublicNote);

/// <summary>The public queue for one filter, with the size of each filter for the page tabs.</summary>
public sealed record PublicCareerQueueResponse(
    string Filter,
    int Waiting,
    int Published,
    int Declined,
    IReadOnlyList<PublicCareerQueueItem> Items);

/// <summary>One occupation's requests, grouped — the admin ranking and the Tools session's input.</summary>
public sealed record CareerRequestSummaryResponse(
    string SocCode,
    string SocTitle,
    IReadOnlyList<string> CipCodes,
    int RequestCount,
    DateTime FirstRequestedUtc,
    DateTime LastRequestedUtc,
    string Status,
    string? PathSlug,
    IReadOnlyList<string> Reasons,
    string? AdminNotes,
    string? PublicNote);

/// <summary>An occupation listed under a CIP group, as the area page and the API show it.</summary>
public sealed record CipOccupationResponse(
    string CipCode,
    string SocCode,
    string SocTitle,
    bool IsHidden,
    string? PathSlug,
    int WaitingRequests);
