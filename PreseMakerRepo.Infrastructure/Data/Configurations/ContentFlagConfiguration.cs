using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Infrastructure.Data.Configurations;

public class ContentFlagConfiguration : IEntityTypeConfiguration<ContentFlag>
{
    public void Configure(EntityTypeBuilder<ContentFlag> builder)
    {
        builder.HasKey(f => f.Id);
        builder.Property(f => f.Reason).HasMaxLength(500);
        builder.Property(f => f.FlaggedUtc).IsRequired();

        // Exactly one of ModuleId/MaterialId must be non-null
        builder.ToTable("ContentFlags", t => t.HasCheckConstraint(
            "CK_ContentFlag_OneTarget",
            "(ModuleId IS NULL AND MaterialId IS NOT NULL) OR (ModuleId IS NOT NULL AND MaterialId IS NULL)"));

        builder.HasOne(f => f.Module)
               .WithMany(m => m.Flags)
               .HasForeignKey(f => f.ModuleId)
               .IsRequired(false)
               .OnDelete(DeleteBehavior.Cascade);

        builder.HasOne(f => f.Material)
               .WithMany(m => m.Flags)
               .HasForeignKey(f => f.MaterialId)
               .IsRequired(false)
               .OnDelete(DeleteBehavior.Cascade);
    }
}
