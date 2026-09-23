using System.Text.Json;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Infrastructure.Seed;

/// <summary>
/// Seeds the occupations each CIP group leads to from <c>cip_soc.json</c>, built by
/// <c>Tools/build_cip_soc_seed.py</c> from the NCES CIP–SOC crosswalk. They are what a reader
/// can request a career path for. Runs after <see cref="CipSeed"/>, because every row
/// references a CIP node.
/// <para>
/// ⚠ Upserts titles and adds new pairs, but <b>never touches <see cref="CipOccupation.IsHidden"/></b>
/// (an admin decision) and <b>never deletes</b> — a pair dropped from a later crosswalk edition is
/// left in place rather than losing the requests already made against it. A pair whose CIP node is
/// missing is skipped and counted, not inserted.
/// </para>
/// </summary>
public class CipOccupationSeed
{
    private readonly AppDbContext _db;
    private readonly IConfiguration _config;
    private readonly ILogger<CipOccupationSeed> _logger;

    private static readonly JsonSerializerOptions JsonOptions = new() { PropertyNameCaseInsensitive = true };

    public CipOccupationSeed(AppDbContext db, IConfiguration config, ILogger<CipOccupationSeed> logger)
    {
        _db = db;
        _config = config;
        _logger = logger;
    }

    public async Task SeedAsync(CancellationToken ct = default)
    {
        var path = _config["CipOccupations:ConfigPath"] ?? "Data/Seed/cip_soc.json";
        if (!File.Exists(path))
        {
            _logger.LogWarning("CIP occupation seed not found at {Path}; skipping.", path);
            return;
        }

        await using var stream = File.OpenRead(path);
        var file = await JsonSerializer.DeserializeAsync<FileJson>(stream, JsonOptions, ct)
                   ?? throw new InvalidOperationException("Failed to parse cip_soc.json");

        var nodes = (await _db.CipNodes.AsNoTracking().Select(n => n.Code).ToListAsync(ct)).ToHashSet();
        var existing = await _db.CipOccupations.ToDictionaryAsync(o => (o.CipCode, o.SocCode), ct);

        int added = 0, updated = 0, skipped = 0;
        foreach (var row in file.Occupations ?? [])
        {
            if (string.IsNullOrWhiteSpace(row.CipCode) || string.IsNullOrWhiteSpace(row.SocCode)) continue;
            if (!nodes.Contains(row.CipCode)) { skipped++; continue; }

            if (existing.TryGetValue((row.CipCode, row.SocCode), out var o))
            {
                if (o.SocTitle == row.SocTitle) continue;
                o.SocTitle = row.SocTitle;
                o.UpdatedUtc = DateTime.UtcNow;
                updated++;
                continue;
            }

            _db.CipOccupations.Add(new CipOccupation
            {
                CipCode = row.CipCode,
                SocCode = row.SocCode,
                SocTitle = row.SocTitle
            });
            added++;
        }

        await _db.SaveChangesAsync(ct);
        _logger.LogInformation(
            "CIP occupation seed complete. {Added} added, {Updated} updated, {Skipped} skipped (no CIP node).",
            added, updated, skipped);
    }

    private record FileJson(string? Source, string? Note, List<RowJson>? Occupations);
    private record RowJson(string CipCode, string SocCode, string SocTitle);
}
