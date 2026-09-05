using FluentValidation;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using PreseMakerRepo.Api.Models;
using PreseMakerRepo.Api.Models.Requests;
using PreseMakerRepo.Api.Models.Responses;
using PreseMakerRepo.Api.Services;
using PreseMakerRepo.Core.Enums;

namespace PreseMakerRepo.Api.Controllers;

/// <summary>
/// Curriculum guide requests — the demand signal for the content pipeline.
///   POST  /api/v1/guide-requests                    [Public]  a visitor asks for a guide
///   GET   /api/v1/guide-requests?status=open        [Admin]   per-course ranking (queue tool input)
///   PATCH /api/v1/guide-requests/{courseId}/status  [Admin]   triage
/// </summary>
[ApiController]
public class GuideRequestsController : ControllerBase
{
    private readonly GuideRequestService _service;
    public GuideRequestsController(GuideRequestService service) => _service = service;

    [HttpPost("api/v1/guide-requests")]
    public async Task<IActionResult> Create(
        [FromBody] CreateGuideRequestRequest request,
        [FromServices] IValidator<CreateGuideRequestRequest> validator)
    {
        var vResult = await validator.ValidateAsync(request);
        if (!vResult.IsValid)
        {
            var details = vResult.Errors.Select(e => new FieldError(e.PropertyName, e.ErrorMessage)).ToList();
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "Validation failed.", details));
        }

        var ip = HttpContext.Connection.RemoteIpAddress?.ToString() ?? "unknown";
        var userId = User.Identity?.IsAuthenticated == true ? User.FindFirst("sub")?.Value : null;
        var result = await _service.CreateAsync(request, ip, userId);

        return result.Outcome switch
        {
            GuideRequestService.CreateOutcome.GuideExists => Conflict(ApiResponse<object?>.Fail(
                ErrorCodes.GuideAlreadyExists, $"A curriculum guide for {result.CourseId} is already published.")),
            GuideRequestService.CreateOutcome.RateLimited => StatusCode(429, ApiResponse<object?>.Fail(
                ErrorCodes.RateLimitExceeded, "Too many requests. Please try again later.")),
            GuideRequestService.CreateOutcome.AlreadyRequested => Ok(ApiResponse<GuideRequestCreatedResponse>.Ok(
                new GuideRequestCreatedResponse(result.CourseId, result.RequestCount, true,
                    "You have already requested this guide today. Thank you — it is on the list."))),
            _ => Ok(ApiResponse<GuideRequestCreatedResponse>.Ok(
                new GuideRequestCreatedResponse(result.CourseId, result.RequestCount, false,
                    result.RequestCount > 1
                        ? $"Thank you. {result.RequestCount} people have now requested a guide for {result.CourseId}."
                        : $"Thank you. Your request for {result.CourseId} has been recorded.")))
        };
    }

    [HttpGet("api/v1/guide-requests")]
    [Authorize(Policy = "AdminOnly")]
    public async Task<IActionResult> List([FromQuery] string? status = "open", [FromQuery] int minCount = 1)
    {
        GuideRequestStatus? st = null;
        if (!string.IsNullOrWhiteSpace(status) && !string.Equals(status, "all", StringComparison.OrdinalIgnoreCase))
        {
            if (!Enum.TryParse<GuideRequestStatus>(status, true, out var parsed))
                return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError,
                    "status must be one of: open, queued, published, declined, all."));
            st = parsed;
        }
        var list = await _service.SummaryAsync(st, Math.Max(1, minCount));
        return Ok(ApiResponse<IReadOnlyList<GuideRequestSummaryResponse>>.Ok(list));
    }

    [HttpPatch("api/v1/guide-requests/{courseId}/status")]
    [Authorize(Policy = "AdminOnly")]
    public async Task<IActionResult> SetStatus(string courseId,
        [FromBody] SetGuideRequestStatusRequest request,
        [FromServices] IValidator<SetGuideRequestStatusRequest> validator)
    {
        var vResult = await validator.ValidateAsync(request);
        if (!vResult.IsValid)
        {
            var details = vResult.Errors.Select(e => new FieldError(e.PropertyName, e.ErrorMessage)).ToList();
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "Validation failed.", details));
        }
        if (!GuideRequestService.TryNormalizeCourseId(courseId, out var id))
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.InvalidCourseId, "Invalid course id."));

        var status = Enum.Parse<GuideRequestStatus>(request.Status, true);
        var updated = await _service.SetStatusAsync(id, status, request.Notes);
        if (updated == 0)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.GuideRequestNotFound, $"No requests found for {id}."));
        return Ok(ApiResponse<MessageResponse>.Ok(new MessageResponse($"{updated} request(s) for {id} marked {status}.")));
    }
}
