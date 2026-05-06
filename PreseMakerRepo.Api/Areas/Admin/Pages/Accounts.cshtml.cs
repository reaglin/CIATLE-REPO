using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Api.Areas.Admin.Pages;

public class AccountsModel : PageModel
{
    private readonly AppDbContext _db;
    private readonly UserManager<Contributor> _userManager;

    public AccountsModel(AppDbContext db, UserManager<Contributor> userManager)
    {
        _db = db;
        _userManager = userManager;
    }

    [BindProperty(SupportsGet = true)] public string? Q { get; set; }

    public record AccountRow(string Id, string Username, string? Email, bool IsAdmin, bool IsSuspended, DateTime RegisteredUtc);

    public IReadOnlyList<AccountRow> Accounts { get; set; } = [];
    public string? CurrentUserId { get; set; }

    public async Task OnGetAsync()
    {
        CurrentUserId = _userManager.GetUserId(User);

        IQueryable<Contributor> query = _db.Users.AsNoTracking();
        if (!string.IsNullOrWhiteSpace(Q))
            query = query.Where(u => u.UserName!.Contains(Q) || u.Email!.Contains(Q));

        var users = await query.OrderBy(u => u.UserName).Take(100).ToListAsync();
        var adminIds = (await _userManager.GetUsersInRoleAsync("Administrator"))
            .Select(a => a.Id).ToHashSet();

        Accounts = users.Select(u => new AccountRow(
            u.Id, u.UserName!, u.Email, adminIds.Contains(u.Id), u.IsSuspended, u.RegisteredUtc
        )).ToList();
    }

    public async Task<IActionResult> OnPostPromoteAsync(string id)
    {
        var user = await _userManager.FindByIdAsync(id);
        if (user is null) return NotFound();
        if (!await _userManager.IsInRoleAsync(user, "Administrator"))
            await _userManager.AddToRoleAsync(user, "Administrator");
        TempData["Success"] = $"{user.UserName} promoted to Administrator.";
        return RedirectToPage();
    }

    public async Task<IActionResult> OnPostDemoteAsync(string id)
    {
        if (id == _userManager.GetUserId(User))
        {
            TempData["Error"] = "You cannot remove your own Administrator role.";
            return RedirectToPage();
        }
        var user = await _userManager.FindByIdAsync(id);
        if (user is null) return NotFound();
        if (await _userManager.IsInRoleAsync(user, "Administrator"))
            await _userManager.RemoveFromRoleAsync(user, "Administrator");
        TempData["Success"] = $"Administrator role removed from {user.UserName}.";
        return RedirectToPage();
    }
}
