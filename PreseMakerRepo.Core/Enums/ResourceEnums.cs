namespace PreseMakerRepo.Core.Enums;

/// <summary>What a course resource is. Extensible — new types need a URL parser and a display.</summary>
public enum ResourceType
{
    Website = 0,
    YouTube = 1
}

/// <summary>A listed resource, or one taken down (hidden everywhere, kept for the record).</summary>
public enum ResourceStatus
{
    Active = 0,
    Removed = 1
}

/// <summary>A visitor's suggested link, waiting for or past review.</summary>
public enum ResourceSubmissionStatus
{
    Pending = 0,
    Approved = 1,
    Rejected = 2
}

/// <summary>How a resource came to be listed for a course.</summary>
public enum ResourceLinkSource
{
    /// <summary>The course the visitor suggested the link for.</summary>
    Submitted = 0,
    /// <summary>Added by the reviewer (the AI session or an admin) — another course the resource suits, or a resource the reviewer found.</summary>
    Reviewer = 1
}
