using System.Text.Json;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using PreseMakerRepo.Core.Constants;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Infrastructure.Seed;

public class TaxonomySeed
{
    private readonly AppDbContext _db;
    private readonly IConfiguration _config;
    private readonly ILogger<TaxonomySeed> _logger;

    private static readonly JsonSerializerOptions JsonOptions = new() { PropertyNameCaseInsensitive = true };

    public TaxonomySeed(AppDbContext db, IConfiguration config, ILogger<TaxonomySeed> logger)
    {
        _db = db;
        _config = config;
        _logger = logger;
    }

    public async Task SeedAsync(CancellationToken ct = default)
    {
        var configPath = _config["Taxonomy:ConfigPath"] ?? "taxonomy.json";

        if (!File.Exists(configPath))
        {
            _logger.LogWarning("Taxonomy config not found at {Path}; skipping taxonomy seed.", configPath);
            return;
        }

        await using var stream = File.OpenRead(configPath);
        var taxFile = await JsonSerializer.DeserializeAsync<TaxonomyFileJson>(stream, JsonOptions, ct)
                      ?? throw new InvalidOperationException("Failed to parse taxonomy.json");

        int upserted = 0;

        foreach (var l1 in taxFile.RootNodes)
        {
            upserted += await UpsertNodeAsync(l1, null, 1, ct);
            foreach (var l2 in l1.Children ?? [])
            {
                upserted += await UpsertNodeAsync(l2, l1.Key, 2, ct);
                foreach (var l3 in l2.Children ?? [])
                {
                    upserted += await UpsertNodeAsync(l3, l2.Key, 3, ct);
                    foreach (var course in l3.Courses ?? [])
                        upserted += await UpsertCourseAsync(course, l3.Key, ct);
                }
            }
        }

        upserted += await EnsureOrphanCourseAsync(ct);

        await _db.SaveChangesAsync(ct);
        _logger.LogInformation("Taxonomy seed complete. {Count} records upserted.", upserted);
    }

    private async Task<int> UpsertNodeAsync(TaxonomyNodeJson json, string? parentKey, int level, CancellationToken ct)
    {
        var existing = await _db.TaxonomyNodes.FindAsync([json.Key], ct);
        if (existing is null)
        {
            _db.TaxonomyNodes.Add(new TaxonomyNode { Key = json.Key, Name = json.Name, Level = level, ParentKey = parentKey });
            return 1;
        }
        if (existing.Name == json.Name) return 0;
        existing.Name = json.Name;
        return 1;
    }

    private async Task<int> UpsertCourseAsync(TaxonomyCourseJson json, string level3Key, CancellationToken ct)
    {
        var courseId = json.CourseId.ToUpperInvariant();
        var existing = await _db.TaxonomyCourses.FindAsync([courseId], ct);
        if (existing is null)
        {
            _db.TaxonomyCourses.Add(new TaxonomyCourse
            {
                CourseId = courseId,
                Level3Key = level3Key,
                Title = json.Title,
                CreditHours = json.CreditHours,
                IsActive = json.IsActive,
                CurriculumGuideUrl = json.CurriculumGuideUrl
            });
            return 1;
        }
        if (existing.Title == json.Title) return 0;
        existing.Title = json.Title;
        return 1;
    }

    private async Task<int> EnsureOrphanCourseAsync(CancellationToken ct)
    {
        var exists = await _db.TaxonomyCourses.AnyAsync(c => c.CourseId == WellKnownIds.OrphanCourseId, ct);
        if (exists) return 0;

        _db.TaxonomyCourses.Add(new TaxonomyCourse
        {
            CourseId = WellKnownIds.OrphanCourseId,
            Level3Key = null,
            Title = "Not Classified",
            IsActive = true
        });
        return 1;
    }

    // Supports both { "nodes": [...] } (spec format) and { "tree": [...] } (SCNS format)
    private record TaxonomyFileJson(
        List<TaxonomyNodeJson>? Nodes,
        List<TaxonomyNodeJson>? Tree)
    {
        public List<TaxonomyNodeJson> RootNodes => Tree ?? Nodes ?? [];
    }
    private record TaxonomyNodeJson(string Key, string Name, List<TaxonomyNodeJson>? Children, List<TaxonomyCourseJson>? Courses);
    private record TaxonomyCourseJson(string CourseId, string Title, int? CreditHours, bool IsActive, string? CurriculumGuideUrl);
}
