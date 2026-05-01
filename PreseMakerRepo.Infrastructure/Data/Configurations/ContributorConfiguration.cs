using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Infrastructure.Data.Configurations;

public class ContributorConfiguration : IEntityTypeConfiguration<Contributor>
{
    public void Configure(EntityTypeBuilder<Contributor> builder)
    {
        builder.Property(c => c.DisplayName).HasMaxLength(100);
        builder.Property(c => c.InstitutionName).HasMaxLength(300);
        builder.Property(c => c.SuspensionReason).HasMaxLength(500);
    }
}
