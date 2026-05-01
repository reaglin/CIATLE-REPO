using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace PreseMakerRepo.Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class AddCurriculumGuide : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "CurriculumGuides",
                columns: table => new
                {
                    CourseId = table.Column<string>(type: "TEXT", maxLength: 50, nullable: false),
                    Title = table.Column<string>(type: "TEXT", maxLength: 300, nullable: false),
                    HtmlContent = table.Column<string>(type: "TEXT", nullable: false),
                    Credits = table.Column<int>(type: "INTEGER", nullable: true),
                    ContactHours = table.Column<int>(type: "INTEGER", nullable: true),
                    Prerequisites = table.Column<string>(type: "TEXT", maxLength: 500, nullable: true),
                    Version = table.Column<string>(type: "TEXT", maxLength: 50, nullable: true),
                    GeneratedUtc = table.Column<DateTime>(type: "TEXT", nullable: false),
                    UpdatedUtc = table.Column<DateTime>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_CurriculumGuides", x => x.CourseId);
                    table.ForeignKey(
                        name: "FK_CurriculumGuides_TaxonomyCourses_CourseId",
                        column: x => x.CourseId,
                        principalTable: "TaxonomyCourses",
                        principalColumn: "CourseId",
                        onDelete: ReferentialAction.Cascade);
                });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "CurriculumGuides");
        }
    }
}
