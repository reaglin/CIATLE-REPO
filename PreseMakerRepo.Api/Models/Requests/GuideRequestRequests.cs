namespace PreseMakerRepo.Api.Models.Requests;

/// <summary>POST /api/v1/guide-requests — a visitor asks for a curriculum guide.</summary>
public sealed record CreateGuideRequestRequest(
    string CourseId,
    string CourseTitle,
    string Institution,
    string? Reason,
    string? Email);

/// <summary>PATCH /api/v1/guide-requests/{courseId}/status — admin triage.</summary>
public sealed record SetGuideRequestStatusRequest(string Status, string? Notes);
