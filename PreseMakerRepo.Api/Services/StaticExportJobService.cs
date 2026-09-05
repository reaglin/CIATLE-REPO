namespace PreseMakerRepo.Api.Services;

/// <summary>
/// Runs one static-site export at a time in the background (an export can take minutes,
/// longer than the reverse proxy's request timeout) and keeps the result files in
/// <c>{Storage:RootPath}/exports/</c>, where they double as content backups.
/// </summary>
public sealed class StaticExportJobService
{
    public sealed class JobStatus
    {
        public bool IsRunning { get; set; }
        public DateTime? StartedUtc { get; set; }
        public DateTime? FinishedUtc { get; set; }
        public int Pages { get; set; }
        public int Assets { get; set; }
        public int Queued { get; set; }
        public string? Current { get; set; }
        public string? Error { get; set; }
        public string? LastFile { get; set; }
        public long LastBytes { get; set; }
        public TimeSpan? LastElapsed { get; set; }
    }

    private readonly IServiceScopeFactory _scopes;
    private readonly ILogger<StaticExportJobService> _log;
    private readonly object _gate = new();
    private CancellationTokenSource? _cts;

    public JobStatus Status { get; } = new();
    public string ExportDirectory { get; }

    public StaticExportJobService(IServiceScopeFactory scopes, IConfiguration config, IWebHostEnvironment env,
        ILogger<StaticExportJobService> log)
    {
        _scopes = scopes; _log = log;
        // Absolute: PhysicalFileResult refuses relative paths, and Storage:RootPath is
        // relative in development ("dev-storage").
        var root = config["Storage:RootPath"];
        var baseDir = string.IsNullOrWhiteSpace(root) ? env.ContentRootPath
                    : Path.IsPathRooted(root) ? root : Path.Combine(env.ContentRootPath, root);
        ExportDirectory = Path.GetFullPath(Path.Combine(baseDir, "exports"));
    }

    /// <summary>Start an export; false when one is already running.</summary>
    public bool Start(Uri localBase, string publicScheme, string publicHost, StaticExportOptions options)
    {
        lock (_gate)
        {
            if (Status.IsRunning) return false;
            Status.IsRunning = true;
            Status.StartedUtc = DateTime.UtcNow; Status.FinishedUtc = null;
            Status.Pages = 0; Status.Assets = 0; Status.Queued = 0; Status.Current = null; Status.Error = null;
            _cts = new CancellationTokenSource();
        }
        var ct = _cts!.Token;
        var file = Path.Combine(ExportDirectory, $"static-site-{DateTime.UtcNow:yyyyMMdd-HHmmss}.zip");

        _ = Task.Run(async () =>
        {
            try
            {
                using var scope = _scopes.CreateScope();
                var exporter = scope.ServiceProvider.GetRequiredService<StaticSiteExporter>();
                var progress = new Progress<StaticExportProgress>(p =>
                {
                    Status.Pages = p.Pages; Status.Assets = p.Assets; Status.Queued = p.Queued; Status.Current = p.Current;
                });
                var result = await exporter.ExportAsync(localBase, publicScheme, publicHost, options, file, progress, ct);
                Status.LastFile = Path.GetFileName(result.ZipPath);
                Status.LastBytes = result.Bytes;
                Status.LastElapsed = result.Elapsed;
                Status.Pages = result.Pages; Status.Assets = result.Assets;
                _log.LogInformation("Static export finished: {File} ({Pages} pages, {Bytes} bytes, {Elapsed})",
                    result.ZipPath, result.Pages, result.Bytes, result.Elapsed);
            }
            catch (OperationCanceledException)
            {
                Status.Error = "Cancelled.";
                TryDelete(file + ".tmp");
            }
            catch (Exception ex)
            {
                Status.Error = ex.Message;
                _log.LogError(ex, "Static export failed");
                TryDelete(file + ".tmp");
            }
            finally
            {
                lock (_gate)
                {
                    Status.IsRunning = false;
                    Status.FinishedUtc = DateTime.UtcNow;
                    Status.Current = null;
                    _cts?.Dispose(); _cts = null;
                }
            }
        }, CancellationToken.None);
        return true;
    }

    public void Cancel()
    {
        lock (_gate) { _cts?.Cancel(); }
    }

    public IReadOnlyList<FileInfo> Files()
    {
        if (!Directory.Exists(ExportDirectory)) return Array.Empty<FileInfo>();
        return new DirectoryInfo(ExportDirectory).GetFiles("static-site-*.zip")
            .OrderByDescending(f => f.LastWriteTimeUtc).ToList();
    }

    /// <summary>Full path of an export file by its bare name, or null if the name is not one of ours.</summary>
    public string? Resolve(string fileName)
    {
        if (string.IsNullOrWhiteSpace(fileName) || fileName != Path.GetFileName(fileName) ||
            !fileName.StartsWith("static-site-", StringComparison.Ordinal) || !fileName.EndsWith(".zip", StringComparison.Ordinal))
            return null;
        var path = Path.Combine(ExportDirectory, fileName);
        return File.Exists(path) ? path : null;
    }

    private static void TryDelete(string path)
    {
        try { if (File.Exists(path)) File.Delete(path); } catch { /* best effort */ }
    }
}
