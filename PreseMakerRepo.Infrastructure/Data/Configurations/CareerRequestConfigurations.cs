using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Infrastructure.Data.Configurations;

public class CipOccupationConfiguration : IEntityTypeConfiguration<CipOccupation>
{
    public void Configure(EntityTypeBuilder<CipOccupation> b)
    {
        b.ToTable("CipOccupations");
        b.HasKey(o => new { o.CipCode, o.SocCode });
        b.Property(o => o.CipCode).HasMaxLength(10).IsRequired();
        b.Property(o => o.SocCode).HasMaxLength(10).IsRequired();
        b.Property(o => o.SocTitle).HasMaxLength(200).IsRequired();

        // ⚠ Restrict, like CareerPath: a CIP node is never deleted by the seed, and an
        // occupation row must not silently vanish with one.
        b.HasOne(o => o.Cip).WithMany()
            .HasForeignKey(o => o.CipCode)
            .OnDelete(DeleteBehavior.Restrict);

        b.HasIndex(o => o.SocCode);
    }
}

public class CareerRequestConfiguration : IEntityTypeConfiguration<CareerRequest>
{
    public void Configure(EntityTypeBuilder<CareerRequest> b)
    {
        b.ToTable("CareerRequests");
        b.HasKey(r => r.Id);
        b.Property(r => r.SocCode).HasMaxLength(10).IsRequired();
        b.Property(r => r.SocTitle).HasMaxLength(200).IsRequired();
        b.Property(r => r.CipCode).HasMaxLength(10).IsRequired();
        b.Property(r => r.Reason).HasMaxLength(1000);
        b.Property(r => r.RequesterIpHash).HasMaxLength(64);
        b.Property(r => r.RequesterUserId).HasMaxLength(450);
        b.Property(r => r.AdminNotes).HasMaxLength(1000);
        b.Property(r => r.Status).HasConversion<int>();
        b.Property(r => r.Channel).HasConversion<int>();

        // Ranking by occupation and filtering by status are the two queue queries.
        b.HasIndex(r => new { r.SocCode, r.Status });
        b.HasIndex(r => r.RequestedUtc);
    }
}
