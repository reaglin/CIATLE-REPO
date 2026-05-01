namespace PreseMakerRepo.Core.Constants;

public static class WellKnownIds
{
    public const string OrphanCourseId = "_ORPHAN_COURSE";

    // Fixed GUID for the orphan module — seeded once; never changes across deployments
    public static readonly Guid OrphanModuleId = new("00000000-0000-0000-0000-000000000001");
}
