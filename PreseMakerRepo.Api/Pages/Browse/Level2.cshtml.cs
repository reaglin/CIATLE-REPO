using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Api.Services;
using PreseMakerRepo.Core.Interfaces;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Api.Pages.Browse;

public class Level2Model : PageModel
{
    private readonly ITaxonomyService _taxonomy;
    private readonly AppDbContext _db;
    private readonly CourseDirectory _directory;

    public Level2Model(ITaxonomyService taxonomy, AppDbContext db, CourseDirectory directory)
    {
        _taxonomy = taxonomy;
        _db = db;
        _directory = directory;
    }

    /// <summary>all · guides · noguide</summary>
    [BindProperty(SupportsGet = true)] public string? Show { get; set; }

    public string Level1Key { get; set; } = string.Empty;
    public string Level2Key { get; set; } = string.Empty;
    public TaxonomyNodeSummary? Discipline { get; set; }
    public TaxonomyNodeSummary? Prefix { get; set; }

    // Populated when prefix is a leaf (no Level 3 children) — standard for SCNS.
    // Every listed course is included, with or without a guide.
    public CourseListView? CourseList { get; set; }
    // Populated when prefix has Level 3 children (3-level taxonomies)
    public IReadOnlyList<TaxonomyNodeSummary> Level3Nodes { get; set; } = [];
    public bool IsLeaf { get; set; }
    public string? Description { get; set; }

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
            CourseList = CourseListView.For(await _directory.ForLeafAsync(level2Key), Show);
        else
            Level3Nodes = Prefix.Children;

        var desc = await _db.TaxonomyNodeDescriptions
            .AsNoTracking()
            .FirstOrDefaultAsync(d => d.NodeKey == Prefix.Key);
        Description = desc?.HtmlContent;

        return Page();
    }
}
