using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Options;
using PreseMakerRepo.Api.Options;
using PreseMakerRepo.Api.Services;

namespace PreseMakerRepo.Api.Services.Visits;

/// <summary>What a page sends when it reports a visit: its path and the page that linked to it.</summary>
public sealed record VisitReport(string? P, string? R);

/// <summary>What the program panel sends when one of its links is clicked: the program's id and "page" or "store".</summary>
public sealed record ProgramClickReport(string? Id, string? L);

/// <summary>
/// <c>POST /visit</c>: the page reports itself (site.js, once there is a sign of a person). Outside
/// <c>/api</c> so the sign-in cookie is read and an administrator's own browsing is left out. Always
/// answers 204, so it tells a caller nothing; counting can never break a page.
/// </summary>
public static class VisitEndpoint
{
    public static void MapVisitReport(this WebApplication app) =>
        app.MapPost("/visit", async (HttpContext ctx, VisitRecorder recorder,
            IMemoryCache cache, IOptions<SecurityOptions> security, ILoggerFactory logs) =>
        {
            try
            {
                // Read here rather than bound, so a malformed body is ignored like any other bad report.
                var report = await ctx.Request.ReadFromJsonAsync<VisitReport>(ctx.RequestAborted);
                if (report is null) return Results.NoContent();
                var ua = ctx.Request.Headers.UserAgent.ToString();
                if (!VisitClassifier.ShouldCountReport(report.P, ua, ctx.User.IsInRole("Administrator")))
                    return Results.NoContent();

                var now = DateTime.UtcNow;
                var hash = VisitClassifier.VisitorHash(security.Value.ReporterIpSalt,
                    ctx.Connection.RemoteIpAddress?.ToString(), ua);

                // A daily cap per visitor, so the count cannot be inflated by sending reports by hand.
                var capKey = $"visit-cap:{hash}:{VisitClassifier.FloridaDay(now):yyyyMMdd}";
                var seen = cache.GetOrCreate(capKey, e => { e.AbsoluteExpirationRelativeToNow = TimeSpan.FromHours(26); return new int[1]; })!;
                if (Interlocked.Increment(ref seen[0]) > VisitClassifier.MaxViewsPerVisitorPerDay)
                    return Results.NoContent();

                recorder.Record(new VisitHit(now, hash,
                    VisitClassifier.NormalizePath(report.P!.Split('?', '#')[0]),
                    VisitClassifier.SourceOf(report.R, ctx.Request.Host.Host)));
            }
            catch (Exception ex)
            {
                logs.CreateLogger("VisitEndpoint").LogDebug(ex, "A visit report was not counted");
            }
            return Results.NoContent();
        }).DisableAntiforgery();

    /// <summary>
    /// <c>POST /visit/program</c>: a click on one of the home page's program-panel links (plan 10.4), sent by
    /// site.js as a beacon while the link opens. Counted by the visitor counter's rules (no bots, no
    /// administrators, a daily cap per visitor), only for a program in the current list. Always 204.
    /// </summary>
    public static void MapProgramClickReport(this WebApplication app) =>
        app.MapPost("/visit/program", async (HttpContext ctx, VisitRecorder recorder, ProgramPanelService programs,
            IMemoryCache cache, IOptions<SecurityOptions> security, ILoggerFactory logs) =>
        {
            try
            {
                var report = await ctx.Request.ReadFromJsonAsync<ProgramClickReport>(ctx.RequestAborted);
                var ua = ctx.Request.Headers.UserAgent.ToString();
                if (report is null || !VisitClassifier.ShouldCountProgramClick(report.L, ua, ctx.User.IsInRole("Administrator"))
                    || !await programs.IsKnownAsync(report.Id, ctx.RequestAborted))
                    return Results.NoContent();

                var now = DateTime.UtcNow;
                var hash = VisitClassifier.VisitorHash(security.Value.ReporterIpSalt,
                    ctx.Connection.RemoteIpAddress?.ToString(), ua);
                var capKey = $"program-click-cap:{hash}:{VisitClassifier.FloridaDay(now):yyyyMMdd}";
                var seen = cache.GetOrCreate(capKey, e => { e.AbsoluteExpirationRelativeToNow = TimeSpan.FromHours(26); return new int[1]; })!;
                if (Interlocked.Increment(ref seen[0]) > VisitClassifier.MaxProgramClicksPerVisitorPerDay)
                    return Results.NoContent();

                recorder.Record(new ProgramClickHit(now, report.Id!, report.L!));
            }
            catch (Exception ex)
            {
                logs.CreateLogger("VisitEndpoint").LogDebug(ex, "A program-panel click was not counted");
            }
            return Results.NoContent();
        }).DisableAntiforgery();
}
