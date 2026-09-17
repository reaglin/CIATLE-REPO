using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace PreseMakerRepo.Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class AddCipAndCareerPaths : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "CipNodes",
                columns: table => new
                {
                    Code = table.Column<string>(type: "TEXT", maxLength: 10, nullable: false),
                    Level = table.Column<int>(type: "INTEGER", nullable: false),
                    Title = table.Column<string>(type: "TEXT", maxLength: 300, nullable: false),
                    Definition = table.Column<string>(type: "TEXT", maxLength: 4000, nullable: true),
                    Examples = table.Column<string>(type: "TEXT", maxLength: 4000, nullable: true),
                    ParentCode = table.Column<string>(type: "TEXT", maxLength: 10, nullable: true),
                    ChildCount = table.Column<int>(type: "INTEGER", nullable: false),
                    EditorialNote = table.Column<string>(type: "TEXT", maxLength: 8000, nullable: true),
                    IsActive = table.Column<bool>(type: "INTEGER", nullable: false),
                    CreatedUtc = table.Column<DateTime>(type: "TEXT", nullable: false),
                    UpdatedUtc = table.Column<DateTime>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_CipNodes", x => x.Code);
                    table.ForeignKey(
                        name: "FK_CipNodes_CipNodes_ParentCode",
                        column: x => x.ParentCode,
                        principalTable: "CipNodes",
                        principalColumn: "Code",
                        onDelete: ReferentialAction.Restrict);
                });

            migrationBuilder.CreateTable(
                name: "CareerPaths",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "TEXT", nullable: false),
                    Slug = table.Column<string>(type: "TEXT", maxLength: 100, nullable: false),
                    Name = table.Column<string>(type: "TEXT", maxLength: 200, nullable: false),
                    CipCode = table.Column<string>(type: "TEXT", maxLength: 10, nullable: false),
                    Description = table.Column<string>(type: "TEXT", maxLength: 2000, nullable: false),
                    SocCode = table.Column<string>(type: "TEXT", maxLength: 20, nullable: true),
                    CredentialNote = table.Column<string>(type: "TEXT", maxLength: 2000, nullable: true),
                    BodyHtml = table.Column<string>(type: "TEXT", nullable: true),
                    IsPublished = table.Column<bool>(type: "INTEGER", nullable: false),
                    SortOrder = table.Column<int>(type: "INTEGER", nullable: false),
                    CreatedUtc = table.Column<DateTime>(type: "TEXT", nullable: false),
                    UpdatedUtc = table.Column<DateTime>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_CareerPaths", x => x.Id);
                    table.ForeignKey(
                        name: "FK_CareerPaths_CipNodes_CipCode",
                        column: x => x.CipCode,
                        principalTable: "CipNodes",
                        principalColumn: "Code",
                        onDelete: ReferentialAction.Restrict);
                });

            migrationBuilder.CreateTable(
                name: "CareerPathCourses",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "TEXT", nullable: false),
                    CareerPathId = table.Column<Guid>(type: "TEXT", nullable: false),
                    CourseId = table.Column<string>(type: "TEXT", maxLength: 50, nullable: false),
                    Reason = table.Column<string>(type: "TEXT", maxLength: 500, nullable: false),
                    VariantNote = table.Column<string>(type: "TEXT", maxLength: 1000, nullable: true),
                    SortOrder = table.Column<int>(type: "INTEGER", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_CareerPathCourses", x => x.Id);
                    table.ForeignKey(
                        name: "FK_CareerPathCourses_CareerPaths_CareerPathId",
                        column: x => x.CareerPathId,
                        principalTable: "CareerPaths",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "CareerPathSources",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "TEXT", nullable: false),
                    CareerPathId = table.Column<Guid>(type: "TEXT", nullable: false),
                    Label = table.Column<string>(type: "TEXT", maxLength: 200, nullable: false),
                    Url = table.Column<string>(type: "TEXT", maxLength: 2048, nullable: false),
                    Note = table.Column<string>(type: "TEXT", maxLength: 500, nullable: true),
                    SortOrder = table.Column<int>(type: "INTEGER", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_CareerPathSources", x => x.Id);
                    table.ForeignKey(
                        name: "FK_CareerPathSources_CareerPaths_CareerPathId",
                        column: x => x.CareerPathId,
                        principalTable: "CareerPaths",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_CareerPathCourses_CareerPathId_SortOrder",
                table: "CareerPathCourses",
                columns: new[] { "CareerPathId", "SortOrder" });

            migrationBuilder.CreateIndex(
                name: "IX_CareerPathCourses_CourseId",
                table: "CareerPathCourses",
                column: "CourseId");

            migrationBuilder.CreateIndex(
                name: "IX_CareerPaths_CipCode_SortOrder",
                table: "CareerPaths",
                columns: new[] { "CipCode", "SortOrder" });

            migrationBuilder.CreateIndex(
                name: "IX_CareerPaths_Slug",
                table: "CareerPaths",
                column: "Slug",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_CareerPathSources_CareerPathId_SortOrder",
                table: "CareerPathSources",
                columns: new[] { "CareerPathId", "SortOrder" });

            migrationBuilder.CreateIndex(
                name: "IX_CipNodes_Level_Code",
                table: "CipNodes",
                columns: new[] { "Level", "Code" });

            migrationBuilder.CreateIndex(
                name: "IX_CipNodes_ParentCode",
                table: "CipNodes",
                column: "ParentCode");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "CareerPathCourses");

            migrationBuilder.DropTable(
                name: "CareerPathSources");

            migrationBuilder.DropTable(
                name: "CareerPaths");

            migrationBuilder.DropTable(
                name: "CipNodes");
        }
    }
}
