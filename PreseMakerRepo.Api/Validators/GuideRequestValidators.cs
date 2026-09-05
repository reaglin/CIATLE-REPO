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
        RuleFor(x => x.CourseTitle)
            .NotEmpty().WithMessage("Enter the course title.")
            .MinimumLength(3).MaximumLength(200);
        RuleFor(x => x.Institution)
            .NotEmpty().WithMessage("Enter the school where the course is offered.")
            .MinimumLength(2).MaximumLength(200);
        RuleFor(x => x.Reason).MaximumLength(1000);
        RuleFor(x => x.Email)
            .EmailAddress().When(x => !string.IsNullOrWhiteSpace(x.Email))
            .WithMessage("Enter a valid email address, or leave it blank.")
            .MaximumLength(256);
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
