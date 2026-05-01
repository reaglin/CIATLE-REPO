namespace PreseMakerRepo.Core.Models;

public class RefreshToken
{
    public Guid Id { get; set; }
    public string ContributorId { get; set; } = string.Empty;
    public Contributor Contributor { get; set; } = null!;

    public string TokenHash { get; set; } = string.Empty;  // SHA-256 of raw token
    public DateTime IssuedUtc { get; set; }
    public DateTime ExpiresUtc { get; set; }
    public bool IsRevoked { get; set; }
    public string? ReplacedByTokenId { get; set; }         // Token rotation chain
    public string? CreatedByIp { get; set; }
}
