using Microsoft.EntityFrameworkCore;
using PreseMakerRepo.Core.Interfaces;
using PreseMakerRepo.Infrastructure.Data;

namespace PreseMakerRepo.Infrastructure.Services;

public class EduLookupService : IEduLookupService
{
    private readonly AppDbContext _db;

    public EduLookupService(AppDbContext db) => _db = db;

    public async Task<EduLookupResult> LookupByEmailAsync(string email)
    {
        var atIndex = email.IndexOf('@');
        if (atIndex < 0)
            return new EduLookupResult(false, null, null, null);

        var domain = email[(atIndex + 1)..].ToLowerInvariant();

        var institution = await _db.EduInstitutions
            .AsNoTracking()
            .FirstOrDefaultAsync(e => e.EmailDomain == domain);

        if (institution is not null)
            return new EduLookupResult(true, institution.InstitutionName, institution.State, institution.Country);

        if (domain.EndsWith(".edu"))
            return new EduLookupResult(true, null, null, null);

        return new EduLookupResult(false, null, null, null);
    }
}
