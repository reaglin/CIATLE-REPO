using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Core.Interfaces;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Api.Pages.Browse;

public class Level2Model : PageModel
{
    private readonly ITaxonomyService _taxonomy;
    private readonly AppDbContext _db;

    public Level2Model(ITaxonomyService taxonomy, AppDbContext db)
    {
        _taxonomy = taxonomy;
        _db = db;
    }

    public string Level1Key { get; set; } = string.Empty;
    public string Level2Key { get; set; } = string.Empty;
    public TaxonomyNodeSummary? Discipline { get; set; }
    public TaxonomyNodeSummary? Prefix { get; set; }

    // Populated when prefix is a leaf (no Level 3 children) — standard for SCNS
    // Only courses with published modules or a curriculum guide are included.
    public IReadOnlyList<TaxonomyCourse> Courses { get; set; } = [];
    // Populated when prefix has Level 3 children (3-level taxonomies)
    public IReadOnlyList<TaxonomyNodeSummary> Level3Nodes { get; set; } = [];
    public bool IsLeaf { get; set; }
    public HashSet<string> CourseIdsWithGuides { get; set; } = [];

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
        {
            var normalizedKey = level2Key.ToUpperInvariant();

            var courseIdsWithModules = (await _db.Modules
                .AsNoTracking()
                .Where(m => m.Status == ContentStatus.Published &&
                            _db.TaxonomyCourses.Any(c => c.CourseId == m.CourseId && c.Level3Key == normalizedKey))
                .Select(m => m.CourseId)
                .Distinct()
                .ToListAsync()).ToHashSet();

            CourseIdsWithGuides = (await _db.CurriculumGuides
                .AsNoTracking()
                .Where(g => _db.TaxonomyCourses.Any(c => c.CourseId == g.CourseId && c.Level3Key == normalizedKey))
                .Select(g => g.CourseId)
                .ToListAsync()).ToHashSet();

            var allCourses = await _taxonomy.GetCoursesByLevel3Async(level2Key);
            Courses = allCourses
                .Where(c => courseIdsWithModules.Contains(c.CourseId) || CourseIdsWithGuides.Contains(c.CourseId))
                .ToList();
        }
        else
        {
            Level3Nodes = Prefix.Children;
        }

        return Page();
    }
}
