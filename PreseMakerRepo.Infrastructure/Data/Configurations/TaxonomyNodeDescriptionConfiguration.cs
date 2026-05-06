using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Infrastructure.Data.Configurations;

public class TaxonomyNodeDescriptionConfiguration : IEntityTypeConfiguration<TaxonomyNodeDescription>
{
    public void Configure(EntityTypeBuilder<TaxonomyNodeDescription> builder)
    {
        builder.HasKey(d => d.NodeKey);
        builder.Property(d => d.NodeKey).HasMaxLength(100);
        builder.Property(d => d.HtmlContent).IsRequired();

        builder.HasOne(d => d.Node)
               .WithOne(n => n.Description)
               .HasForeignKey<TaxonomyNodeDescription>(d => d.NodeKey)
               .OnDelete(DeleteBehavior.Cascade);
    }
}
