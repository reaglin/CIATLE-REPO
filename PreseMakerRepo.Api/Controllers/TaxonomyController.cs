using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;
using PreseMakerRepo.Api.Models;
using PreseMakerRepo.Api.Models.Responses;
using PreseMakerRepo.Core.Interfaces;
using PreseMakerRepo.Infrastructure.Options;

namespace PreseMakerRepo.Api.Controllers;

[ApiController]
[Route("api/v1/taxonomy")]
public class TaxonomyController : ControllerBase
{
    private readonly ITaxonomyService _taxonomy;
    private readonly IConfiguration _config;

    public TaxonomyController(ITaxonomyService taxonomy, IConfiguration config)
    {
        _taxonomy = taxonomy;
        _config = config;
    }

    // GET /api/v1/taxonomy
    [HttpGet]
    public async Task<IActionResult> GetTree()
    {
        var tree = await _taxonomy.GetFullTreeAsync();

        var response = new TaxonomyTreeResponse(
            _config["Repository:Name"] ?? _config["RepositoryName"] ?? "PreseMaker Repository",
            [new LevelLabel(1, "Discipline"), new LevelLabel(2, "Prefix")],
            tree.Roots.Select(ToDto).ToList());

        return Ok(ApiResponse<TaxonomyTreeResponse>.Ok(response));
    }

    // GET /api/v1/taxonomy/{level1Key}
    [HttpGet("{level1Key}")]
    public async Task<IActionResult> GetLevel1(string level1Key)
    {
        var node = await _taxonomy.GetNodeAsync(level1Key);
        if (node is null || node.Level != 1)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.TaxonomyNodeNotFound, "Taxonomy node not found."));

        // Pull aggregated summary for this node
        var tree = await _taxonomy.GetFullTreeAsync();
        var summary = FindSummary(tree.Roots, level1Key);

        var dto = new TaxonomyNodeDto(
            node.Key,
            node.Name,
            node.Level,
            summary?.CourseCount ?? 0,
            summary?.ModuleCount ?? 0,
            summary?.Children.Select(c => new TaxonomyNodeDto(c.Key, c.Name, c.Level, c.CourseCount, c.ModuleCount)).ToList());

        return Ok(ApiResponse<TaxonomyNodeDto>.Ok(dto));
    }

    // GET /api/v1/taxonomy/{level1Key}/{level2Key}
    [HttpGet("{level1Key}/{level2Key}")]
    public async Task<IActionResult> GetLevel2(string level1Key, string level2Key)
    {
        var node = await _taxonomy.GetNodeAsync(level2Key);
        if (node is null || node.Level != 2 || node.ParentKey != level1Key)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.TaxonomyNodeNotFound, "Taxonomy node not found."));

        var parent = node.Parent;
        var tree = await _taxonomy.GetFullTreeAsync();
        var l1Summary = FindSummary(tree.Roots, level1Key);
        var summary = FindSummary(l1Summary?.Children ?? [], level2Key);

        // In the SCNS 2-level taxonomy, level2 nodes are leaves with no children
        var children = summary?.Children
            .Select(c => new TaxonomyNodeDto(c.Key, c.Name, c.Level, c.CourseCount, c.ModuleCount))
            .ToList();

        var dto = new TaxonomyNodeDto(
            node.Key,
            node.Name,
            node.Level,
            summary?.CourseCount ?? 0,
            summary?.ModuleCount ?? 0,
            children,
            parent is null ? null : new NodeParentDto(parent.Key, parent.Name));

        return Ok(ApiResponse<TaxonomyNodeDto>.Ok(dto));
    }

    // GET /api/v1/taxonomy/{level1Key}/{level2Key}/courses  (2-level taxonomy leaf)
    [HttpGet("{level1Key}/{level2Key}/courses")]
    public async Task<IActionResult> GetLevel2Courses(
        string level1Key, string level2Key,
        [FromQuery] int page = 1, [FromQuery] int pageSize = 100)
    {
        var node = await _taxonomy.GetNodeAsync(level2Key);
        if (node is null || node.Level != 2 || node.ParentKey != level1Key)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.TaxonomyNodeNotFound, "Taxonomy node not found."));

        pageSize = Math.Clamp(pageSize, 1, 200);
        var courses = await _taxonomy.GetCoursesByLevel3Async(level2Key);
        var paged = courses
            .OrderBy(c => c.CourseId)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .Select(c => new CourseListItem(c.CourseId, c.Title, c.CreditHours, 0, 0, null, c.CurriculumGuideUrl))
            .ToList();

        var result = new PagedResult<CourseListItem>(
            paged, courses.Count, page, pageSize,
            (int)Math.Ceiling(courses.Count / (double)pageSize));

        return Ok(ApiResponse<PagedResult<CourseListItem>>.Ok(result));
    }

    // GET /api/v1/taxonomy/{level1Key}/{level2Key}/{level3Key}
    [HttpGet("{level1Key}/{level2Key}/{level3Key}")]
    public async Task<IActionResult> GetLevel3(
        string level1Key, string level2Key, string level3Key,
        [FromQuery] int page = 1, [FromQuery] int pageSize = 20)
    {
        var node = await _taxonomy.GetNodeAsync(level3Key);
        if (node is null || node.Level != 3 || node.ParentKey != level2Key)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.TaxonomyNodeNotFound, "Taxonomy node not found."));

        var tree = await _taxonomy.GetFullTreeAsync();
        var l1Summary = FindSummary(tree.Roots, level1Key);
        var l2Summary = FindSummary(l1Summary?.Children ?? [], level2Key);
        var summary = FindSummary(l2Summary?.Children ?? [], level3Key);

        pageSize = Math.Clamp(pageSize, 1, 100);
        var courses = await _taxonomy.GetCoursesByLevel3Async(level3Key);
        var paged = courses
            .OrderBy(c => c.CourseId)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .Select(c => new CourseListItem(c.CourseId, c.Title, c.CreditHours, 0, 0, null, c.CurriculumGuideUrl))
            .ToList();

        var coursesPaged = new PagedResult<CourseListItem>(
            paged,
            courses.Count,
            page,
            pageSize,
            (int)Math.Ceiling(courses.Count / (double)pageSize));

        var l2Node = node.Parent;
        var l1Node = l2Node?.Parent;
        var parent = new
        {
            level2 = l2Node is null ? null : new NodeParentDto(l2Node.Key, l2Node.Name),
            level1 = l1Node is null ? null : new NodeParentDto(l1Node.Key, l1Node.Name)
        };

        var result = new
        {
            key = node.Key,
            name = node.Name,
            level = node.Level,
            parent,
            courseCount = summary?.CourseCount ?? 0,
            moduleCount = summary?.ModuleCount ?? 0,
            courses = coursesPaged
        };

        return Ok(ApiResponse<object>.Ok(result));
    }

    // GET /api/v1/taxonomy/validate/{courseId}
    [HttpGet("validate/{courseId}")]
    public async Task<IActionResult> ValidateCourse(string courseId)
    {
        var result = await _taxonomy.ValidateCourseIdAsync(courseId);

        if (!result.IsValid)
        {
            return Ok(ApiResponse<ValidateCourseResponse>.Ok(new ValidateCourseResponse(
                false, result.CourseId, Reason: result.InvalidReason ?? "Course identifier not found in taxonomy.")));
        }

        var path = result.Path is null ? null : new TaxonomyPathDto(
            result.Path.Level1Key is null ? null : new NodeParentDto(result.Path.Level1Key, result.Path.Level1Name!),
            result.Path.Level2Key is null ? null : new NodeParentDto(result.Path.Level2Key, result.Path.Level2Name!),
            result.Path.Level3Key is null ? null : new NodeParentDto(result.Path.Level3Key, result.Path.Level3Name!));

        var course = await _taxonomy.GetCourseAsync(courseId);

        return Ok(ApiResponse<ValidateCourseResponse>.Ok(new ValidateCourseResponse(
            true,
            result.CourseId,
            result.Title,
            course?.CreditHours,
            path,
            result.CurriculumGuideUrl)));
    }

    private static TaxonomyNodeDto ToDto(TaxonomyNodeSummary s) =>
        new(s.Key, s.Name, s.Level, s.CourseCount, s.ModuleCount,
            s.Children.Count > 0 ? s.Children.Select(ToDto).ToList() : null);

    private static TaxonomyNodeSummary? FindSummary(
        IReadOnlyList<TaxonomyNodeSummary> list, string key) =>
        list.FirstOrDefault(s => s.Key == key);
}
