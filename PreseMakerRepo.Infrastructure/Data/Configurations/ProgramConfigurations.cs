using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using PreseMakerRepo.Core.Models;
using ProgramEntity = PreseMakerRepo.Core.Models.Program;

namespace PreseMakerRepo.Infrastructure.Data.Configurations;

public class ProgramConfiguration : IEntityTypeConfiguration<ProgramEntity>
{
    public void Configure(EntityTypeBuilder<ProgramEntity> b)
    {
        b.ToTable("Programs");
        b.HasKey(p => p.Id);
        b.Property(p => p.Slug).IsRequired().HasMaxLength(100);
        b.Property(p => p.Name).IsRequired().HasMaxLength(200);
        b.Property(p => p.Description).IsRequired().HasMaxLength(2000);
        b.Property(p => p.DegreesNote).HasMaxLength(2000);
        b.HasIndex(p => p.Slug).IsUnique();
        b.HasIndex(p => p.SortOrder);
    }
}

public class ProgramCipConfiguration : IEntityTypeConfiguration<ProgramCip>
{
    public void Configure(EntityTypeBuilder<ProgramCip> b)
    {
        b.ToTable("ProgramCips");
        b.HasKey(c => c.Id);
        b.Property(c => c.CipCode).IsRequired().HasMaxLength(10);
        b.Property(c => c.Note).HasMaxLength(500);

        b.HasOne(c => c.Program)
         .WithMany(p => p.Cips)
         .HasForeignKey(c => c.ProgramId)
         .OnDelete(DeleteBehavior.Cascade);

        // ⚠ No foreign key to CipNode. These are PREFIXES -- "51.38" covers every
        // 6-digit code beneath it -- so they do not have to name a seeded node.
        b.HasIndex(c => new { c.ProgramId, c.CipCode }).IsUnique();
        b.HasIndex(c => c.CipCode);
    }
}

public class CareerPathProgramConfiguration : IEntityTypeConfiguration<CareerPathProgram>
{
    public void Configure(EntityTypeBuilder<CareerPathProgram> b)
    {
        b.ToTable("CareerPathPrograms");
        b.HasKey(x => x.Id);
        b.Property(x => x.Note).HasMaxLength(500);

        b.HasOne(x => x.CareerPath)
         .WithMany()
         .HasForeignKey(x => x.CareerPathId)
         .OnDelete(DeleteBehavior.Cascade);

        b.HasOne(x => x.Program)
         .WithMany(p => p.CareerPaths)
         .HasForeignKey(x => x.ProgramId)
         .OnDelete(DeleteBehavior.Cascade);

        b.HasIndex(x => new { x.CareerPathId, x.ProgramId }).IsUnique();
    }
}

public class InstitutionAwardConfiguration : IEntityTypeConfiguration<InstitutionAward>
{
    public void Configure(EntityTypeBuilder<InstitutionAward> b)
    {
        b.ToTable("InstitutionAwards");
        b.HasKey(a => a.Id);
        b.Property(a => a.UnitId).IsRequired().HasMaxLength(12);
        b.Property(a => a.InstitutionName).IsRequired().HasMaxLength(300);
        b.Property(a => a.InstitutionCode).HasMaxLength(10);
        b.Property(a => a.CipCode).IsRequired().HasMaxLength(10);
        b.Property(a => a.AwardLevel).IsRequired().HasMaxLength(60);

        // "Which schools award anything in this CIP" is THE query this table exists for,
        // and it runs as a prefix match, so CipCode leads the index.
        b.HasIndex(a => a.CipCode);
        b.HasIndex(a => new { a.UnitId, a.CipCode, a.AwardLevel, a.Year }).IsUnique();
    }
}
