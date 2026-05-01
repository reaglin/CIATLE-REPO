using System.Security.Claims;

namespace PreseMakerRepo.Api.Helpers;

public static class ClaimsHelper
{
    public static string? GetUserId(ClaimsPrincipal user) =>
        user.FindFirstValue(ClaimTypes.NameIdentifier) ?? user.FindFirstValue("sub");
}
