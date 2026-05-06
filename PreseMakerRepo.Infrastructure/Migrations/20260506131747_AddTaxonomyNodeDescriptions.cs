using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace PreseMakerRepo.Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class AddTaxonomyNodeDescriptions : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "TaxonomyNodeDescriptions",
                columns: table => new
                {
                    NodeKey = table.Column<string>(type: "TEXT", maxLength: 100, nullable: false),
                    HtmlContent = table.Column<string>(type: "TEXT", nullable: false),
                    UpdatedUtc = table.Column<DateTime>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_TaxonomyNodeDescriptions", x => x.NodeKey);
                    table.ForeignKey(
                        name: "FK_TaxonomyNodeDescriptions_TaxonomyNodes_NodeKey",
                        column: x => x.NodeKey,
                        principalTable: "TaxonomyNodes",
                        principalColumn: "Key",
                        onDelete: ReferentialAction.Cascade);
                });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "TaxonomyNodeDescriptions");
        }
    }
}
