using FluentValidation;
using PreseMakerRepo.Api.Helpers;
using PreseMakerRepo.Api.Models.Requests;
using PreseMakerRepo.Api.Services;

namespace PreseMakerRepo.Api.Validators;

public class SubmitResourceRequestValidator : AbstractValidator<SubmitResourceRequest>
{
    public SubmitResourceRequestValidator()
    {
        RuleFor(x => x.Url).NotEmpty().WithMessage("Enter the link (web address).")
            .MaximumLength(ResourceUrls.MaxLength);
        RuleFor(x => x.Description).MaximumLength(500).WithMessage("Keep the description under 500 characters.");
    }
}

public class ResourceCourseInputValidator : AbstractValidator<ResourceCourseInput>
{
    public ResourceCourseInputValidator()
    {
        RuleFor(x => x.CourseId).NotEmpty().MaximumLength(50);
        RuleFor(x => x.Title!).NotEmpty().MaximumLength(200).When(x => x.Title is not null);
        RuleFor(x => x.Summary!).MinimumLength(20).MaximumLength(2000).When(x => x.Summary is not null);
    }
}

public class ApproveResourceSubmissionRequestValidator : AbstractValidator<ApproveResourceSubmissionRequest>
{
    public ApproveResourceSubmissionRequestValidator()
    {
        RuleFor(x => x.Title).NotEmpty().MaximumLength(200);
        RuleFor(x => x.Summary).NotEmpty().MinimumLength(20).MaximumLength(2000);
        RuleFor(x => x.Note).MaximumLength(300);
        RuleFor(x => x.AlsoFor!.Count).LessThanOrEqualTo(ResourceService.MaxCoursesPerCall)
            .When(x => x.AlsoFor is not null).WithName("alsoFor");
        RuleForEach(x => x.AlsoFor).SetValidator(new ResourceCourseInputValidator());
    }
}

public class RejectResourceSubmissionRequestValidator : AbstractValidator<RejectResourceSubmissionRequest>
{
    public RejectResourceSubmissionRequestValidator()
    {
        RuleFor(x => x.Note).NotEmpty().WithMessage("Give a short reason; it is shown in the public queue.")
            .MaximumLength(300);
    }
}

public class CreateResourceRequestValidator : AbstractValidator<CreateResourceRequest>
{
    public CreateResourceRequestValidator()
    {
        RuleFor(x => x.Url).NotEmpty().MaximumLength(ResourceUrls.MaxLength);
        RuleFor(x => x.Title).NotEmpty().MaximumLength(200);
        RuleFor(x => x.Summary).NotEmpty().MinimumLength(20).MaximumLength(2000);
        RuleFor(x => x.Courses).NotEmpty().WithMessage("List at least one course.");
        RuleFor(x => x.Courses!.Count).LessThanOrEqualTo(ResourceService.MaxCoursesPerCall)
            .When(x => x.Courses is not null).WithName("courses");
        RuleForEach(x => x.Courses).SetValidator(new ResourceCourseInputValidator());
    }
}

public class UpdateResourceRequestValidator : AbstractValidator<UpdateResourceRequest>
{
    public UpdateResourceRequestValidator()
    {
        RuleFor(x => x.Title!).NotEmpty().MaximumLength(200).When(x => x.Title is not null);
        RuleFor(x => x.Summary!).MinimumLength(20).MaximumLength(2000).When(x => x.Summary is not null);
        RuleFor(x => x.Status!)
            .Must(s => s.Equals("active", StringComparison.OrdinalIgnoreCase) || s.Equals("removed", StringComparison.OrdinalIgnoreCase))
            .WithMessage("status must be active or removed.")
            .When(x => x.Status is not null);
    }
}
