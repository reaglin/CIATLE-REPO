# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**PreseMaker Community Repository** — a publicly browsable, contributor-maintained library of course materials organized by a configurable hierarchical taxonomy (Florida SCNS by default). It exposes a REST API for the PreseMaker desktop client, a Razor Pages web frontend for browsing, and an admin console for moderation.

**Current Status:** Three comprehensive spec files exist (`Specifications/`) but implementation has not started. The repo contains only the ASP.NET Core 8 scaffolding template.

## Solution Structure (Target)

Three-project solution (not yet created — currently a single web project):

| Project | Purpose |
|---|---|
| `PreseMakerRepo.Api` | ASP.NET Core host: controllers, Razor pages, admin console |
| `PreseMakerRepo.Core` | Domain models, enums, interfaces — no infrastructure dependencies |
| `PreseMakerRepo.Infrastructure` | EF Core, file storage, email, JWT, services |

URL namespaces: `/api/v1/` (REST), `/browse/` (web frontend), `/admin/` (admin console).

## Build & Run Commands

```bash
# Build
dotnet build

# Run (development)
dotnet run --project CIATLE-REPO

# Watch mode
dotnet watch --project CIATLE-REPO

# Run tests (when test projects exist)
dotnet test
dotnet test --filter "FullyQualifiedName~SomeTestClass"

# Publish for Linux VPS
dotnet publish -c Release -r linux-x64 --self-contained false

# EF Core migrations
dotnet ef migrations add <MigrationName> --project PreseMakerRepo.Infrastructure --startup-project PreseMakerRepo.Api
dotnet ef database update --project PreseMakerRepo.Infrastructure --startup-project PreseMakerRepo.Api
```

## Technology Stack

- **Runtime:** .NET 8, ASP.NET Core 8
- **ORM:** Entity Framework Core 8 (code-first)
- **Database:** SQLite (initial) → PostgreSQL via config swap (`DatabaseProvider` setting)
- **Auth:** ASP.NET Core Identity + JWT Bearer (policy scheme: JWT for `/api/*`, cookies for web pages)
- **File Storage:** Local filesystem, abstracted via `IStorageService` (future: Azure Blob / Backblaze)
- **Email:** MailKit via SMTP
- **Validation:** FluentValidation on all DTOs
- **Logging:** Serilog (file + console)
- **Deployment:** Nginx + systemd on Ubuntu 22.04/24.04 LTS

## Domain Model

**Content Hierarchy:** `TaxonomyCourse` → `Module` → `Material` (each independently publishable).

**Taxonomy:** Three-level tree (`TaxonomyNode`): Discipline → Subdiscipline → Prefix/Subject. Leaf nodes link to `TaxonomyCourse` records. Loaded from `taxonomy.json` at startup via an idempotent `TaxonomySeed` service. Two built-in orphan containers are always created:
- `_ORPHAN_COURSE` — modules with no Level 3 taxonomy match
- `_ORPHAN_MODULE` (`WellKnownIds.OrphanModuleId`) — materials with no module match

**Key Entities:**
- `Contributor` — extends `IdentityUser`; adds display name, institution, EDU verification, suspension status
- `Module` — GUID PK; has JSON columns for `Outcomes` and topic hierarchy; `ContentStatus` enum (Published/Flagged/Removed)
- `Material` — GUID PK; `MaterialType` enum (10 types); filename stored as-is for `Content-Disposition`, actual path is GUID-prefixed
- `ContentFlag` — exactly one of `ModuleId`/`MaterialId` set; reporter IP stored as SHA-256 hash (never raw)
- `RefreshToken` — single-use rotation; token stored as SHA-256 hash; all invalidated on password change
- `EduInstitution` — email domain lookup for institution attribution on contributor profiles

**Enums:** `MaterialType` (10 values), `LicenseType` (4 CC options), `ContentStatus`.

## Authentication & Authorization

- Access tokens: 60-min JWT; refresh tokens: 30-day, single-use rotation
- Policies: `ContributorOnly`, `AdminOnly`, `OwnerOrAdmin`
- Email confirmation required before first publish
- Admin bootstrap: on first startup with no Administrator role, reads `AdminBootstrap` config (email/username/password from env vars) and creates/promotes the account — idempotent

## File Storage Layout

```
/var/presemaker-repo/storage/
  modules/{module-guid}/
    manifest.json          # Disaster recovery metadata
    materials/{material-guid}_{original-filename}
```

- ZIPs assembled on-demand; temp file used for assemblies > 100 MB
- Size limits: 500 MB/module, 200 MB/material
- Original filename never used as a storage path — always GUID-prefixed

## Configuration

All secrets come from environment variables (never appsettings):

| Env Var | Purpose |
|---|---|
| `ConnectionStrings__DefaultConnection` | DB connection string |
| `Jwt__SecretKey` | 256-bit JWT signing key |
| `Email__SmtpPassword` | SMTP credential |
| `AdminBootstrap__Email/Username/Password` | First-run admin account |

Key appsettings sections: `DatabaseProvider`, `Jwt`, `Storage`, `Email`, `Taxonomy`, `Repository` (page sizes, report rate limit, recent modules count).

## API Response Envelope

All REST responses use:
```json
{ "success": true, "data": { ... }, "error": null }
{ "success": false, "data": null, "error": { "code": "ERROR_CODE", "message": "...", "fields": {} } }
```

27 distinct error codes are defined in the API spec (`Specifications/PreseMaker_Repository_API_Specification.md`).

## Security Constraints

- Reporter IP addresses: SHA-256 hashed with salt — never stored raw
- File uploads: MIME type validated, size checked, stored with GUID prefix — original filename never used as path, never executed server-side
- Rate limits: 5 reports/IP/hour; 10 login failures/IP/15 min (temp lockout)
- CORS: restricted to repository domain; PreseMaker client uses `HttpClient`, not browser CORS

## Phase 2 Hooks (Deferred — do not implement in Phase 1)

`IStorageService` abstraction is already planned to allow blob storage migration. `TaxonomyCourse.IsActive` and nullable `Level3Key` are reserved for non-taxonomy courses. Material versioning (`MaterialVersion` table) is planned but not in scope.

## Specifications

All three spec files in `Specifications/` are authoritative for Phase 1 scope:
- `PreseMaker_Repository_Requirements.md` — functional requirements and user roles
- `PreseMaker_Repository_API_Specification.md` — full REST API contract with request/response shapes
- `PreseMaker_Repository_DesignSpec.md` — implementation design: schema, auth flow, storage, deployment, admin console
