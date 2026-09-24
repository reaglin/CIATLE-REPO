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
/// Career-path requests — the demand signal once paths are request-driven (Ron, 2026-09-23).
///   POST  /api/v1/career-requests                           [Public]  ask for a path
///   GET   /api/v1/career-requests?status=open               [Admin]   per-occupation ranking
///   PATCH /api/v1/career-requests/{socCode}/status          [Admin]   triage
///   GET   /api/v1/cip/{code}/occupations                    [Public]  what can be requested under a group
///   PATCH /api/v1/cip/{code}/occupations/{socCode}          [Admin]   hide or show one pairing
/// The public queue is GET /api/v1/queue/careers (QueueController).
/// </summary>
[ApiController]
public class CareerRequestsController : ControllerBase
{
    private readonly CareerRequestService _service;
    public CareerRequestsController(CareerRequestService service) => _service = service;

    [HttpPost("api/v1/career-requests")]
    public async Task<IActionResult> Create(
        [FromBody] CreateCareerRequestRequest request,
        [FromServices] IValidator<CreateCareerRequestRequest> validator)
    {
        var v = await validator.ValidateAsync(request);
        if (!v.IsValid)
        {
            var details = v.Errors.Select(e => new FieldError(e.PropertyName, e.ErrorMessage)).ToList();
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "Validation failed.", details));
        }

        var ip = HttpContext.Connection.RemoteIpAddress?.ToString() ?? "unknown";
        var userId = User.Identity?.IsAuthenticated == true ? User.FindFirst("sub")?.Value : null;
        var r = await _service.CreateAsync(request.SocCode!, request.CipCode!, request.Reason, ip, userId,
            CareerRequestChannel.Api);
        var message = CareerRequestService.MessageFor(r);

        return r.Outcome switch
        {
            CareerRequestService.CreateOutcome.NotListed => NotFound(ApiResponse<object?>.Fail(
                ErrorCodes.OccupationNotFound, $"{r.SocCode} is not listed under CIP {request.CipCode}.")),
            CareerRequestService.CreateOutcome.PathExists => Conflict(ApiResponse<object?>.Fail(
                ErrorCodes.CareerPathExists, $"{message} See /careers/{r.PathSlug}.")),
            CareerRequestService.CreateOutcome.RateLimited or CareerRequestService.CreateOutcome.NetworkRateLimited =>
                StatusCode(429, ApiResponse<object?>.Fail(ErrorCodes.RateLimitExceeded, message)),
            _ => Ok(ApiResponse<CareerRequestCreatedResponse>.Ok(new CareerRequestCreatedResponse(
                r.SocCode, r.SocTitle, r.RequestCount,
                r.Outcome == CareerRequestService.CreateOutcome.AlreadyRequested, message)))
        };
    }

    [HttpGet("api/v1/career-requests")]
    [Authorize(Policy = "AdminOnly")]
    public async Task<IActionResult> List([FromQuery] string? status = "open")
    {
        CareerRequestStatus? st = null;
        if (!string.IsNullOrWhiteSpace(status) && !string.Equals(status, "all", StringComparison.OrdinalIgnoreCase))
        {
            if (!Enum.TryParse<CareerRequestStatus>(status, true, out var parsed))
                return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError,
                    "status must be one of: open, queued, published, declined, all."));
            st = parsed;
        }
        await _service.ClosePublishedAsync();
        var list = await _service.SummaryAsync(st);
        return Ok(ApiResponse<IReadOnlyList<CareerRequestSummaryResponse>>.Ok(list));
    }

    [HttpPatch("api/v1/career-requests/{socCode}/status")]
    [Authorize(Policy = "AdminOnly")]
    public async Task<IActionResult> SetStatus(string socCode,
        [FromBody] SetCareerRequestStatusRequest request,
        [FromServices] IValidator<SetCareerRequestStatusRequest> validator)
    {
        var v = await validator.ValidateAsync(request);
        if (!v.IsValid)
        {
            var details = v.Errors.Select(e => new FieldError(e.PropertyName, e.ErrorMessage)).ToList();
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "Validation failed.", details));
        }
        if (!CareerRequestService.TryNormalizeSoc(socCode, out var soc))
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "socCode must look like 19-3051."));

        var status = Enum.Parse<CareerRequestStatus>(request.Status!, true);
        var n = await _service.SetStatusAsync(soc, status, request.Notes, request.PublicNote);
        if (n == 0)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.CareerRequestNotFound, $"No requests found for {soc}."));
        return Ok(ApiResponse<MessageResponse>.Ok(new MessageResponse($"{n} request(s) for {soc} marked {status}.")));
    }

    [HttpGet("api/v1/cip/{code}/occupations")]
    public async Task<IActionResult> Occupations(string code)
    {
        if (!CareerRequestService.TryNormalizeCipGroup(code, out var cip))
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError,
                "code must be a 4-digit CIP group such as 04.03."));
        var list = await _service.OccupationsAsync([cip]);
        return Ok(ApiResponse<IReadOnlyList<CipOccupationResponse>>.Ok(list));
    }

    [HttpPatch("api/v1/cip/{code}/occupations/{socCode}")]
    [Authorize(Policy = "AdminOnly")]
    public async Task<IActionResult> SetHidden(string code, string socCode, [FromBody] SetOccupationHiddenRequest request)
    {
        if (!CareerRequestService.TryNormalizeCipGroup(code, out var cip) ||
            !CareerRequestService.TryNormalizeSoc(socCode, out var soc))
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError,
                "Use a CIP group like 04.03 and a SOC code like 19-3051."));
        if (!await _service.SetHiddenAsync(cip, soc, request.IsHidden))
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.OccupationNotFound, $"{soc} is not listed under {cip}."));
        return Ok(ApiResponse<MessageResponse>.Ok(new MessageResponse(
            $"{soc} under {cip} is now {(request.IsHidden ? "hidden" : "shown")}.")));
    }
}
