using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Infrastructure.Data.Configurations;

public class GuideRequestConfiguration : IEntityTypeConfiguration<GuideRequest>
{
    public void Configure(EntityTypeBuilder<GuideRequest> b)
    {
        b.ToTable("GuideRequests");
        b.HasKey(r => r.Id);
        b.Property(r => r.CourseId).HasMaxLength(16).IsRequired();
        b.Property(r => r.CourseTitle).HasMaxLength(200).IsRequired();
        b.Property(r => r.Institution).HasMaxLength(200).IsRequired();
        b.Property(r => r.Reason).HasMaxLength(1000);
        b.Property(r => r.RequesterEmail).HasMaxLength(256);
        b.Property(r => r.RequesterIpHash).HasMaxLength(64);
        b.Property(r => r.RequesterUserId).HasMaxLength(450);
        b.Property(r => r.AdminNotes).HasMaxLength(1000);
        b.Property(r => r.Status).HasConversion<int>();
        b.Property(r => r.Channel).HasConversion<int>();

        // Ranking by course and filtering by status are the two admin/queue queries.
        b.HasIndex(r => new { r.CourseId, r.Status });
        b.HasIndex(r => r.RequestedUtc);
    }
}
