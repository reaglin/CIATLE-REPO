using FluentValidation;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using PreseMakerRepo.Api.Models;
using PreseMakerRepo.Api.Models.Requests;
using PreseMakerRepo.Api.Models.Responses;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Api.Controllers;

[ApiController]
[Route("api/v1/guide-template")]
public class GuideTemplateController : ControllerBase
{
    private readonly AppDbContext _db;

    public GuideTemplateController(AppDbContext db) => _db = db;

    // GET /api/v1/guide-template — public
    [HttpGet]
    public async Task<IActionResult> Get()
    {
        var template = await _db.GuideTemplates.FindAsync(1);
        if (template is null)
            return NotFound(ApiResponse<object?>.Fail(
                ErrorCodes.GuideTemplateNotFound,
                "No guide template has been configured for this repository."));

        return Ok(ApiResponse<GuideTemplateResponse>.Ok(
            new GuideTemplateResponse(template.WorkingTitle, template.Prompt, template.UpdatedUtc)));
    }

    // PUT /api/v1/guide-template — admin only
    [Authorize(Policy = "AdminOnly")]
    [HttpPut]
    public async Task<IActionResult> Upsert(
        [FromBody] UpsertGuideTemplateRequest request,
        [FromServices] IValidator<UpsertGuideTemplateRequest> validator)
    {
        var vResult = await validator.ValidateAsync(request);
        if (!vResult.IsValid)
        {
            var details = vResult.Errors
                .Select(e => new FieldError(e.PropertyName, e.ErrorMessage))
                .ToList();
            return BadRequest(ApiResponse<object?>.Fail(
                ErrorCodes.ValidationError, "One or more validation errors occurred.", details));
        }

        var now = DateTime.UtcNow;
        var existing = await _db.GuideTemplates.FindAsync(1);
        if (existing is null)
        {
            _db.GuideTemplates.Add(new RepoGuideTemplate
            {
                Id = 1,
                WorkingTitle = request.WorkingTitle,
                Prompt = request.Prompt,
                UpdatedUtc = now
            });
        }
        else
        {
            existing.WorkingTitle = request.WorkingTitle;
            existing.Prompt = request.Prompt;
            existing.UpdatedUtc = now;
        }

        await _db.SaveChangesAsync();
        return Ok(ApiResponse<MessageResponse>.Ok(new MessageResponse("Guide template saved.")));
    }
}
