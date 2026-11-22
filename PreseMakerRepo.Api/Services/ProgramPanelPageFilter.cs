using Microsoft.AspNetCore.Mvc.Filters;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace PreseMakerRepo.Api.Services;

/// <summary>
/// The program panel on the page a visitor lands on (plan Phase 14; Ron, 2026-11-22: visitors land on many pages, not
/// only the home page). On the first public page a browser opens in a session, this picks a program at random, puts it
/// in <see cref="HttpContext.Items"/> for <c>_ProgramPanel.cshtml</c>, and sets the session cookie
/// <see cref="ProgramPanelService.ShownCookie"/>, so every later page in that browser session leaves the panel out.
/// Never allowed to break a page.
/// </summary>
public sealed class ProgramPanelPageFilter : IAsyncPageFilter
{
    /// <summary>The key under which the program to show waits in <see cref="HttpContext.Items"/>.</summary>
    public const string ItemKey = "fcr:program-panel";

    private readonly ProgramPanelService _programs;
    private readonly ILogger<ProgramPanelPageFilter> _log;

    public ProgramPanelPageFilter(ProgramPanelService programs, ILogger<ProgramPanelPageFilter> log)
    {
        _programs = programs;
        _log = log;
    }

    public Task OnPageHandlerSelectionAsync(PageHandlerSelectedContext context) => Task.CompletedTask;

    public async Task OnPageHandlerExecutionAsync(PageHandlerExecutingContext context, PageHandlerExecutionDelegate next)
    {
        var executed = await next();
        var http = context.HttpContext;
        // Only a page that is about to be drawn normally: not a redirect, a 404 or an error.
        if (executed.Exception is not null && !executed.ExceptionHandled) return;
        if (executed.Result is not (null or PageResult)) return;
        if (http.Response.StatusCode != StatusCodes.Status200OK) return;
        if (!ShouldOffer(http.Request, context.ActionDescriptor.AreaName, context.ActionDescriptor.ViewEnginePath)) return;

        try
        {
            var program = await _programs.PickAsync(http.RequestAborted);
            if (program is null) return;   // the list could not be read: no cookie, so a later page may show it
            http.Items[ItemKey] = program;
            http.Response.Cookies.Append(ProgramPanelService.ShownCookie, "1", new CookieOptions
            {
                Path = "/", SameSite = SameSiteMode.Lax, Secure = http.Request.IsHttps, IsEssential = true, HttpOnly = true
                // No Expires: a session cookie, dropped when the browser closes.
            });
        }
        catch (Exception ex) when (ex is not OperationCanceledException)
        {
            _log.LogWarning(ex, "Could not pick a program for the program panel");
        }
    }

    /// <summary>
    /// True when this request may show the panel: a GET of a public page (not the admin console or the account pages),
    /// in a browser that has not been shown it (or closed it) in this session; not to a crawler, nor the static export.
    /// </summary>
    public static bool ShouldOffer(HttpRequest request, string? area, string? viewEnginePath)
    {
        if (!HttpMethods.IsGet(request.Method)) return false;
        if (!string.IsNullOrEmpty(area)) return false;   // /admin
        if (viewEnginePath is not null && viewEnginePath.StartsWith("/Account", StringComparison.OrdinalIgnoreCase)) return false;
        if (request.Headers.ContainsKey("X-Static-Export")) return false;
        // Crawlers keep no cookies, so they would get it on every page, and a search snippet could quote it (UX review).
        if (Visits.VisitClassifier.IsBot(request.Headers.UserAgent.ToString())) return false;
        if (request.Cookies.ContainsKey(ProgramPanelService.ShownCookie)) return false;
        if (request.Cookies.ContainsKey(ProgramPanelService.ClosedCookie)) return false;
        return true;
    }
}
