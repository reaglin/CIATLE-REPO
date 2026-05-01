using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Core.Interfaces;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Api.Areas.Admin.Pages;

public class FlaggedModel : PageModel
{
    private readonly AppDbContext _db;
    private readonly IEmailService _email;
    private readonly UserManager<Contributor> _userManager;

    public FlaggedModel(AppDbContext db, IEmailService email, UserManager<Contributor> userManager)
    {
        _db = db;
        _email = email;
        _userManager = userManager;
    }

    public record FlaggedItem(string ContentType, Guid ContentId, string? CourseId, string Title,
        string ContributorUsername, string? ContributorEmail, DateTime MostRecentFlagUtc,
        string? FlagReason, int FlagCount);

    public IReadOnlyList<FlaggedItem> Items { get; set; } = [];

    public async Task OnGetAsync()
    {
        var flags = await _db.ContentFlags.AsNoTracking()
            .Where(f => !f.IsResolved)
            .Include(f => f.Module).ThenInclude(m => m!.Contributor)
            .Include(f => f.Module).ThenInclude(m => m!.Course)
            .Include(f => f.Material).ThenInclude(m => m!.Contributor)
            .Include(f => f.Material).ThenInclude(m => m!.Module).ThenInclude(mod => mod.Course)
            .ToListAsync();

        var items = new List<FlaggedItem>();

        foreach (var g in flags.Where(f => f.ModuleId.HasValue && f.Module is not null)
                               .GroupBy(f => f.ModuleId!.Value))
        {
            var rep = g.OrderByDescending(f => f.FlaggedUtc).First();
            var m = rep.Module!;
            items.Add(new FlaggedItem("module", m.Id, m.CourseId, m.Title,
                m.Contributor.UserName!, m.Contributor.Email,
                rep.FlaggedUtc, rep.Reason, g.Count()));
        }

        foreach (var g in flags.Where(f => f.MaterialId.HasValue && f.Material is not null)
                               .GroupBy(f => f.MaterialId!.Value))
        {
            var rep = g.OrderByDescending(f => f.FlaggedUtc).First();
            var mat = rep.Material!;
            items.Add(new FlaggedItem("material", mat.Id, mat.Module?.Course?.CourseId, mat.Title,
                mat.Contributor.UserName!, mat.Contributor.Email,
                rep.FlaggedUtc, rep.Reason, g.Count()));
        }

        Items = items.OrderByDescending(i => i.MostRecentFlagUtc).ToList();
    }

    public async Task<IActionResult> OnPostClearModuleAsync(Guid id, string? note)
    {
        var module = await _db.Modules.FirstOrDefaultAsync(m => m.Id == id);
        if (module is null) return NotFound();

        var adminId = User.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)?.Value;
        var now = DateTime.UtcNow;
        await _db.ContentFlags.Where(f => f.ModuleId == id && !f.IsResolved)
            .ExecuteUpdateAsync(s => s
                .SetProperty(f => f.IsResolved, true)
                .SetProperty(f => f.ResolvedByAdminId, adminId)
                .SetProperty(f => f.ResolvedUtc, now)
                .SetProperty(f => f.ResolutionNote, note));

        if (module.Status == ContentStatus.Flagged)
        {
            module.Status = ContentStatus.Published;
            await _db.SaveChangesAsync();
        }

        TempData["Success"] = "Flag cleared.";
        return RedirectToPage();
    }

    public async Task<IActionResult> OnPostClearMaterialAsync(Guid id, string? note)
    {
        var material = await _db.Materials.FirstOrDefaultAsync(m => m.Id == id);
        if (material is null) return NotFound();

        var adminId = User.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)?.Value;
        var now = DateTime.UtcNow;
        await _db.ContentFlags.Where(f => f.MaterialId == id && !f.IsResolved)
            .ExecuteUpdateAsync(s => s
                .SetProperty(f => f.IsResolved, true)
                .SetProperty(f => f.ResolvedByAdminId, adminId)
                .SetProperty(f => f.ResolvedUtc, now)
                .SetProperty(f => f.ResolutionNote, note));

        if (material.Status == ContentStatus.Flagged)
        {
            material.Status = ContentStatus.Published;
            await _db.SaveChangesAsync();
        }

        TempData["Success"] = "Flag cleared.";
        return RedirectToPage();
    }

    public async Task<IActionResult> OnPostRemoveModuleAsync(Guid id, string reason, bool notify)
    {
        var module = await _db.Modules.Include(m => m.Contributor)
            .FirstOrDefaultAsync(m => m.Id == id);
        if (module is null) return NotFound();

        module.Status = ContentStatus.Removed;
        module.RemovedUtc = DateTime.UtcNow;
        await _db.SaveChangesAsync();

        if (notify && !string.IsNullOrEmpty(module.Contributor.Email))
            _ = _email.SendContentRemovedEmailAsync(module.Contributor.Email,
                module.Contributor.UserName ?? "", module.Title, "module", reason);

        TempData["Success"] = "Module removed.";
        return RedirectToPage();
    }

    public async Task<IActionResult> OnPostRemoveMaterialAsync(Guid id, string reason, bool notify)
    {
        var material = await _db.Materials.Include(m => m.Contributor)
            .FirstOrDefaultAsync(m => m.Id == id);
        if (material is null) return NotFound();

        material.Status = ContentStatus.Removed;
        material.RemovedUtc = DateTime.UtcNow;
        await _db.SaveChangesAsync();

        if (notify && !string.IsNullOrEmpty(material.Contributor.Email))
            _ = _email.SendContentRemovedEmailAsync(material.Contributor.Email,
                material.Contributor.UserName ?? "", material.Title, "material", reason);

        TempData["Success"] = "Material removed.";
        return RedirectToPage();
    }
}
