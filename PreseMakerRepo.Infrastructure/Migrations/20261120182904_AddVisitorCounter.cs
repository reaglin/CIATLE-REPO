using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace PreseMakerRepo.Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class AddVisitorCounter : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "SitePageViews",
                columns: table => new
                {
                    Day = table.Column<DateOnly>(type: "TEXT", nullable: false),
                    Path = table.Column<string>(type: "TEXT", maxLength: 200, nullable: false),
                    Views = table.Column<int>(type: "INTEGER", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_SitePageViews", x => new { x.Day, x.Path });
                });

            migrationBuilder.CreateTable(
                name: "SiteVisits",
                columns: table => new
                {
                    Day = table.Column<DateOnly>(type: "TEXT", nullable: false),
                    VisitorHash = table.Column<string>(type: "TEXT", maxLength: 16, nullable: false),
                    Source = table.Column<string>(type: "TEXT", maxLength: 100, nullable: true),
                    LandingPath = table.Column<string>(type: "TEXT", maxLength: 200, nullable: false),
                    PageViews = table.Column<int>(type: "INTEGER", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_SiteVisits", x => new { x.Day, x.VisitorHash });
                });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "SitePageViews");

            migrationBuilder.DropTable(
                name: "SiteVisits");
        }
    }
}
