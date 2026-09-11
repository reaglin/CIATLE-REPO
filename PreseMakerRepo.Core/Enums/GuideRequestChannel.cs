namespace PreseMakerRepo.Core.Enums;

/// <summary>Where a guide request came from.</summary>
public enum GuideRequestChannel
{
    /// <summary>The /request-guide form (every request before 2026-09-11 is recorded as this).</summary>
    Form = 0,
    /// <summary>The one-click Request Guide button on a course row or course page.</summary>
    Button = 1,
    /// <summary>POST /api/v1/guide-requests.</summary>
    Api = 2
}
