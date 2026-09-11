using FluentValidation;
using PreseMakerRepo.Api.Models.Requests;

namespace PreseMakerRepo.Api.Validators;

public class UpsertCourseRequestValidator : AbstractValidator<UpsertCourseRequest>
{
    public const int MaxOfferingsPerCourse = 250;

    public UpsertCourseRequestValidator()
    {
        RuleFor(x => x.Title).NotEmpty().MaximumLength(300);
        RuleFor(x => x.StateTitle).MaximumLength(300).When(x => x.StateTitle is not null);
        RuleFor(x => x.CreditHours).InclusiveBetween(0, 20).When(x => x.CreditHours.HasValue);
        // Sanity guard against typos, not a course-length policy (PSAV programmes run long).
        RuleFor(x => x.ContactHours).InclusiveBetween(0, 3000).When(x => x.ContactHours.HasValue);
        RuleFor(x => x.TaxonomyKey).MaximumLength(100).When(x => x.TaxonomyKey is not null);
        RuleFor(x => x.Offerings!.Count).LessThanOrEqualTo(MaxOfferingsPerCourse)
            .When(x => x.Offerings is not null)
            .WithName("offerings");
        RuleForEach(x => x.Offerings).SetValidator(new CourseOfferingInputValidator());
    }
}

public class CourseOfferingInputValidator : AbstractValidator<CourseOfferingInput>
{
    public CourseOfferingInputValidator()
    {
        RuleFor(x => x.Institution).NotEmpty().MaximumLength(10)
            .Matches("^[A-Za-z0-9_-]+$").WithMessage("Institution must be a short code, e.g. UCF.");
        RuleFor(x => x.Title).MaximumLength(300).When(x => x.Title is not null);
        RuleFor(x => x.Credits).InclusiveBetween(0m, 99m).When(x => x.Credits.HasValue);
        RuleFor(x => x.ClockHours).InclusiveBetween(0, 3000).When(x => x.ClockHours.HasValue);
    }
}

public class UpsertInstitutionRequestValidator : AbstractValidator<UpsertInstitutionRequest>
{
    public UpsertInstitutionRequestValidator()
    {
        RuleFor(x => x.Code).NotEmpty().MaximumLength(10)
            .Matches("^[A-Za-z0-9_-]+$").WithMessage("Code must be a short institution code, e.g. UCF.");
        RuleFor(x => x.Name).MaximumLength(200).When(x => x.Name is not null);
        RuleFor(x => x.Sector).MaximumLength(40).When(x => x.Sector is not null);
        RuleFor(x => x.ScnsId).MaximumLength(20).When(x => x.ScnsId is not null);
    }
}
