using System.Text.Json;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Infrastructure.Seed;

public class EduSeed
{
    private readonly AppDbContext _db;
    private readonly IHostEnvironment _env;
    private readonly ILogger<EduSeed> _logger;

    private static readonly JsonSerializerOptions JsonOptions = new() { PropertyNameCaseInsensitive = true };

    public EduSeed(AppDbContext db, IHostEnvironment env, ILogger<EduSeed> logger)
    {
        _db = db;
        _env = env;
        _logger = logger;
    }

    public async Task SeedAsync(CancellationToken ct = default)
    {
        if (await _db.EduInstitutions.AnyAsync(ct))
            return;

        var path = Path.Combine(_env.ContentRootPath, "Data", "Seed", "edu_institutions.json");
        if (!File.Exists(path))
        {
            _logger.LogWarning("edu_institutions.json not found at {Path}; skipping EDU institution seed.", path);
            return;
        }

        await using var stream = File.OpenRead(path);
        var institutions = await JsonSerializer.DeserializeAsync<List<EduInstitutionJson>>(stream, JsonOptions, ct) ?? [];

        _db.EduInstitutions.AddRange(institutions.Select(i => new EduInstitution
        {
            EmailDomain = i.EmailDomain.ToLowerInvariant(),
            InstitutionName = i.InstitutionName,
            State = i.State,
            Country = i.Country ?? "US"
        }));

        await _db.SaveChangesAsync(ct);
        _logger.LogInformation("Seeded {Count} EDU institutions.", institutions.Count);
    }

    private record EduInstitutionJson(string EmailDomain, string InstitutionName, string? State, string? Country);
}
