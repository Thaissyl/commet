# Design Class Diagram Blueprint: UC-16 Review Owner Verification - ASP.NET Simple Layered Backend

## Scope

- Included classes: `AdminUI`, `ReviewVerificationController`, `VerificationLogic`, `IOwnerVerificationRepository`, `IUserAccountRepository`, `ICloudStorageGateway`, `IEmailGateway`, `OwnerVerification`, `UserAccount`
- Synchronization source:
  - participant set and call structure from `step-3.0-design-communication-diagram.md`
  - class operations derived from step-3.0 messages and the actual ASP.NET controller implementation

## Class Boxes

### `AdminUI`

- Stereotype: `<<user interaction>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ OpenVerificationReview()`
  - `+ SelectSubmission(in verificationId: Guid)`
  - `+ ApproveVerification(in verificationId: Guid, in dto: ReviewDecisionDto)`
  - `+ RejectVerification(in verificationId: Guid, in dto: ReviewDecisionDto)`

### `ReviewVerificationController`

- Stereotype: `<<coordinator>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ GetPendingSubmissions(out response: List<SubmissionSummaryDto>)`
  - `+ GetSubmissionDetail(in verificationId: Guid, out response: SubmissionDetailResponseDto)`
  - `+ ApproveVerification(in verificationId: Guid, in dto: ReviewDecisionDto, out response: AdminDecisionResponseDto)`
  - `+ RejectVerification(in verificationId: Guid, in dto: ReviewDecisionDto, out response: AdminDecisionResponseDto)`

### `IOwnerVerificationRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ FindPendingAsync(out records: List<OwnerVerification>)`
  - `+ FindByIdAsync(in id: Guid, out verification: OwnerVerification)`
  - `+ UpdateAsync(in entity: OwnerVerification, out persisted: OwnerVerification)`

### `IUserAccountRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ FindByIdAsync(in id: Guid, out owner: UserAccount)`

### `VerificationLogic`

- Stereotype: `<<business logic>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ ValidateDecision(in verification: OwnerVerification, out result: ValidationResult)`

### `ICloudStorageGateway`

- Stereotype: `<<proxy>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ RetrieveDocumentsAsync(in documentRefs: List<String>, out documentUrls: List<String>)`

### `IEmailGateway`

- Stereotype: `<<proxy>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ SendAsync(in message: EmailMessage)`

### `OwnerVerification`

- Stereotype: `<<data abstraction>>`
- Attributes:
  - `- verificationId: Guid`
  - `- ownerId: Guid`
  - `- status: string`
  - `- reviewNote: string`
- Operations:
  - `+ Approve(in reviewNote: String)`
  - `+ Reject(in reviewNote: String)`

### `UserAccount`

- Stereotype: `<<data abstraction>>`
- Attributes:
  - `- userId: Guid`
  - `- fullName: string`
  - `- email: string`
  - `- accountStatus: string`
- Operations:
  - none in current scope

## Relationships

- association:
  - from: `AdminUI`
  - to: `ReviewVerificationController`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `reviews submissions`
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
  - to: `IUserAccountRepository`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `loads owner info`
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
  - association name: `dispatches email`
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
  - from: `IUserAccountRepository`
  - to: `UserAccount`
  - source multiplicity: `1`
  - target multiplicity: `0..*`
  - association name: `manages`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

## Generalizations

- none in current scope

## Notes

- The old `OwnerProfile` / `IOwnerProfileRepository` branch is intentionally removed because it does not exist in the actual controller implementation.
- The decision sequence re-fetches `OwnerVerification` before validation and persistence to preserve controller statelessness.
- Approval and rejection share the same structural flow; rejection adds the non-empty review-note rule.
