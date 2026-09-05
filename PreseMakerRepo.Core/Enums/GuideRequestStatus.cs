namespace PreseMakerRepo.Core.Enums;

/// <summary>Lifecycle of a visitor's request for a curriculum guide.</summary>
public enum GuideRequestStatus
{
    /// <summary>Received; not yet picked up by the content pipeline.</summary>
    Open = 0,
    /// <summary>Added to the generation queue (Tools/queue.csv).</summary>
    Queued = 1,
    /// <summary>The guide has been published.</summary>
    Published = 2,
    /// <summary>Will not be produced (not a real course, out of scope, duplicate…).</summary>
    Declined = 3
}
