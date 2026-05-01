using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using PreseMakerRepo.Core.Interfaces;

namespace PreseMakerRepo.Api.Pages.Browse;

public class Level1Model : PageModel
{
    private readonly ITaxonomyService _taxonomy;
    public Level1Model(ITaxonomyService taxonomy) => _taxonomy = taxonomy;

    public string Level1Key { get; set; } = string.Empty;
    public TaxonomyNodeSummary? Discipline { get; set; }
    public IReadOnlyList<TaxonomyNodeSummary> Children { get; set; } = [];

    public async Task<IActionResult> OnGetAsync(string level1Key)
    {
        Level1Key = level1Key;
        var tree = await _taxonomy.GetFullTreeAsync();
        Discipline = tree.Roots.FirstOrDefault(n => n.Key.Equals(level1Key, StringComparison.OrdinalIgnoreCase));
        if (Discipline is null) return NotFound();
        Children = Discipline.Children;
        return Page();
    }
}
