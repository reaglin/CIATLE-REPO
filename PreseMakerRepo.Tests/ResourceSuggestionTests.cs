using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Memory;
using PreseMakerRepo.Api.Models.Requests;
using PreseMakerRepo.Api.Options;
using PreseMakerRepo.Api.Services;
using PreseMakerRepo.Api.Validators;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;
using PreseMakerRepo.Infrastructure.Options;
using Xunit;
using MsOptions = Microsoft.Extensions.Options.Options;

namespace PreseMakerRepo.Tests;

/// <summary>A visitor's suggested listing (title, summary, other courses) is kept with the suggestion for the reviewer.</summary>
public class ResourceSuggestionTests
{
    [Fact]
    public void Other_courses_are_normalised_without_repeats_or_the_course_itself()
    {
        var typed = ResourceService.SplitCourseIds(" cop2071c, COP2704;COP2071C  cop4710\nBad Id! ");
        Assert.Equal("COP2071C, COP2704", ResourceService.JoinSuggestedCourses(typed, "COP4710"));
        Assert.Null(ResourceService.JoinSuggestedCourses([], "COP4710"));
        Assert.Equal(["COP2071C", "eel3111"], ResourceService.SplitCourseIds("COP 2071C, eel 3111"));
        Assert.Null(ResourceService.JoinSuggestedCourses(null, "COP4710"));
    }

    [Fact]
    public void The_suggestion_is_checked_for_length_and_course_numbers()
    {
        var v = new SubmitResourceRequestValidator();
        Assert.True(v.Validate(new SubmitResourceRequest("https://example.edu/sql", null, "SQL", "A short page on the WHERE clause.", ["COP2071C", "eel 3111"])).IsValid);
        Assert.False(v.Validate(new SubmitResourceRequest("https://example.edu/sql", null, new string('x', 201))).IsValid);
        Assert.False(v.Validate(new SubmitResourceRequest("https://example.edu/sql", null, null, new string('x', 2001))).IsValid);
        Assert.False(v.Validate(new SubmitResourceRequest("https://example.edu/sql", null, null, "Great site")).IsValid);
        Assert.False(v.Validate(new SubmitResourceRequest("https://example.edu/sql", null, null, null, ["<script>"])).IsValid);
        Assert.False(v.Validate(new SubmitResourceRequest("https://example.edu/sql", null, null, null,
            Enumerable.Range(0, 11).Select(i => $"COP{2000 + i}").ToList())).IsValid);
    }

    [Fact]
    public async Task A_submitted_suggestion_reaches_the_review_queue()
    {
        using var conn = new SqliteConnection("DataSource=:memory:");
        conn.Open();
        var options = new DbContextOptionsBuilder<AppDbContext>().UseSqlite(conn).Options;
        using var db = new AppDbContext(options);
        db.Database.EnsureCreated();
        db.TaxonomyNodes.Add(new TaxonomyNode { Key = "COP", Level = 3, Name = "Computer Programming" });
        db.TaxonomyCourses.Add(new TaxonomyCourse { CourseId = "COP4710", Level3Key = "COP", Title = "Database Systems", IsActive = true });
        await db.SaveChangesAsync();

        var service = new ResourceService(db, new MemoryCache(new MemoryCacheOptions()),
            MsOptions.Create(new RepositoryOptions()), MsOptions.Create(new SecurityOptions()));
        var result = await service.SubmitAsync("cop4710",
            new SubmitResourceRequest("https://example.edu/sql-where", "Free page.", "  SQL WHERE  ",
                "A short page on the WHERE clause.", ["cop2071c", "COP4710"]), "203.0.113.5", null);
        Assert.Equal(ResourceService.SubmitOutcome.Submitted, result.Outcome);

        var item = Assert.Single((await service.QueueAsync(ResourceService.QueuePending)).Items);
        Assert.Equal("SQL WHERE", item.SuggestedTitle);
        Assert.Equal("A short page on the WHERE clause.", item.SuggestedSummary);
        Assert.Equal(["COP2071C"], item.SuggestedAlsoFor);
    }
}
