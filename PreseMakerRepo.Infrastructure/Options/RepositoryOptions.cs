namespace PreseMakerRepo.Infrastructure.Options;

public class RepositoryOptions
{
    public int RecentModulesDefaultCount { get; set; } = 10;
    public int DefaultPageSize { get; set; } = 20;
    public int MaxPageSize { get; set; } = 100;
    public int ReportRateLimitPerHour { get; set; } = 5;

    /// <summary>Curriculum-guide requests accepted per requester IP per hour.</summary>
    public int GuideRequestRateLimitPerHour { get; set; } = 5;

    /// <summary>One-click Request Guide button presses accepted per requester IP per hour — higher than the
    /// form limit, because working down a subject page is several clicks.</summary>
    public int GuideRequestButtonRateLimitPerHour { get; set; } = 20;

    /// <summary>One-click career-path Request presses accepted per BROWSER per hour.</summary>
    public int CareerRequestRateLimitPerHour { get; set; } = 20;

    /// <summary>Career-path requests accepted per NETWORK (IP) per hour, across all its browsers -- high
    /// enough for a classroom sharing one school address, low enough to blunt cookie-clearing.</summary>
    public int CareerRequestNetworkRateLimitPerHour { get; set; } = 100;

    /// <summary>Resource suggestions accepted per requester IP per hour.</summary>
    public int ResourceSubmissionRateLimitPerHour { get; set; } = 10;

    /// <summary>Thumbs-up votes accepted per visitor IP per hour — high enough to rate a page of resources,
    /// low enough to blunt a script.</summary>
    public int ResourceVoteRateLimitPerHour { get; set; } = 60;
}
