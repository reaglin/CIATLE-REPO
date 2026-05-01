using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Core.Constants;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Core.Interfaces;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Api.Pages.Browse;

public class IndexModel : PageModel
{
    private readonly AppDbContext _db;
    private readonly ITaxonomyService _taxonomy;

    public IndexModel(AppDbContext db, ITaxonomyService taxonomy)
    {
        _db = db;
        _taxonomy = taxonomy;
    }

    [BindProperty(SupportsGet = true)] public string? Q { get; set; }
    [BindProperty(SupportsGet = true)] public string? Level { get; set; }
    [BindProperty(SupportsGet = true)] public int PageNum { get; set; } = 1;

    public bool IsSearch => !string.IsNullOrWhiteSpace(Q) && Q.Trim().Length >= 2;
    public IReadOnlyList<TaxonomyNodeSummary> Disciplines { get; set; } = [];
    public List<SearchResultItem> SearchResults { get; set; } = [];
    public int TotalResults { get; set; }

    public record SearchResultItem(
        string ResultType, Guid ModuleId, string CourseId, string Title,
        string? Description, string ContributorUsername, bool IsEduVerified,
        string? InstitutionName, DateTime SubmittedUtc,
        Guid? MaterialId, string? MaterialType, string? FileName, string? ModuleTitle);

    public async Task OnGetAsync()
    {
        if (IsSearch)
        {
            await RunSearchAsync(Q!.Trim());
        }
        else
        {
            var tree = await _taxonomy.GetFullTreeAsync();
            Disciplines = tree.Roots;
        }
    }

    private async Task RunSearchAsync(string term)
    {
        const int pageSize = 20;
        var pattern = $"%{term}%";
        var includeModules = Level is null or "all" or "module";
        var includeMaterials = Level is null or "all" or "material";
        var results = new List<SearchResultItem>();

        if (includeModules)
        {
            var modules = await _db.Modules
                .AsNoTracking()
                .Where(m => m.Status == ContentStatus.Published &&
                            m.Id != WellKnownIds.OrphanModuleId &&
                            (EF.Functions.Like(m.Title, pattern) ||
                             EF.Functions.Like(m.Description, pattern) ||
                             EF.Functions.Like(m.OutcomesJson, pattern) ||
                             EF.Functions.Like(m.CourseId, pattern)))
                .Include(m => m.Contributor)
                .ToListAsync();

            results.AddRange(modules.Select(m => new SearchResultItem(
                "module", m.Id, m.CourseId, m.Title, m.Description,
                m.Contributor.UserName!, m.Contributor.IsEduVerified,
                m.Contributor.InstitutionName, m.SubmittedUtc,
                null, null, null, null)));
        }

        if (includeMaterials)
        {
            var materials = await _db.Materials
                .AsNoTracking()
                .Where(m => m.Status == ContentStatus.Published &&
                            (EF.Functions.Like(m.Title, pattern) ||
                             EF.Functions.Like(m.Description ?? string.Empty, pattern)))
                .Include(m => m.Contributor)
                .Include(m => m.Module)
                .ToListAsync();

            results.AddRange(materials.Select(m => new SearchResultItem(
                "material", m.ModuleId, m.Module.CourseId, m.Title, m.Description,
                m.Contributor.UserName!, m.Contributor.IsEduVerified,
                m.Contributor.InstitutionName, m.SubmittedUtc,
                m.Id, m.Type.ToString(), m.FileName, m.Module.Title)));
        }

        TotalResults = results.Count;
        SearchResults = results
            .OrderByDescending(r => r.SubmittedUtc)
            .Skip((PageNum - 1) * pageSize)
            .Take(pageSize)
            .ToList();
    }
}
