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
        RuleFor(x => x.Title).MaximumLength(200).WithMessage("Keep the suggested title under 200 characters.");
        RuleFor(x => x.Summary!).Length(20, 2000).When(x => !string.IsNullOrWhiteSpace(x.Summary))
            .WithMessage("A suggested summary needs 20 to 2,000 characters (or leave it empty).");
        RuleFor(x => x.AlsoFor!.Count).LessThanOrEqualTo(ResourceService.MaxSuggestedAlsoFor)
            .When(x => x.AlsoFor is not null)
            .WithMessage($"Suggest at most {ResourceService.MaxSuggestedAlsoFor} other courses.");
        RuleForEach(x => x.AlsoFor).Must(c => c is not null && ResourceService.CourseIdPattern.IsMatch(ResourceService.NormalizeCourseId(c)))
            .WithMessage((_, c) => $"Other courses: \"{c}\" is not a course number. Use numbers like COP2071C, separated by commas.");
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
        RuleFor(x => x.Title).NotEmpty().WithMessage("Give the listing a title.")
            .MaximumLength(200).WithMessage("Keep the title under 200 characters.");
        RuleFor(x => x.Summary).NotEmpty().MinimumLength(20).MaximumLength(2000)
            .WithMessage("Write a summary of 20 to 2,000 characters.");
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
