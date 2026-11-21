namespace PreseMakerRepo.Core.Models;

/// <summary>
/// Clicks on the home page's program panel (plan 10.4): one row per day (Florida time), program and link.
/// No visitor is recorded here; the same rules as the visitor counter decide what is counted.
/// </summary>
public class ProgramPanelClick
{
    public DateOnly Day { get; set; }

    /// <summary>The program's id in SoftwarePlus.ai's apps.json, e.g. "gamify".</summary>
    public string ProgramId { get; set; } = string.Empty;

    /// <summary>"page" (its SoftwarePlus.ai page) or "store" (the Microsoft Store).</summary>
    public string Link { get; set; } = string.Empty;

    public int Clicks { get; set; }
}
