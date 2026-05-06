using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Core.Interfaces;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Api.Pages.Browse;

public class Level1Model : PageModel
{
    private readonly ITaxonomyService _taxonomy;
    private readonly AppDbContext _db;

    public Level1Model(ITaxonomyService taxonomy, AppDbContext db)
    {
        _taxonomy = taxonomy;
        _db = db;
    }

    public string Level1Key { get; set; } = string.Empty;
    public TaxonomyNodeSummary? Discipline { get; set; }
    public IReadOnlyList<TaxonomyNodeSummary> Children { get; set; } = [];
    public string? Description { get; set; }

    public async Task<IActionResult> OnGetAsync(string level1Key)
    {
        Level1Key = level1Key;
        var tree = await _taxonomy.GetFullTreeAsync();
        Discipline = tree.Roots.FirstOrDefault(n => n.Key.Equals(level1Key, StringComparison.OrdinalIgnoreCase));
        if (Discipline is null) return NotFound();
        Children = Discipline.Children;

        var desc = await _db.TaxonomyNodeDescriptions
            .AsNoTracking()
            .FirstOrDefaultAsync(d => d.NodeKey == Discipline.Key);
        Description = desc?.HtmlContent;

        return Page();
    }
}
