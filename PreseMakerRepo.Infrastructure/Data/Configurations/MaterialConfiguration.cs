using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Infrastructure.Data.Configurations;

public class MaterialConfiguration : IEntityTypeConfiguration<Material>
{
    public void Configure(EntityTypeBuilder<Material> builder)
    {
        builder.HasKey(m => m.Id);

        builder.Property(m => m.Title).IsRequired().HasMaxLength(200);
        builder.Property(m => m.FileName).IsRequired();
        builder.Property(m => m.StoragePath).IsRequired();
        builder.Property(m => m.ContentType).IsRequired().HasMaxLength(200);
        builder.Property(m => m.FileSizeBytes).IsRequired();
        builder.Property(m => m.SubmittedUtc).IsRequired();

        builder.HasIndex(m => m.ModuleId);
        builder.HasIndex(m => m.Type);
        builder.HasIndex(m => m.Status);

        builder.HasOne(m => m.Module)
               .WithMany(m => m.Materials)
               .HasForeignKey(m => m.ModuleId)
               .OnDelete(DeleteBehavior.Cascade);

        builder.HasOne(m => m.Contributor)
               .WithMany(c => c.Materials)
               .HasForeignKey(m => m.ContributorId)
               .OnDelete(DeleteBehavior.Restrict);
    }
}
