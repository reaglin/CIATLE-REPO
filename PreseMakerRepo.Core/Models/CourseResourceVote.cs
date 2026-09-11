namespace PreseMakerRepo.Core.Models;

/// <summary>
/// One visitor's thumbs-up on one course's listing of a resource. Anonymous: the voter is a salted
/// SHA-256 hash of their IP, as for guide requests and content flags, so a vote can be taken back but a
/// voter is never identified. Votes are per listing, so the same link can rank differently on the courses
/// it is listed for (Ron, 2026-09-11: let quality sort itself out instead of capping resources per course).
/// </summary>
public class CourseResourceVote
{
    public Guid CourseResourceId { get; set; }
    public CourseResource CourseResource { get; set; } = null!;

    /// <summary>Salted SHA-256 of the voter's IP; never the raw address.</summary>
    public string VoterHash { get; set; } = string.Empty;

    public DateTime CreatedUtc { get; set; }
}
