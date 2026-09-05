using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace PreseMakerRepo.Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class AddGuideRequests : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "GuideRequests",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "TEXT", nullable: false),
                    CourseId = table.Column<string>(type: "TEXT", maxLength: 16, nullable: false),
                    CourseTitle = table.Column<string>(type: "TEXT", maxLength: 200, nullable: false),
                    Institution = table.Column<string>(type: "TEXT", maxLength: 200, nullable: false),
                    Reason = table.Column<string>(type: "TEXT", maxLength: 1000, nullable: true),
                    RequesterEmail = table.Column<string>(type: "TEXT", maxLength: 256, nullable: true),
                    RequesterIpHash = table.Column<string>(type: "TEXT", maxLength: 64, nullable: true),
                    RequesterUserId = table.Column<string>(type: "TEXT", maxLength: 450, nullable: true),
                    IsInTaxonomy = table.Column<bool>(type: "INTEGER", nullable: false),
                    RequestedUtc = table.Column<DateTime>(type: "TEXT", nullable: false),
                    Status = table.Column<int>(type: "INTEGER", nullable: false),
                    StatusUtc = table.Column<DateTime>(type: "TEXT", nullable: true),
                    AdminNotes = table.Column<string>(type: "TEXT", maxLength: 1000, nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_GuideRequests", x => x.Id);
                });

            migrationBuilder.CreateIndex(
                name: "IX_GuideRequests_CourseId_Status",
                table: "GuideRequests",
                columns: new[] { "CourseId", "Status" });

            migrationBuilder.CreateIndex(
                name: "IX_GuideRequests_RequestedUtc",
                table: "GuideRequests",
                column: "RequestedUtc");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "GuideRequests");
        }
    }
}
