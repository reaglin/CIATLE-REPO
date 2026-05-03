namespace PreseMakerRepo.Core.Models;

public class RepoGuideTemplate
{
    public int Id { get; set; } = 1;   // singleton row
    public string WorkingTitle { get; set; } = string.Empty;
    public string Prompt { get; set; } = string.Empty;
    public DateTime UpdatedUtc { get; set; }
}
