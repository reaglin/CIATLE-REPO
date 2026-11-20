using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using PreseMakerRepo.Api.Services.Visits;

namespace PreseMakerRepo.Api.Areas.Admin.Pages;

/// <summary>How many people visit the site (plan Phase 9.4), from the visitor counter's tables.</summary>
public class VisitorsModel : PageModel
{
    private readonly VisitorStatsService _stats;
    private readonly IConfiguration _config;

    public VisitorsModel(VisitorStatsService stats, IConfiguration config)
    {
        _stats = stats;
        _config = config;
    }

    [BindProperty(SupportsGet = true)]
    public int Days { get; set; } = 30;

    public VisitorStats Stats { get; private set; } = new();

    /// <summary>The home page hides its figure below this (plan 9.5).</summary>
    public int PublicMinimum { get; private set; }

    /// <summary>What the home page shows now (it may trail by up to 10 minutes), or null if it shows nothing.</summary>
    public PublicVisitorFigure? PublicFigure { get; private set; }

    public async Task OnGetAsync(CancellationToken ct)
    {
        if (!VisitorStatsService.Ranges.Contains(Days)) Days = 30;
        Stats = await _stats.GetAsync(Days, ct: ct);
        PublicMinimum = PreseMakerRepo.Api.Pages.IndexModel.PublicVisitorMinimum(_config);
        PublicFigure = await _stats.GetPublicFigureAsync(PublicMinimum, ct: ct);
    }
}
