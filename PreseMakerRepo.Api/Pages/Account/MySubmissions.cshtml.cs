using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Api.Helpers;
using PreseMakerRepo.Core.Constants;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Infrastructure.Data;
using ModuleEntity = PreseMakerRepo.Core.Models.Module;
using MaterialEntity = PreseMakerRepo.Core.Models.Material;

namespace PreseMakerRepo.Api.Pages.Account;

public class MySubmissionsModel : PageModel
{
    private readonly AppDbContext _db;
    public MySubmissionsModel(AppDbContext db) => _db = db;

    [BindProperty(SupportsGet = true)] public string Filter { get; set; } = "all";
    [BindProperty(SupportsGet = true)] public int PageNum { get; set; } = 1;

    public IReadOnlyList<ModuleEntity> Modules { get; set; } = [];
    public IReadOnlyList<MaterialEntity> Materials { get; set; } = [];

    public async Task<IActionResult> OnGetAsync()
    {
        var userId = ClaimsHelper.GetUserId(User);
        if (userId is null) return RedirectToPage("/Account/Login");

        if (Filter is "all" or "module")
        {
            Modules = await _db.Modules.AsNoTracking()
                .Where(m => m.ContributorId == userId && m.Id != WellKnownIds.OrphanModuleId)
                .Include(m => m.Materials)
                .OrderByDescending(m => m.SubmittedUtc)
                .ToListAsync();
        }

        if (Filter is "all" or "material")
        {
            Materials = await _db.Materials.AsNoTracking()
                .Where(m => m.ContributorId == userId)
                .Include(m => m.Module)
                .OrderByDescending(m => m.SubmittedUtc)
                .ToListAsync();
        }

        return Page();
    }

    public static string StatusBadge(ContentStatus status) => status switch
    {
        ContentStatus.Published => "bg-success",
        ContentStatus.Flagged   => "bg-warning text-dark",
        ContentStatus.Removed   => "bg-danger",
        _                       => "bg-secondary"
    };
}
