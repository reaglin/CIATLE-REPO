using FluentValidation;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Options;
using PreseMakerRepo.Api.Models;
using PreseMakerRepo.Api.Models.Requests;
using PreseMakerRepo.Api.Models.Responses;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;
using PreseMakerRepo.Infrastructure.Options;
using System.Security.Cryptography;
using System.Text;

namespace PreseMakerRepo.Api.Controllers;

[ApiController]
public class ReportsController : ControllerBase
{
    private readonly AppDbContext _db;
    private readonly IMemoryCache _cache;
    private readonly RepositoryOptions _repo;

    public ReportsController(AppDbContext db, IMemoryCache cache, IOptions<RepositoryOptions> repo)
    {
        _db = db;
        _cache = cache;
        _repo = repo.Value;
    }

    // POST /api/v1/courses/{courseId}/modules/{moduleId}/report
    [HttpPost("api/v1/courses/{courseId}/modules/{moduleId:guid}/report")]
    public async Task<IActionResult> ReportModule(
        string courseId, Guid moduleId,
        [FromBody] ReportRequest request,
        [FromServices] IValidator<ReportRequest> validator)
    {
        var vResult = await validator.ValidateAsync(request);
        if (!vResult.IsValid)
        {
            var details = vResult.Errors.Select(e => new FieldError(e.PropertyName, e.ErrorMessage)).ToList();
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "Validation failed.", details));
        }

        var module = await _db.Modules.AsNoTracking()
            .FirstOrDefaultAsync(m => m.Id == moduleId &&
                                      m.CourseId == courseId.ToUpperInvariant() &&
                                      m.Status == ContentStatus.Published);
        if (module is null)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.ModuleNotFound, "Module not found."));

        var ip = HttpContext.Connection.RemoteIpAddress?.ToString() ?? "unknown";
        if (!CheckRateLimit(ip))
            return StatusCode(429, ApiResponse<object?>.Fail(ErrorCodes.RateLimitExceeded, "Too many reports. Please try again later."));

        _db.ContentFlags.Add(new ContentFlag
        {
            Id = Guid.NewGuid(),
            ModuleId = moduleId,
            ReporterIpHash = HashIp(ip),
            ReporterUserId = User.Identity?.IsAuthenticated == true
                ? User.FindFirst("sub")?.Value : null,
            FlaggedUtc = DateTime.UtcNow,
            Reason = request.Reason
        });
        await _db.SaveChangesAsync();

        return Ok(ApiResponse<MessageResponse>.Ok(
            new MessageResponse("Thank you. This module has been flagged for review.")));
    }

    // POST /api/v1/courses/{courseId}/modules/{moduleId}/materials/{materialId}/report
    [HttpPost("api/v1/courses/{courseId}/modules/{moduleId:guid}/materials/{materialId:guid}/report")]
    public async Task<IActionResult> ReportMaterial(
        string courseId, Guid moduleId, Guid materialId,
        [FromBody] ReportRequest request,
        [FromServices] IValidator<ReportRequest> validator)
    {
        var vResult = await validator.ValidateAsync(request);
        if (!vResult.IsValid)
        {
            var details = vResult.Errors.Select(e => new FieldError(e.PropertyName, e.ErrorMessage)).ToList();
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "Validation failed.", details));
        }

        var material = await _db.Materials.AsNoTracking()
            .FirstOrDefaultAsync(m => m.Id == materialId &&
                                      m.ModuleId == moduleId &&
                                      m.Status == ContentStatus.Published);
        if (material is null)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.MaterialNotFound, "Material not found."));

        var ip = HttpContext.Connection.RemoteIpAddress?.ToString() ?? "unknown";
        if (!CheckRateLimit(ip))
            return StatusCode(429, ApiResponse<object?>.Fail(ErrorCodes.RateLimitExceeded, "Too many reports. Please try again later."));

        _db.ContentFlags.Add(new ContentFlag
        {
            Id = Guid.NewGuid(),
            MaterialId = materialId,
            ReporterIpHash = HashIp(ip),
            ReporterUserId = User.Identity?.IsAuthenticated == true
                ? User.FindFirst("sub")?.Value : null,
            FlaggedUtc = DateTime.UtcNow,
            Reason = request.Reason
        });
        await _db.SaveChangesAsync();

        return Ok(ApiResponse<MessageResponse>.Ok(
            new MessageResponse("Thank you. This material has been flagged for review.")));
    }

    // ── Helpers ───────────────────────────────────────────────────────────────

    private bool CheckRateLimit(string ip)
    {
        var key = $"report_rate:{HashIp(ip)}";
        var count = _cache.GetOrCreate(key, entry =>
        {
            entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromHours(1);
            return 0;
        });
        if (count >= _repo.ReportRateLimitPerHour) return false;
        _cache.Set(key, count + 1, TimeSpan.FromHours(1));
        return true;
    }

    private static string HashIp(string ip)
    {
        // Salt with a fixed app-level salt; not stored raw per security requirements
        var bytes = SHA256.HashData(Encoding.UTF8.GetBytes("presemaker-ip-salt:" + ip));
        return Convert.ToHexString(bytes).ToLowerInvariant();
    }
}
