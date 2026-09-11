using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using PreseMakerRepo.Api.Models;
using PreseMakerRepo.Api.Models.Requests;
using PreseMakerRepo.Api.Models.Responses;
using PreseMakerRepo.Api.Services;

namespace PreseMakerRepo.Api.Controllers;

/// <summary>
/// Institutions that offer courses (code → name).
///   GET  /api/v1/institutions          [Public]
///   PUT  /api/v1/institutions/{code}   [Admin]
///   POST /api/v1/institutions/batch    [Admin]  up to 1000
/// </summary>
[ApiController]
[Route("api/v1/institutions")]
public class InstitutionsController : ControllerBase
{
    private readonly CourseCatalogService _catalog;

    public InstitutionsController(CourseCatalogService catalog) => _catalog = catalog;

    [HttpGet]
    public async Task<IActionResult> List() =>
        Ok(ApiResponse<List<InstitutionDto>>.Ok(await _catalog.ListInstitutionsAsync(HttpContext.RequestAborted)));

    [Authorize(Policy = "AdminOnly")]
    [HttpPut("{code}")]
    public async Task<IActionResult> Upsert(string code, [FromBody] UpsertInstitutionRequest request)
    {
        if (request.Code is not null &&
            !string.Equals(request.Code.Trim(), code.Trim(), StringComparison.OrdinalIgnoreCase))
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "code in the body does not match the URL."));

        var batch = await _catalog.UpsertInstitutionsAsync([request with { Code = code }], HttpContext.RequestAborted);
        var result = batch.Results[0];
        return result.Outcome switch
        {
            CourseCatalogService.Outcomes.Failed =>
                BadRequest(ApiResponse<object?>.Fail(result.ErrorCode!, result.Message!, result.Fields)),
            CourseCatalogService.Outcomes.Created =>
                StatusCode(201, ApiResponse<InstitutionUpsertResult>.Ok(result)),
            _ => Ok(ApiResponse<InstitutionUpsertResult>.Ok(result))
        };
    }

    [Authorize(Policy = "AdminOnly")]
    [HttpPost("batch")]
    public async Task<IActionResult> Batch([FromBody] BatchUpsertInstitutionsRequest request)
    {
        var items = request.Institutions;
        if (items is null || items.Count == 0)
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "institutions must contain at least one institution."));
        if (items.Count > CourseCatalogService.MaxInstitutionBatch)
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.BatchTooLarge,
                $"A batch may hold at most {CourseCatalogService.MaxInstitutionBatch} institutions; this one has {items.Count}."));

        return Ok(ApiResponse<BatchUpsertInstitutionsResponse>.Ok(
            await _catalog.UpsertInstitutionsAsync(items, HttpContext.RequestAborted)));
    }
}
