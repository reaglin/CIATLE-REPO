using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Api.Pages.Account;

public class ConfirmEmailModel : PageModel
{
    private readonly UserManager<Contributor> _userManager;
    public ConfirmEmailModel(UserManager<Contributor> userManager) => _userManager = userManager;

    public bool Success { get; set; }
    public string Message { get; set; } = string.Empty;

    public async Task<IActionResult> OnGetAsync(string? userId, string? token)
    {
        if (userId is null || token is null)
        {
            Message = "Invalid confirmation link.";
            return Page();
        }

        var user = await _userManager.FindByIdAsync(userId);
        if (user is null)
        {
            Message = "User not found.";
            return Page();
        }

        if (user.EmailConfirmed)
        {
            Message = "This email has already been confirmed.";
            return Page();
        }

        var result = await _userManager.ConfirmEmailAsync(user, token);
        if (result.Succeeded)
        {
            Success = true;
            Message = "Your email has been confirmed. You can now log in.";
        }
        else
        {
            Message = "Email confirmation failed. The link may have expired.";
        }

        return Page();
    }
}
