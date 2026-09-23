using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace PreseMakerRepo.Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class AddCareerRequests : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "AdditionalSocCodes",
                table: "CareerPaths",
                type: "TEXT",
                maxLength: 400,
                nullable: true);

            migrationBuilder.CreateTable(
                name: "CareerRequests",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "TEXT", nullable: false),
                    SocCode = table.Column<string>(type: "TEXT", maxLength: 10, nullable: false),
                    SocTitle = table.Column<string>(type: "TEXT", maxLength: 200, nullable: false),
                    CipCode = table.Column<string>(type: "TEXT", maxLength: 10, nullable: false),
                    Reason = table.Column<string>(type: "TEXT", maxLength: 1000, nullable: true),
                    Channel = table.Column<int>(type: "INTEGER", nullable: false),
                    RequesterIpHash = table.Column<string>(type: "TEXT", maxLength: 64, nullable: true),
                    RequesterUserId = table.Column<string>(type: "TEXT", maxLength: 450, nullable: true),
                    RequestedUtc = table.Column<DateTime>(type: "TEXT", nullable: false),
                    Status = table.Column<int>(type: "INTEGER", nullable: false),
                    StatusUtc = table.Column<DateTime>(type: "TEXT", nullable: true),
                    AdminNotes = table.Column<string>(type: "TEXT", maxLength: 1000, nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_CareerRequests", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "CipOccupations",
                columns: table => new
                {
                    CipCode = table.Column<string>(type: "TEXT", maxLength: 10, nullable: false),
                    SocCode = table.Column<string>(type: "TEXT", maxLength: 10, nullable: false),
                    SocTitle = table.Column<string>(type: "TEXT", maxLength: 200, nullable: false),
                    IsHidden = table.Column<bool>(type: "INTEGER", nullable: false),
                    UpdatedUtc = table.Column<DateTime>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_CipOccupations", x => new { x.CipCode, x.SocCode });
                    table.ForeignKey(
                        name: "FK_CipOccupations_CipNodes_CipCode",
                        column: x => x.CipCode,
                        principalTable: "CipNodes",
                        principalColumn: "Code",
                        onDelete: ReferentialAction.Restrict);
                });

            migrationBuilder.CreateIndex(
                name: "IX_CareerRequests_RequestedUtc",
                table: "CareerRequests",
                column: "RequestedUtc");

            migrationBuilder.CreateIndex(
                name: "IX_CareerRequests_SocCode_Status",
                table: "CareerRequests",
                columns: new[] { "SocCode", "Status" });

            migrationBuilder.CreateIndex(
                name: "IX_CipOccupations_SocCode",
                table: "CipOccupations",
                column: "SocCode");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "CareerRequests");

            migrationBuilder.DropTable(
                name: "CipOccupations");

            migrationBuilder.DropColumn(
                name: "AdditionalSocCodes",
                table: "CareerPaths");
        }
    }
}
