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
using ProgramEntity = PreseMakerRepo.Core.Models.Program;

namespace PreseMakerRepo.Api.Controllers;

/// <summary>
/// Programmes — "a major that supports a career path and is being offered by a Florida school"
/// (Ron, 2026-09-17), sitting one level above a degree.
/// <para>
/// Reads are public; writes are admin-only and come from the <c>Tools/</c> pipeline, the same
/// shape as curriculum guides and career paths — authored as JSON, validated, pushed. ⚠ This
/// controller exists so that adding a programme stops needing a redeploy: until 2026-09-19 the
/// only way in was <c>Data/Seed/programs.json</c>, which ships inside the build.
/// </para>
/// <para>
/// ⚠⚠ A programme owns NO school list. Which institutions offer it is derived here from
/// <see cref="InstitutionAward"/> by CIP prefix, and is stored nowhere.
/// </para>
/// </summary>
[ApiController]
[Route("api/v1/programs")]
public class ProgramsController : ControllerBase
{
    private readonly AppDbContext _db;
    public ProgramsController(AppDbContext db) => _db = db;

    /// <summary>
    /// GET /api/v1/programs — published programmes, each with the number of Florida schools
    /// awarding in its CIP codes. <c>?includeUnpublished=true</c> adds drafts, for admins only.
    /// </summary>
    [HttpGet]
    public async Task<IActionResult> List([FromQuery] bool includeUnpublished = false)
    {
        if (includeUnpublished && !User.IsInRole("Administrator"))
            return StatusCode(StatusCodes.Status403Forbidden, ApiResponse<object?>.Fail(
                ErrorCodes.Forbidden, "Only an administrator can list unpublished programmes."));

        var programs = await _db.Programs.AsNoTracking()
            .Where(p => includeUnpublished || p.IsPublished)
            .Include(p => p.Cips)
            .Include(p => p.CareerPaths)
            .OrderBy(p => p.SortOrder).ThenBy(p => p.Name)
            .ToListAsync();

        var awards = await LoadAwardKeysAsync();

        var list = programs.Select(p => new ProgramSummaryDto(
            p.Slug, p.Name, p.Description,
            CountSchools(awards, p.Cips.Select(c => c.CipCode)),
            p.Cips.Count, p.CareerPaths.Count, p.IsPublished, p.UpdatedUtc)).ToList();

        return Ok(ApiResponse<List<ProgramSummaryDto>>.Ok(list));
    }

    /// <summary>GET /api/v1/programs/{slug} — one programme, with its derived school list.</summary>
    [HttpGet("{slug}")]
    public async Task<IActionResult> Get(string slug)
    {
        var p = await _db.Programs.AsNoTracking()
            .Include(x => x.Cips)
            .Include(x => x.CareerPaths).ThenInclude(l => l.CareerPath)
            .Include(x => x.Related).ThenInclude(r => r.RelatedProgram!).ThenInclude(rp => rp.Cips)
            .Include(x => x.RelatedFrom).ThenInclude(r => r.Program!).ThenInclude(op => op.Cips)
            .FirstOrDefaultAsync(x => x.Slug == slug);

        if (p is null || (!p.IsPublished && !User.IsInRole("Administrator")))
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.ProgramNotFound,
                "No published programme with that slug."));

        var prefixes = p.Cips.OrderBy(c => c.SortOrder).Select(c => c.CipCode).ToList();
        var awards = await _db.InstitutionAwards.AsNoTracking().ToListAsync();
        var mine = awards.Where(a => prefixes.Any(pre => a.CipCode.StartsWith(pre))).ToList();

        var titles = await CipTitlesAsync(prefixes);

        // ⚠ Ordered by NAME, not by completions — the same rule the page follows, because a
        // ranking would read as a recommendation the data does not support.
        var schools = mine
            .GroupBy(a => a.UnitId)
            .Select(g => new ProgramSchoolDto(
                g.Key,
                g.First().InstitutionName,
                g.Select(x => x.InstitutionCode).FirstOrDefault(c => c != null),
                g.Select(x => x.AwardLevel).Distinct().OrderBy(x => x).ToList(),
                g.Sum(x => x.Completions)))
            .OrderBy(s => s.Name)
            .ToList();

        var dto = new ProgramDto(
            p.Slug, p.Name, p.Description, p.DegreesNote, p.BodyHtml, p.IsPublished, p.SortOrder,
            p.CreatedUtc, p.UpdatedUtc,
            p.Cips.OrderBy(c => c.SortOrder)
                  .Select(c => new ProgramCipDto(
                      c.CipCode, titles.GetValueOrDefault(Normalize(c.CipCode)), c.Note,
                      awards.Where(a => a.CipCode.StartsWith(c.CipCode))
                            .Select(a => a.UnitId).Distinct().Count()))
                  .ToList(),
            schools,
            mine.Select(a => a.AwardLevel).Distinct().OrderBy(x => x).ToList(),
            mine.Count > 0 ? mine.Max(a => a.Year) : 0,
            p.CareerPaths.Where(l => l.CareerPath!.IsPublished).OrderBy(l => l.SortOrder)
                         .Select(l => new ProgramCareerPathDto(
                             l.CareerPath!.Slug, l.CareerPath.Name, l.Note, l.IsRoute)).ToList(),
            RelatedOf(p, LoadAwardKeys(awards)));

        return Ok(ApiResponse<ProgramDto>.Ok(dto));
    }

    /// <summary>
    /// PUT /api/v1/programs/{slug} — create or replace a programme and its CIP codes.
    /// ⚠ The codes are REPLACED wholesale, so a push is idempotent and a code dropped from the
    /// source document stops counting schools.
    /// </summary>
    [Authorize(Policy = "AdminOnly")]
    [HttpPut("{slug}")]
    public async Task<IActionResult> Upsert(
        string slug,
        [FromBody] UpsertProgramRequest request,
        [FromServices] IValidator<UpsertProgramRequest> validator)
    {
        slug = (slug ?? string.Empty).Trim().ToLowerInvariant();
        if (!System.Text.RegularExpressions.Regex.IsMatch(slug, @"^[a-z0-9]+(-[a-z0-9]+)*$"))
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError,
                "slug must be lowercase words separated by hyphens, e.g. nursing."));

        var vResult = await validator.ValidateAsync(request);
        if (!vResult.IsValid)
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError,
                "One or more validation errors occurred.",
                vResult.Errors.Select(e => new FieldError(e.PropertyName, e.ErrorMessage)).ToList()));

        var codes = (request.Cips ?? []).Select(c => c.CipCode!.Trim()).ToList();
        if (codes.Distinct().Count() != codes.Count)
            return UnprocessableEntity(ApiResponse<object?>.Fail(ErrorCodes.ValidationError,
                "The same CIP code is listed twice."));

        // ⚠ Every code must name a real branch of the seeded tree. A programme filed on a code
        // that does not exist would quietly count zero schools and read as "offered nowhere",
        // which is worse than a refusal.
        var wanted = codes.Select(Normalize).Distinct().ToList();
        var known = await _db.CipNodes.Where(n => wanted.Contains(n.Code))
                                      .Select(n => n.Code).ToListAsync();
        var unknown = wanted.Except(known).ToList();
        if (unknown.Count > 0)
            return UnprocessableEntity(ApiResponse<object?>.Fail(ErrorCodes.CipNodeNotFound,
                $"CIP code(s) not in the seeded tree: {string.Join(", ", unknown)}. " +
                "Widen the seed (Tools/build_cip_seed.py, EXTRA_GROUPS) — a 6-digit code is " +
                "checked against its 4-digit group."));

        var now = DateTime.UtcNow;
        var program = await _db.Programs.Include(p => p.Cips).Include(p => p.Related)
                                        .FirstOrDefaultAsync(p => p.Slug == slug);

        bool created = program is null;
        if (program is null)
        {
            program = new ProgramEntity { Id = Guid.NewGuid(), Slug = slug, CreatedUtc = now };
            _db.Programs.Add(program);
        }
        else
        {
            _db.ProgramCips.RemoveRange(program.Cips);
            _db.ProgramRelations.RemoveRange(program.Related);
        }

        program.Name = request.Name!.Trim();
        program.Description = request.Description!.Trim();
        program.DegreesNote = Blank(request.DegreesNote);
        program.BodyHtml = string.IsNullOrWhiteSpace(request.BodyHtml)
            ? null : Sanitize(request.BodyHtml);
        program.IsPublished = request.IsPublished ?? false;
        program.SortOrder = request.SortOrder ?? 0;
        program.UpdatedUtc = now;

        int order = 0;
        foreach (var c in request.Cips ?? [])
        {
            _db.ProgramCips.Add(new ProgramCip
            {
                Id = Guid.NewGuid(),
                ProgramId = program.Id,
                CipCode = c.CipCode!.Trim(),
                Note = Blank(c.Note),
                SortOrder = order++
            });
        }

        // ⚠ A related programme must already exist, and must not be the programme itself:
        // a dead link on a page whose whole job is to show a student their options is worse
        // than a refusal.
        var wantRel = (request.Related ?? []).Select(r => r.Slug!.Trim().ToLowerInvariant())
                                             .Distinct().ToList();
        if (wantRel.Contains(slug))
            return UnprocessableEntity(ApiResponse<object?>.Fail(ErrorCodes.ValidationError,
                "A programme cannot be related to itself."));

        var relIds = await _db.Programs.Where(x => wantRel.Contains(x.Slug))
                                       .ToDictionaryAsync(x => x.Slug, x => x.Id);
        var missingRel = wantRel.Except(relIds.Keys).ToList();
        if (missingRel.Count > 0)
            return UnprocessableEntity(ApiResponse<object?>.Fail(ErrorCodes.ProgramNotFound,
                $"Unknown related programme slug(s): {string.Join(", ", missingRel)}. " +
                "Push that programme first, or correct the slug."));

        int rorder = 0;
        foreach (var r in request.Related ?? [])
        {
            var target = r.Slug!.Trim().ToLowerInvariant();
            if (target == slug) continue;
            _db.ProgramRelations.Add(new ProgramRelation
            {
                Id = Guid.NewGuid(),
                ProgramId = program.Id,
                RelatedProgramId = relIds[target],
                Note = Blank(r.Note),
                SortOrder = rorder++
            });
        }

        await _db.SaveChangesAsync();

        // A code matching no award at all is reported, not refused: a code can be real and
        // simply have no Florida completions in the award year.
        var awards = await LoadAwardKeysAsync();
        var unmatched = codes.Where(code => !awards.Any(a => a.Cip.StartsWith(code)))
                             .OrderBy(x => x).ToList();

        return Ok(ApiResponse<UpsertProgramResponse>.Ok(new UpsertProgramResponse(
            slug, created ? "created" : "updated", codes.Count,
            CountSchools(awards, codes), wantRel.Count, unmatched)));
    }

    /// <summary>
    /// DELETE /api/v1/programs/{slug}.
    /// ⚠ Refused while a career path names the programme — the link would cascade away silently
    /// and that path's "Programs that lead here" section would lose a row nobody meant to drop.
    /// Unlink it from the path first.
    /// </summary>
    [Authorize(Policy = "AdminOnly")]
    [HttpDelete("{slug}")]
    public async Task<IActionResult> Delete(string slug)
    {
        var program = await _db.Programs
            .Include(p => p.CareerPaths).ThenInclude(l => l.CareerPath)
            .Include(p => p.Related)
            .Include(p => p.RelatedFrom)
            .FirstOrDefaultAsync(p => p.Slug == slug);

        if (program is null)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.ProgramNotFound,
                "No programme with that slug."));

        if (program.CareerPaths.Count > 0)
        {
            var paths = program.CareerPaths.Select(l => l.CareerPath!.Slug).OrderBy(x => x);
            return Conflict(ApiResponse<object?>.Fail(ErrorCodes.ProgramInUse,
                $"Career path(s) name this programme: {string.Join(", ", paths)}. " +
                "Remove it from their documents and push them before deleting it."));
        }

        // Relations pointing AT this programme are RESTRICT, so clear them explicitly rather
        // than letting the delete fail on a foreign key the caller cannot see.
        _db.ProgramRelations.RemoveRange(program.Related);
        _db.ProgramRelations.RemoveRange(program.RelatedFrom);
        _db.Programs.Remove(program);   // CIP rows cascade
        await _db.SaveChangesAsync();
        return Ok(ApiResponse<MessageResponse>.Ok(new MessageResponse("Programme deleted.")));
    }

    // ── Helpers ──────────────────────────────────────────────────────────────

    private record AwardKey(string UnitId, string Cip);

    /// <summary>
    /// ⚠ One read, then matched in memory — the same shape the pages use. The codes are
    /// PREFIXES, and EF cannot translate a prefix match across an arbitrary list of them.
    /// </summary>
    private async Task<List<AwardKey>> LoadAwardKeysAsync() =>
        await _db.InstitutionAwards.AsNoTracking()
            .Select(a => new AwardKey(a.UnitId, a.CipCode)).ToListAsync();

    private static List<AwardKey> LoadAwardKeys(List<InstitutionAward> awards) =>
        awards.Select(a => new AwardKey(a.UnitId, a.CipCode)).ToList();

    /// <summary>
    /// Neighbouring programmes, read in BOTH directions: the ones this programme names, then the
    /// ones that name it. ⚠ A connection authored on only one side still shows on both, because a
    /// student who lands on the other page needs it just as much — the reverse entry carries the
    /// other programme's note and is flagged <c>mutual: false</c>.
    /// </summary>
    private static List<ProgramRelatedDto> RelatedOf(ProgramEntity p, List<AwardKey> awards)
    {
        var seen = new HashSet<string>();
        var list = new List<ProgramRelatedDto>();

        foreach (var r in p.Related.OrderBy(r => r.SortOrder))
        {
            var t = r.RelatedProgram;
            if (t is null || !t.IsPublished || !seen.Add(t.Slug)) continue;
            list.Add(new ProgramRelatedDto(t.Slug, t.Name, r.Note,
                CountSchools(awards, t.Cips.Select(c => c.CipCode)), true));
        }

        foreach (var r in p.RelatedFrom.OrderBy(r => r.SortOrder))
        {
            var o = r.Program;
            if (o is null || !o.IsPublished || !seen.Add(o.Slug)) continue;
            list.Add(new ProgramRelatedDto(o.Slug, o.Name, r.Note,
                CountSchools(awards, o.Cips.Select(c => c.CipCode)), false));
        }

        return list;
    }

    private static int CountSchools(List<AwardKey> awards, IEnumerable<string> prefixes)
    {
        var list = prefixes.ToList();
        return awards.Where(a => list.Any(p => a.Cip.StartsWith(p)))
                     .Select(a => a.UnitId).Distinct().Count();
    }

    /// <summary>
    /// The tree node a code is checked against: "15." → "15", and a 6-digit code → its 4-digit
    /// group, since the seeded tree stops at four digits.
    /// </summary>
    private static string Normalize(string code)
    {
        code = code.Trim().TrimEnd('.');
        return code.Length == 7 ? code[..5] : code;   // 14.1901 → 14.19
    }

    private async Task<Dictionary<string, string>> CipTitlesAsync(IEnumerable<string> codes)
    {
        var wanted = codes.Select(Normalize).Distinct().ToList();
        return await _db.CipNodes.AsNoTracking().Where(n => wanted.Contains(n.Code))
            .ToDictionaryAsync(n => n.Code, n => n.Title);
    }

    private static string? Blank(string? s) => string.IsNullOrWhiteSpace(s) ? null : s.Trim();

    // Same allow-list as the career-path and taxonomy editors: structure and links, no styling,
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
