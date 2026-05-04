using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using PreseMakerRepo.Core.Constants;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Core.Interfaces;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Api.Pages;

public class IndexModel : PageModel
{
    private readonly AppDbContext _db;
    private readonly ITaxonomyService _taxonomy;
    private readonly IConfiguration _config;

    public IndexModel(AppDbContext db, ITaxonomyService taxonomy, IConfiguration config)
    {
        _db = db;
        _taxonomy = taxonomy;
        _config = config;
    }

    public IReadOnlyList<TaxonomyNodeSummary> Disciplines { get; set; } = [];
    public IReadOnlyList<Core.Models.Module> RecentModules { get; set; } = [];
    public string Level2Label { get; set; } = "Subdiscipline";

    public async Task OnGetAsync()
    {
        Level2Label = _config["SiteSettings:Level2Label"] ?? "Subdiscipline";
        var tree = await _taxonomy.GetFullTreeAsync();
        Disciplines = tree.Roots;

        RecentModules = await _db.Modules
            .AsNoTracking()
            .Where(m => m.Status == ContentStatus.Published && m.Id != WellKnownIds.OrphanModuleId)
            .OrderByDescending(m => m.SubmittedUtc)
            .Take(10)
            .Include(m => m.Contributor)
            .Include(m => m.Course)
            .ToListAsync();
    }
}
