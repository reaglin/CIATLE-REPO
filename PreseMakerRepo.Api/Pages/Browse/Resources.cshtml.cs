using FluentValidation;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Api.Helpers;
using PreseMakerRepo.Api.Models.Requests;
using PreseMakerRepo.Api.Models.Responses;
using PreseMakerRepo.Api.Services;
using PreseMakerRepo.Core.Constants;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Api.Pages.Browse;

/// <summary>A course's reviewed resources, with the Add Resource form at the bottom.</summary>
public class ResourcesModel : PageModel
{
    private readonly AppDbContext _db;
    private readonly ResourceService _resources;
    private readonly IValidator<SubmitResourceRequest> _validator;

    public ResourcesModel(AppDbContext db, ResourceService resources, IValidator<SubmitResourceRequest> validator)
    {
        _db = db;
        _resources = resources;
        _validator = validator;
    }

    [BindProperty] public string? ResourceUrl { get; set; }
    [BindProperty] public string? Description { get; set; }
    /// <summary>Honeypot: hidden from people, filled in by form-spamming bots.</summary>
    [BindProperty] public string? Homepage { get; set; }

    public TaxonomyCourse? Course { get; set; }
    public string DisplayTitle { get; set; } = string.Empty;
    public bool HasGuide { get; set; }
    public IReadOnlyList<CourseResourceDto> Resources { get; set; } = [];
    public int PendingCount { get; set; }
    public string? SuccessMessage { get; set; }
    public List<string> Errors { get; } = new();

    public async Task<IActionResult> OnGetAsync(string courseId) =>
        await LoadAsync(courseId) ? Page() : NotFound();

    public async Task<IActionResult> OnPostAsync(string courseId)
    {
        if (!await LoadAsync(courseId)) return NotFound();

        if (!string.IsNullOrEmpty(Homepage))
        {
            // Look successful to the bot; store nothing.
            SuccessMessage = "Thank you — your suggestion is in the review queue.";
            ResourceUrl = Description = null;
            return Page();
        }

        var request = new SubmitResourceRequest(ResourceUrl, Description);
        var validation = await _validator.ValidateAsync(request);
        if (!validation.IsValid)
        {
            Errors.AddRange(validation.Errors.Select(e => e.ErrorMessage).Distinct());
            return Page();
        }

        var ip = HttpContext.Connection.RemoteIpAddress?.ToString() ?? "unknown";
        var userId = User.Identity?.IsAuthenticated == true ? User.FindFirst("sub")?.Value : null;
        var result = await _resources.SubmitAsync(Course!.CourseId, request, ip, userId);

        if (result.Outcome is ResourceService.SubmitOutcome.Submitted or ResourceService.SubmitOutcome.AlreadySubmitted)
        {
            SuccessMessage = result.Message;
            ResourceUrl = Description = null;
            ModelState.Clear();
            PendingCount = await _resources.PendingCountAsync(Course.CourseId);
        }
        else
        {
            Errors.Add(result.Message);
        }
        return Page();
    }

    private async Task<bool> LoadAsync(string courseId)
    {
        var id = courseId.Trim().ToUpperInvariant();
        Course = await _db.TaxonomyCourses.AsNoTracking()
            .Include(c => c.Level3Node).ThenInclude(n => n!.Parent)
            .FirstOrDefaultAsync(c => c.CourseId == id && c.CourseId != WellKnownIds.OrphanCourseId && c.Level3Key != null);
        if (Course is null) return false;

        var guideTitle = await _db.CurriculumGuides.AsNoTracking()
            .Where(g => g.CourseId == id && g.Title != CurriculumGuide.StubTitle)
            .Select(g => g.Title)
            .FirstOrDefaultAsync();
        HasGuide = guideTitle is not null;
        DisplayTitle = CourseTitles.Display(id, Course.Title, Course.StateTitle, guideTitle);
        Resources = await _resources.ForCourseAsync(id);
        PendingCount = await _resources.PendingCountAsync(id);
        return true;
    }
}
