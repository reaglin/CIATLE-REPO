using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using PreseMakerRepo.Core.Interfaces;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Api.Pages.Account;

public class RegisterModel : PageModel
{
    private readonly UserManager<Contributor> _userManager;
    private readonly IEmailService _email;
    private readonly IEduLookupService _edu;

    public RegisterModel(UserManager<Contributor> userManager, IEmailService email, IEduLookupService edu)
    {
        _userManager = userManager;
        _email = email;
        _edu = edu;
    }

    [BindProperty] public string Username { get; set; } = string.Empty;
    [BindProperty] public string Email { get; set; } = string.Empty;
    [BindProperty] public string Password { get; set; } = string.Empty;
    [BindProperty] public string ConfirmPassword { get; set; } = string.Empty;
    public string? ErrorMessage { get; set; }

    public async Task<IActionResult> OnPostAsync()
    {
        if (Password != ConfirmPassword)
        {
            ErrorMessage = "Passwords do not match.";
            return Page();
        }

        var eduResult = await _edu.LookupByEmailAsync(Email);
        var contributor = new Contributor
        {
            UserName = Username,
            Email = Email,
            DisplayName = Username,
            InstitutionName = eduResult.InstitutionName,
            IsEduVerified = eduResult.IsEdu,
            RegisteredUtc = DateTime.UtcNow
        };

        var result = await _userManager.CreateAsync(contributor, Password);
        if (!result.Succeeded)
        {
            ErrorMessage = string.Join(" ", result.Errors.Select(e => e.Description));
            return Page();
        }

        await _userManager.AddToRoleAsync(contributor, "Contributor");

        var token = await _userManager.GenerateEmailConfirmationTokenAsync(contributor);
        var link = Url.Page("/Account/ConfirmEmail", null,
            new { userId = contributor.Id, token }, Request.Scheme)!;

        await _email.SendConfirmationEmailAsync(Email, Username, link);

        TempData["Success"] = "Registration successful! Check your email to confirm your account.";
        return RedirectToPage("/Account/Login");
    }
}
