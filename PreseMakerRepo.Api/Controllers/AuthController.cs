using FluentValidation;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using PreseMakerRepo.Api.Models;
using PreseMakerRepo.Api.Models.Requests;
using PreseMakerRepo.Api.Models.Responses;
using PreseMakerRepo.Api.Services;
using PreseMakerRepo.Core.Interfaces;
using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Api.Controllers;

[ApiController]
[Route("api/v1/auth")]
public class AuthController : ControllerBase
{
    private readonly UserManager<Contributor> _userManager;
    private readonly IRefreshTokenService _refreshTokens;
    private readonly JwtService _jwt;
    private readonly IEmailService _email;
    private readonly IEduLookupService _eduLookup;

    public AuthController(
        UserManager<Contributor> userManager,
        IRefreshTokenService refreshTokens,
        JwtService jwt,
        IEmailService email,
        IEduLookupService eduLookup)
    {
        _userManager = userManager;
        _refreshTokens = refreshTokens;
        _jwt = jwt;
        _email = email;
        _eduLookup = eduLookup;
    }

    // POST /api/v1/auth/register
    [HttpPost("register")]
    public async Task<IActionResult> Register(
        [FromBody] RegisterRequest request,
        [FromServices] IValidator<RegisterRequest> validator)
    {
        var validation = await validator.ValidateAsync(request);
        if (!validation.IsValid)
            return BadRequest(ValidationError(validation));

        if (await _userManager.FindByNameAsync(request.Username) is not null)
            return Conflict(ApiResponse<object?>.Fail(ErrorCodes.UsernameTaken, "Username is already taken."));

        if (await _userManager.FindByEmailAsync(request.Email) is not null)
            return Conflict(ApiResponse<object?>.Fail(ErrorCodes.EmailTaken, "Email is already registered."));

        var edu = await _eduLookup.LookupByEmailAsync(request.Email);

        var user = new Contributor
        {
            UserName = request.Username,
            Email = request.Email,
            DisplayName = request.Username,
            IsEduVerified = edu.IsEdu,
            InstitutionName = edu.InstitutionName,
            RegisteredUtc = DateTime.UtcNow
        };

        var result = await _userManager.CreateAsync(user, request.Password);
        if (!result.Succeeded)
            return BadRequest(ValidationError(result.Errors));

        await _userManager.AddToRoleAsync(user, "Contributor");

        var token = await _userManager.GenerateEmailConfirmationTokenAsync(user);
        var link = Url.Action(
            nameof(ConfirmEmail),
            "Auth",
            new { userId = user.Id, token },
            Request.Scheme,
            Request.Host.ToUriComponent())!;

        await _email.SendConfirmationEmailAsync(user.Email!, user.UserName!, link);

        return Ok(ApiResponse<RegisterResponse>.Ok(new RegisterResponse(
            "Registration successful. Please check your email to confirm your account.",
            edu.IsEdu,
            edu.InstitutionName)));
    }

    // GET /api/v1/auth/confirm-email
    [HttpGet("confirm-email")]
    public async Task<IActionResult> ConfirmEmail([FromQuery] string userId, [FromQuery] string token)
    {
        var user = await _userManager.FindByIdAsync(userId);
        if (user is null)
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.InvalidToken, "Invalid or expired confirmation token."));

        if (user.EmailConfirmed)
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.EmailAlreadyConfirmed, "Email has already been confirmed."));

        var result = await _userManager.ConfirmEmailAsync(user, token);
        if (!result.Succeeded)
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.InvalidToken, "Invalid or expired confirmation token."));

        return Ok(ApiResponse<MessageResponse>.Ok(new MessageResponse("Email confirmed.")));
    }

    // POST /api/v1/auth/login
    [HttpPost("login")]
    public async Task<IActionResult> Login(
        [FromBody] LoginRequest request,
        [FromServices] IValidator<LoginRequest> validator)
    {
        var validation = await validator.ValidateAsync(request);
        if (!validation.IsValid)
            return BadRequest(ValidationError(validation));

        var user = await _userManager.FindByEmailAsync(request.Email);
        if (user is null || !await _userManager.CheckPasswordAsync(user, request.Password))
            return Unauthorized(ApiResponse<object?>.Fail(ErrorCodes.InvalidCredentials, "Email or password is incorrect."));

        if (user.IsSuspended)
            return StatusCode(403, ApiResponse<object?>.Fail(ErrorCodes.AccountSuspended, "This account has been suspended."));

        if (!user.EmailConfirmed)
            return StatusCode(403, ApiResponse<object?>.Fail(ErrorCodes.EmailNotConfirmed, "Please confirm your email before logging in."));

        return Ok(await BuildLoginResponseAsync(user));
    }

    // POST /api/v1/auth/refresh
    [HttpPost("refresh")]
    public async Task<IActionResult> Refresh(
        [FromBody] RefreshTokenRequest request,
        [FromServices] IValidator<RefreshTokenRequest> validator)
    {
        var validation = await validator.ValidateAsync(request);
        if (!validation.IsValid)
            return BadRequest(ValidationError(validation));

        var found = await _refreshTokens.FindAsync(request.RefreshToken);
        if (found is null || found.IsRevoked)
            return Unauthorized(ApiResponse<object?>.Fail(ErrorCodes.InvalidRefreshToken, "Refresh token is invalid."));

        if (found.ExpiresUtc <= DateTime.UtcNow)
            return Unauthorized(ApiResponse<object?>.Fail(ErrorCodes.RefreshTokenExpired, "Refresh token has expired."));

        var user = await _userManager.FindByIdAsync(found.ContributorId);
        if (user is null)
            return Unauthorized(ApiResponse<object?>.Fail(ErrorCodes.InvalidRefreshToken, "Refresh token is invalid."));

        await _refreshTokens.RevokeAsync(request.RefreshToken);
        return Ok(await BuildLoginResponseAsync(user));
    }

    // POST /api/v1/auth/logout
    [Authorize]
    [HttpPost("logout")]
    public async Task<IActionResult> Logout([FromBody] RefreshTokenRequest request)
    {
        await _refreshTokens.RevokeAsync(request.RefreshToken);
        return Ok(ApiResponse<MessageResponse>.Ok(new MessageResponse("Logged out.")));
    }

    // POST /api/v1/auth/password-reset/request
    [HttpPost("password-reset/request")]
    public async Task<IActionResult> PasswordResetRequest(
        [FromBody] PasswordResetRequestDto request,
        [FromServices] IValidator<PasswordResetRequestDto> validator)
    {
        var validation = await validator.ValidateAsync(request);
        if (!validation.IsValid)
            return BadRequest(ValidationError(validation));

        var user = await _userManager.FindByEmailAsync(request.Email);
        if (user is not null)
        {
            var token = await _userManager.GeneratePasswordResetTokenAsync(user);
            var link = Url.Action(
                "PasswordResetConfirm",
                "Auth",
                new { userId = user.Id, token },
                Request.Scheme,
                Request.Host.ToUriComponent())!;
            await _email.SendPasswordResetEmailAsync(user.Email!, user.UserName!, link);
        }

        return Ok(ApiResponse<MessageResponse>.Ok(
            new MessageResponse("If an account exists for that address, a reset link has been sent.")));
    }

    // POST /api/v1/auth/password-reset/confirm
    [HttpPost("password-reset/confirm")]
    public async Task<IActionResult> PasswordResetConfirm(
        [FromBody] PasswordResetConfirmDto request,
        [FromServices] IValidator<PasswordResetConfirmDto> validator)
    {
        var validation = await validator.ValidateAsync(request);
        if (!validation.IsValid)
            return BadRequest(ValidationError(validation));

        var user = await _userManager.FindByIdAsync(request.UserId);
        if (user is null)
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.InvalidToken, "Invalid or expired reset token."));

        var result = await _userManager.ResetPasswordAsync(user, request.Token, request.NewPassword);
        if (!result.Succeeded)
            return BadRequest(ApiResponse<object?>.Fail(ErrorCodes.InvalidToken, "Invalid or expired reset token."));

        await _refreshTokens.RevokeAllForUserAsync(user.Id);

        return Ok(ApiResponse<MessageResponse>.Ok(new MessageResponse("Password reset successful.")));
    }

    private async Task<ApiResponse<LoginResponse>> BuildLoginResponseAsync(Contributor user)
    {
        var roles = await _userManager.GetRolesAsync(user);
        var (accessToken, expiresAt) = _jwt.GenerateAccessToken(user, roles);
        var ip = HttpContext.Connection.RemoteIpAddress?.ToString();
        var refreshToken = await _refreshTokens.CreateAsync(user.Id, ip);
        var rawToken = refreshToken.ReplacedByTokenId!;
        refreshToken.ReplacedByTokenId = null;

        return ApiResponse<LoginResponse>.Ok(new LoginResponse(
            accessToken,
            rawToken,
            expiresAt,
            new ContributorInfo(user.Id, user.UserName!, user.DisplayName, user.InstitutionName, user.IsEduVerified)));
    }

    private static ApiResponse<object?> ValidationError(FluentValidation.Results.ValidationResult result)
    {
        var details = result.Errors
            .Select(e => new FieldError(e.PropertyName, e.ErrorMessage))
            .ToList();
        return ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "One or more validation errors occurred.", details);
    }

    private static ApiResponse<object?> ValidationError(IEnumerable<IdentityError> errors)
    {
        var details = errors
            .Select(e => new FieldError("", e.Description))
            .ToList();
        return ApiResponse<object?>.Fail(ErrorCodes.ValidationError, "One or more validation errors occurred.", details);
    }
}
