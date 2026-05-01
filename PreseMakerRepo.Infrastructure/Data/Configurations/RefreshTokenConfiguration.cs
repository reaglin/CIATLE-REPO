using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Infrastructure.Data.Configurations;

public class RefreshTokenConfiguration : IEntityTypeConfiguration<RefreshToken>
{
    public void Configure(EntityTypeBuilder<RefreshToken> builder)
    {
        builder.HasKey(t => t.Id);
        builder.Property(t => t.TokenHash).IsRequired().HasMaxLength(100);
        builder.Property(t => t.ContributorId).IsRequired();
        builder.Property(t => t.ReplacedByTokenId).HasMaxLength(100);
        builder.Property(t => t.CreatedByIp).HasMaxLength(50);

        builder.HasIndex(t => t.TokenHash);
        builder.HasIndex(t => t.ContributorId);

        builder.HasOne(t => t.Contributor)
               .WithMany(c => c.RefreshTokens)
               .HasForeignKey(t => t.ContributorId)
               .OnDelete(DeleteBehavior.Cascade);
    }
}
