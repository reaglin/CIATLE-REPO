using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Infrastructure.Data.Configurations;

public class SiteVisitConfiguration : IEntityTypeConfiguration<SiteVisit>
{
    public void Configure(EntityTypeBuilder<SiteVisit> b)
    {
        b.ToTable("SiteVisits");
        b.HasKey(v => new { v.Day, v.VisitorHash });
        b.Property(v => v.VisitorHash).HasMaxLength(16).IsRequired();
        b.Property(v => v.Source).HasMaxLength(100);
        b.Property(v => v.LandingPath).HasMaxLength(200).IsRequired();
    }
}

public class SitePageViewConfiguration : IEntityTypeConfiguration<SitePageView>
{
    public void Configure(EntityTypeBuilder<SitePageView> b)
    {
        b.ToTable("SitePageViews");
        b.HasKey(p => new { p.Day, p.Path });
        b.Property(p => p.Path).HasMaxLength(200).IsRequired();
    }
}
