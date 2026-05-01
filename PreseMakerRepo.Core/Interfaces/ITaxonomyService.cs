using PreseMakerRepo.Core.Models;

namespace PreseMakerRepo.Core.Interfaces;

public interface ITaxonomyService
{
    Task<TaxonomyTree> GetFullTreeAsync();
    Task<TaxonomyNode?> GetNodeAsync(string key);
    Task<TaxonomyCourseValidationResult> ValidateCourseIdAsync(string courseId);
    Task<TaxonomyCourse?> GetCourseAsync(string courseId);
    Task<IReadOnlyList<TaxonomyCourse>> GetCoursesByLevel3Async(string level3Key);
}

public record TaxonomyTree(IReadOnlyList<TaxonomyNodeSummary> Roots);

public record TaxonomyNodeSummary(
    string Key,
    string Name,
    int Level,
    int CourseCount,
    int ModuleCount,
    IReadOnlyList<TaxonomyNodeSummary> Children);

public record TaxonomyCourseValidationResult(
    bool IsValid,
    string CourseId,
    string? Title,
    TaxonomyPath? Path,
    string? CurriculumGuideUrl,
    string? InvalidReason);

public record TaxonomyPath(
    string? Level1Key,
    string? Level1Name,
    string? Level2Key,
    string? Level2Name,
    string? Level3Key,
    string? Level3Name);
