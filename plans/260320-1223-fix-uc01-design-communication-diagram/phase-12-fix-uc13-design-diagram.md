# Phase 12: Document Fix — Rewrite UC-13 step-3.0-design-communication-diagram.md

**Status:** Ready (no code changes needed)
**File:** `C:\Users\welterial\commet\260310-hmss\phase-3\uc-13-submit-owner-verification-aspnet-react\step-3.0-design-communication-diagram.md`

## Context Links

- Use case: `C:\Users\welterial\commet\260310-hmss\step-1.3-uc-13-submit-owner-verification.md`
- Analysis: `C:\Users\welterial\commet\260310-hmss\phase-2\step-2.2-uc-13-submit-owner-verification-main-seq.md`
- Code: `backend/Hmss.Api/Controllers/OwnerVerificationController.cs`

## Errors Being Fixed

| # | Error |
|---|-------|
| 1 | Participant `SubmitVerificationController` → `OwnerVerificationController` |
| 2 | Object layout `IOwnerVerificationRepository --- OwnerVerification` — remove; add `OwnerVerification` directly under controller (controller calls `OwnerVerification.Create(...)` directly) |
| 3 | Msg 1.1: remove `in ownerId: Guid` param (comes from JWT) |
| 4 | Msg 2.1: `in request: VerificationDraftDto` → `in personalInformation: string?`; `FileList` → `IFormFileCollection` |
| 5 | Msg 2.2: `validateRequiredFields` NOT called in `ProcessVerificationDetails` — it's called in `SubmitVerification`; move to seq 3 (before SaveAsync) |
| 6 | Msg 2.3: `uploadDocuments` → `UploadDocumentsAsync`; `FileList` → `IFormFileCollection` |
| 7 | Msg 3.1: remove `in documentUrls: List<String>` as separate param — URLs are inside `VerificationDraftDto` (request.SupportingDocUrls, request.IdDocumentUrl) |
| 8 | Add msg 3.x: `OwnerVerificationController -> OwnerVerification: Create(in ownerId: Guid, in personalInformation: string, in idDocumentUrl: string, in supportingJson: string?, out entity: OwnerVerification)` |
| 9 | Msg 3.2: `save` → `SaveAsync` |

## Corrected Object Layout

```text
Owner --- OwnerUI --- OwnerVerificationController
                       |--- IOwnerVerificationRepository
                       |--- VerificationLogic
                       |--- ICloudStorageGateway --- Cloud Storage
                       |--- OwnerVerification
```

## Corrected Seq 2 & 3 Flow

**Seq 2 (processVerificationDetails):**
- 2.1: `processVerificationDetails(in personalInformation: string?, in documents: IFormFileCollection, out response: ProcessVerificationResponseDto)`
- 2.2: `UploadDocumentsAsync(in documents: IFormFileCollection, out documentUrls: List<String>)` → Cloud Storage
- 2.3: Cloud Storage upload

**Seq 3 (submitVerification):**
- 3.1: `submitVerification(in request: VerificationDraftDto, out response: VerificationSubmissionResponseDto)`
- 3.2: `validateRequiredFields(in request: VerificationDraftDto, out result: ValidationResult)`
- 3.3: `Create(in ownerId: Guid, in personalInformation: string, in idDocumentUrl: string, in supportingJson: string?, out entity: OwnerVerification)`
- 3.4: `SaveAsync(in entity: OwnerVerification, out persisted: OwnerVerification)`

## Todo

- [ ] Rename `SubmitVerificationController` → `OwnerVerificationController` throughout
- [ ] Fix object layout: remove `IOwnerVerificationRepository --- OwnerVerification`; add `OwnerVerification` directly under controller
- [ ] Fix Msg 1.1: remove `in ownerId: Guid`
- [ ] Fix Msg 2.1: first param `in personalInformation: string?`; `FileList` → `IFormFileCollection`
- [ ] Move `validateRequiredFields` from seq 2 to seq 3 (before SaveAsync)
- [ ] Fix Msg 2.3: `UploadDocumentsAsync`; `IFormFileCollection`
- [ ] Fix Msg 3.1: remove `in documentUrls: List<String>` separate param
- [ ] Add msg 3.x: `OwnerVerification.Create(...)`
- [ ] Fix Msg 3.2 (was 3.2): `SaveAsync`

## Success Criteria

- Controller named `OwnerVerificationController`
- `OwnerVerification` under controller in layout (not under repository)
- `validateRequiredFields` in seq 3, not seq 2
- `processVerificationDetails` params use `personalInformation: string?` and `IFormFileCollection`
- `UploadDocumentsAsync` with `IFormFileCollection`
- `OwnerVerification.Create(...)` shown as explicit message
- `SaveAsync` used
