using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Api.Pages.Careers;

/// <summary>
/// One CIP node. Serves both levels: a 2-digit series lists its 4-digit groups, a 4-digit
/// group shows the federal definition and the paths filed under it. One page rather than
/// two because the shape is the same and the tree is only two deep.
/// </summary>
public class AreaModel : PageModel
{
    private readonly AppDbContext _db;
    public AreaModel(AppDbContext db) => _db = db;

    public sealed record ChildView(string Code, string Title, string? Examples, int PathCount);
    public sealed record PathView(string Slug, string Name, string Description, string? SocCode);

    public CipNode Node { get; set; } = null!;
    public CipNode? Parent { get; set; }
    public IReadOnlyList<ChildView> Children { get; set; } = [];
    public IReadOnlyList<PathView> Paths { get; set; } = [];

    public async Task<IActionResult> OnGetAsync(string code)
    {
        code = (code ?? string.Empty).Trim();

        var node = await _db.CipNodes.AsNoTracking()
            .FirstOrDefaultAsync(n => n.Code == code && n.IsActive);
        if (node is null) return NotFound();
        Node = node;

        if (node.ParentCode is not null)
        {
            Parent = await _db.CipNodes.AsNoTracking()
                .FirstOrDefaultAsync(n => n.Code == node.ParentCode);
        }

        var kids = await _db.CipNodes.AsNoTracking()
            .Where(n => n.ParentCode == node.Code && n.IsActive)
            .OrderBy(n => n.Code)
            .Select(n => new { n.Code, n.Title, n.Examples })
            .ToListAsync();

        if (kids.Count > 0)
        {
            var codes = kids.Select(k => k.Code).ToList();
            var counts = await _db.CareerPaths.AsNoTracking()
                .Where(p => p.IsPublished && codes.Contains(p.CipCode))
                .GroupBy(p => p.CipCode)
                .Select(g => new { g.Key, Count = g.Count() })
                .ToDictionaryAsync(g => g.Key, g => g.Count);

            Children = kids
                .Select(k => new ChildView(k.Code, k.Title, k.Examples,
                                           counts.TryGetValue(k.Code, out var c) ? c : 0))
                .ToList();
        }

        // Paths are filed on a group, but list a series' whole subtree on the series page
        // so a visitor landing one level up still sees what exists below.
        Paths = await _db.CareerPaths.AsNoTracking()
            .Where(p => p.IsPublished && (p.CipCode == node.Code || p.CipCode.StartsWith(node.Code + ".")))
            .OrderBy(p => p.SortOrder).ThenBy(p => p.Name)
            .Select(p => new PathView(p.Slug, p.Name, p.Description, p.SocCode))
            .ToListAsync();

        return Page();
    }
}
