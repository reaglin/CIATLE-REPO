using Microsoft.AspNetCore.Authorization;

namespace PreseMakerRepo.Api.Authorization;

public class OwnerOrAdminRequirement : IAuthorizationRequirement { }

public class OwnerOrAdminHandler : AuthorizationHandler<OwnerOrAdminRequirement, string>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        OwnerOrAdminRequirement requirement,
        string resourceOwnerId)
    {
        var userId = context.User.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)?.Value
                  ?? context.User.FindFirst("sub")?.Value;

        if (userId == resourceOwnerId || context.User.IsInRole("Administrator"))
            context.Succeed(requirement);

        return Task.CompletedTask;
    }
}
