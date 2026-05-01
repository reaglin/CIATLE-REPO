using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Core.Interfaces;

public interface IMaterialService
{
    Task<Material?> GetByIdAsync(Guid id, CancellationToken ct = default);
    Task<IReadOnlyList<Material>> GetByModuleAsync(Guid moduleId, CancellationToken ct = default);
    Task<Material> PublishAsync(Material material, Stream content, CancellationToken ct = default);
    Task<Material> UpdateAsync(Material material, Stream? newContent, CancellationToken ct = default);
    Task RetractAsync(Guid id, string requestingUserId, CancellationToken ct = default);
    Task FlagAsync(Guid id, string? reporterIpHash, string? reporterUserId, string? reason, CancellationToken ct = default);
}
