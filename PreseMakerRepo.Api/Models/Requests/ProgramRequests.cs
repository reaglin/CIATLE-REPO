namespace PreseMakerRepo.Api.Models.Requests;

/// <summary>
/// A whole programme in one document. PUT /api/v1/programs/{slug} replaces it and its CIP
/// codes together, so a push is idempotent and a code dropped from the source document
/// actually stops counting schools.
/// <para>
/// ⚠ A programme carries NO school list — Ron, 2026-09-17: <i>"I am going to decouple programs
/// from schools."</i> Which Florida institutions offer it is derived from the federal award
/// table by CIP prefix at read time, so the only thing this document decides is which CIP
/// codes the programme covers.
/// </para>
/// </summary>
public record UpsertProgramRequest(
    string? Name,
    string? Description,
    string? DegreesNote,
    string? BodyHtml,
    bool? IsPublished,
    int? SortOrder,
    List<ProgramCipInput>? Cips,
    List<ProgramRelatedInput>? Related);

/// <summary>
/// A programme a student reading this one should also look at, and — the part that matters —
/// WHY. ⚠ Ron, 2026-09-19: the similarity between mechanical and aerospace engineering, or
/// between civil and its neighbours, is *"something students would not normally know when looking
/// at a career"*. The CIP tree already puts these programmes side by side; only the note can say
/// that aerospace employers hire mechanical graduates in large numbers.
/// </summary>
public record ProgramRelatedInput(
    string? Slug,
    string? Note);

/// <summary>
/// One CIP code the programme covers, matched as a PREFIX against award records — "51.38"
/// covers every 6-digit code beneath it.
/// <para>
/// ⚠⚠ Which codes a programme claims is the whole of its school list, so <see cref="Note"/>
/// carries the evidence. Nursing includes 51.39 (practical nursing) deliberately: defining it
/// as 51.38 alone finds 39 Florida institutions and misses 39 more, every one of them a
/// technical college.
/// </para>
/// </summary>
public record ProgramCipInput(
    string? CipCode,
    string? Note);
