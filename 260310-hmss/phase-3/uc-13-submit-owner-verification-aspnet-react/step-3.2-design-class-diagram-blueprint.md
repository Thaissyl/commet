# Design Class Diagram Blueprint: UC-13 Submit Owner Verification - ASP.NET Simple Layered Backend

## Scope

- Included classes: `OwnerUI`, `SubmitVerificationController`, `IOwnerVerificationRepository`, `VerificationLogic`, `ICloudStorageGateway`, `OwnerVerification`
- Synchronization source:
  - participant set and call structure from `step-3.0-design-communication-diagram.md`
  - class operations derived from step-3.0 messages

## Class Boxes

### `OwnerUI`

- Stereotype: `<<user interaction>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ openVerification()`
  - `+ processDetails(in request: VerificationDraftDto, in documents: FileList)`
  - `+ submitVerification(in request: VerificationDraftDto, in documentUrls: List<String>)`

### `SubmitVerificationController`

- Stereotype: `<<coordinator>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getVerificationForm(in ownerId: Guid, out response: VerificationFormDto)`
  - `+ processVerificationDetails(in request: VerificationDraftDto, in documents: FileList, out response: ProcessVerificationResponseDto)`
  - `+ submitVerification(in request: VerificationDraftDto, in documentUrls: List<String>, out response: SubmissionResponseDto)`

### `IOwnerVerificationRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ save(in entity: OwnerVerification, out persisted: OwnerVerification)`

### `VerificationLogic`

- Stereotype: `<<business logic>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ validateRequiredFields(in request: VerificationDraftDto, out result: ValidationResult)`

### `ICloudStorageGateway`

- Stereotype: `<<proxy>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ uploadDocuments(in documents: FileList, out documentUrls: List<String>)`

### `OwnerVerification`

- Stereotype: `<<data abstraction>>`
- Attributes:
  - `- verificationId: Guid`
  - `- ownerId: Guid`
  - `- personalInformation: string`
  - `- idDocumentRef: string`
  - `- supportingDocsRef: string`
  - `- status: VerificationStatus`
  - `- submittedAt: DateTime`
- Operations:
  - none in current scope

## Relationships

- association:
  - from: `OwnerUI`
  - to: `SubmitVerificationController`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `submits verification`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `SubmitVerificationController`
  - to: `IOwnerVerificationRepository`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `persists`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `SubmitVerificationController`
  - to: `VerificationLogic`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `validates`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `SubmitVerificationController`
  - to: `ICloudStorageGateway`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `uploads documents`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `IOwnerVerificationRepository`
  - to: `OwnerVerification`
  - source multiplicity: `1`
  - target multiplicity: `0..*`
  - association name: `manages`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

## Generalizations

- none in current scope

## Notes

- Two-phase: validation + upload (sequence 2), then save (sequence 3)
- `documentUrls` parameter forwarded from sequence 2 to sequence 3 (stateless pattern)
- New verifications have `status = PendingReview`
- Document upload is synchronous with reply for preview and storage
