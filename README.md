# PreseMaker Community Repository

A publicly browsable, contributor-maintained library of instructional course materials. Built as open-source infrastructure that any school, institution, or organization can deploy and configure for their own course catalog.

**Live implementation:** [Florida Course Repository](https://floridacourserepo.com/) — serving Florida colleges and universities using the Florida Statewide Course Numbering System (SCNS).

---

## What It Does

The PreseMaker Community Repository gives educators a shared, structured place to publish and discover instructional materials. Contributors upload presentations, documents, audio, assignments, and other materials organized by course. Anyone can browse or download — no account required.

- **Publish** — contributors upload materials at the course, module, or individual file level
- **Browse** — public browsing and full-text search across all published content
- **Download** — course packages, individual modules, or single files; ZIP assembly on demand
- **Integrate** — REST API connects directly to the [PreseMaker](https://edu-agentic.com/) desktop authoring tool

---

## Deploy Your Own

This repository is designed to be self-hosted by any organization. A school district, university consortium, company, or professional association can run its own instance with its own taxonomy, branding, and course catalog. The only configuration required is a `taxonomy.json` file that defines your three-level subject hierarchy and course list.

**Technology stack (reference implementation):**
- .NET 8 / ASP.NET Core 8
- Entity Framework Core (SQLite → PostgreSQL via config)
- ASP.NET Core Identity + JWT Bearer authentication
- Razor Pages web frontend + REST API
- Nginx + systemd on Ubuntu 22.04/24.04 LTS

The API specification is implementation-agnostic. You can build a compatible server in any language or framework as long as it conforms to the contract described in [`Specifications/PreseMaker_Repository_API_Specification.md`](Specifications/PreseMaker_Repository_API_Specification.md).

---

## Taxonomy

The repository is organized by a three-level hierarchy you define at setup. Taxonomy is loaded from a single JSON file and does not change during operation.

### Structure

```
Level 1  (e.g., Discipline)
  └── Level 2  (e.g., Subdiscipline)
        └── Level 3  (e.g., Subject Prefix)
              └── Courses
```

### Example: Florida SCNS (reference implementation)

```
Engineering Technologies                     ← Level 1
  └── Electronic Engineering                 ← Level 2
        └── EET  (Electronic Eng. Tech.)     ← Level 3
              ├── EET1084C  Survey of Electronics
              ├── EET1035C  DC/AC Circuits
              └── EET2140C  Electronics I

Natural Sciences
  └── Biology
        └── BSC
              ├── BSC1010C  General Biology I
              └── BSC2085C  Anatomy & Physiology I
```

### Example: Corporate Training

```
Operations                                   ← Level 1
  └── Safety                                 ← Level 2
        └── Hazardous Materials              ← Level 3
              ├── OPS_SAF_001  HAZMAT Level 1
              └── OPS_SAF_002  HAZMAT Level 2

Human Resources
  └── Onboarding
        └── New Employee
              └── HR_NE_001  Company Orientation
```

### Taxonomy Configuration File

```json
{
  "repositoryName": "Florida Engineering Technology Repository",
  "taxonomyVersion": "1.0",
  "identifierSource": "external",
  "levels": [
    { "level": 1, "label": "Discipline" },
    { "level": 2, "label": "Subdiscipline" },
    { "level": 3, "label": "Prefix" }
  ],
  "tree": [
    {
      "key": "ET",
      "name": "Engineering Technologies",
      "children": [
        {
          "key": "EE",
          "name": "Electronic Engineering",
          "children": [
            {
              "key": "EET",
              "name": "Electronic Engineering Technology",
              "courses": [
                {
                  "courseId": "EET1084C",
                  "title": "Survey of Electronics",
                  "creditHours": 3,
                  "curriculumGuideUrl": "https://example.org/curriculum/eet/eet1084c/"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

Set `identifierSource` to `"external"` if your taxonomy supplies course IDs natively (like SCNS), or `"generated"` to have the system suggest IDs using the pattern `{LEVEL3_KEY}_{SEQUENTIAL_NUMBER}` (e.g., `HAZMAT_001`).

---

## Content Model

```
Course  (e.g., EET1084C — Survey of Electronics)
  └── Module  (e.g., Introduction to DC Circuits)
        └── Material  (e.g., Slide deck, PDF notes, audio recording)
```

Each level is independently publishable and downloadable. A **Module** is the primary unit of instruction — it carries learning outcomes, a topic hierarchy, contributor attribution, and a Creative Commons license. **Materials** within a module are typed:

| Type | Description |
|---|---|
| Presentation | Slide-based presentation (.pptx) |
| NarratedPresentation | Presentation with embedded audio |
| InteractiveHTML | Interactive HTML/JavaScript content |
| PrintableHTML | Print-formatted HTML |
| GutenbergHTML | Chunked Gutenberg-style HTML |
| Document | Markdown, plain text, or PDF |
| Image | Image file or ZIP collection |
| Audio | Audio narration or recordings |
| Assignment | Assessment or assignment materials |
| Other | Validated against a configurable allowlist |

---

## API Summary

All endpoints are under `/api/v1/`. The API uses a consistent JSON envelope:

```json
{ "success": true, "data": { } }
{ "success": false, "data": null, "error": { "code": "ERROR_CODE", "message": "..." } }
```

Authentication uses JWT Bearer tokens (60-min access token, 30-day rotating refresh token). Most read operations are public — no account required.

### Authentication

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/auth/register` | Public | Create contributor account |
| GET | `/auth/confirm-email` | Public | Confirm email address |
| POST | `/auth/login` | Public | Get access + refresh token |
| POST | `/auth/refresh` | Public | Rotate refresh token |
| POST | `/auth/logout` | Auth | Revoke session |
| POST | `/auth/password-reset/request` | Public | Send reset email |
| POST | `/auth/password-reset/confirm` | Public | Complete password reset |

### Taxonomy

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/taxonomy` | Public | Full taxonomy tree with counts |
| GET | `/taxonomy/{l1}` | Public | Level 1 node + children |
| GET | `/taxonomy/{l1}/{l2}` | Public | Level 2 node + children |
| GET | `/taxonomy/{l1}/{l2}/{l3}` | Public | Level 3 node + course list |
| GET | `/taxonomy/validate/{courseId}` | Public | Validate a course ID |

### Courses

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/courses` | Public | All courses with published modules |
| GET | `/courses/recent` | Public | Recently published modules |
| GET | `/courses/{courseId}` | Public | Course detail + module list |
| POST | `/courses/{courseId}/publish` | Auth | Publish course package |
| GET | `/courses/{courseId}/download` | Public | Download full course as ZIP |

### Modules

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/courses/{courseId}/modules` | Public | All modules for a course |
| GET | `/courses/{courseId}/modules/{moduleId}` | Public | Module detail + material list |
| POST | `/courses/{courseId}/modules` | Auth | Publish a new module |
| PUT | `/courses/{courseId}/modules/{moduleId}` | Owner/Admin | Update module |
| DELETE | `/courses/{courseId}/modules/{moduleId}` | Owner/Admin | Retract module |
| GET | `/courses/{courseId}/modules/{moduleId}/download` | Public | Download module as ZIP |

### Materials

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `…/modules/{moduleId}/materials` | Public | All materials for a module |
| GET | `…/modules/{moduleId}/materials/{materialId}` | Public | Material detail |
| POST | `…/modules/{moduleId}/materials` | Auth | Publish a new material |
| PUT | `…/modules/{moduleId}/materials/{materialId}` | Owner/Admin | Update material |
| DELETE | `…/modules/{moduleId}/materials/{materialId}` | Owner/Admin | Retract material |
| GET | `…/materials/{materialId}/download` | Public | Download material file |

### Search & Reporting

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/search?q={term}` | Public | Full-text search across all content |
| POST | `…/modules/{moduleId}/report` | Public | Report a module for review |
| POST | `…/materials/{materialId}/report` | Public | Report a material for review |

### Contributor Profile

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/contributors/me` | Auth | Authenticated contributor profile |
| GET | `/contributors/me/submissions` | Auth | Contributor's own submissions |

The full API contract — including all request/response shapes, validation rules, error codes, and accepted MIME types — is documented in [`Specifications/PreseMaker_Repository_API_Specification.md`](Specifications/PreseMaker_Repository_API_Specification.md).

---

## PreseMaker Integration

[PreseMaker](https://edu-agentic.com/) is a desktop authoring tool for building structured course materials. The repository is designed as PreseMaker's publish and retrieve target:

- Publish a course, module, or individual material directly from PreseMaker to any configured repository
- Browse and download materials from within PreseMaker to use as starting points or supplements
- Real-time course ID validation before publishing
- Stored credentials and configurable repository URL (supports staging and production)

Any organization running this repository gets automatic compatibility with PreseMaker for all contributors using the desktop client.

---

## Licensing

All published materials carry a Creative Commons license selected by the contributor at upload time:

| License | Description |
|---|---|
| CC BY 4.0 | Attribution required; any use permitted |
| CC BY-SA 4.0 | Attribution + share alike |
| CC BY-NC 4.0 | Attribution; non-commercial use only |
| CC BY-NC-SA 4.0 | Attribution + non-commercial + share alike |

---

## Specifications

Three detailed specification documents govern Phase 1 scope:

- [`Specifications/PreseMaker_Repository_Requirements.md`](Specifications/PreseMaker_Repository_Requirements.md) — functional requirements and user roles
- [`Specifications/PreseMaker_Repository_API_Specification.md`](Specifications/PreseMaker_Repository_API_Specification.md) — full REST API contract
- [`Specifications/PreseMaker_Repository_DesignSpec.md`](Specifications/PreseMaker_Repository_DesignSpec.md) — schema, auth flow, storage layout, deployment guide

---

## Configuration

Secrets are supplied via environment variables — never in appsettings files:

| Variable | Purpose |
|---|---|
| `ConnectionStrings__DefaultConnection` | Database connection string |
| `Jwt__SecretKey` | 256-bit JWT signing key |
| `Email__SmtpPassword` | SMTP credential |
| `AdminBootstrap__Email/Username/Password` | First-run admin account |

On first startup with no Administrator account present, the system reads the `AdminBootstrap` variables and creates the initial admin account automatically.

---

## Build & Run

```bash
# Build
dotnet build

# Run (development)
dotnet run --project PreseMakerRepo.Api

# Watch mode
dotnet watch --project PreseMakerRepo.Api

# Publish for Linux VPS
dotnet publish -c Release -r linux-x64 --self-contained false

# EF Core migrations
dotnet ef migrations add <MigrationName> \
  --project PreseMakerRepo.Infrastructure \
  --startup-project PreseMakerRepo.Api

dotnet ef database update \
  --project PreseMakerRepo.Infrastructure \
  --startup-project PreseMakerRepo.Api
```

---

## Contributing

This is open-source infrastructure. If you implement a compatible server in another stack, extend the taxonomy tooling, or run an instance for your institution, contributions and feedback are welcome via pull request or issue.
