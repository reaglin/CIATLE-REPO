namespace PreseMakerRepo.Core.Models;

/// <summary>
/// An occupation the federal CIP–SOC crosswalk maps to a CIP group — what a reader can ask a
/// career path to be written for. Seeded from <c>cip_soc.json</c>, built by
/// <c>Tools/build_cip_soc_seed.py</c> from the NCES CIP 2020 / SOC 2018 crosswalk and rolled up
/// from 6-digit programmes to the 4-digit groups the browse tree shows.
/// <para>
/// ⚠ The crosswalk is broad by design — it lists every occupation a programme can plausibly
/// lead to — so some pairings read oddly on a page. <see cref="IsHidden"/> is the admin's way to
/// take one off the list without deleting it; the seed never touches that flag.
/// </para>
/// </summary>
public class CipOccupation
{
    /// <summary>The 4-digit CIP group, e.g. "04.03". Part of the key; references <see cref="CipNode"/>.</summary>
    public string CipCode { get; set; } = string.Empty;

    /// <summary>SOC 2018 code, e.g. "19-3051". Part of the key.</summary>
    public string SocCode { get; set; } = string.Empty;

    /// <summary>The SOC 2018 title, verbatim from the federal file.</summary>
    public string SocTitle { get; set; } = string.Empty;

    /// <summary>Hidden from the area page and not requestable. Admin-controlled; the seed preserves it.</summary>
    public bool IsHidden { get; set; }

    public DateTime UpdatedUtc { get; set; } = DateTime.UtcNow;

    public CipNode? Cip { get; set; }
}
