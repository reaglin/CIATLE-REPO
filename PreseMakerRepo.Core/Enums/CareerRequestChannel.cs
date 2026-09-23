namespace PreseMakerRepo.Core.Enums;

/// <summary>Where a career-path request came from.</summary>
public enum CareerRequestChannel
{
    /// <summary>The one-click Request button on a CIP area page.</summary>
    Button = 0,
    /// <summary>POST /api/v1/career-requests.</summary>
    Api = 1
}
