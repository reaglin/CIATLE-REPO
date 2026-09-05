using FluentValidation;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using PreseMakerRepo.Api.Models.Requests;
using PreseMakerRepo.Api.Services;

namespace PreseMakerRepo.Api.Pages.Browse;

/// <summary>
/// "Request a Curriculum Guide" — reached from a course page without a guide, a guide URL
/// that does not exist, or an empty search. Any SCNS-shaped course id is accepted; the
/// taxonomy title is pre-filled when the course is known.
/// </summary>
public class RequestGuideModel : PageModel
{
    private readonly GuideRequestService _service;
    private readonly IValidator<CreateGuideRequestRequest> _validator;

    public RequestGuideModel(GuideRequestService service, IValidator<CreateGuideRequestRequest> validator)
    {
        _service = service;
        _validator = validator;
    }

    [BindProperty] public string CourseId { get; set; } = string.Empty;
    [BindProperty] public string CourseTitle { get; set; } = string.Empty;
    [BindProperty] public string Institution { get; set; } = string.Empty;
    [BindProperty] public string? Reason { get; set; }
    [BindProperty] public string? Email { get; set; }

    public bool InTaxonomy { get; set; }
    public bool HasGuide { get; set; }
    public int OpenRequests { get; set; }
    public string? TaxonomyTitle { get; set; }
    public string? ResultMessage { get; set; }
    public bool Submitted { get; set; }
    public List<string> Errors { get; } = new();

    public async Task OnGetAsync(string? course)
    {
        if (!string.IsNullOrWhiteSpace(course) && GuideRequestService.TryNormalizeCourseId(course, out var id))
        {
            CourseId = id;
            await LookupAsync(id);
        }
        else if (!string.IsNullOrWhiteSpace(course))
        {
            CourseId = course.Trim().ToUpperInvariant();
        }
    }

    public async Task<IActionResult> OnPostAsync()
    {
        var request = new CreateGuideRequestRequest(CourseId, CourseTitle, Institution, Reason, Email);
        var v = await _validator.ValidateAsync(request);
        if (!v.IsValid)
        {
            Errors.AddRange(v.Errors.Select(e => e.ErrorMessage).Distinct());
            if (GuideRequestService.TryNormalizeCourseId(CourseId, out var id0)) await LookupAsync(id0);
            return Page();
        }

        var ip = HttpContext.Connection.RemoteIpAddress?.ToString() ?? "unknown";
        var userId = User.Identity?.IsAuthenticated == true ? User.FindFirst("sub")?.Value : null;
        var result = await _service.CreateAsync(request, ip, userId);
        CourseId = result.CourseId;
        await LookupAsync(result.CourseId);

        switch (result.Outcome)
        {
            case GuideRequestService.CreateOutcome.GuideExists:
                Errors.Add($"A curriculum guide for {result.CourseId} is already published.");
                return Page();
            case GuideRequestService.CreateOutcome.RateLimited:
                Errors.Add("Too many requests from your connection this hour. Please try again later.");
                return Page();
            case GuideRequestService.CreateOutcome.AlreadyRequested:
                Submitted = true;
                ResultMessage = "You have already requested this guide today — thank you, it is on the list.";
                return Page();
            default:
                Submitted = true;
                ResultMessage = result.RequestCount > 1
                    ? $"Thank you. {result.RequestCount} people have now asked for a guide to {result.CourseId}. Requests decide what we build next."
                    : $"Thank you. Your request for {result.CourseId} has been recorded. Requests decide what we build next.";
                return Page();
        }
    }

    private async Task LookupAsync(string id)
    {
        var (inTax, title, hasGuide, open) = await _service.LookupAsync(id);
        InTaxonomy = inTax; TaxonomyTitle = title; HasGuide = hasGuide; OpenRequests = open;
        if (inTax && string.IsNullOrWhiteSpace(CourseTitle) && !string.IsNullOrWhiteSpace(title)) CourseTitle = title;
    }
}
