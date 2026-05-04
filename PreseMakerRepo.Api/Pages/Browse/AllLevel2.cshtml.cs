using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.Extensions.Configuration;
using PreseMakerRepo.Core.Interfaces;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Api.Pages.Browse;

public class AllLevel2Model : PageModel
{
    private readonly ITaxonomyService _taxonomy;
    private readonly IConfiguration _config;

    public AllLevel2Model(ITaxonomyService taxonomy, IConfiguration config)
    {
        _taxonomy = taxonomy;
        _config = config;
    }

    public record Level2Item(string Key, string Name, string Level1Key, string Level1Name, int CourseCount, int ModuleCount);

    public string Level2Label { get; set; } = "Subdiscipline";
    public IReadOnlyList<Level2Item> Items { get; set; } = [];
    public new int Page { get; set; } = 1;
    public int TotalCount { get; set; }
    public int TotalPages { get; set; }

    private const int PageSize = 50;

    public async Task OnGetAsync(int page = 1)
    {
        Level2Label = _config["SiteSettings:Level2Label"] ?? "Subdiscipline";
        Page = Math.Max(1, page);

        var tree = await _taxonomy.GetFullTreeAsync();

        var all = tree.Roots
            .SelectMany(l1 => l1.Children.Select(l2 => new Level2Item(
                l2.Key, l2.Name, l1.Key, l1.Name, l2.CourseCount, l2.ModuleCount)))
            .OrderBy(x => x.Name)
            .ThenBy(x => x.Key)
            .ToList();

        TotalCount = all.Count;
        TotalPages = (int)Math.Ceiling((double)TotalCount / PageSize);
        Page = Math.Min(Page, Math.Max(1, TotalPages));

        Items = all.Skip((Page - 1) * PageSize).Take(PageSize).ToList();
    }
}
