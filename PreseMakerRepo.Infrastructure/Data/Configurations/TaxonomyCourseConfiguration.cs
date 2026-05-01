using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Infrastructure.Data.Configurations;

public class TaxonomyCourseConfiguration : IEntityTypeConfiguration<TaxonomyCourse>
{
    public void Configure(EntityTypeBuilder<TaxonomyCourse> builder)
    {
        builder.HasKey(c => c.CourseId);
        builder.Property(c => c.CourseId).HasMaxLength(50);
        builder.Property(c => c.Title).IsRequired().HasMaxLength(300);
        builder.Property(c => c.CurriculumGuideUrl).HasMaxLength(500);

        builder.HasOne(c => c.Level3Node)
               .WithMany(n => n.Courses)
               .HasForeignKey(c => c.Level3Key)
               .IsRequired(false)
               .OnDelete(DeleteBehavior.Restrict);
    }
}
