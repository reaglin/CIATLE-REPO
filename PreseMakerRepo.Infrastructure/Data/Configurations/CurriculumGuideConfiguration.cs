using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Infrastructure.Data.Configurations;

public class CurriculumGuideConfiguration : IEntityTypeConfiguration<CurriculumGuide>
{
    public void Configure(EntityTypeBuilder<CurriculumGuide> builder)
    {
        builder.HasKey(g => g.CourseId);
        builder.Property(g => g.CourseId).HasMaxLength(50);
        builder.Property(g => g.Title).IsRequired().HasMaxLength(300);
        builder.Property(g => g.HtmlContent).IsRequired();
        builder.Property(g => g.Prerequisites).HasMaxLength(500);
        builder.Property(g => g.Version).HasMaxLength(50);

        builder.HasOne(g => g.Course)
               .WithOne(c => c.Guide)
               .HasForeignKey<CurriculumGuide>(g => g.CourseId)
               .OnDelete(DeleteBehavior.Cascade);
    }
}
