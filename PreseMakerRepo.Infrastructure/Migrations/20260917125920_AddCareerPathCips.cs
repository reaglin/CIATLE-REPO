using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace PreseMakerRepo.Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class AddCareerPathCips : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "CareerPathCips",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "TEXT", nullable: false),
                    CareerPathId = table.Column<Guid>(type: "TEXT", nullable: false),
                    CipCode = table.Column<string>(type: "TEXT", maxLength: 10, nullable: false),
                    Note = table.Column<string>(type: "TEXT", maxLength: 500, nullable: true),
                    SortOrder = table.Column<int>(type: "INTEGER", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_CareerPathCips", x => x.Id);
                    table.ForeignKey(
                        name: "FK_CareerPathCips_CareerPaths_CareerPathId",
                        column: x => x.CareerPathId,
                        principalTable: "CareerPaths",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_CareerPathCips_CipNodes_CipCode",
                        column: x => x.CipCode,
                        principalTable: "CipNodes",
                        principalColumn: "Code",
                        onDelete: ReferentialAction.Restrict);
                });

            migrationBuilder.CreateIndex(
                name: "IX_CareerPathCips_CareerPathId_CipCode",
                table: "CareerPathCips",
                columns: new[] { "CareerPathId", "CipCode" },
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_CareerPathCips_CipCode",
                table: "CareerPathCips",
                column: "CipCode");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "CareerPathCips");
        }
    }
}
