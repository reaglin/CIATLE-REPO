using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Infrastructure.Data.Configurations;

public class InstitutionConfiguration : IEntityTypeConfiguration<Institution>
{
    public void Configure(EntityTypeBuilder<Institution> b)
    {
        b.ToTable("Institutions");
        b.HasKey(i => i.Code);
        b.Property(i => i.Code).HasMaxLength(10);
        b.Property(i => i.Name).HasMaxLength(200);
        b.Property(i => i.Sector).HasMaxLength(40);
        b.Property(i => i.ScnsId).HasMaxLength(20);
    }
}
