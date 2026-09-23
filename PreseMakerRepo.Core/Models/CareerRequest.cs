using PreseMakerRepo.Core.Enums;

namespace PreseMakerRepo.Core.Models;

/// <summary>
/// A visitor's request for a career path that does not exist yet — the demand signal that
/// drives career-path writing once the authored queue is finished (Ron, 2026-09-23: "the
/// request driven will follow the same pattern as courses"). Modelled on <see cref="GuideRequest"/>:
/// one row per request, deduplicated per requester per day, IP stored as a salted hash only.
/// A request names an OCCUPATION (SOC code), because that is what a path is written for; the
/// CIP group records which page it was asked from.
/// </summary>
public class CareerRequest
{
    public Guid Id { get; set; }

    /// <summary>SOC 2018 code, e.g. "19-3051".</summary>
    public string SocCode { get; set; } = string.Empty;

    /// <summary>The occupation's SOC title at the time of the request.</summary>
    public string SocTitle { get; set; } = string.Empty;

    /// <summary>The 4-digit CIP group whose page the request came from, e.g. "04.03".</summary>
    public string CipCode { get; set; } = string.Empty;

    /// <summary>Optional free text: why the path is wanted.</summary>
    public string? Reason { get; set; }

    public CareerRequestChannel Channel { get; set; } = CareerRequestChannel.Button;

    /// <summary>Salted SHA-256 of the requester's IP; never the raw address.</summary>
    public string? RequesterIpHash { get; set; }

    /// <summary>Signed-in contributor who made the request, if any.</summary>
    public string? RequesterUserId { get; set; }

    public DateTime RequestedUtc { get; set; }

    public CareerRequestStatus Status { get; set; } = CareerRequestStatus.Open;

    /// <summary>When the status last changed.</summary>
    public DateTime? StatusUtc { get; set; }

    public string? AdminNotes { get; set; }
}
