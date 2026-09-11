using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using PreseMakerRepo.Api.Models.Responses;
using PreseMakerRepo.Api.Services;

namespace PreseMakerRepo.Api.Pages.Queue;

/// <summary>The public guide request queue — the order curriculum guides are written in.</summary>
public class GuidesModel : PageModel
{
    private readonly GuideRequestService _service;

    public GuidesModel(GuideRequestService service) => _service = service;

    /// <summary>waiting · published · declined</summary>
    [BindProperty(SupportsGet = true)] public string? Status { get; set; }

    public PublicGuideQueueResponse Queue { get; set; } = null!;

    public async Task OnGetAsync()
    {
        if (!GuideRequestService.TryParseQueueFilter(Status, out var filter) || filter == GuideRequestService.QueueAll)
            filter = GuideRequestService.QueueWaiting;
        Queue = await _service.PublicQueueAsync(filter);
    }
}
