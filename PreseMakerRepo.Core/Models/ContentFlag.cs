namespace PreseMakerRepo.Core.Models;

public class ContentFlag
{
    public Guid Id { get; set; }

    // Exactly one of ModuleId / MaterialId is set per record (enforced by DB check constraint)
    public Guid? ModuleId { get; set; }
    public Module? Module { get; set; }

    public Guid? MaterialId { get; set; }
    public Material? Material { get; set; }

    public string? ReporterIpHash { get; set; }     // SHA-256 + salt; raw IP never stored
    public string? ReporterUserId { get; set; }     // FK if authenticated reporter
    public DateTime FlaggedUtc { get; set; }
    public string? Reason { get; set; }             // Optional free text (max 500 chars)

    public bool IsResolved { get; set; }
    public string? ResolvedByAdminId { get; set; }
    public DateTime? ResolvedUtc { get; set; }
    public string? ResolutionNote { get; set; }
}
