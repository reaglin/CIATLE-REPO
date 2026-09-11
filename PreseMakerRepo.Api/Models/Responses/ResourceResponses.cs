namespace PreseMakerRepo.Api.Models.Responses;

/// <summary>
/// One course's listing of a resource. <see cref="AlsoForCourseIds"/>: other courses where the same link is
/// listed (each with its own title and summary). Status: Active · Removed. Source: Submitted · Reviewer.
/// </summary>
public sealed record CourseResourceDto(
    Guid Id,
    string CourseId,
    string Type,
    string Url,
    string? YouTubeVideoId,
    string Title,
    string Summary,
    string Host,
    string Status,
    string Source,
    int HelpfulCount,
    IReadOnlyList<string> AlsoForCourseIds,
    DateTime CreatedUtc,
    DateTime UpdatedUtc);

/// <summary>Result of a thumbs-up: the listing's new count, and whether this visitor's vote now stands.</summary>
public sealed record ResourceVoteResponse(Guid ResourceId, int HelpfulCount, bool Voted);

/// <summary>Result of a visitor's suggestion: submitted · alreadySubmitted · alreadyListed · recentlyRejected.</summary>
public sealed record ResourceSubmittedResponse(Guid? SubmissionId, string Outcome, string Message);

/// <summary>One suggestion in the public review queue. The URL is data for the reviewer; the page shows it unlinked.
/// The description is the submitter's note — input for the reviewer.</summary>
public sealed record ResourceQueueItem(
    Guid Id,
    string CourseId,
    string CourseTitle,
    string Url,
    string Type,
    string Host,
    string? Description,
    string Status,
    DateTime SubmittedUtc,
    DateTime? DecidedUtc,
    string? DecisionNote,
    Guid? CourseResourceId);

public sealed record ResourceQueueResponse(
    string Filter,
    int Pending,
    int DecidedRecently,
    IReadOnlyList<ResourceQueueItem> Items);

/// <summary>What happened on one course: created · updated · unknownCourse (not listed on the site; nothing written).</summary>
public sealed record ResourceWriteResult(string CourseId, string Outcome, Guid? ResourceId);

/// <summary>Result of approving or rejecting a suggestion.</summary>
public sealed record ResourceDecisionResponse(
    Guid SubmissionId,
    string Status,
    IReadOnlyList<ResourceWriteResult> Results,
    string Message);

/// <summary>Result of listing a link directly.</summary>
public sealed record ResourceCreateResponse(string Url, string Type, IReadOnlyList<ResourceWriteResult> Results);
