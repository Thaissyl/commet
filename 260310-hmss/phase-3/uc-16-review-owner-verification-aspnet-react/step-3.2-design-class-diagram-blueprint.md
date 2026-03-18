# Design Class Diagram Blueprint: UC-16 Review Owner Verification - ASP.NET Simple Layered Backend

## Scope

- Included classes: `AdminUI`, `ReviewVerificationController`, `VerificationLogic`, `IOwnerVerificationRepository`, `IOwnerProfileRepository`, `ICloudStorageGateway`, `IEmailGateway`, `OwnerVerification`, `OwnerProfile`
- Synchronization source:
  - participant set and call structure from `step-3.0-design-communication-diagram.md`
  - class operations derived from step-3.0 messages

## Class Boxes

### `AdminUI`

- Stereotype: `<<user interaction>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ openVerificationReview()`
  - `+ selectSubmission(in verificationId: Guid)`
  - `+ approveVerification(in verificationId: Guid, in reviewNote: String)`

### `ReviewVerificationController`

- Stereotype: `<<coordinator>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getPendingSubmissions(out response: SubmissionListResponseDto)`
  - `+ getSubmissionDetail(in verificationId: Guid, out response: SubmissionDetailResponseDto)`
  - `+ approveVerification(in verificationId: Guid, in reviewNote: String, out response: DecisionResponseDto)`

### `IOwnerVerificationRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ findPending(out list: VerificationList)`
  - `+ findById(in id: Guid, out entity: OwnerVerification)`
  - `+ update(in entity: OwnerVerification, out persisted: OwnerVerification)`

### `IOwnerProfileRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ findByVerificationId(in verificationId: Guid, out entity: OwnerProfile)`
  - `+ update(in entity: OwnerProfile, out persisted: OwnerProfile)`

### `VerificationLogic`

- Stereotype: `<<business logic>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ validateDecision(in verification: OwnerVerification, out result: ValidationResult)`

### `ICloudStorageGateway`

- Stereotype: `<<proxy>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ retrieveDocuments(in documentRefs: List<String>, out documents: FileList)`

### `IEmailGateway`

- Stereotype: `<<proxy>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ sendAsync(in message: EmailMessage)`

### `OwnerVerification`

- Stereotype: `<<data abstraction>>`
- Attributes:
  - `- verificationId: Guid`
  - `- ownerId: Guid`
  - `- personalInformation: string`
  - `- idDocumentRef: string`
  - `- supportingDocsRef: string`
  - `- status: VerificationStatus`
  - `- reviewNote: string`
- Operations:
  - `+ approve(in reviewNote: String, out result: StatusChangeResult)`

### `OwnerProfile`

- Stereotype: `<<data abstraction>>`
- Attributes:
  - `- ownerId: Guid`
  - `- fullName: string`
  - `- verificationStatus: VerificationStatus`
- Operations:
  - `+ verify(out result: StatusChangeResult)`

## Relationships

- association:
  - from: `AdminUI`
  - to: `ReviewVerificationController`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `reviews verifications`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ReviewVerificationController`
  - to: `IOwnerVerificationRepository`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `loads and persists`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ReviewVerificationController`
  - to: `IOwnerProfileRepository`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `loads and persists`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ReviewVerificationController`
  - to: `VerificationLogic`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `validates decision`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ReviewVerificationController`
  - to: `ICloudStorageGateway`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `retrieves documents`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ReviewVerificationController`
  - to: `IEmailGateway`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `dispatches notification`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ReviewVerificationController`
  - to: `OwnerVerification`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `mutates state`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ReviewVerificationController`
  - to: `OwnerProfile`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `mutates state`
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

- association:
  - from: `IOwnerProfileRepository`
  - to: `OwnerProfile`
  - source multiplicity: `1`
  - target multiplicity: `0..*`
  - association name: `manages`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

## Generalizations

- none in current scope

## Notes

- Dual entity modification: `OwnerVerification.approve()` and `OwnerProfile.verify()` both mutate state
- Both entities loaded and persisted separately in sequence 3
- Document retrieval from cloud storage is synchronous with reply for admin review display
- Email dispatch is async (fire-and-forget)
- Alternative flow: reject (similar flow with different status transitions)
