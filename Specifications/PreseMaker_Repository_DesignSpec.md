# PreseMaker Community Repository — Implementation Specification

**Status:** Active  
**Date:** April 2026  
**Implements:** PreseMaker_Repository_API_Specification.md v1.0  
**Follows:** PreseMaker_Repository_Requirements.md  
**Scope:** Phase 1 — .NET 8 / Linux VPS

---

## Table of Contents

1. [Solution Architecture](#1-solution-architecture)
2. [Technology Stack](#2-technology-stack)
3. [Solution Structure](#3-solution-structure)
4. [Data Models & Database Schema](#4-data-models--database-schema)
5. [Authentication & Authorization](#5-authentication--authorization)
6. [Taxonomy Configuration & Seeding](#6-taxonomy-configuration--seeding)
7. [File Storage Design](#7-file-storage-design)
8. [Admin API](#8-admin-api)
9. [Email Service](#9-email-service)
10. [EDU Institution Detection](#10-edu-institution-detection)
11. [Web Frontend Structure](#11-web-frontend-structure)
12. [Admin Console](#12-admin-console)
13. [Configuration Reference](#13-configuration-reference)
14. [Error Handling Standards](#14-error-handling-standards)
15. [Security Considerations](#15-security-considerations)
16. [VPS Deployment](#16-vps-deployment)
17. [Future Phase 2 Hooks](#17-future-phase-2-hooks)

---

## 1. Solution Architecture

The repository is a single-server .NET 8 application deployed on a Linux VPS. Three components share one codebase:

```
┌─────────────────────────────────────────────────────────────┐
│                        VPS (Linux)                          │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              ASP.NET Core Web Application            │   │
│  │                                                      │   │
│  │   ┌─────────────┐  ┌─────────────┐  ┌────────────┐  │   │
│  │   │  REST API   │  │  Razor Web  │  │   Admin    │  │   │
│  │   │  /api/v1/   │  │  /browse/   │  │  /admin/   │  │   │
│  │   └─────────────┘  └─────────────┘  └────────────┘  │   │
│  │                                                      │   │
│  │   ┌─────────────────────────────────────────────┐    │   │
│  │   │              Service Layer                  │    │   │
│  │   │  Auth · Module · Material · Storage         │    │   │
│  │   │  Email · Taxonomy · EduLookup               │    │   │
│  │   └─────────────────────────────────────────────┘    │   │
│  │                                                      │   │
│  │   ┌──────────────────┐   ┌──────────────────────┐    │   │
│  │   │   EF Core + DB   │   │   File System Store  │    │   │
│  │   │  (SQLite/PgSQL)  │   │  /repo-storage/...   │    │   │
│  │   └──────────────────┘   └──────────────────────┘    │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────┐                                        │
│  │   Nginx Proxy   │  TLS termination, static assets        │
│  └─────────────────┘                                        │
└─────────────────────────────────────────────────────────────┘
```

The REST API (`/api/v1/`) implements the PreseMaker Repository API Specification and is consumed by the PreseMaker desktop client and the web frontend.  
The Razor Web frontend (`/`) serves the public browse experience.  
The Admin Console (`/admin/`) is a Razor Pages area behind administrator role authorization.

All three share the same service and data layers — no duplication of business logic.

---

## 2. Technology Stack

| Concern | Choice | Notes |
|---|---|---|
| Runtime | .NET 8 | Matches PreseMaker host |
| Web Framework | ASP.NET Core 8 | Single project hosts API + Razor Pages |
| ORM | Entity Framework Core 8 | Code-first; migrations |
| Database | SQLite (initial) | Swap to PostgreSQL via config when scale warrants |
| Auth | ASP.NET Core Identity + JWT Bearer | Identity for account management; JWT for API clients |
| File Storage | Local filesystem | Abstracted behind `IStorageService`; swap to blob later |
| Email | SMTP via MailKit | Interface-abstracted; any SMTP relay |
| Reverse Proxy | Nginx | TLS via Let's Encrypt / Certbot |
| Process Host | systemd | Auto-restart on VPS |
| Logging | Serilog | File sink + console sink |
| Validation | FluentValidation | Request model validation |

---

## 3. Solution Structure

```
PreseMakerRepo.sln
│
├── src/
│   ├── PreseMakerRepo.Api/              # ASP.NET Core host project
│   │   ├── Controllers/
│   │   │   ├── AuthController.cs
│   │   │   ├── TaxonomyController.cs
│   │   │   ├── CoursesController.cs
│   │   │   ├── ModulesController.cs
│   │   │   ├── MaterialsController.cs
│   │   │   ├── SearchController.cs
│   │   │   └── AdminController.cs
│   │   ├── Areas/
│   │   │   └── Admin/
│   │   │       └── Pages/              # Razor Pages for admin console
│   │   ├── Pages/                      # Razor Pages for public web frontend
│   │   │   ├── Index.cshtml            # Home / recently added
│   │   │   ├── Browse/
│   │   │   │   ├── Index.cshtml        # Level 1 taxonomy grid
│   │   │   │   ├── Level1.cshtml       # Level 2 children
│   │   │   │   ├── Level2.cshtml       # Level 3 children
│   │   │   │   ├── Level3.cshtml       # Courses under a Level 3 node
│   │   │   │   └── Course.cshtml       # Modules for a course
│   │   │   ├── Module/
│   │   │   │   └── Detail.cshtml       # Module detail + material list
│   │   │   ├── Material/
│   │   │   │   └── Detail.cshtml       # Material detail + download
│   │   │   └── Account/
│   │   │       ├── Register.cshtml
│   │   │       ├── Login.cshtml
│   │   │       ├── Profile.cshtml
│   │   │       └── MySubmissions.cshtml
│   │   ├── Middleware/
│   │   │   ├── FileSizeLimitMiddleware.cs
│   │   │   └── RequestLoggingMiddleware.cs
│   │   ├── EmailTemplates/
│   │   ├── appsettings.json
│   │   ├── appsettings.Production.json
│   │   └── Program.cs
│   │
│   ├── PreseMakerRepo.Core/             # Domain — no infrastructure dependencies
│   │   ├── Models/
│   │   │   ├── Contributor.cs
│   │   │   ├── Module.cs
│   │   │   ├── Material.cs
│   │   │   ├── ContentFlag.cs
│   │   │   ├── TaxonomyNode.cs
│   │   │   ├── TaxonomyCourse.cs
│   │   │   └── EduInstitution.cs
│   │   ├── Enums/
│   │   │   ├── MaterialType.cs
│   │   │   ├── LicenseType.cs
│   │   │   └── ContentStatus.cs
│   │   ├── Interfaces/
│   │   │   ├── IModuleService.cs
│   │   │   ├── IMaterialService.cs
│   │   │   ├── IStorageService.cs
│   │   │   ├── IEmailService.cs
│   │   │   ├── ITaxonomyService.cs
│   │   │   └── IEduLookupService.cs
│   │   └── DTOs/
│   │       ├── Requests/
│   │       └── Responses/
│   │
│   ├── PreseMakerRepo.Infrastructure/   # EF Core, storage, email, external services
│   │   ├── Data/
│   │   │   ├── AppDbContext.cs
│   │   │   ├── Migrations/
│   │   │   └── Seed/
│   │   │       ├── TaxonomySeed.cs     # Loads taxonomy.json into DB
│   │   │       └── EduSeed.cs          # Seeded .edu domain → institution map
│   │   ├── Services/
│   │   │   ├── ModuleService.cs
│   │   │   ├── MaterialService.cs
│   │   │   ├── LocalStorageService.cs
│   │   │   ├── SmtpEmailService.cs
│   │   │   ├── TaxonomyService.cs
│   │   │   └── EduLookupService.cs
│   │   └── PreseMakerRepo.Infrastructure.csproj
│   │
│   └── PreseMakerRepo.Core/
│       └── PreseMakerRepo.Core.csproj
│
└── tests/
    ├── PreseMakerRepo.Api.Tests/
    └── PreseMakerRepo.Infrastructure.Tests/
```

---

## 4. Data Models & Database Schema

### 4.1 Contributor

Extends ASP.NET Core Identity `IdentityUser` with repository-specific fields.

```csharp
public class Contributor : IdentityUser
{
    // Inherited from IdentityUser:
    //   Id (string / GUID), UserName, Email, PasswordHash, EmailConfirmed, etc.

    public string? DisplayName { get; set; }          // Optional; falls back to UserName
    public string? InstitutionName { get; set; }      // Set on registration if .edu detected
    public bool IsEduVerified { get; set; }           // True if email domain is .edu
    public bool IsSuspended { get; set; }
    public DateTime RegisteredUtc { get; set; }
    public DateTime? SuspendedUtc { get; set; }
    public string? SuspensionReason { get; set; }

    public ICollection<Module> Modules { get; set; } = new List<Module>();
    public ICollection<Material> Materials { get; set; } = new List<Material>();
}
```

**Table:** `AspNetUsers` (extended by Identity scaffolding; extra columns via migration)

---

### 4.2 Module

```csharp
public class Module
{
    public Guid Id { get; set; }                      // PK
    public string ContributorId { get; set; }         // FK → Contributor.Id
    public Contributor Contributor { get; set; }

    public string CourseId { get; set; }              // FK → TaxonomyCourse.CourseId
    public TaxonomyCourse Course { get; set; }

    public string Title { get; set; }
    public string Description { get; set; }
    public string OutcomesJson { get; set; }          // JSON array of outcome strings
    public string TopicHierarchyJson { get; set; }   // JSON array of topic objects

    public LicenseType License { get; set; }
    public ContentStatus Status { get; set; }         // Published, Flagged, Removed

    public DateTime SubmittedUtc { get; set; }
    public DateTime? UpdatedUtc { get; set; }
    public DateTime? RemovedUtc { get; set; }

    public long TotalStorageBytes { get; set; }       // Sum of material file sizes

    public ICollection<Material> Materials { get; set; } = new List<Material>();
    public ICollection<ContentFlag> Flags { get; set; } = new List<ContentFlag>();
}
```

**Topic hierarchy JSON schema:**
```json
[
  {
    "topic": "Circuit Fundamentals",
    "elements": ["Voltage", "Current", "Resistance", "Power"]
  }
]
```

**Indexes:**
- `CourseId` (non-unique)
- `SubmittedUtc` (non-unique, DESC — supports recency queries)
- `Status` (non-unique)
- `ContributorId` (non-unique)

---

### 4.3 Material

```csharp
public class Material
{
    public Guid Id { get; set; }                      // PK
    public Guid ModuleId { get; set; }               // FK → Module.Id
    public Module Module { get; set; }

    public string ContributorId { get; set; }         // FK → Contributor.Id
    public Contributor Contributor { get; set; }

    public string Title { get; set; }
    public string? Description { get; set; }
    public MaterialType Type { get; set; }
    public LicenseType License { get; set; }
    public ContentStatus Status { get; set; }

    public string FileName { get; set; }              // Original filename
    public string StoragePath { get; set; }           // Relative path within storage root
    public long FileSizeBytes { get; set; }
    public string ContentType { get; set; }           // MIME type

    public DateTime SubmittedUtc { get; set; }
    public DateTime? UpdatedUtc { get; set; }
    public DateTime? RemovedUtc { get; set; }

    public ICollection<ContentFlag> Flags { get; set; } = new List<ContentFlag>();
}
```

**Indexes:**
- `ModuleId` (non-unique)
- `Type` (non-unique)
- `Status` (non-unique)

---

### 4.4 ContentFlag

A single flag entity covers both modules and materials. Exactly one of `ModuleId` or `MaterialId` is set per record.

```csharp
public class ContentFlag
{
    public Guid Id { get; set; }

    public Guid? ModuleId { get; set; }              // Set if flagging a module
    public Module? Module { get; set; }

    public Guid? MaterialId { get; set; }            // Set if flagging a material
    public Material? Material { get; set; }

    public string? ReporterIpHash { get; set; }      // SHA-256 + salt; raw IP never stored
    public string? ReporterUserId { get; set; }      // FK if authenticated reporter
    public DateTime FlaggedUtc { get; set; }
    public string? Reason { get; set; }              // Optional free text (max 500 chars)

    // Admin resolution
    public bool IsResolved { get; set; }
    public string? ResolvedByAdminId { get; set; }
    public DateTime? ResolvedUtc { get; set; }
    public string? ResolutionNote { get; set; }
}
```

**Constraint:** A database check constraint enforces that exactly one of `ModuleId` / `MaterialId` is non-null.

---

### 4.5 TaxonomyNode

Stores the three-level taxonomy tree loaded from `taxonomy.json`.

```csharp
public class TaxonomyNode
{
    public string Key { get; set; }                  // PK — unique within the repository
    public int Level { get; set; }                   // 1, 2, or 3
    public string Name { get; set; }
    public string? ParentKey { get; set; }           // FK → TaxonomyNode.Key (null for Level 1)
    public TaxonomyNode? Parent { get; set; }
    public ICollection<TaxonomyNode> Children { get; set; } = new List<TaxonomyNode>();
    public ICollection<TaxonomyCourse> Courses { get; set; } = new List<TaxonomyCourse>();
}
```

**Note:** `Key` is required to be unique across all levels. Organizations must ensure Level 1, 2, and 3 keys do not collide (e.g., using prefixes like `L1_ET`, `L2_EE`, `L3_EET`, or simply ensuring natural key uniqueness as SCNS does).

---

### 4.6 TaxonomyCourse

```csharp
public class TaxonomyCourse
{
    public string CourseId { get; set; }             // PK — globally unique; uppercase
    public string Level3Key { get; set; }            // FK → TaxonomyNode.Key (Level 3 only)
    public TaxonomyNode Level3Node { get; set; }

    public string Title { get; set; }
    public int? CreditHours { get; set; }
    public bool IsActive { get; set; }               // False = no longer accepting contributions
    public string? CurriculumGuideUrl { get; set; }

    public ICollection<Module> Modules { get; set; } = new List<Module>();
}
```

**Orphan course** (`_ORPHAN_COURSE`) is seeded as a `TaxonomyCourse` with no `Level3Key` association. It is excluded from taxonomy browse queries by a filter on `CourseId`.

---

### 4.7 EduInstitution (Reference Data)

```csharp
public class EduInstitution
{
    public string EmailDomain { get; set; }          // PK — e.g. "fau.edu"
    public string InstitutionName { get; set; }
    public string? State { get; set; }
    public string? Country { get; set; }
}
```

---

### 4.8 RefreshToken

```csharp
public class RefreshToken
{
    public Guid Id { get; set; }
    public string ContributorId { get; set; }
    public string TokenHash { get; set; }            // SHA-256 of raw token
    public DateTime IssuedUtc { get; set; }
    public DateTime ExpiresUtc { get; set; }
    public bool IsRevoked { get; set; }
    public string? ReplacedByTokenId { get; set; }  // Token rotation chain
    public string? CreatedByIp { get; set; }
}
```

---

### 4.9 Enumerations

```csharp
public enum MaterialType
{
    Presentation          = 1,
    NarratedPresentation  = 2,
    InteractiveHTML       = 3,
    PrintableHTML         = 4,
    GutenbergHTML         = 5,
    Document              = 6,
    Image                 = 7,
    Audio                 = 8,
    Assignment            = 9,
    Other                 = 10
}

public enum LicenseType
{
    CcBy40                = 1,
    CcBySa40              = 2,
    CcByNc40              = 3,
    CcByNcSa40            = 4
}

public enum ContentStatus
{
    Published             = 1,
    Flagged               = 2,   // Flagged by report; still publicly visible
    Removed               = 3    // Removed by admin; not publicly visible
}
```

---

### 4.10 Database Notes

**Initial database: SQLite**

SQLite is appropriate for Phase 1:
- Single-server deployment
- Low-to-moderate write concurrency expected
- Zero configuration overhead

Switching to PostgreSQL:
1. Change `"DatabaseProvider"` to `"PostgreSQL"` in configuration and supply connection string.
2. Run `dotnet ef database update`.
3. No code changes required — EF Core provider swap only.

`Program.cs` provider selection:
```csharp
var provider = builder.Configuration["DatabaseProvider"];
if (provider == "PostgreSQL")
    options.UseNpgsql(connectionString);
else
    options.UseSqlite(connectionString);
```

**SQLite connection string:**
```json
"ConnectionStrings": {
  "DefaultConnection": "Data Source=/var/presemaker-repo/data/repo.db"
}
```

---

## 5. Authentication & Authorization

### 5.1 Strategy

ASP.NET Core Identity handles account management (registration, login, password reset, email confirmation). JWT Bearer tokens authenticate API requests. Razor Pages use cookie authentication for the web frontend.

Both schemes coexist via a policy scheme selector in `Program.cs`:

```csharp
builder.Services.AddAuthentication(options =>
{
    options.DefaultScheme = "MultiScheme";
})
.AddPolicyScheme("MultiScheme", null, options =>
{
    options.ForwardDefaultSelector = context =>
        context.Request.Path.StartsWithSegments("/api")
            ? JwtBearerDefaults.AuthenticationScheme
            : CookieAuthenticationDefaults.AuthenticationScheme;
})
.AddJwtBearer(options => { /* JWT config */ })
.AddCookie(options => { /* Cookie config */ });
```

### 5.2 JWT Configuration

```json
"Jwt": {
  "Issuer": "https://yourdomain.com",
  "Audience": "presemaker-repo-api",
  "SecretKey": "<256-bit key — set via environment variable in production>",
  "AccessTokenExpiryMinutes": 60,
  "RefreshTokenExpiryDays": 30
}
```

- Access tokens expire in 60 minutes.
- Refresh tokens are stored hashed (SHA-256), expire in 30 days, single-use (rotated on refresh).
- All tokens invalidated on password change.

### 5.3 Roles

| Role | Description |
|---|---|
| `Contributor` | Default role assigned on registration |
| `Administrator` | Assigned manually; grants access to `/admin/` and admin API endpoints |

Roles are seeded on first run. The first admin account is bootstrapped via config (see Section 12.4).

### 5.4 Authorization Policies

```csharp
builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("ContributorOnly", policy =>
        policy.RequireRole("Contributor", "Administrator"));

    options.AddPolicy("AdminOnly", policy =>
        policy.RequireRole("Administrator"));

    options.AddPolicy("OwnerOrAdmin", policy =>
        policy.AddRequirements(new OwnerOrAdminRequirement()));
});
```

`OwnerOrAdmin` is a custom requirement handler that checks `Module.ContributorId == currentUserId || IsAdmin` (and equivalently for `Material`).

### 5.5 Email Confirmation

Email confirmation is required before a contributor can publish. The flow:
1. Register → account created with `EmailConfirmed = false`.
2. Confirmation email sent with tokenized link.
3. Click link → `EmailConfirmed = true`.
4. Publish endpoints check `EmailConfirmed`; return `403` with `EMAIL_NOT_CONFIRMED` if false.

---

## 6. Taxonomy Configuration & Seeding

### 6.1 Taxonomy File Location

The `taxonomy.json` file is placed in a configurable location on the VPS:

```json
"Taxonomy": {
  "ConfigPath": "/etc/presemaker-repo/taxonomy.json"
}
```

### 6.2 ITaxonomyService Interface

```csharp
public interface ITaxonomyService
{
    Task<TaxonomyTree> GetFullTreeAsync();
    Task<TaxonomyNode?> GetNodeAsync(string key);
    Task<TaxonomyCourseValidationResult> ValidateCourseIdAsync(string courseId);
    Task<TaxonomyCourse?> GetCourseAsync(string courseId);
    Task<IReadOnlyList<TaxonomyCourse>> GetCoursesByLevel3Async(string level3Key);
}

public record TaxonomyCourseValidationResult(
    bool IsValid,
    string CourseId,
    string? Title,
    TaxonomyPath? Path,
    string? CurriculumGuideUrl,
    string? InvalidReason);
```

### 6.3 Seeding Logic

`TaxonomySeed.cs` runs during `dotnet ef database update` (via a custom migration seeder). It reads `taxonomy.json`, walks the tree, and upserts all `TaxonomyNode` and `TaxonomyCourse` records. The seeder is idempotent — running it multiple times on an unchanged file produces no changes.

Orphan containers are created in the same seeding pass if they do not already exist:

```csharp
// Orphan course — no Level3Key; excluded from browse queries
var orphanCourse = new TaxonomyCourse
{
    CourseId = "_ORPHAN_COURSE",
    Level3Key = null,
    Title = "Not Classified",
    IsActive = true
};

// Orphan module — created as a Module record belonging to _ORPHAN_COURSE
var orphanModule = new Module
{
    Id = WellKnownIds.OrphanModuleId,   // Fixed GUID defined in constants
    CourseId = "_ORPHAN_COURSE",
    Title = "Unassigned",
    // ContributorId = system admin account
    Status = ContentStatus.Published
};
```

### 6.4 Course ID Normalization

All course IDs are uppercased on ingest. The `TaxonomyService` normalizes lookup keys before querying:

```csharp
public async Task<TaxonomyCourse?> GetCourseAsync(string courseId)
    => await _db.TaxonomyCourses.FindAsync(courseId.ToUpperInvariant());
```

### 6.5 Browse Query Filters

Taxonomy browse queries exclude orphan containers:

```csharp
private static readonly string[] ExcludedCourseIds = ["_ORPHAN_COURSE"];

var courses = await _db.TaxonomyCourses
    .Where(c => !ExcludedCourseIds.Contains(c.CourseId))
    .Where(c => c.Level3Key == level3Key)
    .ToListAsync();
```

---

## 7. File Storage Design

### 7.1 Storage Root

All material files live under a configurable storage root:

```
/var/presemaker-repo/storage/               ← StorageRootPath in config
  modules/
    {module-guid}/
      manifest.json                         ← Recovery aid; mirrors DB records
      materials/
        {material-guid}_{original-filename}
```

Material files are stored with a GUID prefix to prevent collisions regardless of contributor-supplied names. The original filename is preserved in `Material.FileName` for download `Content-Disposition` headers.

### 7.2 IStorageService Interface

```csharp
public interface IStorageService
{
    Task<string> SaveMaterialAsync(
        Guid moduleId,
        Guid materialId,
        string originalFileName,
        Stream content,
        CancellationToken ct = default);

    Task<Stream> ReadMaterialAsync(
        string storagePath,
        CancellationToken ct = default);

    Task<Stream> BuildModuleZipAsync(
        Guid moduleId,
        CancellationToken ct = default);

    Task<Stream> BuildCourseZipAsync(
        string courseId,
        CancellationToken ct = default);

    Task DeleteModuleAsync(
        Guid moduleId,
        CancellationToken ct = default);

    Task DeleteMaterialAsync(
        string storagePath,
        CancellationToken ct = default);
}
```

`LocalStorageService` implements this against the VPS filesystem. A future `BlobStorageService` implements the same interface with no changes to consumers.

### 7.3 ZIP Assembly

`BuildModuleZipAsync` and `BuildCourseZipAsync` assemble ZIPs on-the-fly using `System.IO.Compression.ZipArchive`. Small archives are assembled in a `MemoryStream`; archives exceeding `LargeZipThresholdBytes` are written to a temp file to avoid memory pressure.

Course ZIPs are structured as:
```
{courseId}_course/
  {module-title-slug}/
    {material-filename}
    {material-filename}
  {module-title-slug}/
    ...
```

### 7.4 Size Limits

```json
"Storage": {
  "MaxModuleSizeBytes":     524288000,   // 500 MB per module submission
  "MaxMaterialSizeBytes":   209715200,   // 200 MB per individual material
  "LargeZipThresholdBytes": 104857600    // 100 MB — use temp file for ZIP
}
```

Size is enforced at two points:
1. `FileSizeLimitMiddleware` rejects requests exceeding `MaxModuleSizeBytes` before the controller runs.
2. The service layer validates individual material sizes and accumulated totals.

### 7.5 manifest.json

Each module folder contains a `manifest.json` for disaster recovery (re-seed DB from storage if needed):

```json
{
  "moduleId": "guid",
  "courseId": "EET1084C",
  "title": "Introduction to Electronics",
  "contributorUsername": "jsmith",
  "submittedUtc": "2026-04-15T10:30:00Z",
  "materials": [
    {
      "materialId": "guid",
      "title": "Introduction Slides",
      "type": "Presentation",
      "originalFileName": "intro_slides.pptx",
      "storagePath": "modules/guid/materials/guid_intro_slides.pptx",
      "fileSizeBytes": 4096000
    }
  ]
}
```

---

## 8. Admin API

The admin API is not part of the public API specification. It is documented here as an implementation detail. All endpoints require the `AdminOnly` authorization policy and are prefixed `/api/v1/admin/`.

### 8.1 GET /api/v1/admin/flagged

Returns all currently flagged modules and materials.

**Response 200:** Paginated list. Each item includes:
- `contentType`: `"module"` | `"material"`
- `contentId`: module or material GUID
- `courseId`, `title`
- `contributor` object
- `flaggedUtc`, `flagReason`, `flagCount`

---

### 8.2 POST /api/v1/admin/modules/{id}/clear-flag

Clears all open flags on a module and re-publishes it if it was in `Flagged` state.

**Request:**
```json
{
  "note": "Reviewed — content is appropriate."
}
```

**Response 200:** `{ "message": "Flag cleared. Module re-published." }`

---

### 8.3 DELETE /api/v1/admin/modules/{id}

Removes a module from public view. Sends removal notification to contributor.

**Request:**
```json
{
  "reason": "Content violates terms of service.",
  "notifyContributor": true
}
```

**Response 200:** `{ "message": "Module removed." }`

---

### 8.4 POST /api/v1/admin/materials/{id}/clear-flag

Same behavior as 8.2 for a material.

**Response 200:** `{ "message": "Flag cleared. Material re-published." }`

---

### 8.5 DELETE /api/v1/admin/materials/{id}

Same behavior as 8.3 for a material.

**Response 200:** `{ "message": "Material removed." }`

---

### 8.6 POST /api/v1/admin/contributors/{id}/suspend

```json
{
  "reason": "Multiple submissions removed for policy violations.",
  "notifyContributor": true
}
```

**Response 200:** `{ "message": "Contributor suspended." }`

---

### 8.7 POST /api/v1/admin/contributors/{id}/reinstate

**Response 200:** `{ "message": "Contributor reinstated." }`

---

### 8.8 POST /api/v1/admin/contributors/{id}/contact

Sends an email directly to a contributor from the admin interface.

**Request:**
```json
{
  "subject": "Regarding your recent submission",
  "body": "We noticed that your module for EET1084C..."
}
```

**Response 200:** `{ "message": "Email sent." }`

---

### 8.9 GET /api/v1/admin/stats

Platform statistics for the admin dashboard.

**Response 200:**
```json
{
  "success": true,
  "data": {
    "totalModules": 284,
    "publishedModules": 276,
    "flaggedModules": 3,
    "removedModules": 5,
    "totalMaterials": 1840,
    "totalContributors": 41,
    "suspendedContributors": 1,
    "modulesByCoursePrefix": [
      { "level3Key": "EET", "count": 142 },
      { "level3Key": "CET", "count": 87 }
    ],
    "recentModules30Days": 28
  }
}
```

---

## 9. Email Service

### 9.1 Interface

```csharp
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
```

### 9.2 SMTP Configuration

```json
"Email": {
  "SmtpHost": "smtp.yourprovider.com",
  "SmtpPort": 587,
  "SmtpUseSsl": true,
  "SmtpUsername": "noreply@yourdomain.com",
  "SmtpPassword": "<set via environment variable>",
  "FromAddress": "noreply@yourdomain.com",
  "FromDisplayName": "PreseMaker Repository",
  "AdminAddress": "admin@yourdomain.com"
}
```

### 9.3 Email Templates

Templates are `.html` files in `src/PreseMakerRepo.Api/EmailTemplates/`. A minimal token substitution (`{{username}}`, `{{link}}`, `{{reason}}`, etc.) is used — no third-party template engine in Phase 1.

| Template File | Trigger |
|---|---|
| `ConfirmEmail.html` | POST /auth/register |
| `PasswordReset.html` | POST /auth/password-reset/request |
| `ContentRemoved.html` | DELETE /admin/modules/{id} or /admin/materials/{id} with notifyContributor=true |
| `AccountSuspended.html` | POST /admin/contributors/{id}/suspend with notifyContributor=true |
| `AdminContact.html` | POST /admin/contributors/{id}/contact |

### 9.4 Failure Handling

Email failures are logged at `Warning` level but do not cause API request failures. The content action proceeds regardless of email delivery success.

---

## 10. EDU Institution Detection

### 10.1 Interface

```csharp
public interface IEduLookupService
{
    Task<EduLookupResult> LookupByEmailAsync(string email);
}

public record EduLookupResult(
    bool IsEdu,
    string? InstitutionName,
    string? State,
    string? Country);
```

### 10.2 Logic

On contributor registration:
1. Extract domain from email address.
2. Query `EduInstitution` table for that domain.
3. If found: set `Contributor.IsEduVerified = true`, `Contributor.InstitutionName = result.InstitutionName`.
4. If not found but domain ends in `.edu`: set `IsEduVerified = true`, `InstitutionName = null` (displayed as "Verified .edu").
5. If domain does not end in `.edu`: `IsEduVerified = false`, `InstitutionName = null`.

### 10.3 Display Rules

| IsEduVerified | InstitutionName | Display |
|---|---|---|
| false | null | `jsmith` |
| true | "Florida Atlantic University" | `jsmith · Florida Atlantic University` |
| true | null | `jsmith · Verified .edu` |

### 10.4 Seed Data

`EduSeed.cs` seeds from `Data/Seed/edu_institutions.json`. Initial seed covers Florida post-secondary institutions. Format:

```json
[
  {
    "emailDomain": "fau.edu",
    "institutionName": "Florida Atlantic University",
    "state": "FL",
    "country": "US"
  }
]
```

---

## 11. Web Frontend Structure

The public web frontend is Razor Pages within the same ASP.NET Core project. Phase 1 is server-rendered with minimal vanilla JavaScript for search and filter enhancements.

### 11.1 Page Map

| URL Pattern | Razor Page | Description |
|---|---|---|
| `/` | `Pages/Index` | Home: recently added + Level 1 taxonomy grid |
| `/browse` | `Pages/Browse/Index` | Level 1 taxonomy nodes |
| `/browse/{level1Key}` | `Pages/Browse/Level1` | Level 2 children |
| `/browse/{level1Key}/{level2Key}` | `Pages/Browse/Level2` | Level 3 children |
| `/browse/{level1Key}/{level2Key}/{level3Key}` | `Pages/Browse/Level3` | Courses under a Level 3 node |
| `/courses/{courseId}` | `Pages/Browse/Course` | Modules for a course |
| `/modules/{moduleId}` | `Pages/Module/Detail` | Module detail + material list |
| `/materials/{materialId}` | `Pages/Material/Detail` | Material detail + download |
| `/account/register` | `Pages/Account/Register` | Registration form |
| `/account/login` | `Pages/Account/Login` | Login form |
| `/account/confirm-email` | `Pages/Account/ConfirmEmail` | Email confirmation handler |
| `/account/password-reset` | `Pages/Account/PasswordReset` | Reset request + confirm |
| `/account/profile` | `Pages/Account/Profile` | Profile management |
| `/account/my-submissions` | `Pages/Account/MySubmissions` | Contributor's own content |
| `/admin` | `Areas/Admin/Pages/Index` | Admin dashboard |
| `/admin/flagged` | `Areas/Admin/Pages/Flagged` | Flagged content queue |
| `/admin/contributors` | `Areas/Admin/Pages/Contributors` | Contributor management |

### 11.2 Home Page Sections

1. **Search bar** — global search, submits to `/browse?q=`
2. **Recently Added** — last 10 modules, sorted by `SubmittedUtc DESC`
3. **Browse by Discipline** — Level 1 taxonomy grid

### 11.3 Module Detail Page Features

- Full metadata: title, description, outcomes, topic hierarchy
- Material list with type badges and file sizes
- Per-material download buttons
- Module ZIP download
- License badge with CC icon and link
- Report button → confirmation modal → POST to report endpoint
- Contributor attribution with institution badge
- Curriculum guide link (sourced from parent `TaxonomyCourse`)

### 11.4 Material Detail Page Features

- Material metadata and type badge
- Download button
- Inline preview toggle for applicable types (HTML rendered in `<iframe>`; images displayed inline)
- License badge, contributor attribution
- Report button

### 11.5 Static Assets

CSS and JavaScript served from `wwwroot/`. All assets are self-hosted — no CDN dependencies for core functionality.

---

## 12. Admin Console

The admin console lives at `/admin/` and requires the `Administrator` role.

### 12.1 Admin Dashboard (`/admin`)

- Module stats cards (total, published, flagged, removed)
- Material count
- Contributor stats (total, suspended)
- Modules by Level 3 key (table)
- Recent modules feed (last 20)

### 12.2 Flagged Content Queue (`/admin/flagged`)

Table of flagged modules and materials with columns:
- Content title, type (module/material), course ID
- Contributor username
- Date flagged, flag reason (if provided)
- Actions: **Clear Flag** | **Remove** | **Contact Contributor**

Each action presents a confirmation modal. Remove and Contact require text input.

### 12.3 Contributor Management (`/admin/contributors`)

Searchable table with columns:
- Username, institution, registration date, module count, material count, status
- Actions: **Suspend** | **Reinstate** | **Contact**

### 12.4 Admin Account Bootstrap

On first deployment, `Program.cs` startup checks for any `Administrator` role member. If none exists, it reads `AdminBootstrap` config:

```json
"AdminBootstrap": {
  "Email": "admin@yourdomain.com",
  "Username": "admin",
  "Password": "<set via environment variable — change immediately>"
}
```

If the email exists as a contributor, it is promoted to Administrator. If the account does not exist, it is created and promoted. This block runs only once (when no admin exists).

---

## 13. Configuration Reference

### 13.1 appsettings.json (non-sensitive defaults)

```json
{
  "DatabaseProvider": "SQLite",
  "ConnectionStrings": {
    "DefaultConnection": "Data Source=/var/presemaker-repo/data/repo.db"
  },
  "Jwt": {
    "Issuer": "https://yourdomain.com",
    "Audience": "presemaker-repo-api",
    "AccessTokenExpiryMinutes": 60,
    "RefreshTokenExpiryDays": 30
  },
  "Storage": {
    "RootPath": "/var/presemaker-repo/storage",
    "MaxModuleSizeBytes": 524288000,
    "MaxMaterialSizeBytes": 209715200,
    "LargeZipThresholdBytes": 104857600,
    "RetainRemovedFileDays": 30
  },
  "Email": {
    "SmtpPort": 587,
    "SmtpUseSsl": true,
    "FromDisplayName": "PreseMaker Repository"
  },
  "Taxonomy": {
    "ConfigPath": "/etc/presemaker-repo/taxonomy.json"
  },
  "Repository": {
    "RecentModulesDefaultCount": 10,
    "DefaultPageSize": 20,
    "MaxPageSize": 100,
    "ReportRateLimitPerHour": 5
  },
  "Logging": {
    "MinimumLevel": "Information",
    "FilePath": "/var/log/presemaker-repo/app-.log",
    "RollingInterval": "Day",
    "RetainedFileCount": 30
  }
}
```

### 13.2 Environment Variables (Production Secrets)

Set via `systemd` service `EnvironmentFile` — never committed to source control:

```
ASPNETCORE_ENVIRONMENT=Production
ASPNETCORE_URLS=http://localhost:5000

ConnectionStrings__DefaultConnection=Data Source=/var/presemaker-repo/data/repo.db
Jwt__SecretKey=<256-bit random key>
Email__SmtpHost=smtp.yourprovider.com
Email__SmtpUsername=noreply@yourdomain.com
Email__SmtpPassword=<smtp password>
Email__FromAddress=noreply@yourdomain.com
Email__AdminAddress=admin@yourdomain.com
AdminBootstrap__Email=admin@yourdomain.com
AdminBootstrap__Username=admin
AdminBootstrap__Password=<initial admin password>
```

---

## 14. Error Handling Standards

### 14.1 Global Exception Handler

`Program.cs` registers a global exception handler middleware. Unhandled exceptions are logged at `Error` level with full stack trace. The response to the client is always the standard error envelope:

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "INTERNAL_SERVER_ERROR",
    "message": "An unexpected error occurred. Please try again.",
    "details": null
  }
}
```

Stack traces are **never** included in responses in the Production environment.

### 14.2 FluentValidation Integration

All request DTOs are validated via FluentValidation before reaching the service layer. Validation failures are caught by a global filter that transforms them into `400 VALIDATION_ERROR` responses using the field-level detail shape defined in the API specification.

---

## 15. Security Considerations

### 15.1 Authentication & Token Security

- JWT `SecretKey` is a minimum 256-bit random value set only via environment variable.
- Refresh tokens are stored as SHA-256 hashes; the raw token is returned to the client once and never stored in plaintext.
- Refresh token rotation: each use issues a new token and invalidates the old one.
- All tokens are invalidated on password change.
- Access tokens are short-lived (60 min) to limit exposure from token theft.

### 15.2 Input Validation

- All API request models are validated via FluentValidation before reaching the service layer.
- File uploads are validated for MIME type and size before being written to disk.
- Course IDs are validated against both format pattern and the `TaxonomyCourse` table.
- String fields are sanitized via `HtmlEncoder.Default.Encode()` before storage where they may be rendered in an HTML context.

### 15.3 File Upload Security

- Uploaded files are stored with GUID-prefixed names; original filenames are never used as storage paths.
- MIME type is validated against the type-specific allowlist (Section 12 of the API spec); the `Content-Type` header alone is not trusted.
- File contents are not executed or interpreted server-side.
- The storage root is outside the web root and not directly accessible via URL; all file serving goes through the API controller, which performs authorization and status checks.

### 15.4 Reporter Privacy

- Reporter IP addresses are hashed with a per-deployment salt (stored in environment config) before storage.
- Raw IPs are never persisted.
- No reporter information is surfaced to contributors or the public.

### 15.5 Rate Limiting

- Report endpoints: 5 reports per IP per hour (in-memory `IMemoryCache`-based limiter).
- Login endpoint: 10 failed attempts per IP per 15 minutes → temporary lockout via ASP.NET Core Identity `LockoutOptions`.
- Upload endpoints: no explicit rate limit in Phase 1 — mitigated by file size limits and the authentication requirement.

### 15.6 HTTPS

- All traffic served over HTTPS only; Nginx enforces HTTP → HTTPS redirect.
- TLS certificate via Let's Encrypt / Certbot with auto-renewal.
- HSTS header: `Strict-Transport-Security: max-age=31536000`.

### 15.7 CORS

The PreseMaker desktop client communicates directly via `HttpClient` and is not subject to CORS. The CORS policy restricts browser-origin requests to the repository's own domain:

```csharp
builder.Services.AddCors(options =>
{
    options.AddPolicy("ApiPolicy", policy =>
    {
        policy.WithOrigins("https://yourdomain.com")
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});
```

---

## 16. VPS Deployment

### 16.1 Minimum Server Specifications

| Resource | Minimum | Recommended |
|---|---|---|
| CPU | 1 vCPU | 2 vCPU |
| RAM | 1 GB | 2 GB |
| OS Disk | 20 GB SSD | 50 GB SSD |
| Storage Volume | 100 GB (separate, expandable) | 250 GB+ |
| OS | Ubuntu 22.04 LTS | Ubuntu 24.04 LTS |
| Runtime | .NET 8 Runtime | .NET 8 Runtime |

The separate storage volume mounts at `/var/presemaker-repo/storage/`, making it straightforward to expand without affecting the OS disk.

### 16.2 Directory Structure on VPS

```
/var/presemaker-repo/
  data/
    repo.db                       # SQLite database
  storage/
    modules/                      # Material files
  logs/

/etc/presemaker-repo/
  taxonomy.json                   # Taxonomy configuration
  environment                     # Secret environment variables (chmod 600)

/opt/presemaker-repo/
  app/                            # Published .NET application binaries
```

### 16.3 systemd Service File

```ini
# /etc/systemd/system/presemaker-repo.service

[Unit]
Description=PreseMaker Community Repository
After=network.target

[Service]
Type=notify
User=presemaker
Group=presemaker
WorkingDirectory=/opt/presemaker-repo/app
ExecStart=/opt/presemaker-repo/app/PreseMakerRepo.Api
Restart=always
RestartSec=10
KillSignal=SIGINT
SyslogIdentifier=presemaker-repo
Environment=ASPNETCORE_ENVIRONMENT=Production
Environment=ASPNETCORE_URLS=http://localhost:5000
EnvironmentFile=/etc/presemaker-repo/environment

[Install]
WantedBy=multi-user.target
```

### 16.4 Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate     /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;

    client_max_body_size 520M;    # Headroom above MaxModuleSizeBytes
    proxy_read_timeout 300s;
    proxy_send_timeout 300s;

    location / {
        proxy_pass         http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header   Upgrade $http_upgrade;
        proxy_set_header   Connection keep-alive;
        proxy_set_header   Host $host;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### 16.5 Deployment Steps (Initial)

```bash
# 1. Create service user (no login shell)
sudo useradd -r -s /usr/sbin/nologin presemaker

# 2. Create directories
sudo mkdir -p /var/presemaker-repo/{data,storage/modules}
sudo mkdir -p /opt/presemaker-repo/app
sudo mkdir -p /etc/presemaker-repo
sudo chown -R presemaker:presemaker /var/presemaker-repo
sudo chown -R presemaker:presemaker /opt/presemaker-repo

# 3. Install .NET 8 Runtime (per Microsoft docs for Ubuntu)

# 4. Place taxonomy.json
sudo cp taxonomy.json /etc/presemaker-repo/taxonomy.json

# 5. Publish application
dotnet publish src/PreseMakerRepo.Api -c Release -o /opt/presemaker-repo/app

# 6. Run migrations (creates SQLite DB; seeds taxonomy and orphan containers)
cd /opt/presemaker-repo/app
dotnet PreseMakerRepo.Api.dll --run-migrations

# 7. Configure secrets in /etc/presemaker-repo/environment
# chmod 600; chown presemaker:presemaker

# 8. Enable and start service
sudo systemctl enable presemaker-repo
sudo systemctl start presemaker-repo

# 9. Configure Nginx and obtain TLS certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 16.6 Updates / Redeployment

```bash
dotnet publish src/PreseMakerRepo.Api -c Release -o /tmp/presemaker-release

sudo systemctl stop presemaker-repo
sudo cp -r /tmp/presemaker-release/* /opt/presemaker-repo/app/
cd /opt/presemaker-repo/app && dotnet PreseMakerRepo.Api.dll --run-migrations
sudo systemctl start presemaker-repo
```

**Taxonomy updates:** To update the taxonomy after initial deployment, replace `/etc/presemaker-repo/taxonomy.json` and re-run `--run-migrations`. The seeder is idempotent — existing records are unchanged; new nodes and courses are added.

### 16.7 Backup Strategy

- **Database:** Daily `sqlite3 repo.db ".backup 'backup_$(date +%Y%m%d).db'"` via cron; retain 30 days.
- **Material files:** Weekly `rsync` to off-VPS storage. Files are immutable once stored, so incremental sync is efficient.
- **Taxonomy config:** `/etc/presemaker-repo/taxonomy.json` backed up with the database; versioned separately in source control (without secrets).

---

## 17. Future Phase 2 Hooks

Design decisions in Phase 1 that explicitly avoid blocking Phase 2:

### 17.1 Non-Taxonomy Course Support

`TaxonomyCourse` has an `IsActive` flag and `Level3Key` is nullable. Phase 2 adds:
- System-generated `CourseId` using the `{LEVEL3_KEY}_{N}` pattern
- A `SuggestedMapping` queue table for AI-assisted taxonomy assignment review
- `ITaxonomyService.SuggestMappingAsync()` — stub returning `null` in Phase 1

### 17.2 Blob Storage Migration

`IStorageService` is already abstracted. A `BlobStorageService` requires:
1. NuGet package addition
2. `"StorageProvider": "Local"` → `"StorageProvider": "AzureBlob"` (or `"Backblaze"`) in config
3. No service layer or controller changes

### 17.3 PostgreSQL Migration

`DatabaseProvider` config key is already implemented in `Program.cs`. Running `dotnet ef migrations add PostgreSQLMigration` and `database update` is the complete operational step.

### 17.4 Material Versioning

`Material.UpdatedUtc` is recorded but no version history is retained in Phase 1. Phase 2 adds a `MaterialVersion` table capturing each prior file version, keyed to `Material.Id` with a sequence number.

### 17.5 RSS / Email Digest

`IModuleService.GetRecentAsync()` already supports the query. A background `IHostedService` on a configurable schedule calling an RSS generator or email digest sender is a self-contained Phase 2 addition.

### 17.6 Taxonomy Setup Wizard

The `taxonomy.json` schema is fully defined. A Razor Pages wizard that writes a valid `taxonomy.json` is a Phase 2 UI addition with no API or data model changes required.

---

*Document ends. Implements: PreseMaker_Repository_API_Specification.md v1.0*
