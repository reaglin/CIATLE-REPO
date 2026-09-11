using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Infrastructure.Data.Configurations;

public class CourseResourceConfiguration : IEntityTypeConfiguration<CourseResource>
{
    public void Configure(EntityTypeBuilder<CourseResource> b)
    {
        b.ToTable("CourseResources");
        b.HasKey(r => r.Id);
        b.Property(r => r.CourseId).HasMaxLength(50).IsRequired();
        b.Property(r => r.Url).HasMaxLength(2048).IsRequired();
        b.Property(r => r.YouTubeVideoId).HasMaxLength(20);
        b.Property(r => r.Title).HasMaxLength(200).IsRequired();
        b.Property(r => r.Summary).HasMaxLength(2000).IsRequired();
        b.Property(r => r.Type).HasConversion<int>();
        b.Property(r => r.Status).HasConversion<int>();
        b.Property(r => r.Source).HasConversion<int>();

        b.HasOne(r => r.Course)
         .WithMany()
         .HasForeignKey(r => r.CourseId)
         .OnDelete(DeleteBehavior.Cascade);

        // A link is listed at most once per course; the same link on other courses is a separate listing.
        b.HasIndex(r => new { r.CourseId, r.Url }).IsUnique();
        // "Also listed for" and the reviewer's "where is this link already listed" both look up by URL.
        b.HasIndex(r => r.Url);
    }
}

public class ResourceSubmissionConfiguration : IEntityTypeConfiguration<ResourceSubmission>
{
    public void Configure(EntityTypeBuilder<ResourceSubmission> b)
    {
        b.ToTable("ResourceSubmissions");
        b.HasKey(s => s.Id);
        b.Property(s => s.CourseId).HasMaxLength(50).IsRequired();
        b.Property(s => s.Url).HasMaxLength(2048).IsRequired();
        b.Property(s => s.YouTubeVideoId).HasMaxLength(20);
        b.Property(s => s.Description).HasMaxLength(500);
        b.Property(s => s.DecisionNote).HasMaxLength(300);
        b.Property(s => s.SubmitterIpHash).HasMaxLength(64);
        b.Property(s => s.SubmitterUserId).HasMaxLength(450);
        b.Property(s => s.Type).HasConversion<int>();
        b.Property(s => s.Status).HasConversion<int>();

        b.HasOne<TaxonomyCourse>()
         .WithMany()
         .HasForeignKey(s => s.CourseId)
         .OnDelete(DeleteBehavior.Cascade);

        b.HasOne<CourseResource>()
         .WithMany()
         .HasForeignKey(s => s.CourseResourceId)
         .OnDelete(DeleteBehavior.SetNull);

        // The queue reads by status and date; duplicates are checked per course.
        b.HasIndex(s => new { s.Status, s.SubmittedUtc });
        b.HasIndex(s => new { s.CourseId, s.Status });
    }
}
