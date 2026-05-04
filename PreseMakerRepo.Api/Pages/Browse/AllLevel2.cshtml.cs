using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.Extensions.Configuration;
using PreseMakerRepo.Core.Interfaces;

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
    public string SelectedLetter { get; set; } = string.Empty;
    public IReadOnlyList<char> AvailableLetters { get; set; } = [];
    public int TotalCount { get; set; }

    public async Task OnGetAsync(string? letter = null)
    {
        Level2Label = _config["SiteSettings:Level2Label"] ?? "Subdiscipline";

        var tree = await _taxonomy.GetFullTreeAsync();

        var all = tree.Roots
            .SelectMany(l1 => l1.Children.Select(l2 => new Level2Item(
                l2.Key, l2.Name, l1.Key, l1.Name, l2.CourseCount, l2.ModuleCount)))
            .OrderBy(x => x.Key)
            .ToList();

        TotalCount = all.Count;

        AvailableLetters = all
            .Where(x => x.Key.Length > 0 && char.IsLetter(x.Key[0]))
            .Select(x => char.ToUpper(x.Key[0]))
            .Distinct()
            .OrderBy(c => c)
            .ToList();

        // Default to first available letter if none specified or invalid
        char chosen = AvailableLetters.Count > 0 ? AvailableLetters[0] : 'A';
        if (!string.IsNullOrEmpty(letter) && char.IsLetter(letter[0]))
        {
            char requested = char.ToUpper(letter[0]);
            if (AvailableLetters.Contains(requested))
                chosen = requested;
        }

        SelectedLetter = chosen.ToString();

        Items = all
            .Where(x => x.Key.Length > 0 &&
                        char.ToUpper(x.Key[0]) == chosen)
            .ToList();
    }
}
