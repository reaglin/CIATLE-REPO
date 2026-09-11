using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace PreseMakerRepo.Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class AddCourseCatalog : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<int>(
                name: "ContactHours",
                table: "TaxonomyCourses",
                type: "INTEGER",
                nullable: true);

            migrationBuilder.AddColumn<DateTime>(
                name: "CreatedUtc",
                table: "TaxonomyCourses",
                type: "TEXT",
                nullable: true);

            migrationBuilder.AddColumn<int>(
                name: "OfferingCount",
                table: "TaxonomyCourses",
                type: "INTEGER",
                nullable: false,
                defaultValue: 0);

            migrationBuilder.AddColumn<int>(
                name: "Source",
                table: "TaxonomyCourses",
                type: "INTEGER",
                nullable: false,
                defaultValue: 0);

            migrationBuilder.AddColumn<string>(
                name: "StateTitle",
                table: "TaxonomyCourses",
                type: "TEXT",
                maxLength: 300,
                nullable: true);

            migrationBuilder.AddColumn<DateTime>(
                name: "UpdatedUtc",
                table: "TaxonomyCourses",
                type: "TEXT",
                nullable: true);

            migrationBuilder.CreateTable(
                name: "Institutions",
                columns: table => new
                {
                    Code = table.Column<string>(type: "TEXT", maxLength: 10, nullable: false),
                    Name = table.Column<string>(type: "TEXT", maxLength: 200, nullable: true),
                    Sector = table.Column<string>(type: "TEXT", maxLength: 40, nullable: true),
                    ScnsId = table.Column<string>(type: "TEXT", maxLength: 20, nullable: true),
                    UpdatedUtc = table.Column<DateTime>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Institutions", x => x.Code);
                });

            migrationBuilder.CreateTable(
                name: "CourseOfferings",
                columns: table => new
                {
                    CourseId = table.Column<string>(type: "TEXT", maxLength: 50, nullable: false),
                    InstitutionCode = table.Column<string>(type: "TEXT", maxLength: 10, nullable: false),
                    InstitutionTitle = table.Column<string>(type: "TEXT", maxLength: 300, nullable: true),
                    Credits = table.Column<decimal>(type: "TEXT", precision: 5, scale: 2, nullable: true),
                    ClockHours = table.Column<int>(type: "INTEGER", nullable: true),
                    IsActive = table.Column<bool>(type: "INTEGER", nullable: false),
                    UpdatedUtc = table.Column<DateTime>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_CourseOfferings", x => new { x.CourseId, x.InstitutionCode });
                    table.ForeignKey(
                        name: "FK_CourseOfferings_Institutions_InstitutionCode",
                        column: x => x.InstitutionCode,
                        principalTable: "Institutions",
                        principalColumn: "Code",
                        onDelete: ReferentialAction.Restrict);
                    table.ForeignKey(
                        name: "FK_CourseOfferings_TaxonomyCourses_CourseId",
                        column: x => x.CourseId,
                        principalTable: "TaxonomyCourses",
                        principalColumn: "CourseId",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_TaxonomyCourses_UpdatedUtc",
                table: "TaxonomyCourses",
                column: "UpdatedUtc");

            migrationBuilder.CreateIndex(
                name: "IX_CourseOfferings_InstitutionCode",
                table: "CourseOfferings",
                column: "InstitutionCode");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "CourseOfferings");

            migrationBuilder.DropTable(
                name: "Institutions");

            migrationBuilder.DropIndex(
                name: "IX_TaxonomyCourses_UpdatedUtc",
                table: "TaxonomyCourses");

            migrationBuilder.DropColumn(
                name: "ContactHours",
                table: "TaxonomyCourses");

            migrationBuilder.DropColumn(
                name: "CreatedUtc",
                table: "TaxonomyCourses");

            migrationBuilder.DropColumn(
                name: "OfferingCount",
                table: "TaxonomyCourses");

            migrationBuilder.DropColumn(
                name: "Source",
                table: "TaxonomyCourses");

            migrationBuilder.DropColumn(
                name: "StateTitle",
                table: "TaxonomyCourses");

            migrationBuilder.DropColumn(
                name: "UpdatedUtc",
                table: "TaxonomyCourses");
        }
    }
}
