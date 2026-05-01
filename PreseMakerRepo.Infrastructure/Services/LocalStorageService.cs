using System.IO.Compression;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Core.Interfaces;
using PreseMakerRepo.Infrastructure.Data;
using PreseMakerRepo.Infrastructure.Options;

namespace PreseMakerRepo.Infrastructure.Services;

public class LocalStorageService : IStorageService
{
    private readonly StorageOptions _options;
    private readonly AppDbContext _db;
    private readonly ILogger<LocalStorageService> _logger;

    public LocalStorageService(IOptions<StorageOptions> options, AppDbContext db, ILogger<LocalStorageService> logger)
    {
        _options = options.Value;
        _db = db;
        _logger = logger;
    }

    public async Task<string> SaveMaterialAsync(
        Guid moduleId, Guid materialId, string originalFileName,
        Stream content, CancellationToken ct = default)
    {
        var materialsDir = Path.Combine(_options.RootPath, "modules", moduleId.ToString(), "materials");
        Directory.CreateDirectory(materialsDir);

        var storedName = $"{materialId}_{originalFileName}";
        var relativePath = Path.Combine("modules", moduleId.ToString(), "materials", storedName);
        var fullPath = Path.Combine(_options.RootPath, relativePath);

        await using var fileStream = File.Create(fullPath);
        await content.CopyToAsync(fileStream, ct);

        _logger.LogDebug("Saved material {MaterialId} to {Path}", materialId, relativePath);
        return relativePath;
    }

    public Task<Stream> ReadMaterialAsync(string storagePath, CancellationToken ct = default)
    {
        var fullPath = Path.Combine(_options.RootPath, storagePath);
        return Task.FromResult<Stream>(File.OpenRead(fullPath));
    }

    public async Task<Stream> BuildModuleZipAsync(Guid moduleId, CancellationToken ct = default)
    {
        var materialsDir = Path.Combine(_options.RootPath, "modules", moduleId.ToString(), "materials");
        if (!Directory.Exists(materialsDir))
            return Stream.Null;

        var entries = Directory.GetFiles(materialsDir)
            .Select(f => (EntryName: Path.GetFileName(f), FilePath: f))
            .ToList();

        return await BuildZipAsync(entries, ct);
    }

    public async Task<Stream> BuildCourseZipAsync(string courseId, CancellationToken ct = default)
    {
        var modules = await _db.Modules
            .AsNoTracking()
            .Where(m => m.CourseId == courseId && m.Status == ContentStatus.Published)
            .Select(m => new { m.Id, m.Title })
            .ToListAsync(ct);

        var entries = new List<(string EntryName, string FilePath)>();
        foreach (var module in modules)
        {
            var slug = Slugify(module.Title);
            var dir = Path.Combine(_options.RootPath, "modules", module.Id.ToString(), "materials");
            if (!Directory.Exists(dir)) continue;

            foreach (var file in Directory.GetFiles(dir))
                entries.Add(($"{courseId}_course/{slug}/{Path.GetFileName(file)}", file));
        }

        return await BuildZipAsync(entries, ct);
    }

    public Task DeleteModuleAsync(Guid moduleId, CancellationToken ct = default)
    {
        var modulePath = Path.Combine(_options.RootPath, "modules", moduleId.ToString());
        if (Directory.Exists(modulePath))
            Directory.Delete(modulePath, recursive: true);
        return Task.CompletedTask;
    }

    public Task DeleteMaterialAsync(string storagePath, CancellationToken ct = default)
    {
        var fullPath = Path.Combine(_options.RootPath, storagePath);
        if (File.Exists(fullPath))
            File.Delete(fullPath);
        return Task.CompletedTask;
    }

    private async Task<Stream> BuildZipAsync(IReadOnlyList<(string EntryName, string FilePath)> entries, CancellationToken ct)
    {
        if (entries.Count == 0)
            return Stream.Null;

        long totalBytes = entries.Sum(e => new FileInfo(e.FilePath).Length);
        bool useTempFile = totalBytes > _options.LargeZipThresholdBytes;

        Stream output;
        string? tempPath = null;

        if (useTempFile)
        {
            tempPath = Path.GetTempFileName();
            output = new FileStream(tempPath, FileMode.Create, FileAccess.ReadWrite);
        }
        else
        {
            output = new MemoryStream();
        }

        using (var archive = new ZipArchive(output, ZipArchiveMode.Create, leaveOpen: true))
        {
            foreach (var (entryName, filePath) in entries)
            {
                var entry = archive.CreateEntry(entryName, CompressionLevel.Optimal);
                await using var entryStream = entry.Open();
                await using var fileStream = File.OpenRead(filePath);
                await fileStream.CopyToAsync(entryStream, ct);
            }
        }

        if (useTempFile)
        {
            output.Dispose();
            return new TempFileStream(tempPath!);
        }

        output.Position = 0;
        return output;
    }

    private static string Slugify(string title) =>
        string.Concat(title.ToLowerInvariant()
            .Select(c => char.IsLetterOrDigit(c) ? c : '-'))
            .Trim('-');

    // Wraps a temp file stream and deletes the file on dispose
    private sealed class TempFileStream : FileStream
    {
        private readonly string _path;

        public TempFileStream(string path)
            : base(path, FileMode.Open, FileAccess.Read, FileShare.Delete)
        {
            _path = path;
        }

        protected override void Dispose(bool disposing)
        {
            base.Dispose(disposing);
            try { File.Delete(_path); } catch { /* best-effort cleanup */ }
        }
    }
}
