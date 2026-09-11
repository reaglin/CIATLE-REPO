using PreseMakerRepo.Core.Enums;

namespace PreseMakerRepo.Core.Models;

/// <summary>
/// A reviewed website or video listed for one course. A link is lightweight, so the same URL may be listed
/// for many courses — each listing has its own title, summary and status, and editing or removing one
/// never touches the others (Ron, 2026-09-11). Resources may be free, or products a vendor suggested; the
/// reviewer's summary says which.
/// </summary>
public class CourseResource
{
    public Guid Id { get; set; }

    public string CourseId { get; set; } = string.Empty;
    public TaxonomyCourse Course { get; set; } = null!;

    public ResourceType Type { get; set; }

    /// <summary>Normalised URL (lowercase scheme and host, no fragment or tracking parameters;
    /// YouTube as https://www.youtube.com/watch?v=ID). Unique per course.</summary>
    public string Url { get; set; } = string.Empty;

    /// <summary>The 11-character video id, for YouTube resources.</summary>
    public string? YouTubeVideoId { get; set; }

    /// <summary>Written by the reviewer.</summary>
    public string Title { get; set; } = string.Empty;

    /// <summary>Plain-text summary written by the reviewing AI for this course — what the resource is, how it
    /// helps here, and whether it is free or a commercial product. Shown with an "AI-written" label.</summary>
    public string Summary { get; set; } = string.Empty;

    public ResourceStatus Status { get; set; } = ResourceStatus.Active;

    /// <summary>Thumbs-up count for this course's listing; kept in step with <see cref="Votes"/>.</summary>
    public int HelpfulCount { get; set; }

    public ICollection<CourseResourceVote> Votes { get; set; } = new List<CourseResourceVote>();

    public ResourceLinkSource Source { get; set; }

    /// <summary>The visitor suggestion this listing came from, for the course it was suggested for.</summary>
    public Guid? SubmissionId { get; set; }

    public DateTime CreatedUtc { get; set; }
    public DateTime UpdatedUtc { get; set; }
}
