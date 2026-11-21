using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using PreseMakerRepo.Api.Services;
using PreseMakerRepo.Api.Services.Visits;

namespace PreseMakerRepo.Api.Areas.Admin.Pages;

/// <summary>How many people visit the site (plan Phase 9.4), from the visitor counter's tables.</summary>
public class VisitorsModel : PageModel
{
    private readonly VisitorStatsService _stats;
    private readonly IConfiguration _config;
    private readonly ProgramPanelService _programs;

    public VisitorsModel(VisitorStatsService stats, IConfiguration config, ProgramPanelService programs)
    {
        _programs = programs;
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

    /// <summary>The programs the panel shows now (from softwareplus.ai/apps.json), by id; empty if it could not be read.</summary>
    public IReadOnlyDictionary<string, PanelProgram> Programs { get; private set; } = new Dictionary<string, PanelProgram>();

    public async Task OnGetAsync(CancellationToken ct)
    {
        if (!VisitorStatsService.Ranges.Contains(Days)) Days = 30;
        Stats = await _stats.GetAsync(Days, ct: ct);
        PublicMinimum = PreseMakerRepo.Api.Pages.IndexModel.PublicVisitorMinimum(_config);
        PublicFigure = await _stats.GetPublicFigureAsync(PublicMinimum, ct: ct);
        Programs = (await _programs.GetProgramsAsync(ct)).ToDictionary(p => p.Id);
    }
}
