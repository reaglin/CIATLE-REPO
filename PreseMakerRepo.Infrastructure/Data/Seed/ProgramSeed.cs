using System.Text.Json;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;
using ProgramEntity = PreseMakerRepo.Core.Models.Program;

namespace PreseMakerRepo.Infrastructure.Seed;

/// <summary>
/// Seeds the curated programmes and the IPEDS award cross-reference, both built by
/// <c>Tools/build_program_seed.py</c>. Idempotent; follows <see cref="CipSeed"/>.
/// <para>
/// ⚠ The two files are seeded independently and neither depends on the other. A programme is
/// curated content; the awards are federal data refreshed once a year. Which schools offer a
/// programme is computed from the two at read time and is stored nowhere — Ron, 2026-09-17:
/// "I am going to decouple programs from schools."
/// </para>
/// </summary>
public class ProgramSeed
{
    private readonly AppDbContext _db;
    private readonly IConfiguration _config;
    private readonly ILogger<ProgramSeed> _logger;

    private static readonly JsonSerializerOptions JsonOptions = new() { PropertyNameCaseInsensitive = true };

    public ProgramSeed(AppDbContext db, IConfiguration config, ILogger<ProgramSeed> logger)
    {
        _db = db;
        _config = config;
        _logger = logger;
    }

    public async Task SeedAsync(CancellationToken ct = default)
    {
        await SeedProgramsAsync(ct);
        await SeedAwardsAsync(ct);
    }

    private async Task SeedProgramsAsync(CancellationToken ct)
    {
        var path = _config["Programs:ConfigPath"] ?? "Data/Seed/programs.json";
        if (!File.Exists(path))
        {
            _logger.LogWarning("Programs seed not found at {Path}; skipping.", path);
            return;
        }

        await using var stream = File.OpenRead(path);
        var file = await JsonSerializer.DeserializeAsync<ProgramFileJson>(stream, JsonOptions, ct);
        var items = file?.Programs ?? [];
        int added = 0, updated = 0;

        foreach (var j in items)
        {
            var p = await _db.Programs.Include(x => x.Cips)
                        .FirstOrDefaultAsync(x => x.Slug == j.Slug, ct);
            if (p is null)
            {
                p = new ProgramEntity { Id = Guid.NewGuid(), Slug = j.Slug, CreatedUtc = DateTime.UtcNow };
                _db.Programs.Add(p);
                added++;
            }
            else
            {
                updated++;
                _db.ProgramCips.RemoveRange(p.Cips);
            }

            p.Name = j.Name;
            p.Description = j.Description ?? string.Empty;
            p.DegreesNote = j.DegreesNote;
            p.SortOrder = j.SortOrder;
            // Seeded programmes are published; unpublishing is an admin action, not a seed one.
            p.IsPublished = true;
            p.UpdatedUtc = DateTime.UtcNow;

            int order = 0;
            foreach (var c in j.Cips ?? [])
            {
                _db.ProgramCips.Add(new ProgramCip
                {
                    Id = Guid.NewGuid(),
                    ProgramId = p.Id,
                    CipCode = c.CipCode,
                    Note = c.Note,
                    SortOrder = order++
                });
            }
        }

        await _db.SaveChangesAsync(ct);
        _logger.LogInformation("Program seed complete. {Added} added, {Updated} updated.", added, updated);
    }

    private async Task SeedAwardsAsync(CancellationToken ct)
    {
        var path = _config["Programs:AwardsPath"] ?? "Data/Seed/institution_awards.json";
        if (!File.Exists(path))
        {
            _logger.LogWarning("Institution awards seed not found at {Path}; skipping.", path);
            return;
        }

        await using var stream = File.OpenRead(path);
        var file = await JsonSerializer.DeserializeAsync<AwardFileJson>(stream, JsonOptions, ct);
        var rows = file?.Awards ?? [];
        if (rows.Count == 0) return;

        // ⚠ Whole-year replace rather than row-by-row upsert. This is a federal file that is
        // reissued annually; reconciling 6,400 rows individually would be slower and would leave
        // withdrawn programmes behind. Replacing one YEAR keeps any other year intact.
        var year = file!.Year;
        var existing = await _db.InstitutionAwards.CountAsync(a => a.Year == year, ct);

        // ⚠ Row COUNT alone is not enough to decide "already seeded". A corrected award-level
        // map changes every LABEL while leaving the count identical, and an earlier version of
        // this check silently skipped exactly that re-seed. Compare the distinct labels too.
        var storedLabels = await _db.InstitutionAwards.Where(a => a.Year == year)
            .Select(a => a.AwardLevel).Distinct().ToListAsync(ct);
        var fileLabels = rows.Select(r => r.AwardLevel).Distinct().ToList();
        var sameLabels = storedLabels.Count == fileLabels.Count
                         && !fileLabels.Except(storedLabels).Any();

        if (existing == rows.Count && sameLabels)
        {
            _logger.LogInformation("Institution awards for {Year} already seeded ({Count} rows).",
                year, existing);
            return;
        }

        if (existing > 0)
        {
            _db.InstitutionAwards.RemoveRange(
                await _db.InstitutionAwards.Where(a => a.Year == year).ToListAsync(ct));
            await _db.SaveChangesAsync(ct);
        }

        // Known institution codes, so the cross-reference can link to our own pages where it can.
        var known = await _db.Institutions.AsNoTracking()
            .Where(i => i.Name != null)
            .ToDictionaryAsync(i => i.Name!.ToUpperInvariant(), i => i.Code, ct);

        foreach (var r in rows)
        {
            known.TryGetValue(r.InstitutionName.ToUpperInvariant(), out var code);
            _db.InstitutionAwards.Add(new InstitutionAward
            {
                Id = Guid.NewGuid(),
                UnitId = r.UnitId,
                InstitutionName = r.InstitutionName,
                InstitutionCode = code,
                CipCode = r.CipCode,
                AwardLevel = r.AwardLevel,
                Completions = r.Completions,
                Year = r.Year
            });
        }

        await _db.SaveChangesAsync(ct);
        _logger.LogInformation("Institution awards seeded: {Count} rows for {Year}.", rows.Count, year);
    }

    private record ProgramFileJson(string? Note, List<ProgramJson>? Programs);
    private record ProgramJson(string Slug, string Name, string? Description, string? DegreesNote,
                               int SortOrder, List<ProgramCipJson>? Cips);
    private record ProgramCipJson(string CipCode, string? Note);

    private record AwardFileJson(string? Source, int Year, List<AwardJson>? Awards)
    {
        public List<AwardJson> Awards { get; init; } = Awards ?? [];
    }
    private record AwardJson(string UnitId, string InstitutionName, string CipCode,
                             string AwardLevel, int Completions, int Year);
}
