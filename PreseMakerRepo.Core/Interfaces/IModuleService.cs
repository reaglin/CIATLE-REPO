using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Core.Interfaces;

public interface IModuleService
{
    Task<IReadOnlyList<Module>> GetRecentAsync(int count, CancellationToken ct = default);
    Task<Module?> GetByIdAsync(Guid id, CancellationToken ct = default);
    Task<IReadOnlyList<Module>> GetByCourseAsync(string courseId, int page, int pageSize, CancellationToken ct = default);
    Task<IReadOnlyList<Module>> GetByContributorAsync(string contributorId, int page, int pageSize, CancellationToken ct = default);
    Task<Module> PublishAsync(Module module, IReadOnlyList<(Material material, Stream content)> materials, CancellationToken ct = default);
    Task<Module> UpdateAsync(Module module, CancellationToken ct = default);
    Task RetractAsync(Guid id, string requestingUserId, CancellationToken ct = default);
    Task FlagAsync(Guid id, string? reporterIpHash, string? reporterUserId, string? reason, CancellationToken ct = default);
}
