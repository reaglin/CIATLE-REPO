using FluentValidation;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using PreseMakerRepo.Api.Models.Requests;
using PreseMakerRepo.Api.Services;
using PreseMakerRepo.Core.Enums;

namespace PreseMakerRepo.Api.Pages.Browse;

/// <summary>
/// "Request a Curriculum Guide". Two ways in:
/// <list type="bullet">
/// <item>The one-click Request Guide button (<see cref="OnPostQuickAsync"/>) — posted by site.js, answers JSON.
///       Without JavaScript the button is a link to this page, which asks for one more click.</item>
/// <item>The form — a listed course needs only an optional note; a course that is not listed yet
///       (reached from an empty search) needs its title and a school.</item>
/// </list>
/// Requests are anonymous: no email is collected.
/// </summary>
public class RequestGuideModel : PageModel
{
    public const string WeeklyNote = "Guides are written in order of demand and the site is updated weekly — check back.";

    private readonly GuideRequestService _service;
    private readonly IValidator<CreateGuideRequestRequest> _validator;

    public RequestGuideModel(GuideRequestService service, IValidator<CreateGuideRequestRequest> validator)
    {
        _service = service;
        _validator = validator;
    }

    [BindProperty] public string CourseId { get; set; } = string.Empty;
    [BindProperty] public string? CourseTitle { get; set; }
    [BindProperty] public string? Institution { get; set; }
    [BindProperty] public string? Reason { get; set; }

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
        var request = new CreateGuideRequestRequest(CourseId, CourseTitle, Institution, Reason, null);
        var v = await _validator.ValidateAsync(request);
        if (GuideRequestService.TryNormalizeCourseId(CourseId, out var normalized)) await LookupAsync(normalized);
        if (!v.IsValid)
        {
            Errors.AddRange(v.Errors.Select(e => e.ErrorMessage).Distinct());
            return Page();
        }

        var result = await _service.CreateAsync(request, ClientIp(), UserId(), GuideRequestChannel.Form);
        CourseId = result.CourseId;
        await LookupAsync(result.CourseId);

        switch (result.Outcome)
        {
            case GuideRequestService.CreateOutcome.GuideExists:
            case GuideRequestService.CreateOutcome.RateLimited:
                Errors.Add(MessageFor(result));
                return Page();
            case GuideRequestService.CreateOutcome.DetailsRequired:
                if (string.IsNullOrWhiteSpace(CourseTitle)) Errors.Add("Enter the course title.");
                if (string.IsNullOrWhiteSpace(Institution)) Errors.Add("Enter a school where the course is offered.");
                return Page();
            default:
                Submitted = true;
                ResultMessage = MessageFor(result);
                return Page();
        }
    }

    /// <summary>The one-click button. Answers JSON for site.js; a plain form post is redirected back.</summary>
    public async Task<IActionResult> OnPostQuickAsync(string? course, string? returnUrl)
    {
        var wantsJson = Request.Headers.Accept.ToString().Contains("application/json", StringComparison.OrdinalIgnoreCase);
        if (!GuideRequestService.TryNormalizeCourseId(course, out var id))
        {
            return wantsJson
                ? new JsonResult(new { outcome = "invalid", message = "That is not a course number." })
                : RedirectToPage(new { course });
        }

        var result = await _service.CreateAsync(new CreateGuideRequestRequest(id, null, null, null, null),
            ClientIp(), UserId(), GuideRequestChannel.Button);
        var message = MessageFor(result);
        var redirect = result.Outcome switch
        {
            GuideRequestService.CreateOutcome.GuideExists => Url.Page("/Browse/Guide", new { courseId = id }),
            GuideRequestService.CreateOutcome.DetailsRequired => Url.Page("/Browse/RequestGuide", new { course = id }),
            _ => null
        };

        if (wantsJson)
        {
            return new JsonResult(new
            {
                outcome = char.ToLowerInvariant(result.Outcome.ToString()[0]) + result.Outcome.ToString()[1..],
                courseId = id,
                requestCount = result.RequestCount,
                message,
                redirect
            });
        }

        if (redirect is not null) return LocalRedirect(redirect);
        TempData[result.Outcome == GuideRequestService.CreateOutcome.RateLimited ? "Error" : "Success"] = message;
        return LocalRedirect(Url.IsLocalUrl(returnUrl) ? returnUrl! : Url.Page("/Browse/Course", new { courseId = id })!);
    }

    private static string MessageFor(GuideRequestService.CreateResult result) => result.Outcome switch
    {
        GuideRequestService.CreateOutcome.Created => result.RequestCount > 1
            ? $"Requested. {result.RequestCount} people have now asked for a guide to {result.CourseId}. {WeeklyNote}"
            : $"Requested. Your request for {result.CourseId} is in the queue. {WeeklyNote}",
        GuideRequestService.CreateOutcome.AlreadyRequested =>
            $"You have already requested {result.CourseId} — it is in the queue. {WeeklyNote}",
        GuideRequestService.CreateOutcome.GuideExists =>
            $"A curriculum guide for {result.CourseId} is already published.",
        GuideRequestService.CreateOutcome.RateLimited =>
            "Too many requests from your connection this hour. Please try again later.",
        _ => $"{result.CourseId} is not listed yet — tell us its title and a school that offers it."
    };

    private string ClientIp() => HttpContext.Connection.RemoteIpAddress?.ToString() ?? "unknown";

    private string? UserId() => User.Identity?.IsAuthenticated == true ? User.FindFirst("sub")?.Value : null;

    private async Task LookupAsync(string id)
    {
        var (inTax, title, hasGuide, _) = await _service.LookupAsync(id);
        InTaxonomy = inTax;
        TaxonomyTitle = title;
        HasGuide = hasGuide;
        OpenRequests = await _service.WaitingCountAsync(id);
    }
}
