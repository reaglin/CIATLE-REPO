using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using PreseMakerRepo.Core.Models;
using System.Security.Claims;

namespace PreseMakerRepo.Api.Pages.Account;

public class LoginModel : PageModel
{
    private readonly UserManager<Contributor> _userManager;
    public LoginModel(UserManager<Contributor> userManager) => _userManager = userManager;

    [BindProperty] public string Email { get; set; } = string.Empty;
    [BindProperty] public string Password { get; set; } = string.Empty;
    [BindProperty] public bool RememberMe { get; set; }
    public string? ReturnUrl { get; set; }
    public string? ErrorMessage { get; set; }

    public void OnGet(string? returnUrl = null) => ReturnUrl = returnUrl;

    public async Task<IActionResult> OnPostAsync(string? returnUrl = null)
    {
        var user = await _userManager.FindByEmailAsync(Email);
        if (user is null || !await _userManager.CheckPasswordAsync(user, Password))
        {
            ErrorMessage = "Invalid email or password.";
            return Page();
        }

        if (user.IsSuspended)
        {
            ErrorMessage = "Your account has been suspended. Contact support for assistance.";
            return Page();
        }

        if (!user.EmailConfirmed)
        {
            ErrorMessage = "Please confirm your email address before logging in.";
            return Page();
        }

        var roles = await _userManager.GetRolesAsync(user);
        var claims = new List<Claim>
        {
            new(ClaimTypes.NameIdentifier, user.Id),
            new(ClaimTypes.Name, user.UserName!),
            new(ClaimTypes.Email, user.Email!)
        };
        claims.AddRange(roles.Select(r => new Claim(ClaimTypes.Role, r)));

        var identity = new ClaimsIdentity(claims, CookieAuthenticationDefaults.AuthenticationScheme);
        var principal = new ClaimsPrincipal(identity);
        var props = new AuthenticationProperties
        {
            IsPersistent = RememberMe,
            ExpiresUtc = DateTimeOffset.UtcNow.AddDays(30)
        };

        await HttpContext.SignInAsync(CookieAuthenticationDefaults.AuthenticationScheme, principal, props);

        if (!string.IsNullOrEmpty(returnUrl) && Url.IsLocalUrl(returnUrl))
            return LocalRedirect(returnUrl);

        return RedirectToPage("/Index");
    }
}
