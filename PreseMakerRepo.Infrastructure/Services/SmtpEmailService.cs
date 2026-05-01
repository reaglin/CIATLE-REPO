using MailKit.Net.Smtp;
using MailKit.Security;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using MimeKit;
using MimeKit.Text;
using PreseMakerRepo.Core.Interfaces;
using PreseMakerRepo.Infrastructure.Options;

namespace PreseMakerRepo.Infrastructure.Services;

public class SmtpEmailService : IEmailService
{
    private readonly EmailOptions _options;
    private readonly IHostEnvironment _env;
    private readonly ILogger<SmtpEmailService> _logger;

    public SmtpEmailService(IOptions<EmailOptions> options, IHostEnvironment env, ILogger<SmtpEmailService> logger)
    {
        _options = options.Value;
        _env = env;
        _logger = logger;
    }

    public async Task SendConfirmationEmailAsync(string toEmail, string username, string confirmationLink)
    {
        var html = await RenderAsync("ConfirmEmail.html", new()
        {
            ["{{username}}"] = username,
            ["{{link}}"] = confirmationLink
        });
        await SendAsync(toEmail, "Confirm Your Email - PreseMaker Repository", html);
    }

    public async Task SendPasswordResetEmailAsync(string toEmail, string username, string resetLink)
    {
        var html = await RenderAsync("PasswordReset.html", new()
        {
            ["{{username}}"] = username,
            ["{{link}}"] = resetLink
        });
        await SendAsync(toEmail, "Reset Your Password - PreseMaker Repository", html);
    }

    public async Task SendContentRemovedEmailAsync(
        string toEmail, string username, string contentTitle, string contentType, string reason)
    {
        var html = await RenderAsync("ContentRemoved.html", new()
        {
            ["{{username}}"] = username,
            ["{{contentTitle}}"] = contentTitle,
            ["{{contentType}}"] = contentType,
            ["{{reason}}"] = reason
        });
        await SendAsync(toEmail, $"Your {contentType} Has Been Removed - PreseMaker Repository", html);
    }

    public async Task SendSuspensionEmailAsync(string toEmail, string username, string reason)
    {
        var html = await RenderAsync("AccountSuspended.html", new()
        {
            ["{{username}}"] = username,
            ["{{reason}}"] = reason
        });
        await SendAsync(toEmail, "Your Account Has Been Suspended - PreseMaker Repository", html);
    }

    public async Task SendAdminContactEmailAsync(string toEmail, string subject, string body)
    {
        var html = await RenderAsync("AdminContact.html", new()
        {
            ["{{subject}}"] = subject,
            ["{{body}}"] = body
        });
        await SendAsync(toEmail, subject, html);
    }

    private async Task<string> RenderAsync(string templateName, Dictionary<string, string> tokens)
    {
        var path = Path.Combine(_env.ContentRootPath, _options.TemplatesPath, templateName);

        if (!File.Exists(path))
        {
            _logger.LogWarning("Email template not found: {Path}. Sending plain-text fallback.", path);
            return string.Join("\n", tokens.Select(t => $"{t.Key}: {t.Value}"));
        }

        var html = await File.ReadAllTextAsync(path);
        foreach (var (token, value) in tokens)
            html = html.Replace(token, value);

        return html;
    }

    private async Task SendAsync(string toEmail, string subject, string htmlBody)
    {
        try
        {
            var message = new MimeMessage();
            message.From.Add(new MailboxAddress(_options.FromDisplayName, _options.FromAddress));
            message.To.Add(MailboxAddress.Parse(toEmail));
            message.Subject = subject;
            message.Body = new TextPart(TextFormat.Html) { Text = htmlBody };

            using var client = new SmtpClient();
            var secureSocket = _options.SmtpUseSsl
                ? SecureSocketOptions.StartTls
                : SecureSocketOptions.None;

            await client.ConnectAsync(_options.SmtpHost, _options.SmtpPort, secureSocket);
            await client.AuthenticateAsync(_options.SmtpUsername, _options.SmtpPassword);
            await client.SendAsync(message);
            await client.DisconnectAsync(true);
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "Failed to send email to {Email} with subject '{Subject}'", toEmail, subject);
        }
    }
}
