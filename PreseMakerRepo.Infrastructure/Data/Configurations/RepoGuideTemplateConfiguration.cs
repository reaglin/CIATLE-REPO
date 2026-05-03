using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Infrastructure.Data.Configurations;

public class RepoGuideTemplateConfiguration : IEntityTypeConfiguration<RepoGuideTemplate>
{
    public void Configure(EntityTypeBuilder<RepoGuideTemplate> builder)
    {
        builder.HasKey(t => t.Id);
        builder.Property(t => t.WorkingTitle).IsRequired().HasMaxLength(200);
        builder.Property(t => t.Prompt).IsRequired();
    }
}
