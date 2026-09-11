using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace PreseMakerRepo.Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class AddResourceVotes : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<int>(
                name: "HelpfulCount",
                table: "CourseResources",
                type: "INTEGER",
                nullable: false,
                defaultValue: 0);

            migrationBuilder.CreateTable(
                name: "CourseResourceVotes",
                columns: table => new
                {
                    CourseResourceId = table.Column<Guid>(type: "TEXT", nullable: false),
                    VoterHash = table.Column<string>(type: "TEXT", maxLength: 64, nullable: false),
                    CreatedUtc = table.Column<DateTime>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_CourseResourceVotes", x => new { x.CourseResourceId, x.VoterHash });
                    table.ForeignKey(
                        name: "FK_CourseResourceVotes_CourseResources_CourseResourceId",
                        column: x => x.CourseResourceId,
                        principalTable: "CourseResources",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "CourseResourceVotes");

            migrationBuilder.DropColumn(
                name: "HelpfulCount",
                table: "CourseResources");
        }
    }
}
