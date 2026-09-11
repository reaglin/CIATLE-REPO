namespace PreseMakerRepo.Api.Models.Requests;

/// <summary>POST /api/v1/courses/{courseId}/resources — a visitor (or a vendor) suggests a link.</summary>
public sealed record SubmitResourceRequest(string? Url, string? Description);

/// <summary>A course to list a resource for. Title and summary default to the request's own; give them to
/// tailor the listing to this course.</summary>
public sealed record ResourceCourseInput(string? CourseId, string? Title, string? Summary);

/// <summary>
/// POST /api/v1/resource-submissions/{id}/approve — the reviewer lists the link for the course it was
/// suggested for, with a title and summary, and optionally for other courses (<see cref="AlsoFor"/>).
/// </summary>
public sealed record ApproveResourceSubmissionRequest(string? Title, string? Summary, string? Note, List<ResourceCourseInput>? AlsoFor);

/// <summary>POST /api/v1/resource-submissions/{id}/reject — with a short public-safe reason.</summary>
public sealed record RejectResourceSubmissionRequest(string? Note);

/// <summary>POST /api/v1/resources — list a link directly for one or more courses (a resource the reviewer found,
/// or more courses for a link already listed). An existing listing of the same link on a course is updated.</summary>
public sealed record CreateResourceRequest(string? Url, string? Title, string? Summary, List<ResourceCourseInput>? Courses);

/// <summary>PATCH /api/v1/resources/{id} — edit one course's listing, or remove ("removed") / restore ("active") it.</summary>
public sealed record UpdateResourceRequest(string? Title, string? Summary, string? Status);
