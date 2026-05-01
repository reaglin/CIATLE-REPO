using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Core.Interfaces;

public interface IRefreshTokenService
{
    Task<RefreshToken> CreateAsync(string contributorId, string? createdByIp, CancellationToken ct = default);
    Task<RefreshToken?> ValidateAsync(string rawToken, CancellationToken ct = default);
    Task<RefreshToken?> FindAsync(string rawToken, CancellationToken ct = default);
    Task RevokeAsync(string rawToken, CancellationToken ct = default);
    Task RevokeAllForUserAsync(string contributorId, CancellationToken ct = default);
}
