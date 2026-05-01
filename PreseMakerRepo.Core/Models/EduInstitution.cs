namespace PreseMakerRepo.Core.Models;

public class EduInstitution
{
    public string EmailDomain { get; set; } = string.Empty;    // PK — e.g. "fau.edu"
    public string InstitutionName { get; set; } = string.Empty;
    public string? State { get; set; }
    public string? Country { get; set; }
}
