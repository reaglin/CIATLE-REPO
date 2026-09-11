using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using PreseMakerRepo.Api.Models.Responses;
using PreseMakerRepo.Api.Services;

namespace PreseMakerRepo.Api.Pages.Queue;

/// <summary>The public resource review queue.</summary>
public class ResourcesModel : PageModel
{
    private readonly ResourceService _resources;

    public ResourcesModel(ResourceService resources) => _resources = resources;

    /// <summary>pending · decided</summary>
    [BindProperty(SupportsGet = true)] public string? Status { get; set; }

    public ResourceQueueResponse Queue { get; set; } = null!;

    public async Task OnGetAsync()
    {
        if (!ResourceService.TryParseQueueFilter(Status, out var filter) || filter == ResourceService.QueueAll)
            filter = ResourceService.QueuePending;
        Queue = await _resources.QueueAsync(filter);
    }
}
