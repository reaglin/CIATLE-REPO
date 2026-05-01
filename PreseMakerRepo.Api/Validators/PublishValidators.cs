using FluentValidation;
using PreseMakerRepo.Api.Models.Requests;
using PreseMakerRepo.Core.Enums;

namespace PreseMakerRepo.Api.Validators;

public class PublishModuleRequestValidator : AbstractValidator<PublishModuleRequest>
{
    public PublishModuleRequestValidator()
    {
        RuleFor(x => x.Title).NotEmpty().Length(3, 120);
        RuleFor(x => x.Description).NotEmpty().Length(10, 2000);
        RuleFor(x => x.License).NotEmpty()
            .Must(v => Enum.TryParse<LicenseType>(v, ignoreCase: true, out _))
            .WithMessage("License must be one of: CcBy40, CcBySa40, CcByNc40, CcByNcSa40.");
        RuleFor(x => x.Materials).NotNull().NotEmpty()
            .WithMessage("At least one material is required.");
        RuleForEach(x => x.Materials).SetValidator(new MaterialMetadataItemValidator());
    }
}

public class MaterialMetadataItemValidator : AbstractValidator<MaterialMetadataItem>
{
    public MaterialMetadataItemValidator()
    {
        RuleFor(x => x.Title).NotEmpty().MaximumLength(200);
        RuleFor(x => x.Type).NotEmpty()
            .Must(v => Enum.TryParse<MaterialType>(v, ignoreCase: true, out _))
            .WithMessage("Material type is not recognized.");
        RuleFor(x => x.FilePartName).NotEmpty();
        RuleFor(x => x.Description).MaximumLength(1000).When(x => x.Description is not null);
    }
}

public class UpdateModuleRequestValidator : AbstractValidator<UpdateModuleRequest>
{
    public UpdateModuleRequestValidator()
    {
        When(x => x.Title is not null, () =>
            RuleFor(x => x.Title!).Length(3, 120));
        When(x => x.Description is not null, () =>
            RuleFor(x => x.Description!).Length(10, 2000));
        When(x => x.License is not null, () =>
            RuleFor(x => x.License!).Must(v => Enum.TryParse<LicenseType>(v, ignoreCase: true, out _))
                .WithMessage("License must be one of: CcBy40, CcBySa40, CcByNc40, CcByNcSa40."));
        When(x => x.Materials is not null, () =>
            RuleForEach(x => x.Materials!).SetValidator(new MaterialMetadataItemValidator()));
    }
}

public class PublishMaterialRequestValidator : AbstractValidator<PublishMaterialRequest>
{
    public PublishMaterialRequestValidator()
    {
        RuleFor(x => x.Title).NotEmpty().MaximumLength(200);
        RuleFor(x => x.Type).NotEmpty()
            .Must(v => Enum.TryParse<MaterialType>(v, ignoreCase: true, out _))
            .WithMessage("Material type is not recognized.");
        RuleFor(x => x.License).NotEmpty()
            .Must(v => Enum.TryParse<LicenseType>(v, ignoreCase: true, out _))
            .WithMessage("License must be one of: CcBy40, CcBySa40, CcByNc40, CcByNcSa40.");
        RuleFor(x => x.Description).MaximumLength(1000).When(x => x.Description is not null);
    }
}

public class UpdateMaterialRequestValidator : AbstractValidator<UpdateMaterialRequest>
{
    public UpdateMaterialRequestValidator()
    {
        When(x => x.Title is not null, () =>
            RuleFor(x => x.Title!).NotEmpty().MaximumLength(200));
        When(x => x.Type is not null, () =>
            RuleFor(x => x.Type!).Must(v => Enum.TryParse<MaterialType>(v, ignoreCase: true, out _))
                .WithMessage("Material type is not recognized."));
        When(x => x.License is not null, () =>
            RuleFor(x => x.License!).Must(v => Enum.TryParse<LicenseType>(v, ignoreCase: true, out _))
                .WithMessage("License must be one of: CcBy40, CcBySa40, CcByNc40, CcByNcSa40."));
    }
}

public class ReportRequestValidator : AbstractValidator<ReportRequest>
{
    public ReportRequestValidator()
    {
        RuleFor(x => x.Reason).MaximumLength(500).When(x => x.Reason is not null);
    }
}
