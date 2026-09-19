using FluentValidation;
using PreseMakerRepo.Api.Models.Requests;

namespace PreseMakerRepo.Api.Validators;

public class UpsertProgramRequestValidator : AbstractValidator<UpsertProgramRequest>
{
    public const int MaxCipsPerProgram = 40;
    public const int MaxRelatedPerProgram = 20;

    public UpsertProgramRequestValidator()
    {
        RuleFor(x => x.Name).NotEmpty().MaximumLength(200);
        RuleFor(x => x.Description).NotEmpty().MaximumLength(2000);
        RuleFor(x => x.DegreesNote).MaximumLength(2000).When(x => x.DegreesNote is not null);

        // ⚠ A programme with no CIP code claims no schools, and the page would say a real
        // programme is offered nowhere. Refuse it rather than publish that.
        RuleFor(x => x.Cips).NotEmpty()
            .WithMessage("A programme needs at least one CIP code — it is what finds the schools.");
        RuleFor(x => x.Cips!.Count).LessThanOrEqualTo(MaxCipsPerProgram)
            .When(x => x.Cips is not null).WithName("cips");

        RuleFor(x => x.Related!.Count).LessThanOrEqualTo(MaxRelatedPerProgram)
            .When(x => x.Related is not null).WithName("related");

        RuleForEach(x => x.Cips).SetValidator(new ProgramCipInputValidator());
        RuleForEach(x => x.Related).SetValidator(new ProgramRelatedInputValidator());
    }
}

public class ProgramRelatedInputValidator : AbstractValidator<ProgramRelatedInput>
{
    public ProgramRelatedInputValidator()
    {
        RuleFor(x => x.Slug).NotEmpty().Matches(@"^[a-z0-9]+(-[a-z0-9]+)*$")
            .WithMessage("Each related programme is named by its slug, e.g. mechanical-engineering.");
        // ⚠ Required, unlike a CIP note: a bare link says "these are near each other", which the
        // reader can already see. The note is the thing they cannot know.
        RuleFor(x => x.Note).NotEmpty().MaximumLength(500)
            .WithMessage("Say WHY a student reading this programme should look at that one.");
    }
}

public class ProgramCipInputValidator : AbstractValidator<ProgramCipInput>
{
    /// <summary>
    /// A 2-digit series ("15", "15."), a 4-digit group ("51.38") or a single 6-digit code
    /// ("14.1901").
    /// <para>
    /// ⚠⚠ The gap in the middle is deliberate. Codes are matched by <c>StartsWith</c>, so
    /// "14.1" would silently sweep in 14.10 through 14.19 — electrical engineering along with
    /// mechanical. Anything that is not a whole level of the tree is refused.
    /// </para>
    /// </summary>
    public const string CipPrefixPattern = @"^\d{2}\.?$|^\d{2}\.\d{2}$|^\d{2}\.\d{4}$";

    public ProgramCipInputValidator()
    {
        RuleFor(x => x.CipCode).NotEmpty().Matches(CipPrefixPattern)
            .WithMessage("cipCode must be a whole level: a series (15 or 15.), a group (51.38) " +
                         "or one 6-digit code (14.1901). A part-code like 14.1 would match a " +
                         "whole range of unrelated groups.");
        RuleFor(x => x.Note).MaximumLength(500).When(x => x.Note is not null);
    }
}
