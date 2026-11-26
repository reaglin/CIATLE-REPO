using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace PreseMakerRepo.Infrastructure.Migrations
{
    /// <summary>
    /// Data only (plan 16.2): takes out the visitor counter's records of the program that, from Saturday 21 to
    /// Tuesday 24 November 2026, opened about 58,000 course-resources pages in a full browser, each from a different
    /// address with no referring site, and waited 5 seconds on each, so it was counted as about 15,000 visitors a day
    /// (people read about 10 pages a day then). Removed for those four days only: visits with no referring site
    /// that landed on a course-resources page or the subject tree, and the page views of those two parts of the site.
    /// The few people who read those pages on those days go with them. Since plan 16.1 a page counts only after a
    /// mouse movement, scroll, tap or key, so waiting is not enough. Runs once; nothing to undo.
    /// </summary>
    public partial class RemoveBotVisitsNov2026 : Migration
    {
        internal const string FirstDay = "2026-11-21";
        internal const string LastDay = "2026-11-24";

        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.Sql($"""
                DELETE FROM "SiteVisits"
                WHERE "Day" >= '{FirstDay}' AND "Day" <= '{LastDay}'
                  AND "Source" IS NULL
                  AND ("LandingPath" LIKE '/courses/%/resources' OR "LandingPath" LIKE '/browse%');
                """);
            migrationBuilder.Sql($"""
                DELETE FROM "SitePageViews"
                WHERE "Day" >= '{FirstDay}' AND "Day" <= '{LastDay}'
                  AND ("Path" LIKE '/courses/%/resources' OR "Path" LIKE '/browse%');
                """);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            // The removed records cannot be brought back; nothing to undo.
        }
    }
}
