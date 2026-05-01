namespace PreseMakerRepo.Api.Models.Responses;

public record LoginResponse(
    string AccessToken,
    string RefreshToken,
    DateTime ExpiresAt,
    ContributorInfo Contributor);

public record ContributorInfo(
    string Id,
    string Username,
    string? DisplayName,
    string? InstitutionName,
    bool IsEduVerified);

public record MessageResponse(string Message);

public record RegisterResponse(
    string Message,
    bool IsEduVerified,
    string? InstitutionName);
