using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using PreseMakerRepo.Api.Models.Responses;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Api.Services;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Api.Pages.Queue;

/// <summary>The public career request queue — the order new career paths are written in.</summary>
public class CareersModel : PageModel
{
    private readonly CareerRequestService _service;
    private readonly AppDbContext _db;

    public CareersModel(CareerRequestService service, AppDbContext db)
    {
        _service = service;
        _db = db;
    }

    /// <summary>waiting · published · declined</summary>
    [BindProperty(SupportsGet = true)] public string? Status { get; set; }

    public PublicCareerQueueResponse Queue { get; set; } = null!;

    /// <summary>CIP code → title, so the "Requested from" column reads as words, not codes.</summary>
    public IReadOnlyDictionary<string, string> FieldTitles { get; set; } = new Dictionary<string, string>();

    public async Task OnGetAsync()
    {
        if (!CareerRequestService.TryParseQueueFilter(Status, out var filter) || filter == CareerRequestService.QueueAll)
            filter = CareerRequestService.QueueWaiting;
        Queue = await _service.PublicQueueAsync(filter);
        var codes = Queue.Items.SelectMany(i => i.CipCodes).Distinct().ToList();
        FieldTitles = await _db.CipNodes.AsNoTracking()
            .Where(n => codes.Contains(n.Code))
            .ToDictionaryAsync(n => n.Code, n => n.Title);
    }
}
