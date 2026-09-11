using System.Text.RegularExpressions;
using FluentValidation;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Memory;
using PreseMakerRepo.Api.Helpers;
using PreseMakerRepo.Api.Models;
using PreseMakerRepo.Api.Models.Requests;
using PreseMakerRepo.Api.Models.Responses;
using PreseMakerRepo.Core.Constants;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;
using PreseMakerRepo.Infrastructure.Services;

namespace PreseMakerRepo.Api.Services;

/// <summary>
/// Base course data — courses with or without a guide — written by the content pipeline in
/// <c>Tools/</c>. The site does not decide which courses exist; it stores what it is sent, places each
/// course in the taxonomy by prefix, and keeps offerings and counts consistent.
///
/// Rules (see COURSE_CATALOG_PLAN.md §6 and Tools/COURSE_API.md):
/// <list type="bullet">
/// <item>Fields left null are left unchanged on an existing course; <c>title</c> is required.</item>
/// <item>The title sent is written — site reviews correct titles — except that the course-id
///       placeholder never replaces a real title.</item>
/// <item>Offerings replace the stored set unless <c>replaceOfferings</c> is false.</item>
/// <item>A batch is validated item by item: a bad row fails alone, the rest are saved together.</item>
/// </list>
/// </summary>
public class CourseCatalogService
{
    public const int MaxCourseBatch = 500;
    public const int MaxInstitutionBatch = 1000;

    public static class Outcomes
    {
        public const string Created = "created";
        public const string Updated = "updated";
        public const string Unchanged = "unchanged";
        public const string Failed = "failed";
    }

    public enum DeleteOutcome { Deleted, NotFound, HasContent }

    private static readonly Regex CourseIdPattern =
        new(@"^[A-Z]{3}\d{4}[A-Z]?(?:-(?:SCNS|[A-Z]{2,5}))?$", RegexOptions.Compiled);

    private readonly AppDbContext _db;
    private readonly IMemoryCache _cache;
    private readonly IValidator<UpsertCourseRequest> _courseValidator;
    private readonly IValidator<UpsertInstitutionRequest> _institutionValidator;

    public CourseCatalogService(AppDbContext db, IMemoryCache cache,
        IValidator<UpsertCourseRequest> courseValidator,
        IValidator<UpsertInstitutionRequest> institutionValidator)
    {
        _db = db;
        _cache = cache;
        _courseValidator = courseValidator;
        _institutionValidator = institutionValidator;
    }

    /// <summary>"eee 3300" → "EEE3300". Accepts the one-number-two-subjects variants ("NUR4826-UWF").</summary>
    public static bool TryNormalizeCourseId(string? raw, out string normalized)
    {
        normalized = new string((raw ?? string.Empty).Where(ch => !char.IsWhiteSpace(ch)).ToArray()).ToUpperInvariant();
        return CourseIdPattern.IsMatch(normalized);
    }

    // ── courses: write ───────────────────────────────────────────────────────

    public async Task<BatchUpsertCoursesResponse> UpsertCoursesAsync(
        IReadOnlyList<UpsertCourseRequest> items, CancellationToken ct = default)
    {
        var results = new CourseUpsertResult[items.Count];
        var accepted = new List<(int Index, string Id, UpsertCourseRequest Request)>();
        var seen = new HashSet<string>(StringComparer.Ordinal);

        for (var i = 0; i < items.Count; i++)
        {
            var req = items[i];
            if (req is null || !TryNormalizeCourseId(req.CourseId, out var id))
            {
                results[i] = FailCourse(req?.CourseId ?? string.Empty, ErrorCodes.InvalidCourseId,
                    "courseId must be an SCNS course id such as EEE3300, EEE3300L or NUR4826-UWF.");
                continue;
            }
            var validation = await _courseValidator.ValidateAsync(req, ct);
            if (!validation.IsValid)
            {
                results[i] = FailCourse(id, ErrorCodes.ValidationError, "One or more validation errors occurred.",
                    validation.Errors.Select(e => new FieldError(e.PropertyName, e.ErrorMessage)).ToList());
                continue;
            }
            if (!seen.Add(id))
            {
                results[i] = FailCourse(id, ErrorCodes.ValidationError, "The same courseId appears more than once in this batch.");
                continue;
            }
            accepted.Add((i, id, req));
        }

        if (accepted.Count > 0)
        {
            // Everything the batch touches is loaded up front: one query per table, not per row.
            var ids = accepted.Select(a => a.Id).ToList();
            var courses = await _db.TaxonomyCourses
                .Where(c => ids.Contains(c.CourseId))
                .ToDictionaryAsync(c => c.CourseId, StringComparer.Ordinal, ct);
            var offerings = (await _db.CourseOfferings.Where(o => ids.Contains(o.CourseId)).ToListAsync(ct))
                .GroupBy(o => o.CourseId)
                .ToDictionary(g => g.Key, g => g.ToList(), StringComparer.Ordinal);
            var nodeKeys = (await _db.TaxonomyNodes.AsNoTracking().Select(n => n.Key).ToListAsync(ct))
                .ToHashSet(StringComparer.Ordinal);
            var institutions = await _db.Institutions.ToDictionaryAsync(i => i.Code, StringComparer.Ordinal, ct);
            var now = DateTime.UtcNow;

            foreach (var (index, id, req) in accepted)
                results[index] = ApplyCourse(id, req, courses, offerings, nodeKeys, institutions, now);

            if (results.Any(r => r.Outcome is Outcomes.Created or Outcomes.Updated))
            {
                await _db.SaveChangesAsync(ct);
                SiteCache.InvalidateCounts(_cache);
            }
        }

        return new BatchUpsertCoursesResponse(
            results.Count(r => r.Outcome == Outcomes.Created),
            results.Count(r => r.Outcome == Outcomes.Updated),
            results.Count(r => r.Outcome == Outcomes.Unchanged),
            results.Count(r => r.Outcome == Outcomes.Failed),
            results);
    }

    private CourseUpsertResult ApplyCourse(
        string id, UpsertCourseRequest req,
        Dictionary<string, TaxonomyCourse> courses,
        Dictionary<string, List<CourseOffering>> offerings,
        HashSet<string> nodeKeys,
        Dictionary<string, Institution> institutions,
        DateTime now)
    {
        // Resolve everything that can fail before touching any entity, so a failed row changes nothing.
        var explicitKey = string.IsNullOrWhiteSpace(req.TaxonomyKey) ? null : req.TaxonomyKey.Trim().ToUpperInvariant();
        if (explicitKey is not null && !nodeKeys.Contains(explicitKey))
            return FailCourse(id, ErrorCodes.TaxonomyNodeNotFound, $"Taxonomy key '{req.TaxonomyKey}' does not exist.");

        var title = req.Title!.Trim();
        var created = false;
        var changed = false;

        if (!courses.TryGetValue(id, out var course))
        {
            var key = explicitKey ?? PrefixKey(id, nodeKeys);
            if (key is null)
                return FailCourse(id, ErrorCodes.TaxonomyPlacementRequired,
                    $"No taxonomy node matches the prefix of {id}. Specify the node via 'taxonomyKey'.");

            course = new TaxonomyCourse
            {
                CourseId = id,
                Level3Key = key,
                Title = title,
                IsActive = req.IsActive ?? true,
                Source = CourseSource.Catalog,
                CreatedUtc = now
            };
            _db.TaxonomyCourses.Add(course);
            courses[id] = course;
            created = true;
        }
        else
        {
            if (explicitKey is not null && course.Level3Key != explicitKey)
            {
                course.Level3Key = explicitKey;
                changed = true;
            }

            // The placeholder (the course id itself) never replaces a real title.
            var sentPlaceholder = !CourseTitles.IsReal(id, title);
            if (course.Title != title && (!sentPlaceholder || !CourseTitles.IsReal(id, course.Title)))
            {
                course.Title = title;
                changed = true;
            }

            if (req.IsActive.HasValue && course.IsActive != req.IsActive.Value)
            {
                course.IsActive = req.IsActive.Value;
                changed = true;
            }
        }

        if (req.StateTitle is not null)
        {
            var stateTitle = Clean(req.StateTitle);
            if (course.StateTitle != stateTitle) { course.StateTitle = stateTitle; changed = true; }
        }
        if (req.CreditHours.HasValue && course.CreditHours != req.CreditHours)
        {
            course.CreditHours = req.CreditHours;
            changed = true;
        }
        if (req.ContactHours.HasValue && course.ContactHours != req.ContactHours)
        {
            course.ContactHours = req.ContactHours;
            changed = true;
        }

        if (req.Offerings is not null &&
            ApplyOfferings(course, req.Offerings, req.ReplaceOfferings ?? true, offerings, institutions, now))
            changed = true;

        if (created || changed) course.UpdatedUtc = now;
        return new CourseUpsertResult(id, created ? Outcomes.Created : changed ? Outcomes.Updated : Outcomes.Unchanged,
            course.Level3Key);
    }

    private bool ApplyOfferings(
        TaxonomyCourse course, IReadOnlyList<CourseOfferingInput> inputs, bool replace,
        Dictionary<string, List<CourseOffering>> offerings,
        Dictionary<string, Institution> institutions,
        DateTime now)
    {
        var changed = false;
        if (!offerings.TryGetValue(course.CourseId, out var current))
        {
            current = [];
            offerings[course.CourseId] = current;
        }

        var sent = new HashSet<string>(StringComparer.Ordinal);
        foreach (var input in inputs)
        {
            var code = input.Institution!.Trim().ToUpperInvariant();
            if (!sent.Add(code)) continue;

            // An unknown code becomes a code-only institution; its name can follow later.
            if (!institutions.ContainsKey(code))
            {
                var institution = new Institution { Code = code, UpdatedUtc = now };
                _db.Institutions.Add(institution);
                institutions[code] = institution;
            }

            var title = Clean(input.Title);
            var active = input.IsActive ?? true;
            var offering = current.FirstOrDefault(o => o.InstitutionCode == code);
            if (offering is null)
            {
                offering = new CourseOffering
                {
                    CourseId = course.CourseId,
                    InstitutionCode = code,
                    InstitutionTitle = title,
                    Credits = input.Credits,
                    ClockHours = input.ClockHours,
                    IsActive = active,
                    UpdatedUtc = now
                };
                _db.CourseOfferings.Add(offering);
                current.Add(offering);
                changed = true;
            }
            else if (offering.InstitutionTitle != title || offering.Credits != input.Credits ||
                     offering.ClockHours != input.ClockHours || offering.IsActive != active)
            {
                offering.InstitutionTitle = title;
                offering.Credits = input.Credits;
                offering.ClockHours = input.ClockHours;
                offering.IsActive = active;
                offering.UpdatedUtc = now;
                changed = true;
            }
        }

        if (replace)
        {
            foreach (var stale in current.Where(o => !sent.Contains(o.InstitutionCode)).ToList())
            {
                _db.CourseOfferings.Remove(stale);
                current.Remove(stale);
                changed = true;
            }
        }

        var activeCount = current.Count(o => o.IsActive);
        if (course.OfferingCount != activeCount)
        {
            course.OfferingCount = activeCount;
            changed = true;
        }
        return changed;
    }

    /// <summary>
    /// Removes a course created in error. Refused when anything hangs off it — a guide (or stub),
    /// modules, or guide requests — because those are someone's work or demand; set it inactive instead.
    /// </summary>
    public async Task<DeleteOutcome> DeleteCourseAsync(string courseId, CancellationToken ct = default)
    {
        var id = courseId.Trim().ToUpperInvariant();
        if (id == WellKnownIds.OrphanCourseId) return DeleteOutcome.NotFound;

        var course = await _db.TaxonomyCourses.FirstOrDefaultAsync(c => c.CourseId == id, ct);
        if (course is null) return DeleteOutcome.NotFound;

        var hasContent = await _db.CurriculumGuides.AnyAsync(g => g.CourseId == id, ct)
                         || await _db.Modules.AnyAsync(m => m.CourseId == id, ct)
                         || await _db.GuideRequests.AnyAsync(r => r.CourseId == id, ct);
        if (hasContent) return DeleteOutcome.HasContent;

        _db.TaxonomyCourses.Remove(course);          // offerings go with it (cascade)
        await _db.SaveChangesAsync(ct);
        SiteCache.InvalidateCounts(_cache);
        return DeleteOutcome.Deleted;
    }

    // ── courses: read ────────────────────────────────────────────────────────

    public async Task<PagedResult<CatalogCourseDto>> ListCoursesAsync(
        string? prefix, bool? hasGuide, bool? active, DateTime? updatedSince,
        int page, int pageSize, CancellationToken ct = default)
    {
        IQueryable<TaxonomyCourse> query = _db.TaxonomyCourses.AsNoTracking()
            .Where(c => c.CourseId != WellKnownIds.OrphanCourseId);

        if (!string.IsNullOrWhiteSpace(prefix))
        {
            var p = prefix.Trim().ToUpperInvariant();
            query = query.Where(c => c.CourseId.StartsWith(p));
        }
        if (active.HasValue)
        {
            var isActive = active.Value;
            query = query.Where(c => c.IsActive == isActive);
        }
        if (updatedSince.HasValue)
        {
            var since = updatedSince.Value.Kind == DateTimeKind.Unspecified
                ? DateTime.SpecifyKind(updatedSince.Value, DateTimeKind.Utc)
                : updatedSince.Value.ToUniversalTime();
            query = query.Where(c => c.UpdatedUtc >= since);
        }
        if (hasGuide == true)
            query = query.Where(c => _db.CurriculumGuides.Any(g => g.CourseId == c.CourseId && g.Title != CurriculumGuide.StubTitle));
        else if (hasGuide == false)
            query = query.Where(c => !_db.CurriculumGuides.Any(g => g.CourseId == c.CourseId && g.Title != CurriculumGuide.StubTitle));

        var total = await query.CountAsync(ct);
        var items = await Project(query.OrderBy(c => c.CourseId).Skip((page - 1) * pageSize).Take(pageSize))
            .ToListAsync(ct);

        return new PagedResult<CatalogCourseDto>(items, total, page, pageSize,
            (int)Math.Ceiling(total / (double)pageSize));
    }

    public async Task<CatalogCourseDetailDto?> GetCourseAsync(string courseId, CancellationToken ct = default)
    {
        var id = courseId.Trim().ToUpperInvariant();
        var course = await Project(_db.TaxonomyCourses.AsNoTracking()
                .Where(c => c.CourseId == id && c.CourseId != WellKnownIds.OrphanCourseId))
            .FirstOrDefaultAsync(ct);
        if (course is null) return null;

        var offerings = await _db.CourseOfferings.AsNoTracking()
            .Where(o => o.CourseId == id)
            .OrderBy(o => o.InstitutionCode)
            .Select(o => new CourseOfferingDto(o.InstitutionCode, o.Institution.Name, o.InstitutionTitle,
                o.Credits, o.ClockHours, o.IsActive))
            .ToListAsync(ct);

        return new CatalogCourseDetailDto(course, offerings);
    }

    private IQueryable<CatalogCourseDto> Project(IQueryable<TaxonomyCourse> query) =>
        query.Select(c => new CatalogCourseDto(
            c.CourseId, c.Title, c.StateTitle, c.CreditHours, c.ContactHours, c.Level3Key,
            c.IsActive, c.Source.ToString(),
            _db.CurriculumGuides.Any(g => g.CourseId == c.CourseId && g.Title != CurriculumGuide.StubTitle),
            c.OfferingCount, c.CreatedUtc, c.UpdatedUtc));

    // ── institutions ─────────────────────────────────────────────────────────

    public Task<List<InstitutionDto>> ListInstitutionsAsync(CancellationToken ct = default) =>
        _db.Institutions.AsNoTracking()
            .OrderBy(i => i.Code)
            .Select(i => new InstitutionDto(i.Code, i.Name, i.Sector, i.ScnsId, i.Offerings.Count(o => o.IsActive)))
            .ToListAsync(ct);

    public async Task<BatchUpsertInstitutionsResponse> UpsertInstitutionsAsync(
        IReadOnlyList<UpsertInstitutionRequest> items, CancellationToken ct = default)
    {
        var institutions = await _db.Institutions.ToDictionaryAsync(i => i.Code, StringComparer.Ordinal, ct);
        var results = new List<InstitutionUpsertResult>(items.Count);
        var seen = new HashSet<string>(StringComparer.Ordinal);
        var now = DateTime.UtcNow;

        foreach (var req in items)
        {
            if (req is null)
            {
                results.Add(new InstitutionUpsertResult(string.Empty, Outcomes.Failed, ErrorCodes.ValidationError, "Empty item."));
                continue;
            }
            var validation = await _institutionValidator.ValidateAsync(req, ct);
            if (!validation.IsValid)
            {
                results.Add(new InstitutionUpsertResult(req.Code ?? string.Empty, Outcomes.Failed, ErrorCodes.ValidationError,
                    "One or more validation errors occurred.",
                    validation.Errors.Select(e => new FieldError(e.PropertyName, e.ErrorMessage)).ToList()));
                continue;
            }

            var code = req.Code!.Trim().ToUpperInvariant();
            if (!seen.Add(code))
            {
                results.Add(new InstitutionUpsertResult(code, Outcomes.Failed, ErrorCodes.ValidationError,
                    "The same code appears more than once in this batch."));
                continue;
            }

            var created = false;
            var changed = false;
            if (!institutions.TryGetValue(code, out var institution))
            {
                institution = new Institution { Code = code };
                _db.Institutions.Add(institution);
                institutions[code] = institution;
                created = true;
            }
            if (req.Name is not null && institution.Name != Clean(req.Name)) { institution.Name = Clean(req.Name); changed = true; }
            if (req.Sector is not null && institution.Sector != Clean(req.Sector)) { institution.Sector = Clean(req.Sector); changed = true; }
            if (req.ScnsId is not null && institution.ScnsId != Clean(req.ScnsId)) { institution.ScnsId = Clean(req.ScnsId); changed = true; }
            if (created || changed) institution.UpdatedUtc = now;

            results.Add(new InstitutionUpsertResult(code,
                created ? Outcomes.Created : changed ? Outcomes.Updated : Outcomes.Unchanged));
        }

        await _db.SaveChangesAsync(ct);
        return new BatchUpsertInstitutionsResponse(
            results.Count(r => r.Outcome == Outcomes.Created),
            results.Count(r => r.Outcome == Outcomes.Updated),
            results.Count(r => r.Outcome == Outcomes.Unchanged),
            results.Count(r => r.Outcome == Outcomes.Failed),
            results);
    }

    // ── helpers ──────────────────────────────────────────────────────────────

    /// <summary>The letters before the first digit ("EEE" from "EEE3300L"), when a taxonomy node has that key.</summary>
    private static string? PrefixKey(string courseId, HashSet<string> nodeKeys)
    {
        var i = 0;
        while (i < courseId.Length && char.IsLetter(courseId[i])) i++;
        if (i == 0 || i >= courseId.Length || !char.IsDigit(courseId[i])) return null;
        var prefix = courseId[..i];
        return nodeKeys.Contains(prefix) ? prefix : null;
    }

    private static CourseUpsertResult FailCourse(string courseId, string code, string message,
        IReadOnlyList<FieldError>? fields = null) =>
        new(courseId, Outcomes.Failed, null, code, message, fields);

    private static string? Clean(string? s) => string.IsNullOrWhiteSpace(s) ? null : s.Trim();
}
