namespace PreseMakerRepo.Core.Interfaces;

public interface IEduLookupService
{
    Task<EduLookupResult> LookupByEmailAsync(string email);
}

public record EduLookupResult(
    bool IsEdu,
    string? InstitutionName,
    string? State,
    string? Country);
