using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using PreseMakerRepo.Api.Services.Visits;

namespace PreseMakerRepo.Api.Pages;

/// <summary>
/// The public visitor page (plan Phase 13; Ron, 2026-11-22: "The visitor page does not need to be hidden behind an
/// admin login"). The admin page's figures without the program-panel clicks and the list of individual addresses.
/// Each range is worked out at most every 10 minutes. Linked from the visitor figure in the header bar.
/// </summary>
public class VisitorsModel : PageModel
{
    private readonly PublicVisitorFigureService _figures;
    public VisitorsModel(PublicVisitorFigureService figures) => _figures = figures;

    [BindProperty(SupportsGet = true)]
    public int Days { get; set; } = 30;

    public VisitorStats Stats { get; private set; } = new();

    /// <summary>True when the range has fewer visitors than the public minimum, so no figures are shown.</summary>
    public bool TooFew { get; private set; }
    public int Minimum { get; private set; }

    public async Task OnGetAsync(CancellationToken ct)
    {
        if (!VisitorStatsService.Ranges.Contains(Days)) Days = 30;
        Minimum = _figures.Minimum;
        Stats = await _figures.GetPageStatsAsync(Days, ct);
        TooFew = Stats.Visitors < Minimum;
    }
}
