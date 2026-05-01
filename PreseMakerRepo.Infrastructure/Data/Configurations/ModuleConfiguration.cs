using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Infrastructure.Data.Configurations;

public class ModuleConfiguration : IEntityTypeConfiguration<Module>
{
    public void Configure(EntityTypeBuilder<Module> builder)
    {
        builder.HasKey(m => m.Id);

        builder.Property(m => m.Title).IsRequired().HasMaxLength(200);
        builder.Property(m => m.Description).IsRequired();
        builder.Property(m => m.OutcomesJson).IsRequired().HasDefaultValue("[]");
        builder.Property(m => m.TopicHierarchyJson).IsRequired().HasDefaultValue("[]");
        builder.Property(m => m.License).IsRequired();
        builder.Property(m => m.Status).IsRequired();
        builder.Property(m => m.SubmittedUtc).IsRequired();
        builder.Property(m => m.TotalStorageBytes).IsRequired();

        builder.HasIndex(m => m.CourseId);
        builder.HasIndex(m => m.SubmittedUtc);
        builder.HasIndex(m => m.Status);
        builder.HasIndex(m => m.ContributorId);

        builder.HasOne(m => m.Contributor)
               .WithMany(c => c.Modules)
               .HasForeignKey(m => m.ContributorId)
               .OnDelete(DeleteBehavior.Restrict);

        builder.HasOne(m => m.Course)
               .WithMany(c => c.Modules)
               .HasForeignKey(m => m.CourseId)
               .OnDelete(DeleteBehavior.Restrict);
    }
}
