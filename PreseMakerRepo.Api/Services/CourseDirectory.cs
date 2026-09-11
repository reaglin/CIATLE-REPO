using System.Linq.Expressions;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Api.Helpers;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Api.Services;

/// <summary>One course as a browse list shows it.</summary>
public sealed record CourseRow(
    string CourseId,
    string Title,
    int? CreditHours,
    int? ContactHours,
    int OfferingCount,
    bool HasGuide,
    bool HasModules);

/// <summary>A course list with its with/without-guide filter applied.</summary>
public sealed record CourseListView(IReadOnlyList<CourseRow> Rows, string Show, int Total, int WithGuide)
{
    public const string ShowAll = "all";
    public const string ShowGuides = "guides";
    public const string ShowNoGuide = "noguide";

    public static CourseListView For(IReadOnlyList<CourseRow> all, string? show)
    {
        var mode = show is ShowGuides or ShowNoGuide ? show : ShowAll;
        IReadOnlyList<CourseRow> rows = mode switch
        {
            ShowGuides => all.Where(r => r.HasGuide).ToList(),
            ShowNoGuide => all.Where(r => !r.HasGuide).ToList(),
            _ => all
        };
        return new CourseListView(rows, mode, all.Count, all.Count(r => r.HasGuide));
    }
}

/// <summary>
/// The course rows the public pages render. A course is listed when it is active, or when it still has a
/// guide or published modules — the predicate the taxonomy counts and the header total use too.
/// </summary>
public class CourseDirectory
{
    private readonly AppDbContext _db;

    public CourseDirectory(AppDbContext db) => _db = db;

    public Task<List<CourseRow>> ForLeafAsync(string leafKey)
    {
        var key = leafKey.ToUpperInvariant();
        return RowsAsync(c => c.Level3Key == key, take: null);
    }

    /// <summary>Courses whose id or title matches; "eee 3300" finds EEE3300.</summary>
    public Task<List<CourseRow>> SearchAsync(string term, int max)
    {
        var pattern = $"%{term}%";
        var compact = new string(term.Where(ch => !char.IsWhiteSpace(ch) && ch != '-').ToArray()).ToUpperInvariant();
        var idPattern = compact.Length > 0 ? $"%{compact}%" : pattern;
        return RowsAsync(c =>
                EF.Functions.Like(c.CourseId, idPattern) ||
                EF.Functions.Like(c.Title, pattern) ||
                (c.StateTitle != null && EF.Functions.Like(c.StateTitle, pattern)) ||
                _db.CurriculumGuides.Any(g => g.CourseId == c.CourseId && EF.Functions.Like(g.Title, pattern)),
            take: max);
    }

    private async Task<List<CourseRow>> RowsAsync(Expression<Func<TaxonomyCourse, bool>> filter, int? take)
    {
        IQueryable<TaxonomyCourse> query = _db.TaxonomyCourses.AsNoTracking()
            .Where(c => c.Level3Key != null)
            .Where(filter)
            .Where(c => c.IsActive ||
                        _db.CurriculumGuides.Any(g => g.CourseId == c.CourseId && g.Title != CurriculumGuide.StubTitle) ||
                        _db.Modules.Any(m => m.CourseId == c.CourseId && m.Status == ContentStatus.Published))
            .OrderBy(c => c.CourseId);
        if (take.HasValue) query = query.Take(take.Value);

        var raw = await query
            .Select(c => new
            {
                c.CourseId,
                c.Title,
                c.StateTitle,
                c.CreditHours,
                c.ContactHours,
                c.OfferingCount,
                GuideTitle = _db.CurriculumGuides
                    .Where(g => g.CourseId == c.CourseId && g.Title != CurriculumGuide.StubTitle)
                    .Select(g => g.Title)
                    .FirstOrDefault(),
                HasModules = _db.Modules.Any(m => m.CourseId == c.CourseId && m.Status == ContentStatus.Published)
            })
            .ToListAsync();

        return raw.Select(r => new CourseRow(
                r.CourseId,
                CourseTitles.Display(r.CourseId, r.Title, r.StateTitle, r.GuideTitle),
                r.CreditHours,
                r.ContactHours,
                r.OfferingCount,
                r.GuideTitle is not null,
                r.HasModules))
            .ToList();
    }
}
