using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using PreseMakerRepo.Api.Services.Visits;

namespace PreseMakerRepo.Api.Areas.Admin.Pages;

/// <summary>How many people visit the site (plan Phase 9.4), from the visitor counter's tables.</summary>
public class VisitorsModel : PageModel
{
    private readonly VisitorStatsService _stats;
    public VisitorsModel(VisitorStatsService stats) => _stats = stats;

    [BindProperty(SupportsGet = true)]
    public int Days { get; set; } = 30;

    public VisitorStats Stats { get; private set; } = new();

    public async Task OnGetAsync(CancellationToken ct)
    {
        if (!VisitorStatsService.Ranges.Contains(Days)) Days = 30;
        Stats = await _stats.GetAsync(Days, ct: ct);
    }
}
