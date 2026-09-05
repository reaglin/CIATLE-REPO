using PreseMakerRepo.Core.Enums;

namespace PreseMakerRepo.Core.Models;

/// <summary>
/// A visitor's request for a curriculum guide that does not exist yet. Requests are the
/// demand signal that drives the content queue: the admin console ranks courses by request
/// count, and the queue tool pulls open requests into <c>Tools/queue.csv</c>.
/// One row per request; the same course requested by several people yields several rows
/// (deduplicated per requester per day). The reporter IP is stored as a salted SHA-256
/// hash only, like <see cref="ContentFlag"/>.
/// </summary>
public class GuideRequest
{
    public Guid Id { get; set; }

    /// <summary>Normalized SCNS course id (uppercase, no spaces), e.g. "EET2325C".</summary>
    public string CourseId { get; set; } = string.Empty;

    /// <summary>Course title as the requester knows it (from the taxonomy when the course is known).</summary>
    public string CourseTitle { get; set; } = string.Empty;

    /// <summary>The school where the course is offered.</summary>
    public string Institution { get; set; } = string.Empty;

    /// <summary>Optional free text: why the guide is wanted, catalog URL, etc.</summary>
    public string? Reason { get; set; }

    /// <summary>Optional — to be told when the guide is published. Never shown publicly.</summary>
    public string? RequesterEmail { get; set; }

    /// <summary>Salted SHA-256 of the requester's IP; never the raw address.</summary>
    public string? RequesterIpHash { get; set; }

    /// <summary>Signed-in contributor who made the request, if any.</summary>
    public string? RequesterUserId { get; set; }

    /// <summary>Whether the course existed in the taxonomy when requested.</summary>
    public bool IsInTaxonomy { get; set; }

    public DateTime RequestedUtc { get; set; }

    public GuideRequestStatus Status { get; set; } = GuideRequestStatus.Open;

    /// <summary>When the status last changed.</summary>
    public DateTime? StatusUtc { get; set; }

    public string? AdminNotes { get; set; }
}
