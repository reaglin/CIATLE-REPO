namespace PreseMakerRepo.Api.Models;

public static class ErrorCodes
{
    public const string ValidationError = "VALIDATION_ERROR";
    public const string QueryTooShort = "QUERY_TOO_SHORT";
    public const string InvalidToken = "INVALID_TOKEN";
    public const string Unauthorized = "UNAUTHORIZED";
    public const string InvalidCredentials = "INVALID_CREDENTIALS";
    public const string InvalidRefreshToken = "INVALID_REFRESH_TOKEN";
    public const string RefreshTokenExpired = "REFRESH_TOKEN_EXPIRED";
    public const string Forbidden = "FORBIDDEN";
    public const string EmailNotConfirmed = "EMAIL_NOT_CONFIRMED";
    public const string AccountSuspended = "ACCOUNT_SUSPENDED";
    public const string EmailAlreadyConfirmed = "EMAIL_ALREADY_CONFIRMED";
    public const string CourseNotFound = "COURSE_NOT_FOUND";
    public const string ModuleNotFound = "MODULE_NOT_FOUND";
    public const string MaterialNotFound = "MATERIAL_NOT_FOUND";
    public const string TaxonomyNodeNotFound = "TAXONOMY_NODE_NOT_FOUND";
    public const string UsernameTaken = "USERNAME_TAKEN";
    public const string EmailTaken = "EMAIL_TAKEN";
    public const string SubmissionTooLarge = "SUBMISSION_TOO_LARGE";
    public const string MaterialTooLarge = "MATERIAL_TOO_LARGE";
    public const string InvalidCourseId = "INVALID_COURSE_ID";
    public const string InvalidModuleId = "INVALID_MODULE_ID";
    public const string InvalidMaterialType = "INVALID_MATERIAL_TYPE";
    public const string GuideNotFound = "GUIDE_NOT_FOUND";
    public const string TaxonomyPlacementRequired = "TAXONOMY_PLACEMENT_REQUIRED";
    public const string GuideTemplateNotFound = "GUIDE_TEMPLATE_NOT_FOUND";
    public const string RateLimitExceeded = "RATE_LIMIT_EXCEEDED";
    public const string InternalServerError = "INTERNAL_SERVER_ERROR";
    public const string ContributorNotFound = "CONTRIBUTOR_NOT_FOUND";
}
