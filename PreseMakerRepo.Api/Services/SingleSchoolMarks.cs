namespace PreseMakerRepo.Api.Services;

/// <summary>
/// When "offered at 1 school" gets the asterisk that links to <see cref="GuideRequestService.SingleSchoolNote"/>
/// (plan 15.1): one school, and no guide yet (once a guide exists the note no longer applies).
/// </summary>
public static class SingleSchoolMarks
{
    public static bool Applies(int offeringCount, bool hasGuide) => offeringCount == 1 && !hasGuide;
}
