using Microsoft.AspNetCore.Identity;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using PreseMakerRepo.Core.Constants;
using PreseMakerRepo.Core.Enums;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Api.Startup;

public static class AdminBootstrap
{
    public static async Task SeedAsync(
        IServiceProvider services,
        IConfiguration configuration,
        ILogger logger)
    {
        var roleManager = services.GetRequiredService<RoleManager<IdentityRole>>();
        var userManager = services.GetRequiredService<UserManager<Contributor>>();
        var db = services.GetRequiredService<AppDbContext>();

        // Ensure roles
        foreach (var role in new[] { "Contributor", "Administrator" })
        {
            if (!await roleManager.RoleExistsAsync(role))
                await roleManager.CreateAsync(new IdentityRole(role));
        }

        // Check if any admin exists already
        var admins = await userManager.GetUsersInRoleAsync("Administrator");
        if (admins.Count > 0)
        {
            await EnsureOrphanModuleAsync(db, admins[0].Id, logger);
            return;
        }

        var email = configuration["AdminBootstrap:Email"];
        var username = configuration["AdminBootstrap:Username"];
        var password = configuration["AdminBootstrap:Password"];

        if (string.IsNullOrWhiteSpace(email) || string.IsNullOrWhiteSpace(username) || string.IsNullOrWhiteSpace(password))
        {
            logger.LogWarning("AdminBootstrap config is missing — skipping admin seed.");
            return;
        }

        var existing = await userManager.FindByEmailAsync(email);
        if (existing is not null)
        {
            await userManager.AddToRoleAsync(existing, "Administrator");
            logger.LogInformation("Promoted existing user {Email} to Administrator.", email);
            await EnsureOrphanModuleAsync(db, existing.Id, logger);
            return;
        }

        var admin = new Contributor
        {
            UserName = username,
            Email = email,
            EmailConfirmed = true,
            DisplayName = username,
            RegisteredUtc = DateTime.UtcNow,
            IsEduVerified = false
        };

        var result = await userManager.CreateAsync(admin, password);
        if (!result.Succeeded)
        {
            logger.LogError("Failed to create admin account: {Errors}",
                string.Join("; ", result.Errors.Select(e => e.Description)));
            return;
        }

        await userManager.AddToRoleAsync(admin, "Administrator");
        logger.LogInformation("Created admin account {Username}.", username);
        await EnsureOrphanModuleAsync(db, admin.Id, logger);
    }

    private static async Task EnsureOrphanModuleAsync(AppDbContext db, string adminId, ILogger logger)
    {
        if (await db.Modules.FindAsync(WellKnownIds.OrphanModuleId) is not null)
            return;

        db.Modules.Add(new Module
        {
            Id = WellKnownIds.OrphanModuleId,
            CourseId = WellKnownIds.OrphanCourseId,
            ContributorId = adminId,
            Title = "Unassigned",
            Description = "Container for materials not assigned to a specific course.",
            License = LicenseType.CcBy40,
            Status = ContentStatus.Published,
            SubmittedUtc = DateTime.UtcNow
        });

        await db.SaveChangesAsync();
        logger.LogInformation("Created orphan module {Id}.", WellKnownIds.OrphanModuleId);
    }
}
