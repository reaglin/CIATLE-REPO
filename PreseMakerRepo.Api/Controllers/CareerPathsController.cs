using FluentValidation;
using Ganss.Xss;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Api.Models;
using PreseMakerRepo.Api.Models.Requests;
using PreseMakerRepo.Api.Models.Responses;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Api.Controllers;

/// <summary>
/// Career paths, and the CIP tree they are filed on.
/// <para>
/// Reads are public; writes are admin-only and come from the <c>Tools/</c> pipeline, the same
/// shape as curriculum guides — authored as JSON, validated, pushed. ⚠ A path is CURATED:
/// nothing here derives a course list from classification data or course-code arithmetic.
/// </para>
/// </summary>
[ApiController]
[Route("api/v1")]
public class CareerPathsController : ControllerBase
{
    private readonly AppDbContext _db;
    public CareerPathsController(AppDbContext db) => _db = db;

    // ── CIP tree ─────────────────────────────────────────────────────────────

    /// <summary>GET /api/v1/cip — the browse framework. <c>?parent=51</c> narrows to one series.</summary>
    [HttpGet("cip")]
    public async Task<IActionResult> GetCip([FromQuery] string? parent, [FromQuery] int? level)
    {
        var q = _db.CipNodes.AsNoTracking().Where(n => n.IsActive);
        if (!string.IsNullOrWhiteSpace(parent)) q = q.Where(n => n.ParentCode == parent);
        if (level.HasValue) q = q.Where(n => n.Level == level.Value);

        var nodes = await q.OrderBy(n => n.Code)
            .Select(n => new CipNodeDto(n.Code, n.Level, n.Title, n.Definition, n.Examples,
                                        n.ParentCode, n.ChildCount))
            .ToListAsync();

        return Ok(ApiResponse<List<CipNodeDto>>.Ok(nodes));
    }

    // ── Career paths ─────────────────────────────────────────────────────────

    /// <summary>GET /api/v1/career-paths — published paths, optionally within one CIP branch.</summary>
    [HttpGet("career-paths")]
    public async Task<IActionResult> List([FromQuery] string? cip)
    {
        var q = _db.CareerPaths.AsNoTracking().Where(p => p.IsPublished);
        if (!string.IsNullOrWhiteSpace(cip))
            q = q.Where(p => p.CipCode == cip || p.CipCode.StartsWith(cip + "."));

        var paths = await q.OrderBy(p => p.SortOrder).ThenBy(p => p.Name)
            .Select(p => new CareerPathSummaryDto(
                p.Slug, p.Name, p.CipCode, p.Cip!.Title, p.Description, p.SocCode,
                p.Courses.Count, p.UpdatedUtc))
            .ToListAsync();

        return Ok(ApiResponse<List<CareerPathSummaryDto>>.Ok(paths));
    }

    /// <summary>GET /api/v1/career-paths/{slug} — one path, whole.</summary>
    [HttpGet("career-paths/{slug}")]
    public async Task<IActionResult> Get(string slug)
    {
        var path = await _db.CareerPaths.AsNoTracking()
            .Include(p => p.Cip)
            .Include(p => p.Cips).ThenInclude(c => c.Cip)
            .Include(p => p.ProgramLinks!).ThenInclude(l => l.Program)
            .Include(p => p.Courses)
            .Include(p => p.Sources)
            .FirstOrDefaultAsync(p => p.Slug == slug && p.IsPublished);

        if (path is null)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.CareerPathNotFound,
                "No published career path with that slug."));

        return Ok(ApiResponse<CareerPathDto>.Ok(ToDto(path)));
    }

    /// <summary>
    /// PUT /api/v1/career-paths/{slug} — create or replace a path, with its courses and sources.
    /// ⚠ Courses and sources are REPLACED wholesale, so a push is idempotent and a course
    /// dropped from the source document actually leaves the page.
    /// </summary>
    [Authorize(Policy = "AdminOnly")]
    [HttpPut("career-paths/{slug}")]
    public async Task<IActionResult> Upsert(
        string slug,
        [FromBody] UpsertCareerPathRequest request,
        [FromServices] IValidator<UpsertCareerPathRequest> validator)
    {
        slug = (slug ?? string.Empty).Trim().ToLowerInvariant();
        if (!System.Text.RegularExpressions.Regex.IsMatch(slug, @"^[a-z0-9]+(-[a-z0-9]+)*$"))
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError,
                "slug must be lowercase words separated by hyphens, e.g. registered-nurse."));

        var vResult = await validator.ValidateAsync(request);
        if (!vResult.IsValid)
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError,
                "One or more validation errors occurred.",
                vResult.Errors.Select(e => new FieldError(e.PropertyName, e.ErrorMessage)).ToList()));

        // ⚠ Every CIP node must already exist. A path filed on a code the tree does not
        // carry would be unreachable by browsing, which is the only way anyone finds one.
        var wanted = new List<string> { request.CipCode! };
        wanted.AddRange((request.CipCodes ?? []).Select(c => c.CipCode!.Trim()));
        // The primary may legitimately repeat in the list; file it once.
        var distinctCips = wanted.Select(c => c.Trim()).Distinct().ToList();

        var known = await _db.CipNodes.Where(n => distinctCips.Contains(n.Code))
                                      .Select(n => n.Code).ToListAsync();
        var unknown = distinctCips.Except(known).ToList();
        if (unknown.Count > 0)
            return UnprocessableEntity(ApiResponse<object?>.Fail(ErrorCodes.CipNodeNotFound,
                $"CIP code(s) not in the seeded tree: {string.Join(", ", unknown)}. " +
                "Widen the seed (Tools/build_cip_seed.py, EXTRA_GROUPS) or file the path elsewhere."));

        var now = DateTime.UtcNow;
        var links = await _db.CareerPathPrograms.ToListAsync();
        var path = await _db.CareerPaths
            .Include(p => p.Cips)
            .Include(p => p.Courses)
            .Include(p => p.Sources)
            .FirstOrDefaultAsync(p => p.Slug == slug);

        bool created = path is null;
        if (path is null)
        {
            path = new CareerPath { Id = Guid.NewGuid(), Slug = slug, CreatedUtc = now };
            _db.CareerPaths.Add(path);
        }
        else
        {
            _db.CareerPathCips.RemoveRange(path.Cips);
            _db.CareerPathPrograms.RemoveRange(links.Where(l => l.CareerPathId == path.Id));
            _db.CareerPathCourses.RemoveRange(path.Courses);
            _db.CareerPathSources.RemoveRange(path.Sources);
        }

        path.Name = request.Name!.Trim();
        path.CipCode = request.CipCode!.Trim();
        path.Description = request.Description!.Trim();
        path.SocCode = Blank(request.SocCode);
        path.CredentialNote = Blank(request.CredentialNote);
        path.BodyHtml = string.IsNullOrWhiteSpace(request.BodyHtml) ? null : Sanitize(request.BodyHtml);
        path.IsPublished = request.IsPublished ?? false;
        path.SortOrder = request.SortOrder ?? 0;
        path.UpdatedUtc = now;

        // ⚠ A programme must already be seeded. A link to a slug that does not exist would
        // render as a dead reference on the career page.
        var wantProgs = (request.Programs ?? []).Select(x => x.Slug!.Trim()).Distinct().ToList();
        var progs = await _db.Programs.Where(p => wantProgs.Contains(p.Slug))
                                      .ToDictionaryAsync(p => p.Slug, p => p.Id);
        var missingProgs = wantProgs.Except(progs.Keys).ToList();
        if (missingProgs.Count > 0)
            return UnprocessableEntity(ApiResponse<object?>.Fail(ErrorCodes.ValidationError,
                $"Unknown programme slug(s): {string.Join(", ", missingProgs)}."));

        int porder = 0;
        foreach (var pr in request.Programs ?? [])
        {
            _db.CareerPathPrograms.Add(new CareerPathProgram
            {
                Id = Guid.NewGuid(),
                CareerPathId = path.Id,
                ProgramId = progs[pr.Slug!.Trim()],
                Note = Blank(pr.Note),
                SortOrder = porder++
            });
        }

        int order = 0;
        // ⚠ The primary is NOT duplicated here -- it lives on the path itself, and the
        // browse pages union the two, so filing it twice would list the path twice.
        foreach (var c in (request.CipCodes ?? []).Where(c => c.CipCode!.Trim() != path.CipCode))
        {
            _db.CareerPathCips.Add(new CareerPathCip
            {
                Id = Guid.NewGuid(),
                CareerPathId = path.Id,
                CipCode = c.CipCode!.Trim(),
                Note = Blank(c.Note),
                SortOrder = order++
            });
        }

        order = 0;
        foreach (var c in request.Courses ?? [])
        {
            _db.CareerPathCourses.Add(new CareerPathCourse
            {
                Id = Guid.NewGuid(),
                CareerPathId = path.Id,
                CourseId = c.CourseId!.Trim().ToUpperInvariant(),
                Reason = c.Reason!.Trim(),
                VariantNote = Blank(c.VariantNote),
                SortOrder = order++
            });
        }

        order = 0;
        foreach (var s in request.Sources ?? [])
        {
            _db.CareerPathSources.Add(new CareerPathSource
            {
                Id = Guid.NewGuid(),
                CareerPathId = path.Id,
                Label = s.Label!.Trim(),
                Url = s.Url!.Trim(),
                Note = Blank(s.Note),
                SortOrder = order++
            });
        }

        await _db.SaveChangesAsync();

        // Courses named but not listed: the push response is where the pipeline learns it
        // owes the catalog their base data, so a path never points at a page that is not there.
        var ids = (request.Courses ?? []).Select(c => c.CourseId!.Trim().ToUpperInvariant()).ToList();
        var listed = await _db.TaxonomyCourses.AsNoTracking()
            .Where(c => ids.Contains(c.CourseId)).Select(c => c.CourseId).ToListAsync();
        var missing = ids.Except(listed).OrderBy(x => x).ToList();

        return Ok(ApiResponse<UpsertCareerPathResponse>.Ok(new UpsertCareerPathResponse(
            slug, created ? "created" : "updated", distinctCips.Count, ids.Count,
            (request.Sources ?? []).Count, missing)));
    }

    /// <summary>DELETE /api/v1/career-paths/{slug} — removes the path and its rows.</summary>
    [Authorize(Policy = "AdminOnly")]
    [HttpDelete("career-paths/{slug}")]
    public async Task<IActionResult> Delete(string slug)
    {
        var path = await _db.CareerPaths.FirstOrDefaultAsync(p => p.Slug == slug);
        if (path is null)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.CareerPathNotFound,
                "No career path with that slug."));

        _db.CareerPaths.Remove(path);   // courses and sources cascade
        await _db.SaveChangesAsync();
        return Ok(ApiResponse<MessageResponse>.Ok(new MessageResponse("Career path deleted.")));
    }

    // ── Helpers ──────────────────────────────────────────────────────────────

    private static string? Blank(string? s) => string.IsNullOrWhiteSpace(s) ? null : s.Trim();

    private static CareerPathDto ToDto(CareerPath p) => new(
        p.Slug, p.Name, p.CipCode, p.Cip?.Title, p.Description, p.SocCode, p.CredentialNote,
        p.BodyHtml, p.SortOrder, p.CreatedUtc, p.UpdatedUtc,
        p.Cips.OrderBy(c => c.SortOrder)
              .Select(c => new CareerPathCipDto(c.CipCode, c.Cip?.Title, c.Note)).ToList(),
        (p.ProgramLinks ?? []).OrderBy(l => l.SortOrder)
              .Select(l => new CareerPathProgramDto(l.Program!.Slug, l.Program.Name, l.Note, 0)).ToList(),
        p.Courses.OrderBy(c => c.SortOrder)
                 .Select(c => new CareerPathCourseDto(c.CourseId, c.Reason, c.VariantNote)).ToList(),
        p.Sources.OrderBy(s => s.SortOrder)
                 .Select(s => new CareerPathSourceDto(s.Label, s.Url, s.Note)).ToList());

    // Same allow-list as the admin taxonomy editor: structure and links, no styling,
    // no scripts, no attributes that can carry behaviour.
    private static readonly HtmlSanitizer _sanitizer = BuildSanitizer();

    private static HtmlSanitizer BuildSanitizer()
    {
        var s = new HtmlSanitizer();
        s.AllowedTags.Clear();
        foreach (var tag in new[]
        {
            "h2","h3","h4","h5","h6","p","br","hr","blockquote",
            "ul","ol","li","a","strong","em","b","i","u","code",
            "table","thead","tbody","tr","th","td","span","div"
        })
            s.AllowedTags.Add(tag);

        s.AllowedAttributes.Clear();
        s.AllowedAttributes.Add("href");
        s.AllowedAttributes.Add("target");
        s.AllowedAttributes.Add("rel");
        s.AllowedAttributes.Add("class");
        s.AllowedCssProperties.Clear();
        return s;
    }

    private static string Sanitize(string input) => _sanitizer.Sanitize(input);
}
