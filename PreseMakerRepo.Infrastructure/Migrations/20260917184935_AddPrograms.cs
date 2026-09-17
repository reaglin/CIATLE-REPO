using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace PreseMakerRepo.Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class AddPrograms : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "InstitutionAwards",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "TEXT", nullable: false),
                    UnitId = table.Column<string>(type: "TEXT", maxLength: 12, nullable: false),
                    InstitutionName = table.Column<string>(type: "TEXT", maxLength: 300, nullable: false),
                    InstitutionCode = table.Column<string>(type: "TEXT", maxLength: 10, nullable: true),
                    CipCode = table.Column<string>(type: "TEXT", maxLength: 10, nullable: false),
                    AwardLevel = table.Column<string>(type: "TEXT", maxLength: 60, nullable: false),
                    Completions = table.Column<int>(type: "INTEGER", nullable: false),
                    Year = table.Column<int>(type: "INTEGER", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_InstitutionAwards", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "Programs",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "TEXT", nullable: false),
                    Slug = table.Column<string>(type: "TEXT", maxLength: 100, nullable: false),
                    Name = table.Column<string>(type: "TEXT", maxLength: 200, nullable: false),
                    Description = table.Column<string>(type: "TEXT", maxLength: 2000, nullable: false),
                    BodyHtml = table.Column<string>(type: "TEXT", nullable: true),
                    DegreesNote = table.Column<string>(type: "TEXT", maxLength: 2000, nullable: true),
                    IsPublished = table.Column<bool>(type: "INTEGER", nullable: false),
                    SortOrder = table.Column<int>(type: "INTEGER", nullable: false),
                    CreatedUtc = table.Column<DateTime>(type: "TEXT", nullable: false),
                    UpdatedUtc = table.Column<DateTime>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Programs", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "CareerPathPrograms",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "TEXT", nullable: false),
                    CareerPathId = table.Column<Guid>(type: "TEXT", nullable: false),
                    ProgramId = table.Column<Guid>(type: "TEXT", nullable: false),
                    Note = table.Column<string>(type: "TEXT", maxLength: 500, nullable: true),
                    SortOrder = table.Column<int>(type: "INTEGER", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_CareerPathPrograms", x => x.Id);
                    table.ForeignKey(
                        name: "FK_CareerPathPrograms_CareerPaths_CareerPathId",
                        column: x => x.CareerPathId,
                        principalTable: "CareerPaths",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_CareerPathPrograms_Programs_ProgramId",
                        column: x => x.ProgramId,
                        principalTable: "Programs",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "ProgramCips",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "TEXT", nullable: false),
                    ProgramId = table.Column<Guid>(type: "TEXT", nullable: false),
                    CipCode = table.Column<string>(type: "TEXT", maxLength: 10, nullable: false),
                    Note = table.Column<string>(type: "TEXT", maxLength: 500, nullable: true),
                    SortOrder = table.Column<int>(type: "INTEGER", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_ProgramCips", x => x.Id);
                    table.ForeignKey(
                        name: "FK_ProgramCips_Programs_ProgramId",
                        column: x => x.ProgramId,
                        principalTable: "Programs",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_CareerPathPrograms_CareerPathId_ProgramId",
                table: "CareerPathPrograms",
                columns: new[] { "CareerPathId", "ProgramId" },
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_CareerPathPrograms_ProgramId",
                table: "CareerPathPrograms",
                column: "ProgramId");

            migrationBuilder.CreateIndex(
                name: "IX_InstitutionAwards_CipCode",
                table: "InstitutionAwards",
                column: "CipCode");

            migrationBuilder.CreateIndex(
                name: "IX_InstitutionAwards_UnitId_CipCode_AwardLevel_Year",
                table: "InstitutionAwards",
                columns: new[] { "UnitId", "CipCode", "AwardLevel", "Year" },
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_ProgramCips_CipCode",
                table: "ProgramCips",
                column: "CipCode");

            migrationBuilder.CreateIndex(
                name: "IX_ProgramCips_ProgramId_CipCode",
                table: "ProgramCips",
                columns: new[] { "ProgramId", "CipCode" },
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_Programs_Slug",
                table: "Programs",
                column: "Slug",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_Programs_SortOrder",
                table: "Programs",
                column: "SortOrder");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "CareerPathPrograms");

            migrationBuilder.DropTable(
                name: "InstitutionAwards");

            migrationBuilder.DropTable(
                name: "ProgramCips");

            migrationBuilder.DropTable(
                name: "Programs");
        }
    }
}
