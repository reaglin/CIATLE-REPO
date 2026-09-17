using FluentValidation;
using PreseMakerRepo.Api.Models.Requests;

namespace PreseMakerRepo.Api.Validators;

public class UpsertCareerPathRequestValidator : AbstractValidator<UpsertCareerPathRequest>
{
    public const int MaxCoursesPerPath = 120;
    public const int MaxSourcesPerPath = 40;

    public UpsertCareerPathRequestValidator()
    {
        RuleFor(x => x.Name).NotEmpty().MaximumLength(200);
        // A path is filed on a 4-digit CIP group. The controller checks the code exists;
        // this only rejects a shape that cannot be one.
        RuleFor(x => x.CipCode).NotEmpty().Matches(@"^\d{2}\.\d{2}$")
            .WithMessage("cipCode must be a 4-digit CIP group, e.g. 51.38.");
        RuleFor(x => x.Description).NotEmpty().MaximumLength(2000);
        RuleFor(x => x.SocCode).Matches(@"^\d{2}-\d{4}$")
            .When(x => !string.IsNullOrWhiteSpace(x.SocCode))
            .WithMessage("socCode must look like 29-1141, or be omitted.");
        RuleFor(x => x.CredentialNote).MaximumLength(2000).When(x => x.CredentialNote is not null);

        RuleFor(x => x.Courses!.Count).LessThanOrEqualTo(MaxCoursesPerPath)
            .When(x => x.Courses is not null).WithName("courses");
        RuleFor(x => x.Sources!.Count).LessThanOrEqualTo(MaxSourcesPerPath)
            .When(x => x.Sources is not null).WithName("sources");

        RuleForEach(x => x.Courses).SetValidator(new CareerPathCourseInputValidator());
        RuleForEach(x => x.Sources).SetValidator(new CareerPathSourceInputValidator());
    }
}

public class CareerPathCourseInputValidator : AbstractValidator<CareerPathCourseInput>
{
    public CareerPathCourseInputValidator()
    {
        // Same id grammar as the course catalog, including the -SCNS / -<INST> split
        // that exists because one SCNS number can carry two different subjects.
        RuleFor(x => x.CourseId).NotEmpty()
            .Matches(@"^[A-Z]{3}\d{4}[A-Z]?(-(SCNS|[A-Z]{2,5}))?$")
            .WithMessage("courseId must be an SCNS id, e.g. NUR3125 or NUR4286-UWF.");
        // ⚠ Required by design: a course with no stated reason is a course nobody justified.
        RuleFor(x => x.Reason).NotEmpty().MaximumLength(500)
            .WithMessage("Every course on a path needs a reason it is there.");
        RuleFor(x => x.VariantNote).MaximumLength(1000).When(x => x.VariantNote is not null);
    }
}

public class CareerPathSourceInputValidator : AbstractValidator<CareerPathSourceInput>
{
    public CareerPathSourceInputValidator()
    {
        RuleFor(x => x.Label).NotEmpty().MaximumLength(200);
        RuleFor(x => x.Url).NotEmpty().MaximumLength(2048)
            .Must(u => Uri.TryCreate(u, UriKind.Absolute, out var uri)
                       && (uri.Scheme == Uri.UriSchemeHttp || uri.Scheme == Uri.UriSchemeHttps))
            .WithMessage("url must be an absolute http(s) URL.");
        RuleFor(x => x.Note).MaximumLength(500).When(x => x.Note is not null);
    }
}
