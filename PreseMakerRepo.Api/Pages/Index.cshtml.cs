using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.Extensions.Configuration;
using PreseMakerRepo.Core.Interfaces;

namespace PreseMakerRepo.Api.Pages;

public class IndexModel : PageModel
{
    private readonly ITaxonomyService _taxonomy;
    private readonly IConfiguration _config;

    public IndexModel(ITaxonomyService taxonomy, IConfiguration config)
    {
        _taxonomy = taxonomy;
        _config = config;
    }

    public IReadOnlyList<TaxonomyNodeSummary> Disciplines { get; set; } = [];
    public string Level2Label { get; set; } = "Subdiscipline";

    public async Task OnGetAsync()
    {
        Level2Label = _config["SiteSettings:Level2Label"] ?? "Subdiscipline";
        var tree = await _taxonomy.GetFullTreeAsync();
        Disciplines = tree.Roots;
    }
}
