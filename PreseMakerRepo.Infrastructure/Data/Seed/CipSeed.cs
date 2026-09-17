using System.Text.Json;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Infrastructure.Seed;

/// <summary>
/// Seeds the CIP (Classification of Instructional Programs) browse tree from
/// <c>cip.json</c>, built by <c>Tools/build_cip_seed.py</c> from the NCES CIP 2020 file.
/// Idempotent, and follows <see cref="TaxonomySeed"/>: missing file logs a warning and
/// skips rather than failing startup.
/// <para>
/// ⚠ <b>Titles and definitions are NCES's own words.</b> The seed overwrites them on every
/// run so a corrected federal file propagates — but it never touches
/// <see cref="CipNode.EditorialNote"/>, which is ours and is admin-edited.
/// </para>
/// <para>
/// ⚠⚠ <b>A node is never deleted here.</b> The 4-digit level is scoped by course evidence,
/// which moves as catalogues are re-harvested; deleting on absence would drop a group an
/// author had already hung a <see cref="CareerPath"/> on. Nodes that fall out of scope are
/// left in place, and the foreign key from CareerPath restricts deletion anyway.
/// </para>
/// </summary>
public class CipSeed
{
    private readonly AppDbContext _db;
    private readonly IConfiguration _config;
    private readonly ILogger<CipSeed> _logger;

    private static readonly JsonSerializerOptions JsonOptions = new() { PropertyNameCaseInsensitive = true };

    public CipSeed(AppDbContext db, IConfiguration config, ILogger<CipSeed> logger)
    {
        _db = db;
        _config = config;
        _logger = logger;
    }

    public async Task SeedAsync(CancellationToken ct = default)
    {
        var path = _config["Cip:ConfigPath"] ?? "Data/Seed/cip.json";

        if (!File.Exists(path))
        {
            _logger.LogWarning("CIP seed not found at {Path}; skipping CIP seed.", path);
            return;
        }

        await using var stream = File.OpenRead(path);
        var file = await JsonSerializer.DeserializeAsync<CipFileJson>(stream, JsonOptions, ct)
                   ?? throw new InvalidOperationException("Failed to parse cip.json");

        // EF orders inserts by dependency, so the self-reference resolves itself; the sort
        // is for a stable, readable insert order rather than for correctness.
        var nodes = (file.Nodes ?? []).OrderBy(n => n.Level).ThenBy(n => n.Code).ToList();
        int added = 0, updated = 0;

        foreach (var json in nodes)
        {
            var existing = await _db.CipNodes.FindAsync([json.Code], ct);
            if (existing is null)
            {
                _db.CipNodes.Add(new CipNode
                {
                    Code = json.Code,
                    Level = json.Level,
                    Title = json.Title,
                    Definition = Nullify(json.Definition),
                    Examples = Nullify(json.Examples),
                    ParentCode = json.Parent,
                    ChildCount = json.ChildCount
                });
                added++;
                continue;
            }

            if (existing.Title == json.Title
                && existing.Definition == Nullify(json.Definition)
                && existing.Examples == Nullify(json.Examples)
                && existing.ParentCode == json.Parent
                && existing.Level == json.Level
                && existing.ChildCount == json.ChildCount)
            {
                continue;
            }

            existing.Title = json.Title;
            existing.Definition = Nullify(json.Definition);
            existing.Examples = Nullify(json.Examples);
            existing.ParentCode = json.Parent;
            existing.Level = json.Level;
            existing.ChildCount = json.ChildCount;
            existing.UpdatedUtc = DateTime.UtcNow;
            updated++;
        }

        await _db.SaveChangesAsync(ct);
        _logger.LogInformation(
            "CIP seed complete. {Added} added, {Updated} updated, {Total} nodes in file ({Scope}).",
            added, updated, nodes.Count, file.Scope ?? "unspecified scope");
    }

    private static string? Nullify(string? s) => string.IsNullOrWhiteSpace(s) ? null : s;

    private record CipFileJson(string? Source, string? Scope, string? Note, List<CipNodeJson>? Nodes);

    private record CipNodeJson(
        string Code,
        int Level,
        string Title,
        string? Definition,
        string? Examples,
        string? Parent,
        int ChildCount);
}
