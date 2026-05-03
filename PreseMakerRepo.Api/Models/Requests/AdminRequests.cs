namespace PreseMakerRepo.Api.Models.Requests;

public record ClearFlagRequest(string? Note);

public record AdminRemoveRequest(string Reason, bool NotifyContributor = true);

public record SuspendContributorRequest(string Reason, bool NotifyContributor = true);

public record AdminContactRequest(string Subject, string Body);

public record ConfirmEmailRequest(string Email);
