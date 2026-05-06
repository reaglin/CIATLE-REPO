namespace PreseMakerRepo.Core.Models;

public class TaxonomyNodeDescription
{
    public string NodeKey { get; set; } = string.Empty;
    public TaxonomyNode? Node { get; set; }
    public string HtmlContent { get; set; } = string.Empty;
    public DateTime UpdatedUtc { get; set; }
}
