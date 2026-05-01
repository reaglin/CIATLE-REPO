namespace PreseMakerRepo.Core.Interfaces;

public interface IStorageService
{
    Task<string> SaveMaterialAsync(
        Guid moduleId,
        Guid materialId,
        string originalFileName,
        Stream content,
        CancellationToken ct = default);

    Task<Stream> ReadMaterialAsync(
        string storagePath,
        CancellationToken ct = default);

    Task<Stream> BuildModuleZipAsync(
        Guid moduleId,
        CancellationToken ct = default);

    Task<Stream> BuildCourseZipAsync(
        string courseId,
        CancellationToken ct = default);

    Task DeleteModuleAsync(
        Guid moduleId,
        CancellationToken ct = default);

    Task DeleteMaterialAsync(
        string storagePath,
        CancellationToken ct = default);
}
