using Microsoft.AspNetCore.Mvc;
using PreseMakerRepo.Api.Models;
using PreseMakerRepo.Api.Models.Responses;
using PreseMakerRepo.Api.Services;

namespace PreseMakerRepo.Api.Controllers;

/// <summary>
/// The public queues — readable by anyone, including the AI sessions that work them.
///   GET /api/v1/queue/guides?status=waiting|published|declined|all   [Public]
/// </summary>
[ApiController]
public class QueueController : ControllerBase
{
    private readonly GuideRequestService _guideRequests;

    public QueueController(GuideRequestService guideRequests) => _guideRequests = guideRequests;

    [HttpGet("api/v1/queue/guides")]
    public async Task<IActionResult> Guides([FromQuery] string? status = null)
    {
        if (!GuideRequestService.TryParseQueueFilter(status, out var filter))
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError,
                "status must be one of: waiting, published, declined, all."));

        return Ok(ApiResponse<PublicGuideQueueResponse>.Ok(await _guideRequests.PublicQueueAsync(filter)));
    }
}
