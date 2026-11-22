using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using PreseMakerRepo.Api.Services;
using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Configuration;
using PreseMakerRepo.Api.Services.Visits;
using PreseMakerRepo.Core.Interfaces;

namespace PreseMakerRepo.Api.Pages;

public class IndexModel : PageModel
{
    private readonly ITaxonomyService _taxonomy;
    private readonly IConfiguration _config;
    private readonly ILogger<IndexModel> _log;

    public IndexModel(ITaxonomyService taxonomy, IConfiguration config, ILogger<IndexModel> log)
    {
        _taxonomy = taxonomy;
        _config = config;
        _log = log;
    }

    public IReadOnlyList<TaxonomyNodeSummary> Disciplines { get; set; } = [];
    public string Level2Label { get; set; } = "Subdiscipline";
    public async Task OnGetAsync()
    {
        Level2Label = _config["SiteSettings:Level2Label"] ?? "Subdiscipline";
        var tree = await _taxonomy.GetFullTreeAsync();
        Disciplines = tree.Roots;
    }

    /// <summary>No public visitor figure is shown below this many visitors (<c>SiteSettings:PublicVisitorMinimum</c>, default 100).
    /// The figure itself is in the header bar now (<see cref="PublicVisitorFigureService"/>).</summary>
    public static int PublicVisitorMinimum(IConfiguration config) =>
        config.GetValue("SiteSettings:PublicVisitorMinimum", 100);
}
