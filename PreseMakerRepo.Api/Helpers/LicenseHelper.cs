using PreseMakerRepo.Core.Enums;

namespace PreseMakerRepo.Api.Helpers;

public static class LicenseHelper
{
    private static readonly Dictionary<LicenseType, (string DisplayName, string Url)> Map = new()
    {
        [LicenseType.CcBy40]     = ("CC BY 4.0",      "https://creativecommons.org/licenses/by/4.0/"),
        [LicenseType.CcBySa40]   = ("CC BY-SA 4.0",   "https://creativecommons.org/licenses/by-sa/4.0/"),
        [LicenseType.CcByNc40]   = ("CC BY-NC 4.0",   "https://creativecommons.org/licenses/by-nc/4.0/"),
        [LicenseType.CcByNcSa40] = ("CC BY-NC-SA 4.0","https://creativecommons.org/licenses/by-nc-sa/4.0/"),
    };

    public static string DisplayName(LicenseType license) =>
        Map.TryGetValue(license, out var v) ? v.DisplayName : license.ToString();

    public static string Url(LicenseType license) =>
        Map.TryGetValue(license, out var v) ? v.Url : string.Empty;
}
