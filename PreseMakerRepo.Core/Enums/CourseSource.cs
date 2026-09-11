namespace PreseMakerRepo.Core.Enums;

/// <summary>How a <see cref="Models.TaxonomyCourse"/> came to exist.</summary>
public enum CourseSource
{
    /// <summary>Created as a side effect of a curriculum guide push or a module publish (every course before 2026-09-11).</summary>
    Guide = 0,
    /// <summary>Created from base course data over the course catalog API, with or without a guide.</summary>
    Catalog = 1
}
