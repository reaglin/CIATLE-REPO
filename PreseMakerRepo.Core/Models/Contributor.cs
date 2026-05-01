using Microsoft.AspNetCore.Identity;

namespace PreseMakerRepo.Core.Models;

public class Contributor : IdentityUser
{
    public string? DisplayName { get; set; }
    public string? InstitutionName { get; set; }
    public bool IsEduVerified { get; set; }
    public bool IsSuspended { get; set; }
    public DateTime RegisteredUtc { get; set; }
    public DateTime? SuspendedUtc { get; set; }
    public string? SuspensionReason { get; set; }

    public ICollection<Module> Modules { get; set; } = new List<Module>();
    public ICollection<Material> Materials { get; set; } = new List<Material>();
    public ICollection<RefreshToken> RefreshTokens { get; set; } = new List<RefreshToken>();
}
