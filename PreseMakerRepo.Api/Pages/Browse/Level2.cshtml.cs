using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using PreseMakerRepo.Core.Interfaces;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Api.Pages.Browse;

public class Level2Model : PageModel
{
    private readonly ITaxonomyService _taxonomy;
    public Level2Model(ITaxonomyService taxonomy) => _taxonomy = taxonomy;

    public string Level1Key { get; set; } = string.Empty;
    public string Level2Key { get; set; } = string.Empty;
    public TaxonomyNodeSummary? Discipline { get; set; }
    public TaxonomyNodeSummary? Prefix { get; set; }

    // Populated when prefix is a leaf (no Level 3 children) — standard for SCNS
    public IReadOnlyList<TaxonomyCourse> Courses { get; set; } = [];
    // Populated when prefix has Level 3 children (3-level taxonomies)
    public IReadOnlyList<TaxonomyNodeSummary> Level3Nodes { get; set; } = [];
    public bool IsLeaf { get; set; }

    public async Task<IActionResult> OnGetAsync(string level1Key, string level2Key)
    {
        Level1Key = level1Key;
        Level2Key = level2Key;

        var tree = await _taxonomy.GetFullTreeAsync();
        Discipline = tree.Roots.FirstOrDefault(n => n.Key.Equals(level1Key, StringComparison.OrdinalIgnoreCase));
        if (Discipline is null) return NotFound();

        Prefix = Discipline.Children.FirstOrDefault(n => n.Key.Equals(level2Key, StringComparison.OrdinalIgnoreCase));
        if (Prefix is null) return NotFound();

        IsLeaf = !Prefix.Children.Any();

        if (IsLeaf)
            Courses = await _taxonomy.GetCoursesByLevel3Async(level2Key);
        else
            Level3Nodes = Prefix.Children;

        return Page();
    }
}
