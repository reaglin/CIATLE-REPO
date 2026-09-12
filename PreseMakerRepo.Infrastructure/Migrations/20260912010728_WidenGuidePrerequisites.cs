using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace PreseMakerRepo.Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class WidenGuidePrerequisites : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            // Deliberately empty, and it must still be kept.
            //
            // Raising CurriculumGuide.Prerequisites from 500 to 1000 characters changes the model but emits
            // no SQLite DDL: SQLite stores TEXT without a declared width, so there is nothing to alter and
            // longer values were always physically storable. What this migration does is carry the new
            // width into the model snapshot, so that the planned PostgreSQL swap generates varchar(1000)
            // rather than varchar(500) — and so the history records when the ceiling moved.
            //
            // Do not delete it as a no-op: without it the snapshot and the configuration disagree, and the
            // next migration generated on a non-SQLite provider would quietly narrow the column.
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            // Nothing to undo on SQLite, for the same reason. Reverting the width is a model change only.
        }
    }
}
