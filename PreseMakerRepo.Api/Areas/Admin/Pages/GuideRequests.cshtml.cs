using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using PreseMakerRepo.Api.Models.Responses;
using PreseMakerRepo.Api.Services;
using PreseMakerRepo.Core.Enums;

namespace PreseMakerRepo.Api.Areas.Admin.Pages;

/// <summary>Guide requests ranked by demand, with triage. The queue tool reads the same
/// ranking over the API (GET /api/v1/guide-requests) — see Tools/QUEUE_GUIDE.md.</summary>
public class GuideRequestsModel : PageModel
{
    private readonly GuideRequestService _service;
    public GuideRequestsModel(GuideRequestService service) => _service = service;

    [BindProperty(SupportsGet = true)] public string Status { get; set; } = "open";
    public IReadOnlyList<GuideRequestSummaryResponse> Items { get; set; } = [];
    public int TotalRequests { get; set; }
    public int HeldCount { get; set; }
    [TempData] public string? Message { get; set; }

    public async Task OnGetAsync()
    {
        // Requests whose guide has since been published are closed on view.
        await _service.ClosePublishedAsync();
        GuideRequestStatus? st = Enum.TryParse<GuideRequestStatus>(Status, true, out var parsed) ? parsed : null;
        Items = await _service.SummaryAsync(st);
        TotalRequests = Items.Sum(i => i.RequestCount);
        HeldCount = st == GuideRequestStatus.Held ? Items.Count : (await _service.SummaryAsync(GuideRequestStatus.Held)).Count;
    }

    /// <summary>Decline one held course, or the held courses the page showed ("shown"), each with the reason
    /// recorded when it was held. Never more than was on screen: a course put on hold since is left alone.</summary>
    public async Task<IActionResult> OnPostDeclineHeldAsync(string? courseId, string[]? shown)
    {
        var raw = !string.IsNullOrWhiteSpace(courseId) ? [courseId] : shown ?? [];
        var only = raw.Select(c => GuideRequestService.TryNormalizeCourseId(c, out var id) ? id : null)
            .OfType<string>().ToList();
        if (only.Count == 0) return RedirectToPage(new { Status });
        var declined = await _service.DeclineHeldAsync(only);
        Message = declined.Count == 0 ? "Nothing on hold was declined."
            : $"Declined with their reasons: {string.Join(", ", declined)}. The reasons now show in the public queue. "
              + "To undo one, open the Declined tab and set it to Open.";
        return RedirectToPage(new { Status });
    }

    // ⚠ The new status is "newStatus", not "status": the form also posts the hidden page filter as
    // "Status", form keys are case-insensitive, and a string parameter binds the FIRST value -- so a
    // parameter named "status" received the filter and every choice was silently ignored (found by the
    // UX review of 2026-09-23).
    public async Task<IActionResult> OnPostSetStatusAsync(string courseId, string newStatus, string? notes)
    {
        if (GuideRequestService.TryNormalizeCourseId(courseId, out var id) &&
            Enum.TryParse<GuideRequestStatus>(newStatus, true, out var st))
        {
            if (st == GuideRequestStatus.Held && string.IsNullOrWhiteSpace(notes))
            {
                Message = $"{id}: a hold needs its reason (type it in the box; it is shown publicly if declined).";
                return RedirectToPage(new { Status });
            }
            var n = await _service.SetStatusAsync(id, st, notes);
            Message = $"{id}: {n} request(s) marked {st}.";
        }
        return RedirectToPage(new { Status });
    }

    /// <summary>Open requests as CSV in queue.csv's column order (course_id, title, …) for a manual
    /// import; the queue tool's <c>import-requests</c> does the same over the API.</summary>
    public async Task<IActionResult> OnGetCsvAsync()
    {
        var items = await _service.SummaryAsync(GuideRequestStatus.Open);
        var sb = new System.Text.StringBuilder();
        sb.AppendLine("course_id,title,request_count,institutions,first_requested_utc,last_requested_utc,in_taxonomy");
        foreach (var i in items)
            sb.AppendLine(string.Join(",", Csv(i.CourseId), Csv(i.CourseTitle), i.RequestCount,
                Csv(string.Join("; ", i.Institutions)), i.FirstRequestedUtc.ToString("u"), i.LastRequestedUtc.ToString("u"), i.InTaxonomy));
        return File(System.Text.Encoding.UTF8.GetBytes(sb.ToString()), "text/csv",
            $"guide-requests-{DateTime.UtcNow:yyyyMMdd}.csv");
    }

    private static string Csv(string s) => "\"" + s.Replace("\"", "\"\"") + "\"";
}
