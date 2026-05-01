namespace PreseMakerRepo.Core.Enums;

public enum ContentStatus
{
    Published = 1,
    Flagged   = 2,  // Flagged by report; still publicly visible
    Removed   = 3   // Removed by admin; not publicly visible
}
