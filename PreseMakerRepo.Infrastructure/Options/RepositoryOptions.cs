namespace PreseMakerRepo.Infrastructure.Options;

public class RepositoryOptions
{
    public int RecentModulesDefaultCount { get; set; } = 10;
    public int DefaultPageSize { get; set; } = 20;
    public int MaxPageSize { get; set; } = 100;
    public int ReportRateLimitPerHour { get; set; } = 5;
}
