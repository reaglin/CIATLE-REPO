using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using PreseMakerRepo.Api.Helpers;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Api.Pages.Account;

public class ProfileModel : PageModel
{
    private readonly UserManager<Contributor> _userManager;
    public ProfileModel(UserManager<Contributor> userManager) => _userManager = userManager;

    public Contributor? Contributor { get; set; }

    public async Task<IActionResult> OnGetAsync()
    {
        var userId = ClaimsHelper.GetUserId(User);
        Contributor = await _userManager.FindByIdAsync(userId!);
        if (Contributor is null) return RedirectToPage("/Account/Login");
        return Page();
    }
}
