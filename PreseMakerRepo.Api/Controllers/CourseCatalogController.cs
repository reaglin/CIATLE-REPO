using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using PreseMakerRepo.Api.Models;
using PreseMakerRepo.Api.Models.Requests;
using PreseMakerRepo.Api.Models.Responses;
using PreseMakerRepo.Api.Services;

namespace PreseMakerRepo.Api.Controllers;

/// <summary>
/// Base course data — courses with or without a guide. Written by the content pipeline in Tools/
/// (contract: Tools/COURSE_API.md).
///   GET    /api/v1/courses/catalog                 [Public]  list for reconciliation (filters, paging)
///   GET    /api/v1/courses/{courseId}/offerings    [Public]  one course's base data + offerings
///   PUT    /api/v1/courses/{courseId}              [Admin]   upsert one course
///   POST   /api/v1/courses/batch                   [Admin]   upsert up to 500 courses
///   DELETE /api/v1/courses/{courseId}              [Admin]   remove a course created in error
/// </summary>
[ApiController]
public class CourseCatalogController : ControllerBase
{
    private readonly CourseCatalogService _catalog;

    public CourseCatalogController(CourseCatalogService catalog) => _catalog = catalog;

    [HttpGet("api/v1/courses/catalog")]
    public async Task<IActionResult> List(
        [FromQuery] string? prefix = null,
        [FromQuery] bool? hasGuide = null,
        [FromQuery] bool? active = null,
        [FromQuery] DateTime? updatedSince = null,
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 100)
    {
        page = Math.Max(page, 1);
        pageSize = Math.Clamp(pageSize, 1, 1000);
        var result = await _catalog.ListCoursesAsync(prefix, hasGuide, active, updatedSince, page, pageSize,
            HttpContext.RequestAborted);
        return Ok(ApiResponse<PagedResult<CatalogCourseDto>>.Ok(result));
    }

    [HttpGet("api/v1/courses/{courseId}/offerings")]
    public async Task<IActionResult> Get(string courseId)
    {
        var detail = await _catalog.GetCourseAsync(courseId, HttpContext.RequestAborted);
        return detail is null
            ? NotFound(ApiResponse<object?>.Fail(ErrorCodes.CourseNotFound, "Course not found."))
            : Ok(ApiResponse<CatalogCourseDetailDto>.Ok(detail));
    }

    [Authorize(Policy = "AdminOnly")]
    [HttpPut("api/v1/courses/{courseId}")]
    public async Task<IActionResult> Upsert(string courseId, [FromBody] UpsertCourseRequest request)
    {
        if (!CourseCatalogService.TryNormalizeCourseId(courseId, out var id))
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.InvalidCourseId,
                "courseId must be an SCNS course id such as EEE3300, EEE3300L or NUR4826-UWF."));
        if (request.CourseId is not null &&
            (!CourseCatalogService.TryNormalizeCourseId(request.CourseId, out var bodyId) || bodyId != id))
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError,
                "courseId in the body does not match the URL."));

        var batch = await _catalog.UpsertCoursesAsync([request with { CourseId = id }], HttpContext.RequestAborted);
        var result = batch.Results[0];

        return result.Outcome switch
        {
            CourseCatalogService.Outcomes.Failed when result.ErrorCode is ErrorCodes.TaxonomyPlacementRequired
                                                                   or ErrorCodes.TaxonomyNodeNotFound =>
                UnprocessableEntity(ApiResponse<object?>.Fail(result.ErrorCode, result.Message!, result.Fields)),
            CourseCatalogService.Outcomes.Failed =>
                BadRequest(ApiResponse<object?>.Fail(result.ErrorCode!, result.Message!, result.Fields)),
            CourseCatalogService.Outcomes.Created =>
                StatusCode(201, ApiResponse<CourseUpsertResult>.Ok(result)),
            _ => Ok(ApiResponse<CourseUpsertResult>.Ok(result))
        };
    }

    [Authorize(Policy = "AdminOnly")]
    [HttpPost("api/v1/courses/batch")]
    public async Task<IActionResult> Batch([FromBody] BatchUpsertCoursesRequest request)
    {
        var items = request.Courses;
        if (items is null || items.Count == 0)
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "courses must contain at least one course."));
        if (items.Count > CourseCatalogService.MaxCourseBatch)
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.BatchTooLarge,
                $"A batch may hold at most {CourseCatalogService.MaxCourseBatch} courses; this one has {items.Count}."));

        var result = await _catalog.UpsertCoursesAsync(items, HttpContext.RequestAborted);
        return Ok(ApiResponse<BatchUpsertCoursesResponse>.Ok(result));
    }

    [Authorize(Policy = "AdminOnly")]
    [HttpDelete("api/v1/courses/{courseId}")]
    public async Task<IActionResult> Delete(string courseId)
    {
        var outcome = await _catalog.DeleteCourseAsync(courseId, HttpContext.RequestAborted);
        return outcome switch
        {
            CourseCatalogService.DeleteOutcome.NotFound =>
                NotFound(ApiResponse<object?>.Fail(ErrorCodes.CourseNotFound, "Course not found.")),
            CourseCatalogService.DeleteOutcome.HasContent =>
                Conflict(ApiResponse<object?>.Fail(ErrorCodes.CourseHasContent,
                    "The course has a curriculum guide, modules or guide requests. Set isActive to false instead.")),
            _ => Ok(ApiResponse<MessageResponse>.Ok(new MessageResponse($"Course {courseId.Trim().ToUpperInvariant()} deleted.")))
        };
    }
}
