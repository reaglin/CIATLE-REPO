using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Configuration;
using PreseMakerRepo.Api.Services.Visits;
using PreseMakerRepo.Core.Interfaces;

namespace PreseMakerRepo.Api.Pages;

public class IndexModel : PageModel
{
    private const string VisitorFigureKey = "home:visitor-figure";

    private readonly ITaxonomyService _taxonomy;
    private readonly IConfiguration _config;
    private readonly VisitorStatsService _visitors;
    private readonly IMemoryCache _cache;
    private readonly ILogger<IndexModel> _log;

    public IndexModel(ITaxonomyService taxonomy, IConfiguration config, VisitorStatsService visitors,
        IMemoryCache cache, ILogger<IndexModel> log)
    {
        _taxonomy = taxonomy;
        _config = config;
        _visitors = visitors;
        _cache = cache;
        _log = log;
    }

    public IReadOnlyList<TaxonomyNodeSummary> Disciplines { get; set; } = [];
    public string Level2Label { get; set; } = "Subdiscipline";
    /// <summary>The public visitor figure (plan 9.5), or null to show none.</summary>
    public PublicVisitorFigure? VisitorFigure { get; set; }

    public async Task OnGetAsync()
    {
        Level2Label = _config["SiteSettings:Level2Label"] ?? "Subdiscipline";
        var tree = await _taxonomy.GetFullTreeAsync();
        Disciplines = tree.Roots;
        VisitorFigure = await GetVisitorFigureAsync();
    }

    /// <summary>The home page shows no figure below this many visitors (<c>SiteSettings:PublicVisitorMinimum</c>, default 100).</summary>
    public static int PublicVisitorMinimum(IConfiguration config) =>
        config.GetValue("SiteSettings:PublicVisitorMinimum", 100);

    // Worked out at most every 10 minutes, and never allowed to break the home page.
    private async Task<PublicVisitorFigure?> GetVisitorFigureAsync()
    {
        if (_cache.TryGetValue(VisitorFigureKey, out PublicVisitorFigure? cached)) return cached;
        try
        {
            var figure = await _visitors.GetPublicFigureAsync(PublicVisitorMinimum(_config), ct: HttpContext.RequestAborted);
            // "Nothing yet" is kept only a minute (the counter saves once a minute), so the first figure shows promptly.
            _cache.Set(VisitorFigureKey, figure, TimeSpan.FromMinutes(figure is null ? 1 : 10));
            return figure;
        }
        catch (Exception ex) when (ex is not OperationCanceledException)
        {
            _log.LogWarning(ex, "Could not work out the home page's visitor figure");
            return null;
        }
    }
}
