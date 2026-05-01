using System.Security.Cryptography;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Core.Interfaces;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Infrastructure.Services;

public class RefreshTokenService : IRefreshTokenService
{
    private readonly AppDbContext _db;
    private const int TokenLifetimeDays = 30;

    public RefreshTokenService(AppDbContext db) => _db = db;

    public async Task<RefreshToken> CreateAsync(string contributorId, string? createdByIp, CancellationToken ct = default)
    {
        var raw = GenerateRaw();
        var token = new RefreshToken
        {
            Id = Guid.NewGuid(),
            ContributorId = contributorId,
            TokenHash = Hash(raw),
            IssuedUtc = DateTime.UtcNow,
            ExpiresUtc = DateTime.UtcNow.AddDays(TokenLifetimeDays),
            IsRevoked = false,
            CreatedByIp = createdByIp
        };

        _db.RefreshTokens.Add(token);
        await _db.SaveChangesAsync(ct);

        // Return a copy with the raw value surfaced via ReplacedByTokenId (temp carrier)
        // Caller reads token.ReplacedByTokenId as the raw value, then clears it.
        // Better: return a tuple/DTO. Using record here to keep it clean.
        token.ReplacedByTokenId = raw;
        return token;
    }

    public async Task<RefreshToken?> ValidateAsync(string rawToken, CancellationToken ct = default)
    {
        var hash = Hash(rawToken);
        return await _db.RefreshTokens
            .FirstOrDefaultAsync(t => t.TokenHash == hash
                                   && !t.IsRevoked
                                   && t.ExpiresUtc > DateTime.UtcNow, ct);
    }

    public async Task<RefreshToken?> FindAsync(string rawToken, CancellationToken ct = default)
    {
        var hash = Hash(rawToken);
        return await _db.RefreshTokens.FirstOrDefaultAsync(t => t.TokenHash == hash, ct);
    }

    public async Task RevokeAsync(string rawToken, CancellationToken ct = default)
    {
        var hash = Hash(rawToken);
        var token = await _db.RefreshTokens.FirstOrDefaultAsync(t => t.TokenHash == hash, ct);
        if (token is null) return;
        token.IsRevoked = true;
        await _db.SaveChangesAsync(ct);
    }

    public async Task RevokeAllForUserAsync(string contributorId, CancellationToken ct = default)
    {
        await _db.RefreshTokens
            .Where(t => t.ContributorId == contributorId && !t.IsRevoked)
            .ExecuteUpdateAsync(s => s.SetProperty(t => t.IsRevoked, true), ct);
    }

    private static string GenerateRaw() =>
        Convert.ToBase64String(RandomNumberGenerator.GetBytes(64));

    internal static string Hash(string raw)
    {
        var bytes = SHA256.HashData(System.Text.Encoding.UTF8.GetBytes(raw));
        return Convert.ToHexString(bytes).ToLowerInvariant();
    }
}
