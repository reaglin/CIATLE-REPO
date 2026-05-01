namespace PreseMakerRepo.Core.Models;

public class TaxonomyNode
{
    public string Key { get; set; } = string.Empty;    // PK — unique across all levels
    public int Level { get; set; }                      // 1, 2, or 3
    public string Name { get; set; } = string.Empty;

    public string? ParentKey { get; set; }
    public TaxonomyNode? Parent { get; set; }

    public ICollection<TaxonomyNode> Children { get; set; } = new List<TaxonomyNode>();
    public ICollection<TaxonomyCourse> Courses { get; set; } = new List<TaxonomyCourse>();
}
