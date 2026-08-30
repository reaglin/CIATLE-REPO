# Pending server changes

Changes that need a **server redeploy** (`.\Deployment\deploy-update.ps1` from the repo
root) to take effect. Curriculum guide content does *not* belong here — guides publish over
the REST API and need no deploy.

Bundle these into the next deploy, then delete the entry.

---

## PSAV guides render "0 credit hours"

**File:** `PreseMakerRepo.Api/Pages/Browse/Guide.cshtml` (~line 27)

The credits badge renders whenever `Credits.HasValue`, and `0` *has* a value:

```cshtml
@if (Model.Guide.Credits.HasValue)
{
    <span class="badge bg-secondary">@Model.Guide.Credits credit hours</span>
}
```

PSAV (Postsecondary Adult Vocational) clock-hour courses correctly carry `credits: 0` with
the real measurement in `contact_hours`. So roughly 20+ live guides — PRN0091, BCV0640C,
EEV0752 and the rest of the PSAV set pushed 2026-08-30 — display a meaningless
`0 credit hours` badge beside a correct `450 contact hours` badge.

**Fix:** only render the badge when credits are greater than zero.

```cshtml
@if (Model.Guide.Credits > 0)
{
    <span class="badge bg-secondary">@Model.Guide.Credits credit hours</span>
}
```

`Credits` is `int?`, and in C# `null > 0` is `false`, so this covers the null case too and
the `.HasValue` check is redundant.

**Consider alongside it:** a PSAV guide then shows only a contact-hours badge with no
indication it is a clock-hour course. A `<span class="badge bg-info">PSAV clock-hour</span>`
badge when `Credits == 0 && ContactHours > 0` would make the distinction explicit rather
than merely absent. Optional — decide when implementing.

**Verify after deploy:** `https://floridacourserepo.com/browse/...` for PRN0091 shows
"450 contact hours" and no credit-hours badge, while a normal transfer course (ACG2021C)
still shows "3 credit hours".

*Deferred 2026-08-30 — the validator `ContactHours` cap raise deployed the same day; this was
held back to avoid a second deploy.*
