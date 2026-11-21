using System.Security.Claims;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace PreseMakerRepo.Api.Pages.Account;

/// <summary>
/// Where the sign-in cookie sends a signed-in account that lacks the role a page needs (Program.cs, AccessDeniedPath).
/// It says which account is signed in and its roles, so "wrong account" is obvious. (Missing until 2026-11-21: it was a 404.)
/// </summary>
public class AccessDeniedModel : PageModel
{
    [BindProperty(SupportsGet = true)]
    public string? ReturnUrl { get; set; }

    public IReadOnlyList<string> Roles { get; private set; } = [];
    public bool WantsAdmin => ReturnUrl?.StartsWith("/admin", StringComparison.OrdinalIgnoreCase) == true;

    public void OnGet()
    {
        Roles = User.FindAll(ClaimTypes.Role).Select(c => c.Value).ToList();
        Response.StatusCode = StatusCodes.Status403Forbidden;
    }
}
