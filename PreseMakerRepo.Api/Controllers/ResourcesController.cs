using FluentValidation;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using PreseMakerRepo.Api.Models;
using PreseMakerRepo.Api.Models.Requests;
using PreseMakerRepo.Api.Models.Responses;
using PreseMakerRepo.Api.Services;
using Outcome = PreseMakerRepo.Api.Services.ResourceService.ChangeOutcome;

namespace PreseMakerRepo.Api.Controllers;

/// <summary>
/// Course resources. Every listing belongs to one course; the same link may be listed for many courses, each
/// with its own title and summary. Contract for the reviewing AI session: Tools/RESOURCE_API.md.
///   GET    /api/v1/courses/{courseId}/resources            [Public]  a course's listings
///   POST   /api/v1/courses/{courseId}/resources            [Public]  suggest a link (review queue)
///   GET    /api/v1/resources?url=…                         [Public]  every course listing that link
///   GET    /api/v1/resources/{id}                          [Public]  one listing
///   POST   /api/v1/resource-submissions/{id}/approve       [Admin]   list it (title, summary, alsoFor)
///   POST   /api/v1/resource-submissions/{id}/reject        [Admin]   with a public reason
///   POST   /api/v1/resources                               [Admin]   list a link directly for courses
///   PATCH  /api/v1/resources/{id}                          [Admin]   edit / remove / restore one listing
///   DELETE /api/v1/resources/{id}                          [Admin]   delete one listing
/// The review queue itself is GET /api/v1/queue/resources (QueueController).
/// </summary>
[ApiController]
public class ResourcesController : ControllerBase
{
    private readonly ResourceService _resources;

    public ResourcesController(ResourceService resources) => _resources = resources;

    [HttpGet("api/v1/courses/{courseId}/resources")]
    public async Task<IActionResult> ForCourse(string courseId)
    {
        if (!await _resources.CourseIsListedAsync(courseId))
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.CourseNotFound, "Course not found."));
        return Ok(ApiResponse<IReadOnlyList<CourseResourceDto>>.Ok(await _resources.ForCourseAsync(courseId)));
    }

    [HttpPost("api/v1/courses/{courseId}/resources")]
    public async Task<IActionResult> Submit(string courseId, [FromBody] SubmitResourceRequest request,
        [FromServices] IValidator<SubmitResourceRequest> validator)
    {
        var validation = await validator.ValidateAsync(request);
        if (!validation.IsValid) return BadRequest(ValidationError(validation));

        var ip = HttpContext.Connection.RemoteIpAddress?.ToString() ?? "unknown";
        var userId = User.Identity?.IsAuthenticated == true ? User.FindFirst("sub")?.Value : null;
        var result = await _resources.SubmitAsync(courseId, request, ip, userId);

        return result.Outcome switch
        {
            ResourceService.SubmitOutcome.CourseNotFound =>
                NotFound(ApiResponse<object?>.Fail(ErrorCodes.CourseNotFound, result.Message)),
            ResourceService.SubmitOutcome.InvalidUrl =>
                BadRequest(ApiResponse<object?>.Fail(ErrorCodes.InvalidResourceUrl, result.Message)),
            ResourceService.SubmitOutcome.RateLimited =>
                StatusCode(429, ApiResponse<object?>.Fail(ErrorCodes.RateLimitExceeded, result.Message)),
            _ => Ok(ApiResponse<ResourceSubmittedResponse>.Ok(
                new ResourceSubmittedResponse(result.SubmissionId, Camel(result.Outcome.ToString()), result.Message)))
        };
    }

    /// <summary>Thumbs-up one course's listing, or take the vote back. Anonymous, one vote per visitor.</summary>
    [HttpPost("api/v1/resources/{id:guid}/helpful")]
    public async Task<IActionResult> Helpful(Guid id)
    {
        var ip = HttpContext.Connection.RemoteIpAddress?.ToString() ?? "unknown";
        var result = await _resources.VoteAsync(id, ip);
        return result.Outcome switch
        {
            ResourceService.VoteOutcome.NotFound =>
                NotFound(ApiResponse<object?>.Fail(ErrorCodes.ResourceNotFound, "Resource not found.")),
            ResourceService.VoteOutcome.RateLimited =>
                StatusCode(429, ApiResponse<object?>.Fail(ErrorCodes.RateLimitExceeded,
                    "Too many votes from your connection this hour. Please try again later.")),
            _ => Ok(ApiResponse<ResourceVoteResponse>.Ok(
                new ResourceVoteResponse(id, result.HelpfulCount, result.Voted)))
        };
    }

    [HttpGet("api/v1/resources")]
    public async Task<IActionResult> ForUrl([FromQuery] string? url)
    {
        var result = await _resources.ForUrlAsync(url, includeRemoved: User.IsInRole("Administrator"));
        return result.Outcome == Outcome.Done
            ? Ok(ApiResponse<IReadOnlyList<CourseResourceDto>>.Ok(result.Value!))
            : BadRequest(ApiResponse<object?>.Fail(ErrorCodes.InvalidResourceUrl, result.Message));
    }

    [HttpGet("api/v1/resources/{id:guid}")]
    public async Task<IActionResult> Get(Guid id)
    {
        var resource = await _resources.GetAsync(id, includeRemoved: User.IsInRole("Administrator"));
        return resource is null
            ? NotFound(ApiResponse<object?>.Fail(ErrorCodes.ResourceNotFound, "Resource not found."))
            : Ok(ApiResponse<CourseResourceDto>.Ok(resource));
    }

    [Authorize(Policy = "AdminOnly")]
    [HttpPost("api/v1/resource-submissions/{id:guid}/approve")]
    public async Task<IActionResult> Approve(Guid id, [FromBody] ApproveResourceSubmissionRequest request,
        [FromServices] IValidator<ApproveResourceSubmissionRequest> validator)
    {
        var validation = await validator.ValidateAsync(request);
        if (!validation.IsValid) return BadRequest(ValidationError(validation));
        var result = await _resources.ApproveAsync(id, request);
        return result.Outcome == Outcome.Done
            ? Ok(ApiResponse<ResourceDecisionResponse>.Ok(result.Value!))
            : Failure(result.Outcome, result.Message, submission: true);
    }

    [Authorize(Policy = "AdminOnly")]
    [HttpPost("api/v1/resource-submissions/{id:guid}/reject")]
    public async Task<IActionResult> Reject(Guid id, [FromBody] RejectResourceSubmissionRequest request,
        [FromServices] IValidator<RejectResourceSubmissionRequest> validator)
    {
        var validation = await validator.ValidateAsync(request);
        if (!validation.IsValid) return BadRequest(ValidationError(validation));
        var result = await _resources.RejectAsync(id, request.Note!);
        return result.Outcome == Outcome.Done
            ? Ok(ApiResponse<ResourceDecisionResponse>.Ok(result.Value!))
            : Failure(result.Outcome, result.Message, submission: true);
    }

    [Authorize(Policy = "AdminOnly")]
    [HttpPost("api/v1/resources")]
    public async Task<IActionResult> Create([FromBody] CreateResourceRequest request,
        [FromServices] IValidator<CreateResourceRequest> validator)
    {
        var validation = await validator.ValidateAsync(request);
        if (!validation.IsValid) return BadRequest(ValidationError(validation));
        var result = await _resources.CreateAsync(request);
        return result.Outcome == Outcome.Done
            ? Ok(ApiResponse<ResourceCreateResponse>.Ok(result.Value!))
            : Failure(result.Outcome, result.Message);
    }

    [Authorize(Policy = "AdminOnly")]
    [HttpPatch("api/v1/resources/{id:guid}")]
    public async Task<IActionResult> Update(Guid id, [FromBody] UpdateResourceRequest request,
        [FromServices] IValidator<UpdateResourceRequest> validator)
    {
        var validation = await validator.ValidateAsync(request);
        if (!validation.IsValid) return BadRequest(ValidationError(validation));
        var result = await _resources.UpdateAsync(id, request);
        return result.Outcome == Outcome.Done
            ? Ok(ApiResponse<CourseResourceDto>.Ok(result.Value!))
            : Failure(result.Outcome, result.Message);
    }

    [Authorize(Policy = "AdminOnly")]
    [HttpDelete("api/v1/resources/{id:guid}")]
    public async Task<IActionResult> Delete(Guid id) =>
        await _resources.DeleteAsync(id) == Outcome.Done
            ? Ok(ApiResponse<MessageResponse>.Ok(new MessageResponse("Resource listing deleted.")))
            : NotFound(ApiResponse<object?>.Fail(ErrorCodes.ResourceNotFound, "Resource not found."));

    private IActionResult Failure(Outcome outcome, string message, bool submission = false) => outcome switch
    {
        Outcome.NotFound => NotFound(ApiResponse<object?>.Fail(
            submission ? ErrorCodes.ResourceSubmissionNotFound : ErrorCodes.ResourceNotFound, message)),
        Outcome.NotPending => Conflict(ApiResponse<object?>.Fail(ErrorCodes.SubmissionNotPending, message)),
        Outcome.InvalidUrl => BadRequest(ApiResponse<object?>.Fail(ErrorCodes.InvalidResourceUrl, message)),
        _ => UnprocessableEntity(ApiResponse<object?>.Fail(ErrorCodes.CourseNotFound, message))
    };

    private static ApiResponse<object?> ValidationError(FluentValidation.Results.ValidationResult result) =>
        ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "One or more validation errors occurred.",
            result.Errors.Select(e => new FieldError(e.PropertyName, e.ErrorMessage)).ToList());

    private static string Camel(string s) => char.ToLowerInvariant(s[0]) + s[1..];
}
