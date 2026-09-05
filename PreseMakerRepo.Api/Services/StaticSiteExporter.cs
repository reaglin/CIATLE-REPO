using System.IO.Compression;
using System.Net;
using System.Text;
using System.Text.Json;
using System.Text.RegularExpressions;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Core.Constants;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Api.Services;

public sealed class StaticExportOptions
{
    /// <summary>Include a page for every active taxonomy course (thousands) rather than only
    /// courses that have a guide or published modules.</summary>
    public bool IncludeAllCourses { get; set; }
    /// <summary>Include module and material detail pages (file downloads still point at the live site).</summary>
    public bool IncludeModules { get; set; } = true;
    public int MaxPages { get; set; } = 25_000;
}

public sealed class StaticExportProgress
{
    public int Pages { get; set; }
    public int Assets { get; set; }
    public int Queued { get; set; }
    public string? Current { get; set; }
}

public sealed record StaticExportResult(string ZipPath, int Pages, int Assets, long Bytes, TimeSpan Elapsed);

/// <summary>
/// Builds a self-contained static copy of the public site — the browse tree, every course
/// page in scope, every curriculum guide, module/material detail pages — as a zip that
/// unzips into a working site (open <c>index.html</c>). It works by fetching the live pages
/// from this same server over loopback and rewriting the HTML:
///
///  • internal page links become relative links to the exported <c>…/index.html</c> files;
///  • stylesheets, scripts, and images are copied from wwwroot and linked relatively;
///  • anything that needs the server — search, accounts, admin, the API, file downloads,
///    the request form — becomes an absolute link to the live site;
///  • a small banner marks each page as a static copy with a link to its live version.
///
/// Every page is <c>{path}/index.html</c>; query-string variants (letter navigation,
/// pagination) become <c>{path}/index__{query}.html</c>. Because the copy is rendered by the
/// real pages, it also serves as a readable content backup.
/// </summary>
public sealed class StaticSiteExporter
{
    private static readonly Regex AttrLink = new(
        @"(?<attr>\b(?:href|src|action)\s*=\s*)(?<q>[""'])(?<url>[^""']*)\k<q>",
        RegexOptions.IgnoreCase | RegexOptions.Compiled);
    private static readonly Regex BodyOpen = new(@"<body\b[^>]*>", RegexOptions.IgnoreCase | RegexOptions.Compiled);
    private static readonly Regex GuidSeg = new(@"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", RegexOptions.IgnoreCase | RegexOptions.Compiled);

    private readonly IHttpClientFactory _http;
    private readonly IWebHostEnvironment _env;
    private readonly IServiceScopeFactory _scopes;
    private readonly ILogger<StaticSiteExporter> _log;

    public StaticSiteExporter(IHttpClientFactory http, IWebHostEnvironment env,
        IServiceScopeFactory scopes, ILogger<StaticSiteExporter> log)
    {
        _http = http; _env = env; _scopes = scopes; _log = log;
    }

    public async Task<StaticExportResult> ExportAsync(
        Uri localBase, string publicScheme, string publicHost, StaticExportOptions options,
        string zipPath, IProgress<StaticExportProgress>? progress, CancellationToken ct)
    {
        var started = DateTime.UtcNow;
        var live = $"{publicScheme}://{publicHost}";
        var courseScope = await CourseScopeAsync(options, ct);

        var client = _http.CreateClient();
        client.BaseAddress = localBase;
        client.Timeout = TimeSpan.FromSeconds(60);
        client.DefaultRequestHeaders.Host = publicHost;
        client.DefaultRequestHeaders.Add("X-Static-Export", "1");

        var queue = new Queue<string>();
        var seen = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        void Enqueue(string key) { if (seen.Add(key)) queue.Enqueue(key); }

        Enqueue("/");
        Enqueue("/browse");
        Enqueue("/browse/subdisciplines");
        foreach (var (id, hasGuide) in courseScope.OrderBy(kv => kv.Key))
        {
            Enqueue($"/courses/{id}");
            if (hasGuide) Enqueue($"/courses/{id}/guide");
        }

        var assets = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        var prog = new StaticExportProgress();
        int pages = 0;

        Directory.CreateDirectory(Path.GetDirectoryName(zipPath)!);
        var tmpZip = zipPath + ".tmp";
        if (File.Exists(tmpZip)) File.Delete(tmpZip);

        using (var zip = ZipFile.Open(tmpZip, ZipArchiveMode.Create))
        {
            while (queue.Count > 0)
            {
                ct.ThrowIfCancellationRequested();
                if (pages >= options.MaxPages) { _log.LogWarning("Static export stopped at MaxPages={Max}", options.MaxPages); break; }

                var key = queue.Dequeue();
                prog.Current = key; prog.Queued = queue.Count; progress?.Report(prog);

                string html;
                try
                {
                    using var resp = await client.GetAsync(key, ct);
                    if (!resp.IsSuccessStatusCode) { _log.LogDebug("Skip {Url}: {Status}", key, resp.StatusCode); continue; }
                    var type = resp.Content.Headers.ContentType?.MediaType ?? "";
                    if (!type.Contains("html", StringComparison.OrdinalIgnoreCase)) continue;
                    html = await resp.Content.ReadAsStringAsync(ct);
                }
                catch (HttpRequestException ex)
                {
                    _log.LogWarning(ex, "Static export could not fetch {Url}", key);
                    continue;
                }

                var (path, query) = Split(key);
                var pageZipPath = ZipPathFor(path, query);

                var rewritten = AttrLink.Replace(html, m =>
                {
                    var url = m.Groups["url"].Value;
                    var attr = m.Groups["attr"].Value;
                    var q = m.Groups["q"].Value;
                    var isAction = attr.TrimStart().StartsWith("action", StringComparison.OrdinalIgnoreCase);
                    var replacement = Rewrite(url, isAction, path, pageZipPath, publicHost, live, courseScope, options,
                        onPage: Enqueue, onAsset: a => assets.Add(a));
                    return replacement is null ? m.Value : $"{attr}{q}{WebUtility.HtmlEncode(replacement)}{q}";
                });

                rewritten = BodyOpen.Replace(rewritten, m =>
                    m.Value + Banner(live, path, query, started, Relative(pageZipPath, "index.html")), 1);

                WriteText(zip, pageZipPath, rewritten);
                pages++; prog.Pages = pages;
            }

            // Assets referenced by any page, copied once from wwwroot.
            foreach (var asset in assets.OrderBy(a => a))
            {
                ct.ThrowIfCancellationRequested();
                var rel = asset.TrimStart('/').Replace('/', Path.DirectorySeparatorChar);
                var file = Path.Combine(_env.WebRootPath, rel);
                if (!File.Exists(file)) { _log.LogDebug("Asset missing: {Asset}", asset); continue; }
                zip.CreateEntryFromFile(file, asset.TrimStart('/'), CompressionLevel.Optimal);
                prog.Assets++;
            }
            progress?.Report(prog);

            WriteText(zip, "manifest.json", JsonSerializer.Serialize(new
            {
                site = live, generatedUtc = started, pages, assets = prog.Assets,
                includeAllCourses = options.IncludeAllCourses, includeModules = options.IncludeModules,
                courses = courseScope.Count, guides = courseScope.Count(kv => kv.Value)
            }, new JsonSerializerOptions { WriteIndented = true }));
            WriteText(zip, "README.txt",
                $"Static copy of {live} generated {started:yyyy-MM-dd HH:mm} UTC.\r\n\r\n" +
                "Open index.html in a browser. Every page is {path}/index.html; guides are under courses/{ID}/guide/.\r\n" +
                "Search, accounts, the admin console, file downloads and the guide-request form need the live site\r\n" +
                "and link to it. Content is a snapshot — see manifest.json.\r\n");
        }

        File.Move(tmpZip, zipPath, overwrite: true);
        var bytes = new FileInfo(zipPath).Length;
        return new StaticExportResult(zipPath, pages, prog.Assets, bytes, DateTime.UtcNow - started);
    }

    // ── scope ────────────────────────────────────────────────────────────────

    /// <summary>Course id → has guide, for the courses whose pages are exported.</summary>
    private async Task<Dictionary<string, bool>> CourseScopeAsync(StaticExportOptions options, CancellationToken ct)
    {
        using var scope = _scopes.CreateScope();
        var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        var guides = await db.CurriculumGuides.AsNoTracking().Select(g => g.CourseId).ToListAsync(ct);
        var result = guides.ToDictionary(id => id, _ => true, StringComparer.OrdinalIgnoreCase);

        var withModules = await db.Modules.AsNoTracking()
            .Where(m => m.Status == ContentStatus.Published && m.Id != WellKnownIds.OrphanModuleId && m.CourseId != null)
            .Select(m => m.CourseId!).Distinct().ToListAsync(ct);
        foreach (var id in withModules) result.TryAdd(id, false);

        if (options.IncludeAllCourses)
        {
            var all = await db.TaxonomyCourses.AsNoTracking()
                .Where(c => c.IsActive && c.CourseId != WellKnownIds.OrphanCourseId)
                .Select(c => c.CourseId).ToListAsync(ct);
            foreach (var id in all) result.TryAdd(id, false);
        }
        result.Remove(WellKnownIds.OrphanCourseId);
        return result;
    }

    // ── link rewriting ───────────────────────────────────────────────────────

    /// <summary>Returns the replacement URL, or null to leave the attribute untouched.</summary>
    private static string? Rewrite(string url, bool isFormAction, string currentPath, string currentZipPath,
        string publicHost, string live, Dictionary<string, bool> courseScope, StaticExportOptions options,
        Action<string> onPage, Action<string> onAsset)
    {
        var raw = WebUtility.HtmlDecode(url).Trim();
        if (raw.Length == 0 || raw.StartsWith('#') || raw.StartsWith("mailto:", StringComparison.OrdinalIgnoreCase) ||
            raw.StartsWith("javascript:", StringComparison.OrdinalIgnoreCase) || raw.StartsWith("data:", StringComparison.OrdinalIgnoreCase) ||
            raw.StartsWith("tel:", StringComparison.OrdinalIgnoreCase))
            return null;

        Uri abs;
        try { abs = new Uri(new Uri(live + (currentPath.StartsWith('/') ? currentPath : "/" + currentPath)), raw); }
        catch { return null; }
        if (!string.Equals(abs.Host, publicHost, StringComparison.OrdinalIgnoreCase) &&
            !string.Equals(abs.Host, "localhost", StringComparison.OrdinalIgnoreCase))
            return null;                                   // external link — untouched

        var path = abs.AbsolutePath;
        var query = abs.Query;
        if (path.Length > 1) path = path.TrimEnd('/');

        // Static assets: copied from wwwroot, cache-busting query dropped.
        if (path.StartsWith("/css/") || path.StartsWith("/js/") || path.StartsWith("/lib/") ||
            path.StartsWith("/images/") || path.Equals("/favicon.ico", StringComparison.OrdinalIgnoreCase))
        {
            onAsset(path);
            return Relative(currentZipPath, path.TrimStart('/'));
        }

        // Forms and server-only areas point at the live site.
        if (isFormAction || !IsExportablePage(path, courseScope, options))
            return live + path + query;

        var key = path + query;
        onPage(key);
        return Relative(currentZipPath, ZipPathFor(path, query)) + abs.Fragment;
    }

    private static bool IsExportablePage(string path, Dictionary<string, bool> courseScope, StaticExportOptions options)
    {
        if (path == "/" || path == "/browse" || path.StartsWith("/browse/")) return true;
        var segs = path.Trim('/').Split('/');
        if (segs.Length >= 2 && segs[0] == "courses")
        {
            if (!courseScope.ContainsKey(segs[1])) return false;
            return segs.Length == 2 || (segs.Length == 3 && segs[2] == "guide");
        }
        if (options.IncludeModules && segs.Length == 2 && (segs[0] == "modules" || segs[0] == "materials") && GuidSeg.IsMatch(segs[1]))
            return true;
        return false;
    }

    // ── paths ────────────────────────────────────────────────────────────────

    private static (string Path, string Query) Split(string key)
    {
        int i = key.IndexOf('?');
        return i < 0 ? (key, "") : (key[..i], key[i..]);
    }

    /// <summary>"/browse/x" → "browse/x/index.html"; "/browse/x?letter=B" → "browse/x/index__letter=B.html".</summary>
    public static string ZipPathFor(string path, string query)
    {
        var dir = path.Trim('/');
        var name = "index";
        if (!string.IsNullOrEmpty(query))
        {
            var q = query.TrimStart('?');
            var safe = new string(q.Select(ch => char.IsLetterOrDigit(ch) || ch is '=' or '_' or '-' ? ch : '_').ToArray());
            if (safe.Length > 80) safe = safe[..80];
            name = "index__" + safe;
        }
        return dir.Length == 0 ? $"{name}.html" : $"{dir}/{name}.html";
    }

    /// <summary>Relative link from one zip entry to another ("browse/a/index.html" → "courses/X/index.html" = "../../courses/X/index.html").</summary>
    public static string Relative(string fromZipPath, string toZipPath)
    {
        var fromDirs = fromZipPath.Split('/')[..^1];
        var toParts = toZipPath.Split('/');
        int common = 0;
        while (common < fromDirs.Length && common < toParts.Length - 1 &&
               string.Equals(fromDirs[common], toParts[common], StringComparison.OrdinalIgnoreCase))
            common++;
        var up = string.Concat(Enumerable.Repeat("../", fromDirs.Length - common));
        var down = string.Join("/", toParts[common..]);
        var rel = up + down;
        return rel.Length == 0 ? "./" : rel;
    }

    private static string Banner(string live, string path, string query, DateTime generated, string homeRel) =>
        "\n<div class=\"static-export-banner\" style=\"background:#fff3cd;border-bottom:1px solid #ffe69c;color:#664d03;" +
        "font:13px/1.4 'Segoe UI',Arial,sans-serif;padding:.4rem 1rem;text-align:center\">" +
        $"Static copy of <a href=\"{WebUtility.HtmlEncode(live)}\" style=\"color:#664d03\">{WebUtility.HtmlEncode(live)}</a> " +
        $"generated {generated:yyyy-MM-dd}. Search, accounts and downloads use the live site — " +
        $"<a href=\"{WebUtility.HtmlEncode(live + path + query)}\" style=\"color:#664d03\">open this page live</a>.</div>\n";

    private static void WriteText(ZipArchive zip, string entryPath, string text)
    {
        var entry = zip.CreateEntry(entryPath, CompressionLevel.Optimal);
        using var s = entry.Open();
        var bytes = new UTF8Encoding(false).GetBytes(text);
        s.Write(bytes, 0, bytes.Length);
    }
}
