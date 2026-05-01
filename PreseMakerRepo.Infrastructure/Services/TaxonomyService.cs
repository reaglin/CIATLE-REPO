using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Core.Interfaces;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Infrastructure.Services;

public class TaxonomyService : ITaxonomyService
{
    private readonly AppDbContext _db;

    public TaxonomyService(AppDbContext db) => _db = db;

    public async Task<TaxonomyTree> GetFullTreeAsync()
    {
        var nodes = await _db.TaxonomyNodes.AsNoTracking().ToDictionaryAsync(n => n.Key);

        // Count published modules per leaf taxonomy key via course membership
        var moduleCountByLeaf = await _db.Modules
            .AsNoTracking()
            .Where(m => m.Status == ContentStatus.Published)
            .Join(_db.TaxonomyCourses.Where(c => c.Level3Key != null),
                  m => m.CourseId,
                  c => c.CourseId,
                  (_, c) => c.Level3Key!)
            .GroupBy(k => k)
            .Select(g => new { Key = g.Key, Count = g.Count() })
            .ToDictionaryAsync(x => x.Key, x => x.Count);

        // Count distinct courses with at least one published module per leaf taxonomy key
        var courseCountByLeaf = await _db.TaxonomyCourses
            .AsNoTracking()
            .Where(c => c.Level3Key != null &&
                        _db.Modules.Any(m => m.CourseId == c.CourseId && m.Status == ContentStatus.Published))
            .GroupBy(c => c.Level3Key!)
            .Select(g => new { Key = g.Key, Count = g.Count() })
            .ToDictionaryAsync(x => x.Key, x => x.Count);

        var roots = nodes.Values
            .Where(n => n.Level == 1)
            .OrderBy(n => n.Name)
            .Select(n => BuildSummary(n, nodes, moduleCountByLeaf, courseCountByLeaf))
            .ToList();

        return new TaxonomyTree(roots);
    }

    public async Task<TaxonomyNode?> GetNodeAsync(string key) =>
        await _db.TaxonomyNodes
            .AsNoTracking()
            .Include(n => n.Children)
            .FirstOrDefaultAsync(n => n.Key == key);

    public async Task<TaxonomyCourseValidationResult> ValidateCourseIdAsync(string courseId)
    {
        var normalized = courseId.ToUpperInvariant();
        var course = await _db.TaxonomyCourses
            .AsNoTracking()
            .Include(c => c.Level3Node)
                .ThenInclude(n => n!.Parent)
                    .ThenInclude(n => n!.Parent)
            .FirstOrDefaultAsync(c => c.CourseId == normalized);

        if (course is null)
            return new TaxonomyCourseValidationResult(false, normalized, null, null, null, "Course ID not found");

        TaxonomyPath? path = null;
        if (course.Level3Node is not null)
        {
            var l3 = course.Level3Node;
            var l2 = l3.Parent;
            var l1 = l2?.Parent;
            path = new TaxonomyPath(l1?.Key, l1?.Name, l2?.Key, l2?.Name, l3.Key, l3.Name);
        }

        return new TaxonomyCourseValidationResult(true, normalized, course.Title, path, course.CurriculumGuideUrl, null);
    }

    public async Task<TaxonomyCourse?> GetCourseAsync(string courseId) =>
        await _db.TaxonomyCourses.FindAsync(courseId.ToUpperInvariant());

    public async Task<IReadOnlyList<TaxonomyCourse>> GetCoursesByLevel3Async(string level3Key) =>
        await _db.TaxonomyCourses
            .AsNoTracking()
            .Where(c => c.Level3Key == level3Key && c.IsActive)
            .OrderBy(c => c.CourseId)
            .ToListAsync();

    private static TaxonomyNodeSummary BuildSummary(
        TaxonomyNode node,
        Dictionary<string, TaxonomyNode> allNodes,
        Dictionary<string, int> moduleCountByLeaf,
        Dictionary<string, int> courseCountByLeaf)
    {
        var children = allNodes.Values
            .Where(n => n.ParentKey == node.Key)
            .OrderBy(n => n.Name)
            .Select(n => BuildSummary(n, allNodes, moduleCountByLeaf, courseCountByLeaf))
            .ToList();

        bool isLeaf = !children.Any();
        var moduleCount = isLeaf
            ? moduleCountByLeaf.GetValueOrDefault(node.Key, 0)
            : children.Sum(c => c.ModuleCount);
        var courseCount = isLeaf
            ? courseCountByLeaf.GetValueOrDefault(node.Key, 0)
            : children.Sum(c => c.CourseCount);

        return new TaxonomyNodeSummary(node.Key, node.Name, node.Level, courseCount, moduleCount, children);
    }
}
