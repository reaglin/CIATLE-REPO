namespace PreseMakerRepo.Api.Helpers;

/// <summary>The "N courses · M guides" line used on every browse card and header.</summary>
public static class CountText
{
    public static string Courses(int courses, int guides, int modules = 0)
    {
        var text = $"{courses:N0} course{(courses == 1 ? "" : "s")} · {guides:N0} guide{(guides == 1 ? "" : "s")}";
        if (modules > 0) text += $" · {modules:N0} module{(modules == 1 ? "" : "s")}";
        return text;
    }
}
