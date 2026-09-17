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
    public DbSet<GuideRequest> GuideRequests => Set<GuideRequest>();
    public DbSet<Institution> Institutions => Set<Institution>();
    public DbSet<CourseOffering> CourseOfferings => Set<CourseOffering>();
    public DbSet<CourseResource> CourseResources => Set<CourseResource>();
    public DbSet<ResourceSubmission> ResourceSubmissions => Set<ResourceSubmission>();
    public DbSet<CourseResourceVote> CourseResourceVotes => Set<CourseResourceVote>();

    // CIP taxonomy + Career Paths (2026-09-17). The CIP tree is the browse framework for
    // both Career Paths and, later, Programs -- one tree, both hang off it (Ron's call).
    public DbSet<CipNode> CipNodes => Set<CipNode>();
    public DbSet<CareerPath> CareerPaths => Set<CareerPath>();
    public DbSet<CareerPathCip> CareerPathCips => Set<CareerPathCip>();
    public DbSet<CareerPathCourse> CareerPathCourses => Set<CareerPathCourse>();
    public DbSet<CareerPathSource> CareerPathSources => Set<CareerPathSource>();

    protected override void OnModelCreating(ModelBuilder builder)
    {
        base.OnModelCreating(builder);
        builder.ApplyConfigurationsFromAssembly(typeof(AppDbContext).Assembly);
    }
}
