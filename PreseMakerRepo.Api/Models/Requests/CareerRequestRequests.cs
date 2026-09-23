namespace PreseMakerRepo.Api.Models.Requests;

/// <summary>
/// POST /api/v1/career-requests — ask for a career path. <see cref="SocCode"/> names the
/// occupation (e.g. "19-3051"); <see cref="CipCode"/> is the 4-digit CIP group it is listed
/// under (e.g. "04.03"). <see cref="Reason"/> is optional.
/// </summary>
public record CreateCareerRequestRequest(string? SocCode, string? CipCode, string? Reason);

/// <summary>PATCH /api/v1/career-requests/{socCode}/status — admin triage.</summary>
public record SetCareerRequestStatusRequest(string? Status, string? Notes);

/// <summary>PATCH /api/v1/cip/{code}/occupations/{socCode} — hide or show one crosswalk pairing.</summary>
public record SetOccupationHiddenRequest(bool IsHidden);
