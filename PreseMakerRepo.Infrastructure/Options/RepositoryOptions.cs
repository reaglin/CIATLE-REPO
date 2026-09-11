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
}
