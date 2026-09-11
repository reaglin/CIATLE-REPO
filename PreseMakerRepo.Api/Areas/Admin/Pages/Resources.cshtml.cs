using FluentValidation;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using PreseMakerRepo.Api.Models.Requests;
using PreseMakerRepo.Api.Models.Responses;
using PreseMakerRepo.Api.Services;

namespace PreseMakerRepo.Api.Areas.Admin.Pages;

/// <summary>
/// Course resources for Ron: the review queue (approve / reject / reopen) and every course listing (edit /
/// remove / restore / delete). The AI reviewer does the same work over the API; this page is for reversals.
/// </summary>
public class ResourcesModel : PageModel
{
    private readonly ResourceService _resources;
    private readonly IValidator<ApproveResourceSubmissionRequest> _approveValidator;
    private readonly IValidator<UpdateResourceRequest> _updateValidator;

    public ResourcesModel(ResourceService resources,
        IValidator<ApproveResourceSubmissionRequest> approveValidator,
        IValidator<UpdateResourceRequest> updateValidator)
    {
        _resources = resources;
        _approveValidator = approveValidator;
        _updateValidator = updateValidator;
    }

    /// <summary>pending · decided · listed</summary>
    [BindProperty(SupportsGet = true)] public string Tab { get; set; } = "pending";
    [BindProperty(SupportsGet = true)] public string? Q { get; set; }

    public ResourceQueueResponse? Queue { get; set; }
    public List<CourseResourceDto> Listings { get; set; } = [];
    [TempData] public string? Message { get; set; }

    public async Task OnGetAsync()
    {
        if (Tab == "listed")
            Listings = await _resources.AdminListAsync(Q);
        else
            Queue = await _resources.QueueAsync(Tab == "decided" ? ResourceService.QueueDecided : ResourceService.QueuePending);
    }

    public async Task<IActionResult> OnPostApproveAsync(Guid id, string? title, string? summary, string? alsoFor, string? note)
    {
        var also = (alsoFor ?? string.Empty)
            .Split([',', ';', ' ', '\n', '\r', '\t'], StringSplitOptions.RemoveEmptyEntries)
            .Select(c => new ResourceCourseInput(c, null, null))
            .ToList();
        var request = new ApproveResourceSubmissionRequest(title, summary, note, also);
        var validation = await _approveValidator.ValidateAsync(request);
        if (!validation.IsValid)
        {
            Message = "Not approved: " + string.Join(" ", validation.Errors.Select(e => e.ErrorMessage));
            return RedirectToPage(new { Tab, Q });
        }
        var result = await _resources.ApproveAsync(id, request);
        var unknown = result.Value?.Results.Where(r => r.Outcome == ResourceService.WriteOutcomes.UnknownCourse).Select(r => r.CourseId).ToList();
        Message = result.Message + (unknown is { Count: > 0 } ? $" Not listed on the site: {string.Join(", ", unknown)}." : "");
        return RedirectToPage(new { Tab, Q });
    }

    public async Task<IActionResult> OnPostRejectAsync(Guid id, string? note)
    {
        if (string.IsNullOrWhiteSpace(note))
        {
            Message = "Not rejected: give a short reason (it is shown in the public queue).";
            return RedirectToPage(new { Tab, Q });
        }
        var result = await _resources.RejectAsync(id, note.Length > 300 ? note[..300] : note);
        Message = result.Message;
        return RedirectToPage(new { Tab, Q });
    }

    public async Task<IActionResult> OnPostReopenAsync(Guid id)
    {
        Message = await _resources.ReopenAsync(id) == ResourceService.ChangeOutcome.Done
            ? "Suggestion returned to the queue."
            : "Suggestion not found.";
        return RedirectToPage(new { Tab, Q });
    }

    public async Task<IActionResult> OnPostUpdateAsync(Guid id, string? title, string? summary)
    {
        var request = new UpdateResourceRequest(title, summary, null);
        var validation = await _updateValidator.ValidateAsync(request);
        Message = validation.IsValid
            ? (await _resources.UpdateAsync(id, request)).Message
            : "Not saved: " + string.Join(" ", validation.Errors.Select(e => e.ErrorMessage));
        return RedirectToPage(new { Tab, Q });
    }

    public async Task<IActionResult> OnPostStatusAsync(Guid id, string status)
    {
        Message = (await _resources.UpdateAsync(id, new UpdateResourceRequest(null, null, status))).Message;
        return RedirectToPage(new { Tab, Q });
    }

    public async Task<IActionResult> OnPostDeleteAsync(Guid id)
    {
        Message = await _resources.DeleteAsync(id) == ResourceService.ChangeOutcome.Done ? "Listing deleted." : "Listing not found.";
        return RedirectToPage(new { Tab, Q });
    }
}
