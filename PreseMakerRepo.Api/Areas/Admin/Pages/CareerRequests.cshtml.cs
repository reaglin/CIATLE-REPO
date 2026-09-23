using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Api.Models.Responses;
using PreseMakerRepo.Api.Services;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Api.Areas.Admin.Pages;

/// <summary>
/// Career-path requests ranked by demand, with triage — the career twin of Guide Requests. The
/// Tools session reads the same ranking over GET /api/v1/career-requests. Also manages which
/// crosswalk occupations are hidden from the area pages.
/// </summary>
public class CareerRequestsModel : PageModel
{
    private readonly CareerRequestService _service;
    private readonly AppDbContext _db;

    public CareerRequestsModel(CareerRequestService service, AppDbContext db)
    {
        _service = service;
        _db = db;
    }

    public sealed record HiddenRow(string CipCode, string SocCode, string SocTitle);

    [BindProperty(SupportsGet = true)] public string Status { get; set; } = "open";
    public IReadOnlyList<CareerRequestSummaryResponse> Items { get; set; } = [];
    public IReadOnlyList<HiddenRow> Hidden { get; set; } = [];
    public int TotalRequests { get; set; }
    [TempData] public string? Message { get; set; }
    [TempData] public bool MessageOk { get; set; }

    public async Task OnGetAsync()
    {
        // Requests whose occupation a published path now covers are closed on view.
        await _service.ClosePublishedAsync();
        CareerRequestStatus? st = Enum.TryParse<CareerRequestStatus>(Status, true, out var parsed) ? parsed : null;
        Items = await _service.SummaryAsync(st);
        TotalRequests = Items.Sum(i => i.RequestCount);
        Hidden = await _db.CipOccupations.AsNoTracking()
            .Where(o => o.IsHidden)
            .OrderBy(o => o.CipCode).ThenBy(o => o.SocTitle)
            .Select(o => new HiddenRow(o.CipCode, o.SocCode, o.SocTitle))
            .ToListAsync();
    }

    // ⚠ "newStatus", not "status" -- see GuideRequestsModel.OnPostSetStatusAsync for why.
    public async Task<IActionResult> OnPostSetStatusAsync(string soc, string newStatus, string? notes)
    {
        if (CareerRequestService.TryNormalizeSoc(soc, out var s) &&
            Enum.TryParse<CareerRequestStatus>(newStatus, true, out var st))
        {
            var n = await _service.SetStatusAsync(s, st, notes);
            MessageOk = n > 0;
            Message = n > 0 ? $"{s}: {n} request(s) marked {st}." : $"No requests found for {s}.";
        }
        else
        {
            MessageOk = false;
            Message = "The status was not changed: choose a status from the list and try again.";
        }
        return RedirectToPage(new { Status });
    }

    public async Task<IActionResult> OnPostHiddenAsync(string cip, string soc, bool hide)
    {
        if (CareerRequestService.TryNormalizeCipGroup(cip, out var c) &&
            CareerRequestService.TryNormalizeSoc(soc, out var s) &&
            await _service.SetHiddenAsync(c, s, hide))
        {
            MessageOk = true;
            Message = $"{s} under {c} is now {(hide ? "hidden from" : "shown on")} the Career Paths page.";
        }
        else
        {
            MessageOk = false;
            Message = $"No occupation {soc} is listed under CIP {cip}. Check both codes on the area page.";
        }
        return RedirectToPage(new { Status });
    }
}
