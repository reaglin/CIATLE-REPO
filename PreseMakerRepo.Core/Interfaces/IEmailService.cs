namespace PreseMakerRepo.Core.Interfaces;

public interface IEmailService
{
    Task SendConfirmationEmailAsync(
        string toEmail, string username, string confirmationLink);

    Task SendPasswordResetEmailAsync(
        string toEmail, string username, string resetLink);

    Task SendContentRemovedEmailAsync(
        string toEmail, string username,
        string contentTitle, string contentType, string reason);

    Task SendSuspensionEmailAsync(
        string toEmail, string username, string reason);

    Task SendAdminContactEmailAsync(
        string toEmail, string subject, string body);
}
