namespace PreseMakerRepo.Infrastructure.Options;

public class EmailOptions
{
    public string SmtpHost { get; set; } = string.Empty;
    public int SmtpPort { get; set; } = 587;
    public bool SmtpUseSsl { get; set; } = true;
    public string SmtpUsername { get; set; } = string.Empty;
    public string SmtpPassword { get; set; } = string.Empty;
    public string FromAddress { get; set; } = string.Empty;
    public string FromDisplayName { get; set; } = "PreseMaker Repository";
    public string AdminAddress { get; set; } = string.Empty;
    public string TemplatesPath { get; set; } = "EmailTemplates";
}
