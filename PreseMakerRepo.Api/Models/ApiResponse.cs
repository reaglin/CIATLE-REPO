namespace PreseMakerRepo.Api.Models;

public sealed record ApiResponse<T>(bool Success, T? Data, ApiError? Error)
{
    public static ApiResponse<T> Ok(T data) => new(true, data, null);
    public static ApiResponse<T> Fail(string code, string message) => new(false, default, new ApiError(code, message));
    public static ApiResponse<T> Fail(string code, string message, IReadOnlyList<FieldError>? details) =>
        new(false, default, new ApiError(code, message, details));
}

public static class ApiResponse
{
    public static ApiResponse<object?> Ok() => new(true, null, null);
    public static ApiResponse<object?> Fail(string code, string message) => new(false, null, new ApiError(code, message));
}

public sealed record ApiError(string Code, string Message, IReadOnlyList<FieldError>? Details = null);

public sealed record FieldError(string Field, string Message);
