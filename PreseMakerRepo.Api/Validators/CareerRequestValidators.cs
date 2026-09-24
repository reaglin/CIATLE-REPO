using FluentValidation;
using PreseMakerRepo.Api.Models.Requests;
using PreseMakerRepo.Api.Services;
using PreseMakerRepo.Core.Enums;

namespace PreseMakerRepo.Api.Validators;

public class CreateCareerRequestRequestValidator : AbstractValidator<CreateCareerRequestRequest>
{
    public CreateCareerRequestRequestValidator()
    {
        RuleFor(x => x.SocCode)
            .Must(s => CareerRequestService.TryNormalizeSoc(s, out _))
            .WithMessage("socCode must be a SOC 2018 code such as 19-3051.");
        RuleFor(x => x.CipCode)
            .Must(c => CareerRequestService.TryNormalizeCipGroup(c, out _))
            .WithMessage("cipCode must be a 4-digit CIP group such as 04.03.");
        RuleFor(x => x.Reason).MaximumLength(1000);
    }
}

public class SetCareerRequestStatusRequestValidator : AbstractValidator<SetCareerRequestStatusRequest>
{
    public SetCareerRequestStatusRequestValidator()
    {
        RuleFor(x => x.Status)
            .NotEmpty()
            .Must(s => Enum.TryParse<CareerRequestStatus>(s, true, out _))
            .WithMessage("Status must be one of: Open, Queued, Published, Declined.");
        RuleFor(x => x.Notes).MaximumLength(1000);
        RuleFor(x => x.PublicNote).MaximumLength(500);
    }
}
