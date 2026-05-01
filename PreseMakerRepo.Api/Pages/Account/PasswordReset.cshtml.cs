using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using PreseMakerRepo.Core.Interfaces;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Api.Pages.Account;

public class PasswordResetModel : PageModel
{
    private readonly UserManager<Contributor> _userManager;
    private readonly IEmailService _email;

    public PasswordResetModel(UserManager<Contributor> userManager, IEmailService email)
    {
        _userManager = userManager;
        _email = email;
    }

    // Request form bindings
    [BindProperty] public string RequestEmail { get; set; } = string.Empty;

    // Confirm form bindings
    [BindProperty] public string ConfirmToken { get; set; } = string.Empty;
    [BindProperty] public string ConfirmEmail { get; set; } = string.Empty;
    [BindProperty] public string NewPassword { get; set; } = string.Empty;
    [BindProperty] public string ConfirmPassword { get; set; } = string.Empty;

    public bool IsConfirmMode { get; set; }
    public string? ErrorMessage { get; set; }

    public void OnGet(string? token, string? email)
    {
        IsConfirmMode = token is not null && email is not null;
        if (IsConfirmMode)
        {
            ConfirmToken = token!;
            ConfirmEmail = email!;
        }
    }

    // POST: send reset email
    public async Task<IActionResult> OnPostRequestAsync()
    {
        var user = await _userManager.FindByEmailAsync(RequestEmail);
        if (user is not null)
        {
            var token = await _userManager.GeneratePasswordResetTokenAsync(user);
            var link = Url.Page("/Account/PasswordReset", null,
                new { token, email = RequestEmail }, Request.Scheme)!;
            await _email.SendPasswordResetEmailAsync(RequestEmail, user.UserName ?? "", link);
        }
        // Anti-enumeration: always show success
        TempData["Success"] = "If that email is registered, a reset link has been sent.";
        return RedirectToPage();
    }

    // POST: apply new password
    public async Task<IActionResult> OnPostConfirmAsync()
    {
        IsConfirmMode = true;

        if (NewPassword != ConfirmPassword)
        {
            ErrorMessage = "Passwords do not match.";
            return Page();
        }

        var user = await _userManager.FindByEmailAsync(ConfirmEmail);
        if (user is null)
        {
            ErrorMessage = "Invalid request.";
            return Page();
        }

        var result = await _userManager.ResetPasswordAsync(user, ConfirmToken, NewPassword);
        if (!result.Succeeded)
        {
            ErrorMessage = "Password reset failed. The link may have expired.";
            return Page();
        }

        TempData["Success"] = "Password reset successful. You can now log in.";
        return RedirectToPage("/Account/Login");
    }
}
