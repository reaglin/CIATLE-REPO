using PreseMakerRepo.Core.Enums;

namespace PreseMakerRepo.Core.Models;

public class Module
{
    public Guid Id { get; set; }

    public string ContributorId { get; set; } = string.Empty;
    public Contributor Contributor { get; set; } = null!;

    public string CourseId { get; set; } = string.Empty;
    public TaxonomyCourse Course { get; set; } = null!;

    public string Title { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;

    // JSON array of outcome strings: ["Students will be able to..."]
    public string OutcomesJson { get; set; } = "[]";

    // JSON array of topic objects: [{"topic":"...","elements":["..."]}]
    public string TopicHierarchyJson { get; set; } = "[]";

    public LicenseType License { get; set; }
    public ContentStatus Status { get; set; }

    public DateTime SubmittedUtc { get; set; }
    public DateTime? UpdatedUtc { get; set; }
    public DateTime? RemovedUtc { get; set; }

    public long TotalStorageBytes { get; set; }

    public ICollection<Material> Materials { get; set; } = new List<Material>();
    public ICollection<ContentFlag> Flags { get; set; } = new List<ContentFlag>();
}
