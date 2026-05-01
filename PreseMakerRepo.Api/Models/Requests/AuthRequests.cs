namespace PreseMakerRepo.Api.Models.Requests;

public record RegisterRequest(string Username, string Email, string Password);

public record LoginRequest(string Email, string Password);

public record RefreshTokenRequest(string RefreshToken);

public record PasswordResetRequestDto(string Email);

public record PasswordResetConfirmDto(string UserId, string Token, string NewPassword);
