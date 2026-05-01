using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Infrastructure.Data.Configurations;

public class EduInstitutionConfiguration : IEntityTypeConfiguration<EduInstitution>
{
    public void Configure(EntityTypeBuilder<EduInstitution> builder)
    {
        builder.HasKey(e => e.EmailDomain);
        builder.Property(e => e.EmailDomain).HasMaxLength(100);
        builder.Property(e => e.InstitutionName).IsRequired().HasMaxLength(300);
        builder.Property(e => e.State).HasMaxLength(10);
        builder.Property(e => e.Country).HasMaxLength(10);
    }
}
