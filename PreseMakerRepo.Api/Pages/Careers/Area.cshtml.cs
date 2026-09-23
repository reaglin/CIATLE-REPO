using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Api.Models.Responses;
using PreseMakerRepo.Api.Services;
using PreseMakerRepo.Core.Enums;
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
    private readonly CareerRequestService _requests;

    public AreaModel(AppDbContext db, CareerRequestService requests)
    {
        _db = db;
        _requests = requests;
    }

    public sealed record ChildView(string Code, string Title, string? Examples, int PathCount);
    /// <param name="Note">Why the path is filed here, when this is not its primary node.</param>
    public sealed record PathView(string Slug, string Name, string Description, string? SocCode,
                                  bool IsPrimary, string? Note);

    public CipNode Node { get; set; } = null!;
    public CipNode? Parent { get; set; }
    public IReadOnlyList<ChildView> Children { get; set; } = [];
    public IReadOnlyList<PathView> Paths { get; set; } = [];

    /// <summary>
    /// Occupations this group leads to (NCES CIP–SOC crosswalk) that have no path yet — each with
    /// a Request button. Empty on a 2-digit series page, where occupations are listed per group.
    /// </summary>
    public IReadOnlyList<CipOccupationResponse> Requestable { get; set; } = [];

    /// <summary>Occupations a published path covers, where that path is not already listed above.</summary>
    public IReadOnlyList<CipOccupationResponse> CoveredElsewhere { get; set; } = [];
    public IReadOnlyDictionary<string, string> PathNames { get; set; } = new Dictionary<string, string>();

    /// <summary>How many crosswalk occupations this group has at all, hidden ones excluded -- tells the
    /// empty state apart: "all already have a path" versus "the federal list links none here".</summary>
    public int OccupationCount { get; set; }

    /// <summary>The confirmation or problem from the last Request press, shown beside the list.</summary>
    [TempData] public string? RequestMessage { get; set; }
    [TempData] public bool RequestOk { get; set; }
    [TempData] public string? RequestedSoc { get; set; }

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
            // A path counts under a child if that child is its primary OR one of its
            // additional anchors -- a law path is real on the political-science page.
            var byPrimary = await _db.CareerPaths.AsNoTracking()
                .Where(p => p.IsPublished && codes.Contains(p.CipCode))
                .Select(p => new { p.CipCode, p.Slug }).ToListAsync();
            var byLink = await _db.CareerPathCips.AsNoTracking()
                .Where(c => c.CareerPath!.IsPublished && codes.Contains(c.CipCode))
                .Select(c => new { c.CipCode, c.CareerPath!.Slug }).ToListAsync();

            var counts = byPrimary.Concat(byLink)
                .GroupBy(x => x.CipCode)
                .ToDictionary(g => g.Key, g => g.Select(x => x.Slug).Distinct().Count());

            Children = kids
                .Select(k => new ChildView(k.Code, k.Title, k.Examples,
                                           counts.TryGetValue(k.Code, out var c) ? c : 0))
                .ToList();
        }

        // Paths are filed on a group, but list a series' whole subtree on the series page
        // so a visitor landing one level up still sees what exists below.
        var primary = await _db.CareerPaths.AsNoTracking()
            .Where(p => p.IsPublished && (p.CipCode == node.Code || p.CipCode.StartsWith(node.Code + ".")))
            .OrderBy(p => p.SortOrder).ThenBy(p => p.Name)
            .Select(p => new PathView(p.Slug, p.Name, p.Description, p.SocCode, true, null))
            .ToListAsync();

        // ⚠ The additional anchors are the whole point of the link table: a student browsing
        // Political Science must find Lawyer, whose primary node is Law. The note travels with
        // it so the page can say WHY it is listed here rather than just listing it.
        var linked = await _db.CareerPathCips.AsNoTracking()
            .Where(c => c.CareerPath!.IsPublished
                        && (c.CipCode == node.Code || c.CipCode.StartsWith(node.Code + ".")))
            .OrderBy(c => c.CareerPath!.SortOrder).ThenBy(c => c.CareerPath!.Name)
            .Select(c => new PathView(c.CareerPath!.Slug, c.CareerPath.Name, c.CareerPath.Description,
                                      c.CareerPath.SocCode, false, c.Note))
            .ToListAsync();

        var seen = primary.Select(x => x.Slug).ToHashSet();
        Paths = primary.Concat(linked.Where(x => seen.Add(x.Slug))).ToList();

        if (node.Level == 4)
        {
            var occ = await _requests.OccupationsAsync([node.Code]);
            var listed = Paths.Select(p => p.Slug).ToHashSet();
            OccupationCount = occ.Count;
            Requestable = occ.Where(o => o.PathSlug is null).ToList();
            CoveredElsewhere = occ.Where(o => o.PathSlug is not null && !listed.Contains(o.PathSlug)).ToList();
            var slugs = CoveredElsewhere.Select(o => o.PathSlug!).Distinct().ToList();
            PathNames = await _db.CareerPaths.AsNoTracking()
                .Where(p => slugs.Contains(p.Slug))
                .ToDictionaryAsync(p => p.Slug, p => p.Name);
        }

        return Page();
    }

    /// <summary>
    /// The one-click Request button. Records the request and comes back to the same place on the
    /// page with a confirmation, so the reader sees the count go up where they pressed.
    /// </summary>
    public async Task<IActionResult> OnPostRequestAsync(string code, string? soc)
    {
        var ip = HttpContext.Connection.RemoteIpAddress?.ToString() ?? "unknown";
        var userId = User.Identity?.IsAuthenticated == true ? User.FindFirst("sub")?.Value : null;

        if (!CareerRequestService.TryNormalizeSoc(soc, out var s) ||
            !CareerRequestService.TryNormalizeCipGroup(code, out var c))
        {
            RequestOk = false;
            RequestMessage = "That request could not be read. Please try the button again.";
            return RedirectToPage(null, null, new { code }, "request-a-path");
        }

        var result = await _requests.CreateAsync(s, c, null, ip, userId, CareerRequestChannel.Button);
        RequestOk = result.Outcome is CareerRequestService.CreateOutcome.Created
                                   or CareerRequestService.CreateOutcome.AlreadyRequested;
        RequestMessage = CareerRequestService.MessageFor(result);
        RequestedSoc = s;
        return RedirectToPage(null, null, new { code }, "request-a-path");
    }
}
