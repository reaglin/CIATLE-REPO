using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Core.Interfaces;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Api.Areas.Admin.Pages;

public class ContributorsModel : PageModel
{
    private readonly AppDbContext _db;
    private readonly UserManager<Contributor> _userManager;
    private readonly IEmailService _email;

    public ContributorsModel(AppDbContext db, UserManager<Contributor> userManager, IEmailService email)
    {
        _db = db;
        _userManager = userManager;
        _email = email;
    }

    [BindProperty(SupportsGet = true)] public string? Q { get; set; }

    public record ContributorRow(string Id, string Username, string? Email, string? InstitutionName,
        bool IsEduVerified, bool IsSuspended, DateTime RegisteredUtc, int ModuleCount, int MaterialCount);

    public IReadOnlyList<ContributorRow> Contributors { get; set; } = [];

    public async Task OnGetAsync()
    {
        IQueryable<Contributor> query = _db.Users.AsNoTracking();

        if (!string.IsNullOrWhiteSpace(Q))
            query = query.Where(u => u.UserName!.Contains(Q) || u.Email!.Contains(Q));

        var users = await query.OrderBy(u => u.UserName).Take(100).ToListAsync();
        var userIds = users.Select(u => u.Id).ToList();

        var moduleCounts = await _db.Modules.AsNoTracking()
            .Where(m => userIds.Contains(m.ContributorId) && m.Status != ContentStatus.Removed)
            .GroupBy(m => m.ContributorId)
            .Select(g => new { Id = g.Key, Count = g.Count() })
            .ToDictionaryAsync(x => x.Id, x => x.Count);

        var materialCounts = await _db.Materials.AsNoTracking()
            .Where(m => userIds.Contains(m.ContributorId) && m.Status != ContentStatus.Removed)
            .GroupBy(m => m.ContributorId)
            .Select(g => new { Id = g.Key, Count = g.Count() })
            .ToDictionaryAsync(x => x.Id, x => x.Count);

        Contributors = users.Select(u => new ContributorRow(
            u.Id, u.UserName!, u.Email, u.InstitutionName, u.IsEduVerified, u.IsSuspended,
            u.RegisteredUtc,
            moduleCounts.GetValueOrDefault(u.Id),
            materialCounts.GetValueOrDefault(u.Id))).ToList();
    }

    public async Task<IActionResult> OnPostSuspendAsync(string id, string reason, bool notify)
    {
        var user = await _userManager.FindByIdAsync(id);
        if (user is null) return NotFound();
        user.IsSuspended = true;
        await _userManager.UpdateAsync(user);
        if (notify && !string.IsNullOrEmpty(user.Email))
            _ = _email.SendSuspensionEmailAsync(user.Email, user.UserName ?? "", reason);
        TempData["Success"] = $"{user.UserName} suspended.";
        return RedirectToPage();
    }

    public async Task<IActionResult> OnPostReinstateAsync(string id)
    {
        var user = await _userManager.FindByIdAsync(id);
        if (user is null) return NotFound();
        user.IsSuspended = false;
        await _userManager.UpdateAsync(user);
        TempData["Success"] = $"{user.UserName} reinstated.";
        return RedirectToPage();
    }

    public async Task<IActionResult> OnPostContactAsync(string id, string subject, string body)
    {
        var user = await _userManager.FindByIdAsync(id);
        if (user is null || string.IsNullOrEmpty(user.Email)) return NotFound();
        await _email.SendAdminContactEmailAsync(user.Email, subject, body);
        TempData["Success"] = $"Email sent to {user.UserName}.";
        return RedirectToPage();
    }
}
