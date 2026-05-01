using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using PreseMakerRepo.Core.Interfaces;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Api.Pages.Browse;

public class Level3Model : PageModel
{
    private readonly ITaxonomyService _taxonomy;
    public Level3Model(ITaxonomyService taxonomy) => _taxonomy = taxonomy;

    public string Level1Key { get; set; } = string.Empty;
    public string Level2Key { get; set; } = string.Empty;
    public string Level3Key { get; set; } = string.Empty;
    public TaxonomyNodeSummary? Discipline { get; set; }
    public TaxonomyNodeSummary? Prefix { get; set; }
    public TaxonomyNodeSummary? Subject { get; set; }
    public IReadOnlyList<TaxonomyCourse> Courses { get; set; } = [];

    public async Task<IActionResult> OnGetAsync(string level1Key, string level2Key, string level3Key)
    {
        Level1Key = level1Key;
        Level2Key = level2Key;
        Level3Key = level3Key;

        var tree = await _taxonomy.GetFullTreeAsync();
        Discipline = tree.Roots.FirstOrDefault(n => n.Key.Equals(level1Key, StringComparison.OrdinalIgnoreCase));
        if (Discipline is null) return NotFound();

        Prefix = Discipline.Children.FirstOrDefault(n => n.Key.Equals(level2Key, StringComparison.OrdinalIgnoreCase));
        if (Prefix is null) return NotFound();

        Subject = Prefix.Children.FirstOrDefault(n => n.Key.Equals(level3Key, StringComparison.OrdinalIgnoreCase));
        if (Subject is null) return NotFound();

        Courses = await _taxonomy.GetCoursesByLevel3Async(level3Key);
        return Page();
    }
}
