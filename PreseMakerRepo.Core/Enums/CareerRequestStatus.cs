namespace PreseMakerRepo.Core.Enums;

/// <summary>Lifecycle of a visitor's request for a career path.</summary>
public enum CareerRequestStatus
{
    /// <summary>Received; not yet picked up by the content session.</summary>
    Open = 0,
    /// <summary>Being researched and written.</summary>
    Queued = 1,
    /// <summary>A published path now covers the occupation.</summary>
    Published = 2,
    /// <summary>Will not be written (out of scope, covered elsewhere, not a Florida career…).</summary>
    Declined = 3
}
