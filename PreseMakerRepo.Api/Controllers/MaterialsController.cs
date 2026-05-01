using FluentValidation;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;
using PreseMakerRepo.Api.Helpers;
using PreseMakerRepo.Api.Models;
using PreseMakerRepo.Api.Models.Requests;
using PreseMakerRepo.Api.Models.Responses;
using PreseMakerRepo.Core.Constants;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Core.Interfaces;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;
using PreseMakerRepo.Infrastructure.Options;
using System.Text.Json;

namespace PreseMakerRepo.Api.Controllers;

[ApiController]
[Route("api/v1/courses/{courseId}/modules/{moduleId:guid}/materials")]
public class MaterialsController : ControllerBase
{
    private readonly AppDbContext _db;
    private readonly IStorageService _storage;
    private readonly StorageOptions _storageOpts;
    private readonly RepositoryOptions _repo;
    private readonly UserManager<Contributor> _userManager;

    public MaterialsController(
        AppDbContext db,
        IStorageService storage,
        IOptions<StorageOptions> storageOpts,
        IOptions<RepositoryOptions> repo,
        UserManager<Contributor> userManager)
    {
        _db = db;
        _storage = storage;
        _storageOpts = storageOpts.Value;
        _repo = repo.Value;
        _userManager = userManager;
    }

    // GET /api/v1/courses/{courseId}/modules/{moduleId}/materials
    [HttpGet]
    public async Task<IActionResult> ListMaterials(
        string courseId, Guid moduleId,
        [FromQuery] string sort = "newest",
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 20)
    {
        var module = await _db.Modules.AsNoTracking()
            .FirstOrDefaultAsync(m => m.Id == moduleId &&
                                      m.CourseId == courseId.ToUpperInvariant() &&
                                      m.Status == ContentStatus.Published);
        if (module is null)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.ModuleNotFound, "Module not found."));

        pageSize = Math.Clamp(pageSize, 1, _repo.MaxPageSize);
        page = Math.Max(page, 1);

        IQueryable<Material> query = _db.Materials.AsNoTracking()
            .Where(m => m.ModuleId == moduleId && m.Status == ContentStatus.Published)
            .Include(m => m.Contributor);

        var total = await query.CountAsync();
        query = sort == "oldest"
            ? query.OrderBy(m => m.SubmittedUtc)
            : query.OrderByDescending(m => m.SubmittedUtc);

        var materials = await query.Skip((page - 1) * pageSize).Take(pageSize).ToListAsync();
        var items = materials.Select(m => ToSummaryDto(m, courseId, moduleId, Request)).ToList();

        return Ok(ApiResponse<PagedResult<MaterialSummaryDto>>.Ok(
            new PagedResult<MaterialSummaryDto>(items, total, page, pageSize,
                (int)Math.Ceiling(total / (double)pageSize))));
    }

    // GET /api/v1/courses/{courseId}/modules/{moduleId}/materials/{materialId}
    [HttpGet("{materialId:guid}")]
    public async Task<IActionResult> GetMaterial(string courseId, Guid moduleId, Guid materialId)
    {
        var material = await _db.Materials.AsNoTracking()
            .Include(m => m.Contributor)
            .FirstOrDefaultAsync(m => m.Id == materialId &&
                                      m.ModuleId == moduleId &&
                                      m.Status == ContentStatus.Published);
        if (material is null)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.MaterialNotFound, "Material not found."));

        var dto = new MaterialDetailDto(
            material.Id, material.ModuleId, courseId.ToUpperInvariant(),
            material.Title, material.Type.ToString(), material.Description,
            material.FileName, material.FileSizeBytes, material.ContentType,
            new ContributorBriefDto(material.Contributor.UserName!, material.Contributor.DisplayName,
                material.Contributor.InstitutionName, material.Contributor.IsEduVerified),
            material.License.ToString(),
            LicenseHelper.DisplayName(material.License),
            LicenseHelper.Url(material.License),
            material.SubmittedUtc, material.UpdatedUtc,
            material.Status.ToString(),
            BuildDownloadUrl(Request, courseId, moduleId, materialId));

        return Ok(ApiResponse<MaterialDetailDto>.Ok(dto));
    }

    // POST /api/v1/courses/{courseId}/modules/{moduleId}/materials
    [Authorize(Policy = "ContributorOnly")]
    [HttpPost]
    [RequestSizeLimit(209_715_200)]
    public async Task<IActionResult> PublishMaterial(
        string courseId, Guid moduleId,
        [FromServices] IValidator<PublishMaterialRequest> validator)
    {
        var userId = ClaimsHelper.GetUserId(User);
        var contributor = await _userManager.FindByIdAsync(userId!);
        if (contributor is null) return Unauthorized();
        if (contributor.IsSuspended)
            return StatusCode(403, ApiResponse<object?>.Fail(ErrorCodes.AccountSuspended, "Account is suspended."));
        if (!contributor.EmailConfirmed)
            return StatusCode(403, ApiResponse<object?>.Fail(ErrorCodes.EmailNotConfirmed, "Email not confirmed."));

        var module = await _db.Modules
            .FirstOrDefaultAsync(m => m.Id == moduleId &&
                                      m.CourseId == courseId.ToUpperInvariant() &&
                                      m.Status == ContentStatus.Published);
        if (module is null || module.Id == WellKnownIds.OrphanModuleId)
            return UnprocessableEntity(ApiResponse<object?>.Fail(ErrorCodes.InvalidModuleId, "Module not found or not eligible."));

        if (!Request.HasFormContentType)
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "Request must be multipart/form-data."));

        var form = await Request.ReadFormAsync();
        var metadataPart = form["metadata"].FirstOrDefault();
        if (metadataPart is null)
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "Missing 'metadata' form field."));

        PublishMaterialRequest? req;
        try { req = JsonSerializer.Deserialize<PublishMaterialRequest>(metadataPart, JsonOpts); }
        catch { return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "Invalid metadata JSON.")); }

        if (req is null) return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "Empty metadata."));

        var vResult = await validator.ValidateAsync(req);
        if (!vResult.IsValid) return BadRequest(ValidationError(vResult));

        if (!MaterialTypeHelper.TryParse(req.Type, out var matType))
            return UnprocessableEntity(ApiResponse<object?>.Fail(ErrorCodes.InvalidMaterialType, "Material type is not recognized."));

        var file = form.Files.GetFile("file");
        if (file is null)
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "Missing 'file' form field."));

        if (file.Length > _storageOpts.MaxMaterialSizeBytes)
            return StatusCode(413, ApiResponse<object?>.Fail(ErrorCodes.MaterialTooLarge, "File exceeds size limit."));

        if (!MaterialTypeHelper.IsMimeAccepted(matType, file.ContentType, _storageOpts.OtherMimeTypes))
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError,
                $"Content type '{file.ContentType}' is not accepted for material type '{req.Type}'."));

        Enum.TryParse<LicenseType>(req.License, ignoreCase: true, out var license);
        var materialId = Guid.NewGuid();
        await using var stream = file.OpenReadStream();
        var storagePath = await _storage.SaveMaterialAsync(moduleId, materialId, file.FileName, stream);

        _db.Materials.Add(new Material
        {
            Id = materialId,
            ModuleId = moduleId,
            ContributorId = userId!,
            Title = req.Title,
            Description = req.Description,
            Type = matType,
            License = license,
            Status = ContentStatus.Published,
            FileName = file.FileName,
            StoragePath = storagePath,
            FileSizeBytes = file.Length,
            ContentType = file.ContentType,
            SubmittedUtc = DateTime.UtcNow
        });

        await _db.SaveChangesAsync();

        return StatusCode(201, ApiResponse<object>.Ok(new
        {
            materialId,
            moduleId,
            courseId = courseId.ToUpperInvariant(),
            materialUrl = $"{Request.Scheme}://{Request.Host}/api/v1/courses/{courseId}/modules/{moduleId}/materials/{materialId}"
        }));
    }

    // PUT /api/v1/courses/{courseId}/modules/{moduleId}/materials/{materialId}
    [Authorize]
    [HttpPut("{materialId:guid}")]
    [RequestSizeLimit(209_715_200)]
    public async Task<IActionResult> UpdateMaterial(
        string courseId, Guid moduleId, Guid materialId,
        [FromServices] IValidator<UpdateMaterialRequest> validator)
    {
        var material = await _db.Materials
            .FirstOrDefaultAsync(m => m.Id == materialId &&
                                      m.ModuleId == moduleId &&
                                      m.Status != ContentStatus.Removed);
        if (material is null)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.MaterialNotFound, "Material not found."));

        var userId = ClaimsHelper.GetUserId(User);
        if (material.ContributorId != userId && !User.IsInRole("Administrator"))
            return StatusCode(403, ApiResponse<object?>.Fail(ErrorCodes.Forbidden, "You do not own this material."));

        if (!Request.HasFormContentType)
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "Request must be multipart/form-data."));

        var form = await Request.ReadFormAsync();
        var metadataPart = form["metadata"].FirstOrDefault();
        if (metadataPart is null)
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "Missing 'metadata' form field."));

        UpdateMaterialRequest? req;
        try { req = JsonSerializer.Deserialize<UpdateMaterialRequest>(metadataPart, JsonOpts); }
        catch { return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "Invalid metadata JSON.")); }

        if (req is null) return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "Empty metadata."));

        var vResult = await validator.ValidateAsync(req);
        if (!vResult.IsValid) return BadRequest(ValidationError(vResult));

        if (req.Title is not null) material.Title = req.Title;
        if (req.Description is not null) material.Description = req.Description;
        if (req.Type is not null && MaterialTypeHelper.TryParse(req.Type, out var newType))
            material.Type = newType;
        if (req.License is not null && Enum.TryParse<LicenseType>(req.License, ignoreCase: true, out var newLic))
            material.License = newLic;

        var file = form.Files.GetFile("file");
        if (file is not null)
        {
            if (file.Length > _storageOpts.MaxMaterialSizeBytes)
                return StatusCode(413, ApiResponse<object?>.Fail(ErrorCodes.MaterialTooLarge, "File exceeds size limit."));

            if (!MaterialTypeHelper.IsMimeAccepted(material.Type, file.ContentType, _storageOpts.OtherMimeTypes))
                return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.ValidationError,
                    $"Content type '{file.ContentType}' is not accepted for this material type."));

            await _storage.DeleteMaterialAsync(material.StoragePath);
            await using var stream = file.OpenReadStream();
            material.StoragePath = await _storage.SaveMaterialAsync(moduleId, materialId, file.FileName, stream);
            material.FileSizeBytes = file.Length;
            material.ContentType = file.ContentType;
            material.FileName = file.FileName;
        }

        material.UpdatedUtc = DateTime.UtcNow;
        await _db.SaveChangesAsync();

        return Ok(ApiResponse<object>.Ok(new { materialId, message = "Material updated." }));
    }

    // DELETE /api/v1/courses/{courseId}/modules/{moduleId}/materials/{materialId}
    [Authorize]
    [HttpDelete("{materialId:guid}")]
    public async Task<IActionResult> DeleteMaterial(string courseId, Guid moduleId, Guid materialId)
    {
        var material = await _db.Materials
            .FirstOrDefaultAsync(m => m.Id == materialId &&
                                      m.ModuleId == moduleId &&
                                      m.Status != ContentStatus.Removed);
        if (material is null)
            return NotFound(ApiResponse<object?>.Fail(ErrorCodes.MaterialNotFound, "Material not found."));

        var userId = ClaimsHelper.GetUserId(User);
        if (material.ContributorId != userId && !User.IsInRole("Administrator"))
            return StatusCode(403, ApiResponse<object?>.Fail(ErrorCodes.Forbidden, "You do not own this material."));

        material.Status = ContentStatus.Removed;
        material.RemovedUtc = DateTime.UtcNow;
        await _db.SaveChangesAsync();

        return Ok(ApiResponse<MessageResponse>.Ok(new MessageResponse("Material retracted.")));
    }

    // ── Helpers ───────────────────────────────────────────────────────────────

    private static readonly JsonSerializerOptions JsonOpts = new() { PropertyNameCaseInsensitive = true };

    private static MaterialSummaryDto ToSummaryDto(Material m, string courseId, Guid moduleId, HttpRequest req) =>
        new(m.Id, m.Title, m.Type.ToString(), m.Description,
            m.FileName, m.FileSizeBytes, m.ContentType,
            new ContributorBriefDto(m.Contributor.UserName!, m.Contributor.DisplayName,
                m.Contributor.InstitutionName, m.Contributor.IsEduVerified),
            m.License.ToString(), LicenseHelper.DisplayName(m.License),
            m.SubmittedUtc,
            BuildDownloadUrl(req, courseId, moduleId, m.Id));

    private static string BuildDownloadUrl(HttpRequest req, string courseId, Guid moduleId, Guid materialId) =>
        $"{req.Scheme}://{req.Host}/api/v1/courses/{courseId}/modules/{moduleId}/materials/{materialId}/download";

    private static ApiResponse<object?> ValidationError(FluentValidation.Results.ValidationResult result)
    {
        var details = result.Errors.Select(e => new FieldError(e.PropertyName, e.ErrorMessage)).ToList();
        return ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "One or more validation errors occurred.", details);
    }
}
