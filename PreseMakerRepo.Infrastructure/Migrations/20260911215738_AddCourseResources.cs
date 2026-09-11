using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace PreseMakerRepo.Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class AddCourseResources : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "CourseResources",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "TEXT", nullable: false),
                    CourseId = table.Column<string>(type: "TEXT", maxLength: 50, nullable: false),
                    Type = table.Column<int>(type: "INTEGER", nullable: false),
                    Url = table.Column<string>(type: "TEXT", maxLength: 2048, nullable: false),
                    YouTubeVideoId = table.Column<string>(type: "TEXT", maxLength: 20, nullable: true),
                    Title = table.Column<string>(type: "TEXT", maxLength: 200, nullable: false),
                    Summary = table.Column<string>(type: "TEXT", maxLength: 2000, nullable: false),
                    Status = table.Column<int>(type: "INTEGER", nullable: false),
                    Source = table.Column<int>(type: "INTEGER", nullable: false),
                    SubmissionId = table.Column<Guid>(type: "TEXT", nullable: true),
                    CreatedUtc = table.Column<DateTime>(type: "TEXT", nullable: false),
                    UpdatedUtc = table.Column<DateTime>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_CourseResources", x => x.Id);
                    table.ForeignKey(
                        name: "FK_CourseResources_TaxonomyCourses_CourseId",
                        column: x => x.CourseId,
                        principalTable: "TaxonomyCourses",
                        principalColumn: "CourseId",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "ResourceSubmissions",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "TEXT", nullable: false),
                    CourseId = table.Column<string>(type: "TEXT", maxLength: 50, nullable: false),
                    Url = table.Column<string>(type: "TEXT", maxLength: 2048, nullable: false),
                    Type = table.Column<int>(type: "INTEGER", nullable: false),
                    YouTubeVideoId = table.Column<string>(type: "TEXT", maxLength: 20, nullable: true),
                    Description = table.Column<string>(type: "TEXT", maxLength: 500, nullable: true),
                    Status = table.Column<int>(type: "INTEGER", nullable: false),
                    DecisionNote = table.Column<string>(type: "TEXT", maxLength: 300, nullable: true),
                    CourseResourceId = table.Column<Guid>(type: "TEXT", nullable: true),
                    SubmittedUtc = table.Column<DateTime>(type: "TEXT", nullable: false),
                    DecidedUtc = table.Column<DateTime>(type: "TEXT", nullable: true),
                    SubmitterIpHash = table.Column<string>(type: "TEXT", maxLength: 64, nullable: true),
                    SubmitterUserId = table.Column<string>(type: "TEXT", maxLength: 450, nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_ResourceSubmissions", x => x.Id);
                    table.ForeignKey(
                        name: "FK_ResourceSubmissions_CourseResources_CourseResourceId",
                        column: x => x.CourseResourceId,
                        principalTable: "CourseResources",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.SetNull);
                    table.ForeignKey(
                        name: "FK_ResourceSubmissions_TaxonomyCourses_CourseId",
                        column: x => x.CourseId,
                        principalTable: "TaxonomyCourses",
                        principalColumn: "CourseId",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_CourseResources_CourseId_Url",
                table: "CourseResources",
                columns: new[] { "CourseId", "Url" },
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_CourseResources_Url",
                table: "CourseResources",
                column: "Url");

            migrationBuilder.CreateIndex(
                name: "IX_ResourceSubmissions_CourseId_Status",
                table: "ResourceSubmissions",
                columns: new[] { "CourseId", "Status" });

            migrationBuilder.CreateIndex(
                name: "IX_ResourceSubmissions_CourseResourceId",
                table: "ResourceSubmissions",
                column: "CourseResourceId");

            migrationBuilder.CreateIndex(
                name: "IX_ResourceSubmissions_Status_SubmittedUtc",
                table: "ResourceSubmissions",
                columns: new[] { "Status", "SubmittedUtc" });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "ResourceSubmissions");

            migrationBuilder.DropTable(
                name: "CourseResources");
        }
    }
}
