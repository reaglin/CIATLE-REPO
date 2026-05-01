# PreseMaker Community Repository — API Specification

**Version:** 1.0  
**Date:** April 2026  
**Status:** Active  
**Type:** REST API Reference — Implementation-Agnostic

---

## Table of Contents

1. [Overview](#1-overview)
2. [Conventions](#2-conventions)
3. [Authentication](#3-authentication)
4. [Taxonomy](#4-taxonomy)
5. [Courses](#5-courses)
6. [Modules](#6-modules)
7. [Materials](#7-materials)
8. [Reporting](#8-reporting)
9. [Contributor Profile](#9-contributor-profile)
10. [Search](#10-search)
11. [Error Codes Reference](#11-error-codes-reference)
12. [Accepted MIME Types by Material Type](#12-accepted-mime-types-by-material-type)
13. [License Reference](#13-license-reference)

---

## 1. Overview

This document specifies the public REST API for the PreseMaker Community Repository. It defines all endpoint paths, request and response structures, the authentication model, and error handling behavior. It is independent of any specific implementation technology; a companion implementation document covers how the API is realized in a particular technology stack and deployment environment.

All endpoints are versioned under `/api/v1/`. The version segment is explicit to allow future versioning without breaking existing clients.

The API serves two consumer types:

- **PreseMaker desktop client** — the primary API consumer; performs all publish, retrieve, and browse operations on behalf of a contributor
- **Repository web frontend** — the public browse experience; uses the same API endpoints

---

## 2. Conventions

### 2.1 Base URL

All endpoint paths in this document are relative to:
```
{repositoryBaseUrl}/api/v1
```

### 2.2 Request Headers

**All requests:**
```
Accept: application/json
X-Client-Name: {client_identifier}       // Optional; logged for diagnostics
X-Client-Version: {version_string}       // Optional; logged; recorded on submissions
```

**Authenticated requests:**
```
Authorization: Bearer {access_token}
```

**JSON body requests:**
```
Content-Type: application/json
```

**File upload requests:**
```
Content-Type: multipart/form-data; boundary={boundary}
```

### 2.3 Standard Response Envelope

All responses use a consistent envelope structure.

**Success:**
```json
{
  "success": true,
  "data": { }
}
```

**Error:**
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable description.",
    "details": null
  }
}
```

### 2.4 Pagination

All list endpoints support pagination via query parameters:

| Parameter | Default | Maximum |
|---|---|---|
| `page` | 1 | — |
| `pageSize` | 20 | 100 |

**Paginated response shape:**
```json
{
  "success": true,
  "data": {
    "items": [ ],
    "totalCount": 142,
    "page": 1,
    "pageSize": 20,
    "totalPages": 8
  }
}
```

### 2.5 Sorting

Where supported, the `sort` query parameter accepts:
- `newest` (default) — descending by submission date
- `oldest` — ascending by submission date

### 2.6 Authorization Notation

Throughout this document:
- **[Public]** — no authentication required
- **[Auth]** — requires a valid Bearer access token
- **[Owner or Admin]** — requires the authenticated user to be the content owner or an Administrator
- **[Admin]** — requires the Administrator role

---

## 3. Authentication

### 3.1 Token Model

The API uses JWT Bearer tokens for stateless authentication.

- **Access tokens** are short-lived (implementation-configured; default 60 minutes)
- **Refresh tokens** are long-lived (implementation-configured; default 30 days), single-use, and rotated on each use
- All tokens issued to an account are invalidated on password change

### 3.2 POST /auth/register [Public]

Creates a contributor account. Sends a confirmation email to the supplied address.

**Request:**
```json
{
  "username": "jsmith",
  "email": "jsmith@fau.edu",
  "password": "SecurePass123!"
}
```

**Validation:**
- `username`: 3–30 characters; alphanumeric, underscore, or hyphen; unique across the repository
- `email`: valid format; unique across the repository
- `password`: minimum 8 characters; at least one uppercase letter, one digit, one special character

**Response 200:**
```json
{
  "success": true,
  "data": {
    "message": "Registration successful. Please check your email to confirm your account.",
    "isEduVerified": true,
    "institutionName": "Florida Atlantic University"
  }
}
```

**Response 400:** `VALIDATION_ERROR`  
**Response 409:** `USERNAME_TAKEN` | `EMAIL_TAKEN`

---

### 3.3 GET /auth/confirm-email [Public]

Confirms a contributor's email address using the tokenized link sent at registration.

**Query Parameters:**
- `userId` — contributor identifier
- `token` — confirmation token from the email link

**Response 200:**
```json
{
  "success": true,
  "data": {
    "message": "Email confirmed."
  }
}
```

**Response 400:** `INVALID_TOKEN` | `EMAIL_ALREADY_CONFIRMED`

---

### 3.4 POST /auth/login [Public]

Authenticates a contributor and returns an access token and refresh token.

**Request:**
```json
{
  "email": "jsmith@fau.edu",
  "password": "SecurePass123!"
}
```

**Response 200:**
```json
{
  "success": true,
  "data": {
    "accessToken": "eyJ...",
    "refreshToken": "opaque-token-string",
    "expiresAt": "2026-04-29T14:00:00Z",
    "contributor": {
      "id": "guid",
      "username": "jsmith",
      "displayName": "John Smith",
      "institutionName": "Florida Atlantic University",
      "isEduVerified": true
    }
  }
}
```

**Response 401:** `INVALID_CREDENTIALS`  
**Response 403:** `ACCOUNT_SUSPENDED` | `EMAIL_NOT_CONFIRMED`

---

### 3.5 POST /auth/refresh [Public]

Exchanges a valid refresh token for a new access token and refresh token pair. The supplied refresh token is immediately invalidated (single-use rotation).

**Request:**
```json
{
  "refreshToken": "opaque-token-string"
}
```

**Response 200:** Same shape as login response (3.4).  
**Response 401:** `INVALID_REFRESH_TOKEN` | `REFRESH_TOKEN_EXPIRED`

---

### 3.6 POST /auth/logout [Auth]

Revokes the supplied refresh token, ending the session.

**Request:**
```json
{
  "refreshToken": "opaque-token-string"
}
```

**Response 200:**
```json
{
  "success": true,
  "data": {
    "message": "Logged out."
  }
}
```

---

### 3.7 POST /auth/password-reset/request [Public]

Sends a password reset link to the registered email address. Always returns success regardless of whether the email is registered, to prevent email enumeration.

**Request:**
```json
{
  "email": "jsmith@fau.edu"
}
```

**Response 200:**
```json
{
  "success": true,
  "data": {
    "message": "If an account exists for that address, a reset link has been sent."
  }
}
```

---

### 3.8 POST /auth/password-reset/confirm [Public]

Completes the password reset flow using the token from the reset email.

**Request:**
```json
{
  "userId": "guid",
  "token": "reset-token-string",
  "newPassword": "NewSecurePass456!"
}
```

**Response 200:**
```json
{
  "success": true,
  "data": {
    "message": "Password reset successful."
  }
}
```

**Response 400:** `INVALID_TOKEN` | `VALIDATION_ERROR`

---

## 4. Taxonomy

The taxonomy is the three-level hierarchy configured at repository setup. Taxonomy endpoints are read-only; the taxonomy is not modified via the API in Phase 1.

### 4.1 GET /taxonomy [Public]

Returns the full taxonomy tree with submission counts at each node. Course lists are not included in the full tree response; use the Level 3 endpoint (4.4) for course listings.

**Response 200:**
```json
{
  "success": true,
  "data": {
    "repositoryName": "Florida Engineering Technology Repository",
    "levels": [
      { "level": 1, "label": "Discipline" },
      { "level": 2, "label": "Subdiscipline" },
      { "level": 3, "label": "Prefix" }
    ],
    "tree": [
      {
        "key": "ET",
        "name": "Engineering Technologies",
        "courseCount": 142,
        "moduleCount": 890,
        "children": [
          {
            "key": "EE",
            "name": "Electronic Engineering",
            "courseCount": 48,
            "moduleCount": 310,
            "children": [
              {
                "key": "EET",
                "name": "Electronic Engineering Technology",
                "courseCount": 12,
                "moduleCount": 84
              }
            ]
          }
        ]
      }
    ]
  }
}
```

---

### 4.2 GET /taxonomy/{level1Key} [Public]

Returns a Level 1 node with its Level 2 children and counts.

**Path Parameters:**
- `level1Key` — the key of the Level 1 node (e.g., `ET`)

**Response 200:**
```json
{
  "success": true,
  "data": {
    "key": "ET",
    "name": "Engineering Technologies",
    "level": 1,
    "courseCount": 142,
    "moduleCount": 890,
    "children": [
      {
        "key": "EE",
        "name": "Electronic Engineering",
        "courseCount": 48,
        "moduleCount": 310
      }
    ]
  }
}
```

**Response 404:** `TAXONOMY_NODE_NOT_FOUND`

---

### 4.3 GET /taxonomy/{level1Key}/{level2Key} [Public]

Returns a Level 2 node with its Level 3 children and counts.

**Response 200:**
```json
{
  "success": true,
  "data": {
    "key": "EE",
    "name": "Electronic Engineering",
    "level": 2,
    "parent": { "key": "ET", "name": "Engineering Technologies" },
    "courseCount": 48,
    "moduleCount": 310,
    "children": [
      {
        "key": "EET",
        "name": "Electronic Engineering Technology",
        "courseCount": 12,
        "moduleCount": 84
      }
    ]
  }
}
```

**Response 404:** `TAXONOMY_NODE_NOT_FOUND`

---

### 4.4 GET /taxonomy/{level1Key}/{level2Key}/{level3Key} [Public]

Returns a Level 3 node with its course list (paginated).

**Query Parameters:** `sort`, `page`, `pageSize`

**Response 200:**
```json
{
  "success": true,
  "data": {
    "key": "EET",
    "name": "Electronic Engineering Technology",
    "level": 3,
    "parent": {
      "level2": { "key": "EE", "name": "Electronic Engineering" },
      "level1": { "key": "ET", "name": "Engineering Technologies" }
    },
    "courses": {
      "items": [
        {
          "courseId": "EET1084C",
          "title": "Survey of Electronics",
          "creditHours": 3,
          "moduleCount": 7,
          "materialCount": 42,
          "newestSubmissionDate": "2026-04-15T00:00:00Z",
          "curriculumGuideUrl": "https://example.org/curriculum/eet/eet1084c/"
        }
      ],
      "totalCount": 12,
      "page": 1,
      "pageSize": 20,
      "totalPages": 1
    }
  }
}
```

**Response 404:** `TAXONOMY_NODE_NOT_FOUND`

---

### 4.5 GET /taxonomy/validate/{courseId} [Public]

Validates a course identifier against the taxonomy without requiring a publish attempt. Used by client applications to confirm a course ID before enabling publish controls.

**Path Parameters:**
- `courseId` — the course identifier to validate (e.g., `EET1084C`)

**Response 200 (valid):**
```json
{
  "success": true,
  "data": {
    "isValid": true,
    "courseId": "EET1084C",
    "title": "Survey of Electronics",
    "creditHours": 3,
    "taxonomyPath": {
      "level1": { "key": "ET", "name": "Engineering Technologies" },
      "level2": { "key": "EE", "name": "Electronic Engineering" },
      "level3": { "key": "EET", "name": "Electronic Engineering Technology" }
    },
    "curriculumGuideUrl": "https://example.org/curriculum/eet/eet1084c/"
  }
}
```

**Response 200 (invalid):**
```json
{
  "success": true,
  "data": {
    "isValid": false,
    "courseId": "EET9999",
    "reason": "Course identifier not found in taxonomy."
  }
}
```

*Note: This endpoint always returns HTTP 200. The `isValid` field in the response body carries the validation result.*

---

## 5. Courses

A Course is a container identified by a globally unique course ID from the taxonomy. It holds modules and, through them, materials. A course entry may exist in the repository either as a full package (with modules and materials) or as a metadata-only entry awaiting module contributions.

### 5.1 GET /courses [Public]

Returns all courses that have at least one published module, optionally filtered by taxonomy node.

**Query Parameters:**
- `level1` — filter by Level 1 key
- `level2` — filter by Level 2 key
- `level3` — filter by Level 3 key
- `sort`, `page`, `pageSize`

**Response 200:** Paginated list of CourseListItem objects (same shape as items in section 4.4).

---

### 5.2 GET /courses/{courseId} [Public]

Returns course detail including a summary list of published modules.

**Path Parameters:**
- `courseId` — e.g., `EET1084C`

**Response 200:**
```json
{
  "success": true,
  "data": {
    "courseId": "EET1084C",
    "title": "Survey of Electronics",
    "creditHours": 3,
    "taxonomyPath": {
      "level1": { "key": "ET", "name": "Engineering Technologies" },
      "level2": { "key": "EE", "name": "Electronic Engineering" },
      "level3": { "key": "EET", "name": "Electronic Engineering Technology" }
    },
    "curriculumGuideUrl": "https://example.org/curriculum/eet/eet1084c/",
    "moduleCount": 7,
    "materialCount": 42,
    "newestSubmissionDate": "2026-04-15T00:00:00Z",
    "modules": [
      {
        "moduleId": "guid",
        "title": "Introduction to Electronics",
        "contributor": {
          "username": "jsmith",
          "displayName": "John Smith",
          "institutionName": "Florida Atlantic University",
          "isEduVerified": true
        },
        "license": "CcBy40",
        "licenseDisplayName": "CC BY 4.0",
        "licenseUrl": "https://creativecommons.org/licenses/by/4.0/",
        "submittedUtc": "2026-04-15T10:30:00Z",
        "materialCount": 6,
        "materialTypes": ["Presentation", "Document", "Audio"]
      }
    ]
  }
}
```

**Response 404:** `COURSE_NOT_FOUND`

---

### 5.3 POST /courses/{courseId}/publish [Auth]

Publishes a course-level package. May include one or more modules inline (each optionally with materials), or publish the course as a metadata-only container.

**Request:** `multipart/form-data`

The request contains a `metadata` part (JSON) and zero or more file parts. File parts are referenced by name from within the metadata.

**Metadata part:**
```json
{
  "courseId": "EET1084C",
  "modules": [
    {
      "title": "Introduction to Electronics",
      "description": "Covers foundational concepts of DC circuits.",
      "outcomes": [
        "Apply Ohm's Law to simple circuits.",
        "Identify passive electronic components."
      ],
      "topicHierarchy": [
        {
          "topic": "Circuit Fundamentals",
          "elements": ["Voltage", "Current", "Resistance", "Power"]
        },
        {
          "topic": "Passive Components",
          "elements": ["Resistors", "Capacitors", "Inductors"]
        }
      ],
      "license": "CcBy40",
      "materials": [
        {
          "title": "Introduction Slides",
          "type": "Presentation",
          "description": "Slide deck for Module 1.",
          "filePartName": "module_0_material_0"
        },
        {
          "title": "Module Notes",
          "type": "Document",
          "filePartName": "module_0_material_1"
        }
      ]
    }
  ]
}
```

**File parts** are named using the `filePartName` values declared in the metadata:
```
Content-Disposition: form-data; name="module_0_material_0"; filename="intro_slides.pptx"
Content-Type: application/vnd.openxmlformats-officedocument.presentationml.presentation

[binary data]
```

**Validation:**
- `courseId` must exist in the taxonomy
- Each module `title`: 3–120 characters
- Each module `description`: 10–2000 characters
- Each declared `filePartName` must have a corresponding file part in the request
- Each file's MIME type must be accepted for the declared material type (see Section 12)
- Individual file size and total request size must be within configured limits

**Response 201:**
```json
{
  "success": true,
  "data": {
    "courseId": "EET1084C",
    "modulesPublished": 1,
    "materialsPublished": 2,
    "courseUrl": "https://yourdomain.com/courses/EET1084C"
  }
}
```

**Response 400:** `VALIDATION_ERROR`  
**Response 403:** `EMAIL_NOT_CONFIRMED` | `ACCOUNT_SUSPENDED`  
**Response 413:** `SUBMISSION_TOO_LARGE`  
**Response 422:** `INVALID_COURSE_ID`

---

### 5.4 GET /courses/{courseId}/download [Public]

Downloads all published modules and their materials for a course as a single ZIP archive.

**Response 200:** Binary ZIP stream
```
Content-Type: application/zip
Content-Disposition: attachment; filename="{courseId}_course_{shortId}.zip"
```

**Response 404:** `COURSE_NOT_FOUND`

---

### 5.5 GET /courses/recent [Public]

Returns the most recently published modules across all courses.

**Query Parameters:**
- `count` — number of results, 1–50 (default 10)
- `level1`, `level2`, `level3` — optional taxonomy filter

**Response 200:**
```json
{
  "success": true,
  "data": {
    "items": [ ]
  }
}
```

Each item is a ModuleSummary object (same shape as modules listed under 5.2).

---

## 6. Modules

A Module is a unit of instruction within a course. It carries its own metadata and can be published, retrieved, and reused independently of other modules in the same course.

### 6.1 GET /courses/{courseId}/modules [Public]

Returns all published modules for a course.

**Query Parameters:** `sort`, `page`, `pageSize`

**Response 200:** Paginated list of ModuleSummary objects (same shape as modules listed in section 5.2).

**Response 404:** `COURSE_NOT_FOUND`

---

### 6.2 GET /courses/{courseId}/modules/{moduleId} [Public]

Returns full module detail including the material list.

**Response 200:**
```json
{
  "success": true,
  "data": {
    "moduleId": "guid",
    "courseId": "EET1084C",
    "title": "Introduction to Electronics",
    "description": "Covers foundational concepts of DC circuits.",
    "outcomes": [
      "Apply Ohm's Law to simple circuits.",
      "Identify passive electronic components."
    ],
    "topicHierarchy": [
      {
        "topic": "Circuit Fundamentals",
        "elements": ["Voltage", "Current", "Resistance", "Power"]
      }
    ],
    "contributor": {
      "username": "jsmith",
      "displayName": "John Smith",
      "institutionName": "Florida Atlantic University",
      "isEduVerified": true
    },
    "license": "CcBy40",
    "licenseDisplayName": "CC BY 4.0",
    "licenseUrl": "https://creativecommons.org/licenses/by/4.0/",
    "submittedUtc": "2026-04-15T10:30:00Z",
    "updatedUtc": null,
    "status": "Published",
    "materials": [
      {
        "materialId": "guid",
        "title": "Introduction Slides",
        "type": "Presentation",
        "description": "Slide deck for Module 1.",
        "fileName": "intro_slides.pptx",
        "fileSizeBytes": 4096000,
        "contentType": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "downloadUrl": "/api/v1/courses/EET1084C/modules/{moduleId}/materials/{materialId}/download"
      }
    ],
    "downloadAllUrl": "/api/v1/courses/EET1084C/modules/{moduleId}/download"
  }
}
```

**Response 404:** `MODULE_NOT_FOUND`

---

### 6.3 POST /courses/{courseId}/modules [Auth]

Publishes a new module under a course. Requires a valid course ID and at least one material file.

**Request:** `multipart/form-data`

**Metadata part:**
```json
{
  "title": "Introduction to Electronics",
  "description": "Covers foundational concepts of DC circuits.",
  "outcomes": ["Apply Ohm's Law to simple circuits."],
  "topicHierarchy": [
    {
      "topic": "Circuit Fundamentals",
      "elements": ["Voltage", "Current", "Resistance"]
    }
  ],
  "license": "CcBy40",
  "materials": [
    {
      "title": "Introduction Slides",
      "type": "Presentation",
      "description": "Slide deck for this module.",
      "filePartName": "material_0"
    }
  ]
}
```

**File parts:** Named by `filePartName` values declared in the metadata.

**Validation:**
- `courseId` must exist in taxonomy
- `title`: 3–120 characters
- `description`: 10–2000 characters
- At least one material with a corresponding file part
- File type and size validation per material (see Section 12)

**Response 201:**
```json
{
  "success": true,
  "data": {
    "moduleId": "guid",
    "courseId": "EET1084C",
    "materialsPublished": 1,
    "moduleUrl": "https://yourdomain.com/courses/EET1084C/modules/{moduleId}"
  }
}
```

**Response 400:** `VALIDATION_ERROR`  
**Response 403:** `EMAIL_NOT_CONFIRMED` | `ACCOUNT_SUSPENDED`  
**Response 404:** `COURSE_NOT_FOUND`  
**Response 413:** `SUBMISSION_TOO_LARGE`  
**Response 422:** `INVALID_COURSE_ID`

---

### 6.4 PUT /courses/{courseId}/modules/{moduleId} [Owner or Admin]

Updates a module's metadata and optionally replaces material files. Omitted metadata fields are left unchanged. New file parts for a given `filePartName` replace the existing material file; omitted material parts are left unchanged.

**Request:** Same `multipart/form-data` shape as POST (6.3).

**Response 200:**
```json
{
  "success": true,
  "data": {
    "moduleId": "guid",
    "message": "Module updated."
  }
}
```

**Response 400:** `VALIDATION_ERROR`  
**Response 403:** `FORBIDDEN`  
**Response 404:** `MODULE_NOT_FOUND`

---

### 6.5 DELETE /courses/{courseId}/modules/{moduleId} [Owner or Admin]

Retracts (soft-deletes) a module. The module is removed from public browse but files are retained for a configurable period before permanent deletion.

**Response 200:**
```json
{
  "success": true,
  "data": {
    "message": "Module retracted."
  }
}
```

**Response 403:** `FORBIDDEN`  
**Response 404:** `MODULE_NOT_FOUND`

---

### 6.6 GET /courses/{courseId}/modules/{moduleId}/download [Public]

Downloads all materials in the module as a ZIP archive.

**Response 200:** Binary ZIP stream
```
Content-Type: application/zip
Content-Disposition: attachment; filename="{courseId}_{moduleTitle_slug}_{shortId}.zip"
```

**Response 404:** `MODULE_NOT_FOUND`

---

## 7. Materials

A Material is an individual instructional resource within a module. Each material has a declared type that governs accepted file formats and any special handling.

### 7.1 GET /courses/{courseId}/modules/{moduleId}/materials [Public]

Returns all published materials for a module.

**Query Parameters:** `sort`, `page`, `pageSize`

**Response 200:** Paginated list of MaterialSummary objects.

**MaterialSummary shape:**
```json
{
  "materialId": "guid",
  "title": "Introduction Slides",
  "type": "Presentation",
  "description": "Slide deck for this module.",
  "fileName": "intro_slides.pptx",
  "fileSizeBytes": 4096000,
  "contentType": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
  "contributor": { },
  "license": "CcBy40",
  "licenseDisplayName": "CC BY 4.0",
  "submittedUtc": "2026-04-15T10:30:00Z",
  "downloadUrl": "/api/v1/courses/EET1084C/modules/{moduleId}/materials/{materialId}/download"
}
```

**Response 404:** `MODULE_NOT_FOUND`

---

### 7.2 GET /courses/{courseId}/modules/{moduleId}/materials/{materialId} [Public]

Returns full material detail.

**Response 200:**
```json
{
  "success": true,
  "data": {
    "materialId": "guid",
    "moduleId": "guid",
    "courseId": "EET1084C",
    "title": "Introduction Slides",
    "type": "Presentation",
    "description": "Slide deck for Module 1.",
    "fileName": "intro_slides.pptx",
    "fileSizeBytes": 4096000,
    "contentType": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "contributor": {
      "username": "jsmith",
      "displayName": "John Smith",
      "institutionName": "Florida Atlantic University",
      "isEduVerified": true
    },
    "license": "CcBy40",
    "licenseDisplayName": "CC BY 4.0",
    "licenseUrl": "https://creativecommons.org/licenses/by/4.0/",
    "submittedUtc": "2026-04-15T10:30:00Z",
    "updatedUtc": null,
    "status": "Published",
    "downloadUrl": "/api/v1/courses/EET1084C/modules/{moduleId}/materials/{materialId}/download"
  }
}
```

**Response 404:** `MATERIAL_NOT_FOUND`

---

### 7.3 POST /courses/{courseId}/modules/{moduleId}/materials [Auth]

Publishes a new material under a module.

**Request:** `multipart/form-data`

**Metadata part:**
```json
{
  "title": "Introduction Slides",
  "type": "Presentation",
  "description": "Slide deck for Module 1.",
  "license": "CcBy40"
}
```

**File part:**
```
Content-Disposition: form-data; name="file"; filename="intro_slides.pptx"
Content-Type: application/vnd.openxmlformats-officedocument.presentationml.presentation

[binary data]
```

**Validation:**
- `moduleId` must exist and be published (the `_ORPHAN_MODULE` container does not accept direct contributions)
- `type` must be a recognized material type
- File MIME type must be accepted for the declared type (see Section 12)
- File size must be within configured limit

**Response 201:**
```json
{
  "success": true,
  "data": {
    "materialId": "guid",
    "moduleId": "guid",
    "courseId": "EET1084C",
    "materialUrl": "https://yourdomain.com/courses/EET1084C/modules/{moduleId}/materials/{materialId}"
  }
}
```

**Response 400:** `VALIDATION_ERROR`  
**Response 403:** `EMAIL_NOT_CONFIRMED` | `ACCOUNT_SUSPENDED`  
**Response 404:** `MODULE_NOT_FOUND`  
**Response 413:** `MATERIAL_TOO_LARGE`  
**Response 422:** `INVALID_MODULE_ID` | `INVALID_MATERIAL_TYPE`

---

### 7.4 PUT /courses/{courseId}/modules/{moduleId}/materials/{materialId} [Owner or Admin]

Updates material metadata and optionally replaces the file. Omitted metadata fields are left unchanged. If a file part is included, it replaces the existing file.

**Request:** Same `multipart/form-data` shape as POST (7.3). File part is optional.

**Response 200:**
```json
{
  "success": true,
  "data": {
    "materialId": "guid",
    "message": "Material updated."
  }
}
```

**Response 400:** `VALIDATION_ERROR`  
**Response 403:** `FORBIDDEN`  
**Response 404:** `MATERIAL_NOT_FOUND`

---

### 7.5 DELETE /courses/{courseId}/modules/{moduleId}/materials/{materialId} [Owner or Admin]

Retracts (soft-deletes) a material. Files are retained for a configurable period before permanent deletion.

**Response 200:**
```json
{
  "success": true,
  "data": {
    "message": "Material retracted."
  }
}
```

**Response 403:** `FORBIDDEN`  
**Response 404:** `MATERIAL_NOT_FOUND`

---

### 7.6 GET /courses/{courseId}/modules/{moduleId}/materials/{materialId}/download [Public]

Downloads the material file.

**Response 200:** Binary file stream
```
Content-Type: {material content type}
Content-Disposition: attachment; filename="{originalFileName}"
Content-Length: {fileSizeBytes}
```

**Response 404:** `MATERIAL_NOT_FOUND`

---

## 8. Reporting

Any visitor may report a module or material for administrator review. No authentication is required. Reported content remains publicly visible until an administrator acts.

Rate limiting applies: a configured maximum number of reports may be submitted per IP address per hour.

### 8.1 POST /courses/{courseId}/modules/{moduleId}/report [Public]

Reports a module for administrator review.

**Request:**
```json
{
  "reason": "Optional free-text reason for the report. Maximum 500 characters."
}
```

The `reason` field is optional. If omitted, the report is submitted without a reason.

**Response 200:**
```json
{
  "success": true,
  "data": {
    "message": "Thank you. This module has been flagged for review."
  }
}
```

**Response 404:** `MODULE_NOT_FOUND`  
**Response 429:** `RATE_LIMIT_EXCEEDED`

---

### 8.2 POST /courses/{courseId}/modules/{moduleId}/materials/{materialId}/report [Public]

Reports a material for administrator review.

**Request:** Same shape as 8.1.

**Response 200:**
```json
{
  "success": true,
  "data": {
    "message": "Thank you. This material has been flagged for review."
  }
}
```

**Response 404:** `MATERIAL_NOT_FOUND`  
**Response 429:** `RATE_LIMIT_EXCEEDED`

---

## 9. Contributor Profile

### 9.1 GET /contributors/me [Auth]

Returns the authenticated contributor's profile.

**Response 200:**
```json
{
  "success": true,
  "data": {
    "id": "guid",
    "username": "jsmith",
    "displayName": "John Smith",
    "email": "jsmith@fau.edu",
    "institutionName": "Florida Atlantic University",
    "isEduVerified": true,
    "registeredUtc": "2026-01-15T00:00:00Z",
    "submissionCounts": {
      "modules": 14,
      "materials": 87
    }
  }
}
```

---

### 9.2 GET /contributors/me/submissions [Auth]

Returns the authenticated contributor's own submissions. Includes removed items (not visible to other users).

**Query Parameters:**
- `level` — `module` | `material` | `all` (default)
- `sort`, `page`, `pageSize`

**Response 200:** Paginated list. Each item includes `level`, `status` (Published / Flagged / Removed), and level-appropriate metadata.

---

## 10. Search

### 10.1 GET /search [Public]

Full-text search across module titles, module descriptions, learning outcomes, topic hierarchies, and course IDs.

**Query Parameters:**

| Parameter | Description |
|---|---|
| `q` | Search term — required; minimum 2 characters |
| `level` | `module` \| `material` \| `all` (default) |
| `level1` | Filter by Level 1 taxonomy key |
| `level2` | Filter by Level 2 taxonomy key |
| `level3` | Filter by Level 3 taxonomy key |
| `courseId` | Exact match on course ID |
| `materialType` | Filter by material type (e.g., `Presentation`, `Audio`) |
| `sort` | `newest` (default) \| `oldest` |
| `page`, `pageSize` | Pagination |

**Response 200:** Paginated list of search results.

Each result object:
```json
{
  "resultType": "module",
  "moduleId": "guid",
  "courseId": "EET1084C",
  "title": "Introduction to Electronics",
  "description": "Covers foundational concepts...",
  "contributor": {
    "username": "jsmith",
    "institutionName": "Florida Atlantic University",
    "isEduVerified": true
  },
  "submittedUtc": "2026-04-15T10:30:00Z",
  "taxonomyPath": {
    "level1": { "key": "ET", "name": "Engineering Technologies" },
    "level2": { "key": "EE", "name": "Electronic Engineering" },
    "level3": { "key": "EET", "name": "Electronic Engineering Technology" }
  }
}
```

For `resultType: "material"`, the object additionally includes `materialType`, `fileName`, `moduleId`, and `moduleTitle`.

**Response 400:** `QUERY_TOO_SHORT`

---

## 11. Error Codes Reference

| HTTP Status | Code | Meaning |
|---|---|---|
| 400 | `VALIDATION_ERROR` | Request model validation failed; `details` array contains field-level errors |
| 400 | `QUERY_TOO_SHORT` | Search query is fewer than 2 characters |
| 400 | `INVALID_TOKEN` | Confirmation or reset token is invalid or expired |
| 401 | `UNAUTHORIZED` | No valid Bearer token was provided |
| 401 | `INVALID_CREDENTIALS` | Login email or password is incorrect |
| 401 | `INVALID_REFRESH_TOKEN` | Refresh token is invalid or has already been used |
| 401 | `REFRESH_TOKEN_EXPIRED` | Refresh token has passed its expiry time |
| 403 | `FORBIDDEN` | Authenticated but insufficient permissions for this operation |
| 403 | `EMAIL_NOT_CONFIRMED` | Account exists but email address has not been confirmed |
| 403 | `ACCOUNT_SUSPENDED` | Account has been suspended by an administrator |
| 404 | `COURSE_NOT_FOUND` | Course not found |
| 404 | `MODULE_NOT_FOUND` | Module not found or has been retracted |
| 404 | `MATERIAL_NOT_FOUND` | Material not found or has been retracted |
| 404 | `TAXONOMY_NODE_NOT_FOUND` | Taxonomy key does not match any node |
| 409 | `USERNAME_TAKEN` | Registration username is already in use |
| 409 | `EMAIL_TAKEN` | Registration email is already in use |
| 409 | `EMAIL_ALREADY_CONFIRMED` | Email confirmation has already been completed |
| 413 | `SUBMISSION_TOO_LARGE` | Total upload size exceeds the configured limit |
| 413 | `MATERIAL_TOO_LARGE` | A single material file exceeds the configured limit |
| 422 | `INVALID_COURSE_ID` | Course ID format is valid but the ID is not present in the taxonomy |
| 422 | `INVALID_MODULE_ID` | Module ID is not found or is not eligible to receive contributions |
| 422 | `INVALID_MATERIAL_TYPE` | Declared material type is not recognized |
| 429 | `RATE_LIMIT_EXCEEDED` | Request limit for this endpoint has been exceeded |
| 500 | `INTERNAL_SERVER_ERROR` | Unhandled server error |

**Validation error detail shape** (used when `code` is `VALIDATION_ERROR`):
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "One or more validation errors occurred.",
    "details": [
      { "field": "title", "message": "Title must be between 3 and 120 characters." },
      { "field": "materials[0].type", "message": "Material type is required." }
    ]
  }
}
```

---

## 12. Accepted MIME Types by Material Type

| Material Type | Accepted MIME Types |
|---|---|
| Presentation | `application/vnd.openxmlformats-officedocument.presentationml.presentation` |
| NarratedPresentation | `application/vnd.openxmlformats-officedocument.presentationml.presentation` |
| InteractiveHTML | `text/html`, `application/zip` |
| PrintableHTML | `text/html` |
| GutenbergHTML | `text/html` |
| Document | `text/markdown`, `text/plain`, `application/pdf` |
| Image | `image/png`, `image/jpeg`, `image/gif`, `image/svg+xml`, `application/zip` |
| Audio | `audio/mpeg`, `audio/wav`, `application/zip` |
| Assignment | `application/pdf`, `text/html`, `text/markdown`, `application/zip` |
| Other | Validated against a configurable allowlist defined at repository setup |

Implementations must validate file content against the declared MIME type, not solely the `Content-Type` header or file extension.

New material types and their accepted MIME types are added to the configuration without requiring API version changes.

---

## 13. License Reference

| Value | Display Name | URL |
|---|---|---|
| `CcBy40` | CC BY 4.0 | https://creativecommons.org/licenses/by/4.0/ |
| `CcBySa40` | CC BY-SA 4.0 | https://creativecommons.org/licenses/by-sa/4.0/ |
| `CcByNc40` | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| `CcByNcSa40` | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |

---

*Followed by: PreseMaker_Repository_DesignSpec.md (Implementation)*
