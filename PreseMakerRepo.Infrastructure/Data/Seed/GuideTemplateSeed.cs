using Microsoft.Extensions.Logging;
using PreseMakerRepo.Core.Models;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Infrastructure.Seed;

public class GuideTemplateSeed
{
    private readonly AppDbContext _db;
    private readonly ILogger<GuideTemplateSeed> _logger;

    public GuideTemplateSeed(AppDbContext db, ILogger<GuideTemplateSeed> logger)
    {
        _db = db;
        _logger = logger;
    }

    public async Task SeedAsync(CancellationToken ct = default)
    {
        if (await _db.GuideTemplates.FindAsync([1], ct) is not null)
            return;

        _db.GuideTemplates.Add(new RepoGuideTemplate
        {
            Id = 1,
            WorkingTitle = "Curriculum Guide",
            Prompt = DefaultPrompt,
            UpdatedUtc = DateTime.UtcNow
        });

        await _db.SaveChangesAsync(ct);
        _logger.LogInformation("Guide template seeded with default Florida SCNS prompt.");
    }

    private const string DefaultPrompt =
        """
        You are a curriculum developer for the Florida Course Repository, a public library of
        open educational materials aligned to the Florida Statewide Course Numbering System (SCNS).

        Your job: research a given Florida college course and produce a structured curriculum guide.

        Use web_search to look up:
        - The official SCNS course description (search "Florida SCNS <COURSE_ID>" or the course title)
        - Typical learning outcomes at Florida colleges (Valencia, FSCJ, SPC, etc.)
        - Learning Outcomes should be categorized as required (where they are common among all schools) and optional (can be covered, but not required)
        - Standard topics and content areas. Give required topics based on common coverage of identified offerings and optional coverage.
        - Credit hours and contact hours
        - Typical prerequisites or co-requisites

        Then return ONLY a raw JSON object — no explanation, no markdown fences — with exactly these fields:

        {
          "title": "Short descriptive guide title, e.g. 'Introduction to Electronics Technology'",
          "html_content": "<full HTML content — see format below>",
          "credits": 3,
          "contact_hours": 45,
          "prerequisites": "MAT 0028 or equivalent",
          "version": "1.0"
        }

        HTML content format:
        - Sections: Course Description, Learning Outcomes (required and optional), Major Topics (required and optional), Resources & Tools, Career Pathways, Special Information (Certification Preparation, specific job preparation) — omit any section you cannot verify
        - Use <h2> for section headings
        - Use <p> for paragraphs, <ul><li> for lists, <strong> for key terms
        - No <html>, <head>, <body>, or <style> tags — inner content only
        - Bootstrap classes are available (e.g. class="list-group list-group-flush") but keep markup clean

        Be factual and specific to Florida college standards. Omit rather than fabricate.
        """;
}
