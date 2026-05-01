namespace PreseMakerRepo.Infrastructure.Options;

public class StorageOptions
{
    public string RootPath { get; set; } = "/var/presemaker-repo/storage";
    public long MaxModuleSizeBytes { get; set; } = 524_288_000;    // 500 MB
    public long MaxMaterialSizeBytes { get; set; } = 209_715_200;  // 200 MB
    public long LargeZipThresholdBytes { get; set; } = 104_857_600; // 100 MB
    public int RetainRemovedFileDays { get; set; } = 30;
    // Accepted MIME types for MaterialType.Other — empty means nothing is accepted
    public string[] OtherMimeTypes { get; set; } = [];
}
