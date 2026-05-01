using PreseMakerRepo.Core.Enums;

namespace PreseMakerRepo.Core.Models;

public class Material
{
    public Guid Id { get; set; }

    public Guid ModuleId { get; set; }
    public Module Module { get; set; } = null!;

    public string ContributorId { get; set; } = string.Empty;
    public Contributor Contributor { get; set; } = null!;

    public string Title { get; set; } = string.Empty;
    public string? Description { get; set; }
    public MaterialType Type { get; set; }
    public LicenseType License { get; set; }
    public ContentStatus Status { get; set; }

    public string FileName { get; set; } = string.Empty;       // Original filename
    public string StoragePath { get; set; } = string.Empty;    // Relative path within storage root
    public long FileSizeBytes { get; set; }
    public string ContentType { get; set; } = string.Empty;    // MIME type

    public DateTime SubmittedUtc { get; set; }
    public DateTime? UpdatedUtc { get; set; }
    public DateTime? RemovedUtc { get; set; }

    public ICollection<ContentFlag> Flags { get; set; } = new List<ContentFlag>();
}
