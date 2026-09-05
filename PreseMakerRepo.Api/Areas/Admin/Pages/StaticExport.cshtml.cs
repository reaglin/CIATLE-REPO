using Microsoft.AspNetCore.Hosting.Server;
using Microsoft.AspNetCore.Hosting.Server.Features;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using PreseMakerRepo.Api.Services;

namespace PreseMakerRepo.Api.Areas.Admin.Pages;

/// <summary>Start, watch, download, and delete static-site exports.</summary>
public class StaticExportModel : PageModel
{
    private readonly StaticExportJobService _jobs;
    private readonly IServer _server;
    private readonly IConfiguration _config;

    public StaticExportModel(StaticExportJobService jobs, IServer server, IConfiguration config)
    {
        _jobs = jobs; _server = server; _config = config;
    }

    [BindProperty] public bool IncludeAllCourses { get; set; }
    [BindProperty] public bool IncludeModules { get; set; } = true;
    [TempData] public string? Message { get; set; }

    public StaticExportJobService.JobStatus Status => _jobs.Status;
    public IReadOnlyList<FileInfo> Files { get; set; } = [];
    public string ExportDirectory => _jobs.ExportDirectory;

    public void OnGet() => Files = _jobs.Files();

    public IActionResult OnPostStart()
    {
        var local = LocalBase();
        if (local is null)
        {
            Message = "Could not determine the server's local address to fetch pages from.";
            return RedirectToPage();
        }
        // The public address the "live site" links point at. Configured
        // (SiteSettings:PublicBaseUrl) so a reverse proxy that does not forward the
        // Host header cannot turn every live link into http://localhost:5000/…
        var scheme = Request.Scheme;
        var host = Request.Host.Value ?? "floridacourserepo.com";
        if (Uri.TryCreate(_config["SiteSettings:PublicBaseUrl"], UriKind.Absolute, out var pub))
        {
            scheme = pub.Scheme;
            host = pub.IsDefaultPort ? pub.Host : $"{pub.Host}:{pub.Port}";
        }
        var started = _jobs.Start(local, scheme, host,
            new StaticExportOptions { IncludeAllCourses = IncludeAllCourses, IncludeModules = IncludeModules });
        Message = started ? "Export started." : "An export is already running.";
        return RedirectToPage();
    }

    public IActionResult OnPostCancel()
    {
        _jobs.Cancel();
        Message = "Cancelling…";
        return RedirectToPage();
    }

    public IActionResult OnGetDownload(string file)
    {
        var path = _jobs.Resolve(file);
        if (path is null) return NotFound();
        return PhysicalFile(path, "application/zip", Path.GetFileName(path));
    }

    public IActionResult OnPostDelete(string file)
    {
        var path = _jobs.Resolve(file);
        if (path is not null)
        {
            System.IO.File.Delete(path);
            Message = $"Deleted {Path.GetFileName(path)}.";
        }
        return RedirectToPage();
    }

    /// <summary>The Kestrel address to crawl over loopback (http://localhost:5000 in production).</summary>
    private Uri? LocalBase()
    {
        var addresses = _server.Features.Get<IServerAddressesFeature>()?.Addresses;
        var first = addresses?.FirstOrDefault(a => a.StartsWith("http://", StringComparison.OrdinalIgnoreCase))
                    ?? addresses?.FirstOrDefault();
        if (first is null) return null;
        first = first.Replace("://*", "://localhost").Replace("://+", "://localhost")
                     .Replace("://0.0.0.0", "://localhost").Replace("://[::]", "://localhost");
        return Uri.TryCreate(first, UriKind.Absolute, out var uri) ? uri : null;
    }
}
