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
    private readonly ProgramPanelService _programs;

    public IndexModel(ITaxonomyService taxonomy, IConfiguration config, ILogger<IndexModel> log, ProgramPanelService programs)
    {
        _programs = programs;
        _taxonomy = taxonomy;
        _config = config;
        _log = log;
    }

    public IReadOnlyList<TaxonomyNodeSummary> Disciplines { get; set; } = [];
    public string Level2Label { get; set; } = "Subdiscipline";
    /// <summary>The program shown in the panel (plan Phase 10), or null to show none.</summary>
    public PanelProgram? Program { get; set; }

    public async Task OnGetAsync()
    {
        Level2Label = _config["SiteSettings:Level2Label"] ?? "Subdiscipline";
        var tree = await _taxonomy.GetFullTreeAsync();
        Disciplines = tree.Roots;
        Program = await PickProgramAsync();
    }

    /// <summary>
    /// The panel's × without JavaScript (with it, site.js sets the cookie and hides the panel in place): sets
    /// the session cookie and reloads the home page without the panel (plan 10.3).
    /// </summary>
    public IActionResult OnPostCloseProgram()
    {
        Response.Cookies.Append(ProgramPanelService.ClosedCookie, "1", new CookieOptions
        {
            Path = "/", SameSite = SameSiteMode.Lax, Secure = Request.IsHttps, IsEssential = true
            // No Expires: a session cookie, dropped when the browser closes.
        });
        return RedirectToPage();
    }

    // A program at random, unless this browser closed the panel in this session, or this is the static
    // export (a static copy cannot be closed or count clicks). Never allowed to break the home page.
    private async Task<PanelProgram?> PickProgramAsync()
    {
        if (Request.Cookies.ContainsKey(ProgramPanelService.ClosedCookie)) return null;
        if (Request.Headers.ContainsKey("X-Static-Export")) return null;
        try { return await _programs.PickAsync(HttpContext.RequestAborted); }
        catch (Exception ex) when (ex is not OperationCanceledException)
        {
            _log.LogWarning(ex, "Could not pick a program for the home page's panel");
            return null;
        }
    }

    /// <summary>No public visitor figure is shown below this many visitors (<c>SiteSettings:PublicVisitorMinimum</c>, default 100).
    /// The figure itself is in the header bar now (<see cref="PublicVisitorFigureService"/>).</summary>
    public static int PublicVisitorMinimum(IConfiguration config) =>
        config.GetValue("SiteSettings:PublicVisitorMinimum", 100);
}
