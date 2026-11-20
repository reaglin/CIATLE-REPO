using Microsoft.Extensions.Options;
using PreseMakerRepo.Api.Options;
using PreseMakerRepo.Api.Services.Visits;

namespace PreseMakerRepo.Api.Middleware;

/// <summary>
/// Counts a page view once the page has been sent, when <see cref="VisitClassifier.ShouldCount"/>
/// says it was a person opening a public page. Only a salted hash of the address and browser is
/// kept. Runs after authentication, so administrators' own browsing is left out.
/// </summary>
public sealed class VisitCounterMiddleware
{
    private readonly RequestDelegate _next;
    private readonly VisitRecorder _recorder;
    private readonly string _salt;

    public VisitCounterMiddleware(RequestDelegate next, VisitRecorder recorder, IOptions<SecurityOptions> security)
    {
        _next = next;
        _recorder = recorder;
        _salt = security.Value.ReporterIpSalt;
    }

    public async Task InvokeAsync(HttpContext ctx)
    {
        await _next(ctx);

        try
        {
            var req = ctx.Request;
            var ua = req.Headers.UserAgent.ToString();
            var prefetch = req.Headers["Sec-Purpose"].ToString().Contains("prefetch", StringComparison.OrdinalIgnoreCase)
                        || req.Headers["Purpose"].ToString().Contains("prefetch", StringComparison.OrdinalIgnoreCase);
            if (!VisitClassifier.ShouldCount(req.Method, req.Path.Value, ctx.Response.StatusCode,
                    ctx.Response.ContentType, ua, ctx.User.IsInRole("Administrator"), prefetch))
                return;

            var ip = ctx.Connection.RemoteIpAddress?.ToString();
            _recorder.Record(new VisitHit(
                DateTime.UtcNow,
                VisitClassifier.VisitorHash(_salt, ip, ua),
                VisitClassifier.NormalizePath(req.Path.Value!),
                VisitClassifier.SourceOf(req.Headers.Referer.ToString(), req.Host.Host)));
        }
        catch
        {
            // Counting must never break a page.
        }
    }
}
