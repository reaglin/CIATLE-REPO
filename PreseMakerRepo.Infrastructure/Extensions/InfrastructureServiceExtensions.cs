using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using PreseMakerRepo.Core.Interfaces;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;
using PreseMakerRepo.Infrastructure.Options;
using PreseMakerRepo.Infrastructure.Seed;
using PreseMakerRepo.Infrastructure.Services;

namespace PreseMakerRepo.Infrastructure.Extensions;

public static class InfrastructureServiceExtensions
{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        // Database — SQLite by default; swap to PostgreSQL via config
        services.AddDbContext<AppDbContext>(options =>
        {
            var provider = configuration["DatabaseProvider"] ?? "SQLite";
            var connectionString = configuration.GetConnectionString("DefaultConnection");

            if (provider == "PostgreSQL")
                options.UseNpgsql(connectionString);
            else
                options.UseSqlite(connectionString);
        });

        // Identity — AddIdentityCore avoids registering default cookie schemes;
        // the API layer configures its own multi-scheme auth (JWT + cookies).
        services.AddIdentityCore<Contributor>(options =>
        {
            options.SignIn.RequireConfirmedEmail = true;
            options.Lockout.MaxFailedAccessAttempts = 10;
            options.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(15);
            options.Password.RequireDigit = true;
            options.Password.RequiredLength = 8;
        })
        .AddRoles<IdentityRole>()
        .AddEntityFrameworkStores<AppDbContext>()
        .AddDefaultTokenProviders();

        // Typed options
        services.Configure<StorageOptions>(configuration.GetSection("Storage"));
        services.Configure<EmailOptions>(configuration.GetSection("Email"));
        services.Configure<RepositoryOptions>(configuration.GetSection("Repository"));

        // Services
        services.AddScoped<IStorageService, LocalStorageService>();
        services.AddScoped<IEmailService, SmtpEmailService>();
        services.AddScoped<IEduLookupService, EduLookupService>();
        services.AddScoped<ITaxonomyService, TaxonomyService>();
        services.AddScoped<IRefreshTokenService, RefreshTokenService>();

        // Seeders (called from startup pipeline)
        services.AddScoped<TaxonomySeed>();
        services.AddScoped<EduSeed>();
        services.AddScoped<GuideTemplateSeed>();

        return services;
    }
}
