using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Memory;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Core.Interfaces;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Infrastructure.Services;

public class TaxonomyService : ITaxonomyService
{
    private static readonly TimeSpan TreeCacheFor = TimeSpan.FromMinutes(10);

    private readonly AppDbContext _db;
    private readonly IMemoryCache _cache;

    public TaxonomyService(AppDbContext db, IMemoryCache cache)
    {
        _db = db;
        _cache = cache;
    }

    /// <summary>
    /// The tree with per-node counts. Every browse page renders it, and with the full course catalog the
    /// counts are grouped over tens of thousands of rows, so it is cached; course and guide writes drop
    /// the entry (<see cref="SiteCache.InvalidateCounts"/>).
    /// </summary>
    public async Task<TaxonomyTree> GetFullTreeAsync() =>
        (await _cache.GetOrCreateAsync(SiteCache.TaxonomyTreeKey, entry =>
        {
            entry.AbsoluteExpirationRelativeToNow = TreeCacheFor;
            return BuildTreeAsync();
        }))!;

    private async Task<TaxonomyTree> BuildTreeAsync()
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

        // Courses listed per leaf: every active course, plus any course that still has a guide or
        // published modules. The same predicate as CourseDirectory and SiteStatsService, so a leaf's
        // count, its course list and the header total agree.
        var courseCountByLeaf = await _db.TaxonomyCourses
            .AsNoTracking()
            .Where(c => c.Level3Key != null &&
                        (c.IsActive ||
                         _db.CurriculumGuides.Any(g => g.CourseId == c.CourseId && g.Title != CurriculumGuide.StubTitle) ||
                         _db.Modules.Any(m => m.CourseId == c.CourseId && m.Status == ContentStatus.Published)))
            .GroupBy(c => c.Level3Key!)
            .Select(g => new { Key = g.Key, Count = g.Count() })
            .ToDictionaryAsync(x => x.Key, x => x.Count);

        // Published curriculum guides per leaf (module stubs are not guides).
        var guideCountByLeaf = await _db.CurriculumGuides
            .AsNoTracking()
            .Where(g => g.Title != CurriculumGuide.StubTitle)
            .Join(_db.TaxonomyCourses.Where(c => c.Level3Key != null),
                  g => g.CourseId,
                  c => c.CourseId,
                  (_, c) => c.Level3Key!)
            .GroupBy(k => k)
            .Select(g => new { Key = g.Key, Count = g.Count() })
            .ToDictionaryAsync(x => x.Key, x => x.Count);

        var counts = new LeafCounts(moduleCountByLeaf, courseCountByLeaf, guideCountByLeaf);
        var roots = nodes.Values
            .Where(n => n.Level == 1)
            .OrderBy(n => n.Name)
            .Select(n => BuildSummary(n, nodes, counts))
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
            .Where(c => c.Level3Key == level3Key.ToUpper() && c.IsActive)
            .OrderBy(c => c.CourseId)
            .ToListAsync();

    private sealed record LeafCounts(
        Dictionary<string, int> Modules,
        Dictionary<string, int> Courses,
        Dictionary<string, int> Guides);

    private static TaxonomyNodeSummary BuildSummary(
        TaxonomyNode node,
        Dictionary<string, TaxonomyNode> allNodes,
        LeafCounts counts)
    {
        var children = allNodes.Values
            .Where(n => n.ParentKey == node.Key)
            .OrderBy(n => n.Name)
            .Select(n => BuildSummary(n, allNodes, counts))
            .ToList();

        bool isLeaf = !children.Any();
        var moduleCount = isLeaf ? counts.Modules.GetValueOrDefault(node.Key, 0) : children.Sum(c => c.ModuleCount);
        var courseCount = isLeaf ? counts.Courses.GetValueOrDefault(node.Key, 0) : children.Sum(c => c.CourseCount);
        var guideCount = isLeaf ? counts.Guides.GetValueOrDefault(node.Key, 0) : children.Sum(c => c.GuideCount);

        return new TaxonomyNodeSummary(node.Key, node.Name, node.Level, courseCount, moduleCount, guideCount, children);
    }
}
