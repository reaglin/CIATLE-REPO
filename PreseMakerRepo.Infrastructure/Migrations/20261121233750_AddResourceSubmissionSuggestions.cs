using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace PreseMakerRepo.Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class AddResourceSubmissionSuggestions : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "SuggestedAlsoFor",
                table: "ResourceSubmissions",
                type: "TEXT",
                maxLength: 600,
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "SuggestedSummary",
                table: "ResourceSubmissions",
                type: "TEXT",
                maxLength: 2000,
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "SuggestedTitle",
                table: "ResourceSubmissions",
                type: "TEXT",
                maxLength: 200,
                nullable: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "SuggestedAlsoFor",
                table: "ResourceSubmissions");

            migrationBuilder.DropColumn(
                name: "SuggestedSummary",
                table: "ResourceSubmissions");

            migrationBuilder.DropColumn(
                name: "SuggestedTitle",
                table: "ResourceSubmissions");
        }
    }
}
