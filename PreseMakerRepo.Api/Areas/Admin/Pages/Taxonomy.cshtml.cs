using Ganss.Xss;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Api.Areas.Admin.Pages;

public class TaxonomyModel : PageModel
{
    private readonly AppDbContext _db;

    public TaxonomyModel(AppDbContext db) => _db = db;

    public IReadOnlyList<TaxonomyNode> Level1Nodes { get; set; } = [];
    public Dictionary<string, string> Descriptions { get; set; } = new();

    public async Task OnGetAsync()
    {
        Level1Nodes = await _db.TaxonomyNodes
            .AsNoTracking()
            .Where(n => n.Level == 1)
            .Include(n => n.Children)
                .ThenInclude(n => n.Children)
                    .ThenInclude(n => n.Courses)
            .OrderBy(n => n.Name)
            .ToListAsync();

        Descriptions = await _db.TaxonomyNodeDescriptions
            .AsNoTracking()
            .ToDictionaryAsync(d => d.NodeKey, d => d.HtmlContent);
    }

    public async Task<IActionResult> OnPostEditNodeAsync(string key, string name)
    {
        var node = await _db.TaxonomyNodes.FindAsync(key);
        if (node is null) return NotFound();
        node.Name = name.Trim();
        await _db.SaveChangesAsync();
        TempData["Success"] = $"Node \"{key}\" updated.";
        return RedirectToPage();
    }

    public async Task<IActionResult> OnPostEditCourseAsync(
        string courseId, string title, int? creditHours, bool isActive, string? curriculumGuideUrl)
    {
        var course = await _db.TaxonomyCourses.FindAsync(courseId);
        if (course is null) return NotFound();
        course.Title = title.Trim();
        course.CreditHours = creditHours;
        course.IsActive = isActive;
        course.CurriculumGuideUrl = string.IsNullOrWhiteSpace(curriculumGuideUrl) ? null : curriculumGuideUrl.Trim();
        await _db.SaveChangesAsync();
        TempData["Success"] = $"Course {courseId} updated.";
        return RedirectToPage();
    }

    public async Task<IActionResult> OnPostSaveDescriptionAsync(string key, string htmlContent)
    {
        var node = await _db.TaxonomyNodes.FindAsync(key);
        if (node is null) return NotFound();

        var sanitized = Sanitize(htmlContent);

        var existing = await _db.TaxonomyNodeDescriptions.FindAsync(key);

        if (string.IsNullOrWhiteSpace(sanitized))
        {
            if (existing is not null)
                _db.TaxonomyNodeDescriptions.Remove(existing);
        }
        else if (existing is null)
        {
            _db.TaxonomyNodeDescriptions.Add(new TaxonomyNodeDescription
            {
                NodeKey = key,
                HtmlContent = sanitized,
                UpdatedUtc = DateTime.UtcNow
            });
        }
        else
        {
            existing.HtmlContent = sanitized;
            existing.UpdatedUtc = DateTime.UtcNow;
        }

        await _db.SaveChangesAsync();
        TempData["Success"] = $"Description for \"{key}\" saved.";
        return RedirectToPage();
    }

    private static readonly HtmlSanitizer _sanitizer = BuildSanitizer();

    private static HtmlSanitizer BuildSanitizer()
    {
        var s = new HtmlSanitizer();

        s.AllowedTags.Clear();
        foreach (var tag in new[]
        {
            "h2","h3","h4","h5","h6",
            "p","br","hr","blockquote",
            "ul","ol","li",
            "a","strong","em","b","i","u",
            "table","thead","tbody","tr","th","td",
            "span","div"
        })
            s.AllowedTags.Add(tag);

        s.AllowedAttributes.Clear();
        s.AllowedAttributes.Add("href");
        s.AllowedAttributes.Add("target");
        s.AllowedAttributes.Add("rel");
        s.AllowedAttributes.Add("class");

        // Strip all inline styles
        s.AllowedCssProperties.Clear();

        return s;
    }

    private static string Sanitize(string input) =>
        string.IsNullOrWhiteSpace(input) ? string.Empty : _sanitizer.Sanitize(input);
}
