using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Core.Constants;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Api.Areas.Admin.Pages;

public class IndexModel : PageModel
{
    private readonly AppDbContext _db;
    public IndexModel(AppDbContext db) => _db = db;

    public int TotalModules { get; set; }
    public int PublishedModules { get; set; }
    public int FlaggedModules { get; set; }
    public int RemovedModules { get; set; }
    public int TotalMaterials { get; set; }
    public int TotalContributors { get; set; }
    public int SuspendedContributors { get; set; }
    public int OpenFlags { get; set; }
    public int RecentModules30Days { get; set; }
    public IReadOnlyList<Module> RecentModulesList { get; set; } = [];

    public async Task OnGetAsync()
    {
        var moduleCounts = await _db.Modules.AsNoTracking()
            .Where(m => m.Id != WellKnownIds.OrphanModuleId)
            .GroupBy(m => m.Status)
            .Select(g => new { Status = g.Key, Count = g.Count() })
            .ToListAsync();

        TotalModules     = moduleCounts.Sum(x => x.Count);
        PublishedModules = moduleCounts.FirstOrDefault(x => x.Status == ContentStatus.Published)?.Count ?? 0;
        FlaggedModules   = moduleCounts.FirstOrDefault(x => x.Status == ContentStatus.Flagged)?.Count ?? 0;
        RemovedModules   = moduleCounts.FirstOrDefault(x => x.Status == ContentStatus.Removed)?.Count ?? 0;

        TotalMaterials = await _db.Materials.AsNoTracking()
            .CountAsync(m => m.Status != ContentStatus.Removed);

        TotalContributors = await _db.Users.CountAsync();
        SuspendedContributors = await _db.Users.CountAsync(u => u.IsSuspended);
        OpenFlags = await _db.ContentFlags.AsNoTracking().CountAsync(f => !f.IsResolved);

        var cutoff = DateTime.UtcNow.AddDays(-30);
        RecentModules30Days = await _db.Modules.AsNoTracking()
            .CountAsync(m => m.Status == ContentStatus.Published &&
                             m.Id != WellKnownIds.OrphanModuleId &&
                             m.SubmittedUtc >= cutoff);

        RecentModulesList = await _db.Modules.AsNoTracking()
            .Where(m => m.Status == ContentStatus.Published && m.Id != WellKnownIds.OrphanModuleId)
            .OrderByDescending(m => m.SubmittedUtc)
            .Take(20)
            .Include(m => m.Contributor)
            .ToListAsync();
    }
}
