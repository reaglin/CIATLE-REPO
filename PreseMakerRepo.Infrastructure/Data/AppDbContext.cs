using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Infrastructure.Data;

public class AppDbContext : IdentityDbContext<Contributor, IdentityRole, string>
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

    public DbSet<Module> Modules => Set<Module>();
    public DbSet<Material> Materials => Set<Material>();
    public DbSet<ContentFlag> ContentFlags => Set<ContentFlag>();
    public DbSet<TaxonomyNode> TaxonomyNodes => Set<TaxonomyNode>();
    public DbSet<TaxonomyCourse> TaxonomyCourses => Set<TaxonomyCourse>();
    public DbSet<EduInstitution> EduInstitutions => Set<EduInstitution>();
    public DbSet<RefreshToken> RefreshTokens => Set<RefreshToken>();
    public DbSet<CurriculumGuide> CurriculumGuides => Set<CurriculumGuide>();
    public DbSet<RepoGuideTemplate> GuideTemplates => Set<RepoGuideTemplate>();
    public DbSet<TaxonomyNodeDescription> TaxonomyNodeDescriptions => Set<TaxonomyNodeDescription>();

    protected override void OnModelCreating(ModelBuilder builder)
    {
        base.OnModelCreating(builder);
        builder.ApplyConfigurationsFromAssembly(typeof(AppDbContext).Assembly);
    }
}
