using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace PreseMakerRepo.Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class AddProgramPanelClicks : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "ProgramPanelClicks",
                columns: table => new
                {
                    Day = table.Column<DateOnly>(type: "TEXT", nullable: false),
                    ProgramId = table.Column<string>(type: "TEXT", maxLength: 40, nullable: false),
                    Link = table.Column<string>(type: "TEXT", maxLength: 10, nullable: false),
                    Clicks = table.Column<int>(type: "INTEGER", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_ProgramPanelClicks", x => new { x.Day, x.ProgramId, x.Link });
                });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "ProgramPanelClicks");
        }
    }
}
