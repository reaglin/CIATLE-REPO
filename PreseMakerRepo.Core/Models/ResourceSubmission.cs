using PreseMakerRepo.Core.Enums;

namespace PreseMakerRepo.Core.Models;

/// <summary>
/// A link a visitor suggested on a course's Resources page — the public review queue. Anonymous; the
/// submitter IP is kept only as a salted SHA-256 hash (rate limiting), like <see cref="ContentFlag"/>.
/// </summary>
public class ResourceSubmission
{
    public Guid Id { get; set; }

    public string CourseId { get; set; } = string.Empty;

    /// <summary>Normalised URL, as on <see cref="Resource.Url"/>.</summary>
    public string Url { get; set; } = string.Empty;

    public ResourceType Type { get; set; }
    public string? YouTubeVideoId { get; set; }

    /// <summary>The submitter's optional note — input for the reviewer; not shown on the course page.</summary>
    public string? Description { get; set; }

    /// <summary>The title the submitter suggests for the listing (optional; the reviewer's Approve form starts from it).</summary>
    public string? SuggestedTitle { get; set; }

    /// <summary>The summary the submitter suggests for the listing (optional; the reviewer edits it before approving).</summary>
    public string? SuggestedSummary { get; set; }

    /// <summary>Other courses the submitter suggests listing it for: course ids, comma-separated (optional).</summary>
    public string? SuggestedAlsoFor { get; set; }

    public ResourceSubmissionStatus Status { get; set; } = ResourceSubmissionStatus.Pending;

    /// <summary>Short, public-safe reason shown in the queue (why it was not added, or a note on approval).</summary>
    public string? DecisionNote { get; set; }

    /// <summary>The listing created (or updated) for the suggested course when the submission was approved.</summary>
    public Guid? CourseResourceId { get; set; }

    public DateTime SubmittedUtc { get; set; }
    public DateTime? DecidedUtc { get; set; }

    public string? SubmitterIpHash { get; set; }
    public string? SubmitterUserId { get; set; }
}
