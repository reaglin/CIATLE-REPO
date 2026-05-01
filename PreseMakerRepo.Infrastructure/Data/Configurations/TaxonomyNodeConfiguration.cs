using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Infrastructure.Data.Configurations;

public class TaxonomyNodeConfiguration : IEntityTypeConfiguration<TaxonomyNode>
{
    public void Configure(EntityTypeBuilder<TaxonomyNode> builder)
    {
        builder.HasKey(n => n.Key);
        builder.Property(n => n.Key).HasMaxLength(100);
        builder.Property(n => n.Name).IsRequired().HasMaxLength(200);
        builder.Property(n => n.Level).IsRequired();

        builder.HasOne(n => n.Parent)
               .WithMany(n => n.Children)
               .HasForeignKey(n => n.ParentKey)
               .IsRequired(false)
               .OnDelete(DeleteBehavior.Restrict);
    }
}
