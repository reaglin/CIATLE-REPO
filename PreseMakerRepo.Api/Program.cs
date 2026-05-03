using System.Text;
using FluentValidation;
using Microsoft.AspNetCore.HttpOverrides;
using Microsoft.EntityFrameworkCore;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Authorization;
using Microsoft.IdentityModel.Tokens;
using PreseMakerRepo.Api.Authorization;
using PreseMakerRepo.Api.Middleware;
using PreseMakerRepo.Api.Options;
using PreseMakerRepo.Api.Services;
using PreseMakerRepo.Api.Startup;
using PreseMakerRepo.Api.Validators;
using PreseMakerRepo.Infrastructure.Data;
using PreseMakerRepo.Infrastructure.Extensions;
using PreseMakerRepo.Infrastructure.Seed;
using Serilog;
using Serilog.Events;

Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Override("Microsoft", LogEventLevel.Warning)
    .WriteTo.Console()
    .CreateBootstrapLogger();

try
{
    var builder = WebApplication.CreateBuilder(args);

    builder.Host.UseSerilog((ctx, services, config) => config
        .ReadFrom.Configuration(ctx.Configuration)
        .ReadFrom.Services(services)
        .Enrich.FromLogContext()
        .WriteTo.Console()
        .WriteTo.File(
            ctx.Configuration["Logging:FilePath"] ?? "logs/app-.log",
            rollingInterval: RollingInterval.Day,
            retainedFileCountLimit: 30));

    // Infrastructure: DB, Identity core, all services
    builder.Services.AddInfrastructure(builder.Configuration);

    // ForwardedHeaders — trust X-Forwarded-For/Proto from local Nginx proxy
    builder.Services.Configure<ForwardedHeadersOptions>(options =>
    {
        options.ForwardedHeaders = ForwardedHeaders.XForwardedFor | ForwardedHeaders.XForwardedProto;
        options.KnownNetworks.Clear();
        options.KnownProxies.Clear();
        options.KnownProxies.Add(System.Net.IPAddress.Loopback);
        options.KnownProxies.Add(System.Net.IPAddress.IPv6Loopback);
    });

    // JWT options + service
    builder.Services.Configure<JwtOptions>(builder.Configuration.GetSection("Jwt"));
    builder.Services.Configure<SecurityOptions>(builder.Configuration.GetSection("Security"));
    builder.Services.AddSingleton<JwtService>();

    // Multi-scheme auth: /api/* → JWT Bearer, everything else → Cookie
    builder.Services.AddAuthentication(options =>
    {
        options.DefaultScheme = "MultiScheme";
    })
    .AddPolicyScheme("MultiScheme", null, options =>
    {
        options.ForwardDefaultSelector = ctx =>
            ctx.Request.Path.StartsWithSegments("/api")
                ? JwtBearerDefaults.AuthenticationScheme
                : CookieAuthenticationDefaults.AuthenticationScheme;
    })
    .AddJwtBearer(options =>
    {
        var section = builder.Configuration.GetSection("Jwt");
        var secretKey = section["SecretKey"]
            ?? throw new InvalidOperationException("Jwt:SecretKey must be set via environment variable.");
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = section["Issuer"],
            ValidAudience = section["Audience"],
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(secretKey)),
            ClockSkew = TimeSpan.Zero
        };
    })
    .AddCookie(options =>
    {
        options.LoginPath = "/account/login";
        options.LogoutPath = "/account/logout";
        options.AccessDeniedPath = "/account/access-denied";
        options.ExpireTimeSpan = TimeSpan.FromDays(30);
        options.SlidingExpiration = true;
    });

    // Authorization policies
    builder.Services.AddAuthorization(options =>
    {
        options.AddPolicy("ContributorOnly", policy =>
            policy.RequireRole("Contributor", "Administrator"));
        options.AddPolicy("AdminOnly", policy =>
            policy.RequireRole("Administrator"));
        options.AddPolicy("OwnerOrAdmin", policy =>
            policy.AddRequirements(new OwnerOrAdminRequirement()));
    });
    builder.Services.AddSingleton<IAuthorizationHandler, OwnerOrAdminHandler>();

    // CORS — restrict to configured origins; desktop client bypasses CORS entirely
    builder.Services.AddCors(options =>
    {
        options.AddPolicy("ApiPolicy", policy =>
        {
            var origins = builder.Configuration.GetSection("Cors:AllowedOrigins").Get<string[]>() ?? [];
            if (origins.Length > 0)
                policy.WithOrigins(origins).AllowAnyMethod().AllowAnyHeader();
            else
                policy.AllowAnyOrigin().AllowAnyMethod().AllowAnyHeader();
        });
    });

    // FluentValidation
    builder.Services.AddValidatorsFromAssemblyContaining<RegisterRequestValidator>();

    // Memory cache (rate limiting)
    builder.Services.AddMemoryCache();

    // MVC + Razor Pages
    builder.Services.AddControllersWithViews()
        .AddJsonOptions(opts =>
            opts.JsonSerializerOptions.PropertyNamingPolicy = System.Text.Json.JsonNamingPolicy.CamelCase);
    builder.Services.AddRouting(opts => opts.LowercaseUrls = true);
    builder.Services.AddRazorPages(options =>
    {
        options.Conventions.AuthorizeAreaFolder("Admin", "/", "AdminOnly");
        options.Conventions.AuthorizePage("/account/profile");
        options.Conventions.AuthorizePage("/account/my-submissions");
        options.Conventions.AuthorizePage("/account/logout");
    });

    var app = builder.Build();

    // Startup pipeline: migrations → seeds → admin bootstrap
    using (var scope = app.Services.CreateScope())
    {
        var sp = scope.ServiceProvider;
        var startupLogger = sp.GetRequiredService<ILoggerFactory>().CreateLogger("Startup");

        var db = sp.GetRequiredService<AppDbContext>();
        await db.Database.MigrateAsync();

        await sp.GetRequiredService<TaxonomySeed>().SeedAsync();
        await sp.GetRequiredService<EduSeed>().SeedAsync();
        await sp.GetRequiredService<GuideTemplateSeed>().SeedAsync();
        await AdminBootstrap.SeedAsync(sp, builder.Configuration, startupLogger);
    }

    // --run-migrations: apply DB schema and seeds, then exit (used during deployment)
    if (args.Contains("--run-migrations"))
    {
        Log.Information("Migration-only mode complete. Exiting.");
        return;
    }

    // Request pipeline
    app.UseForwardedHeaders();
    app.UseMiddleware<GlobalExceptionMiddleware>();

    if (!app.Environment.IsDevelopment())
        app.UseHsts();

    app.UseHttpsRedirection();
    app.UseStaticFiles();
    app.UseRouting();
    app.UseCors("ApiPolicy");
    app.UseAuthentication();
    app.UseAuthorization();

    app.MapControllerRoute(
        name: "default",
        pattern: "{controller=Home}/{action=Index}/{id?}");
    app.MapRazorPages();

    await app.RunAsync();
}
catch (Exception ex) when (ex is not HostAbortedException)
{
    Log.Fatal(ex, "Application startup failed");
}
finally
{
    Log.CloseAndFlush();
}
