using FluentValidation;
using PreseMakerRepo.Api.Models.Requests;
using PreseMakerRepo.Api.Services;

namespace PreseMakerRepo.Api.Validators;

public class CreateGuideRequestRequestValidator : AbstractValidator<CreateGuideRequestRequest>
{
    public CreateGuideRequestRequestValidator()
    {
        RuleFor(x => x.CourseId)
            .NotEmpty().WithMessage("Enter the course number (e.g. EET2325C).")
            .Must(id => GuideRequestService.TryNormalizeCourseId(id, out _))
            .WithMessage("Course number must be an SCNS code: three letters and four digits, optionally followed by C or L (e.g. ENC1101, EET2325C).");
        // Title and school are required only for a course that is not listed — the service decides that,
        // because only it knows whether the course is listed.
        RuleFor(x => x.CourseTitle!)
            .MinimumLength(3).WithMessage("The course title must be at least 3 characters.")
            .MaximumLength(200)
            .When(x => !string.IsNullOrWhiteSpace(x.CourseTitle));
        RuleFor(x => x.Institution!)
            .MinimumLength(2).WithMessage("The school name must be at least 2 characters.")
            .MaximumLength(200)
            .When(x => !string.IsNullOrWhiteSpace(x.Institution));
        RuleFor(x => x.Reason).MaximumLength(1000);
    }
}

public class SetGuideRequestStatusRequestValidator : AbstractValidator<SetGuideRequestStatusRequest>
{
    public SetGuideRequestStatusRequestValidator()
    {
        RuleFor(x => x.Status)
            .NotEmpty()
            .Must(s => Enum.TryParse<PreseMakerRepo.Core.Enums.GuideRequestStatus>(s, true, out _))
            .WithMessage("Status must be one of: Open, Queued, Published, Declined.");
        RuleFor(x => x.Notes).MaximumLength(1000);
    }
}
