using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Infrastructure.Data.Configurations;

public class CourseOfferingConfiguration : IEntityTypeConfiguration<CourseOffering>
{
    public void Configure(EntityTypeBuilder<CourseOffering> b)
    {
        b.ToTable("CourseOfferings");
        b.HasKey(o => new { o.CourseId, o.InstitutionCode });
        b.Property(o => o.CourseId).HasMaxLength(50);
        b.Property(o => o.InstitutionCode).HasMaxLength(10);
        b.Property(o => o.InstitutionTitle).HasMaxLength(300);
        b.Property(o => o.Credits).HasPrecision(5, 2);

        b.HasOne(o => o.Course)
         .WithMany(c => c.Offerings)
         .HasForeignKey(o => o.CourseId)
         .OnDelete(DeleteBehavior.Cascade);

        // An institution is never deleted out from under its offerings.
        b.HasOne(o => o.Institution)
         .WithMany(i => i.Offerings)
         .HasForeignKey(o => o.InstitutionCode)
         .OnDelete(DeleteBehavior.Restrict);

        b.HasIndex(o => o.InstitutionCode);
    }
}
