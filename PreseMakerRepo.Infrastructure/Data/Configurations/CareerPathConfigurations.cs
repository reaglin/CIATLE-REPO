using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Infrastructure.Data.Configurations;

/// <summary>
/// The CIP browse tree. Same shape as <see cref="TaxonomyNodeConfiguration"/>: a string key
/// and a self-reference, restricted on delete so a series cannot be removed under its groups.
/// </summary>
public class CipNodeConfiguration : IEntityTypeConfiguration<CipNode>
{
    public void Configure(EntityTypeBuilder<CipNode> b)
    {
        b.ToTable("CipNodes");
        b.HasKey(n => n.Code);
        b.Property(n => n.Code).HasMaxLength(10);
        b.Property(n => n.Title).IsRequired().HasMaxLength(300);
        b.Property(n => n.Definition).HasMaxLength(4000);
        b.Property(n => n.Examples).HasMaxLength(4000);
        b.Property(n => n.ParentCode).HasMaxLength(10);
        b.Property(n => n.EditorialNote).HasMaxLength(8000);

        b.HasOne(n => n.Parent)
         .WithMany(n => n.Children)
         .HasForeignKey(n => n.ParentCode)
         .IsRequired(false)
         .OnDelete(DeleteBehavior.Restrict);

        // The series index page lists level 2; a group page lists its children in code order.
        b.HasIndex(n => new { n.Level, n.Code });
    }
}

public class CareerPathConfiguration : IEntityTypeConfiguration<CareerPath>
{
    public void Configure(EntityTypeBuilder<CareerPath> b)
    {
        b.ToTable("CareerPaths");
        b.HasKey(p => p.Id);
        b.Property(p => p.Slug).IsRequired().HasMaxLength(100);
        b.Property(p => p.Name).IsRequired().HasMaxLength(200);
        b.Property(p => p.CipCode).IsRequired().HasMaxLength(10);
        b.Property(p => p.Description).IsRequired().HasMaxLength(2000);
        b.Property(p => p.SocCode).HasMaxLength(20);
        b.Property(p => p.AdditionalSocCodes).HasMaxLength(400);
        b.Property(p => p.CredentialNote).HasMaxLength(2000);

        // A path is filed under a CIP node and cannot outlive it; restricting the delete
        // means reseeding the taxonomy can never silently drop authored content.
        b.HasOne(p => p.Cip)
         .WithMany(n => n.CareerPaths)
         .HasForeignKey(p => p.CipCode)
         .OnDelete(DeleteBehavior.Restrict);

        b.HasIndex(p => p.Slug).IsUnique();
        b.HasIndex(p => new { p.CipCode, p.SortOrder });
    }
}

public class CareerPathCipConfiguration : IEntityTypeConfiguration<CareerPathCip>
{
    public void Configure(EntityTypeBuilder<CareerPathCip> b)
    {
        b.ToTable("CareerPathCips");
        b.HasKey(c => c.Id);
        b.Property(c => c.CipCode).IsRequired().HasMaxLength(10);
        b.Property(c => c.Note).HasMaxLength(500);

        b.HasOne(c => c.CareerPath)
         .WithMany(p => p.Cips)
         .HasForeignKey(c => c.CareerPathId)
         .OnDelete(DeleteBehavior.Cascade);

        // Restricted like the primary: reseeding the taxonomy must never quietly
        // unfile a path that an author deliberately hung on a node.
        b.HasOne(c => c.Cip)
         .WithMany()
         .HasForeignKey(c => c.CipCode)
         .OnDelete(DeleteBehavior.Restrict);

        // A path is filed under a given code at most once.
        b.HasIndex(c => new { c.CareerPathId, c.CipCode }).IsUnique();
        // The area page asks "which paths are filed here" -- this is that lookup.
        b.HasIndex(c => c.CipCode);
    }
}

public class CareerPathCourseConfiguration : IEntityTypeConfiguration<CareerPathCourse>
{
    public void Configure(EntityTypeBuilder<CareerPathCourse> b)
    {
        b.ToTable("CareerPathCourses");
        b.HasKey(c => c.Id);
        b.Property(c => c.CourseId).IsRequired().HasMaxLength(50);
        b.Property(c => c.Reason).IsRequired().HasMaxLength(500);
        b.Property(c => c.VariantNote).HasMaxLength(1000);

        b.HasOne(c => c.CareerPath)
         .WithMany(p => p.Courses)
         .HasForeignKey(c => c.CareerPathId)
         .OnDelete(DeleteBehavior.Cascade);

        // ⚠ No foreign key to TaxonomyCourse, deliberately — the same decision
        // GuideRequest makes. An author places a course by its SCNS id, and a path may
        // legitimately name a course the site does not list yet; that is the signal to
        // list it (Tools/CLAUDE.md: pathway-derived rows are the third demand signal),
        // not a constraint violation. The page joins on the id and shows what it finds.
        b.HasIndex(c => c.CourseId);
        b.HasIndex(c => new { c.CareerPathId, c.SortOrder });
    }
}

public class CareerPathSourceConfiguration : IEntityTypeConfiguration<CareerPathSource>
{
    public void Configure(EntityTypeBuilder<CareerPathSource> b)
    {
        b.ToTable("CareerPathSources");
        b.HasKey(s => s.Id);
        b.Property(s => s.Label).IsRequired().HasMaxLength(200);
        b.Property(s => s.Url).IsRequired().HasMaxLength(2048);
        b.Property(s => s.Note).HasMaxLength(500);

        b.HasOne(s => s.CareerPath)
         .WithMany(p => p.Sources)
         .HasForeignKey(s => s.CareerPathId)
         .OnDelete(DeleteBehavior.Cascade);

        b.HasIndex(s => new { s.CareerPathId, s.SortOrder });
    }
}
