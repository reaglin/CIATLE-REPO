namespace PreseMakerRepo.Core.Models;

/// <summary>
/// One visitor on one day (Florida time) — the visitor counter, Phase 9 of docs/DEVELOPMENT-PLAN.md
/// (Ron, 2026-11-20: "know how many people are visiting the site"). A visitor is one IP address with
/// one browser, held only as a salted hash: the raw address is never stored. Crawlers, bots, scripts,
/// administrators, the API and /admin are never counted (<c>VisitClassifier</c>).
/// </summary>
public class SiteVisit
{
    /// <summary>The day in Florida (America/New_York).</summary>
    public DateOnly Day { get; set; }

    /// <summary>First 16 hex characters of a salted SHA-256 of IP + user agent.</summary>
    public string VisitorHash { get; set; } = string.Empty;

    /// <summary>
    /// Where the visitor came from on their first page that day: the referring site's host
    /// (e.g. "google.com"), or null when the browser sent none (typed address, bookmark, app).
    /// </summary>
    public string? Source { get; set; }

    /// <summary>The first page the visitor opened that day.</summary>
    public string LandingPath { get; set; } = string.Empty;

    /// <summary>Pages the visitor opened that day.</summary>
    public int PageViews { get; set; }
}

/// <summary>Page views of one page on one day (Florida time). No visitor is recorded here.</summary>
public class SitePageView
{
    public DateOnly Day { get; set; }

    /// <summary>The page's path with no query string, e.g. "/courses/EEL4205/guide".</summary>
    public string Path { get; set; } = string.Empty;

    public int Views { get; set; }
}
