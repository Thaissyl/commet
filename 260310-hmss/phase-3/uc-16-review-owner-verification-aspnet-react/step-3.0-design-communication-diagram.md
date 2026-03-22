# Design Communication Diagram: UC-16 Review Owner Verification - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: `AdminUI -> ReviewVerificationController`, then controller-to-repository, controller-to-logic, and controller-to-gateway calls
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label
- Separate reply arrows intentionally omitted - `out` parameters represent returned data
- Request flow style: synchronous request handling with fire-and-forget email dispatch

## Object Layout

```text
System Admin --- AdminUI --- ReviewVerificationController
                              |--- VerificationLogic
                              |--- IOwnerVerificationRepository
                              |--- IUserAccountRepository
                              |--- ICloudStorageGateway --- Cloud Storage
                              |--- IEmailGateway --- Email Provider
```

## Participants

| Position | Object                       | Stereotype             |
| -------- | ---------------------------- | ---------------------- |
| 1        | System Admin                 | Actor (primary)        |
| 2        | AdminUI                      | `<<user interaction>>` |
| 3        | ReviewVerificationController | `<<coordinator>>`      |
| 4        | VerificationLogic            | `<<business logic>>`   |
| 5        | IOwnerVerificationRepository | `<<database wrapper>>` |
| 6        | IUserAccountRepository       | `<<database wrapper>>` |
| 7        | ICloudStorageGateway         | `<<proxy>>`            |
| 8        | Cloud Storage                | Actor (secondary)      |
| 9        | IEmailGateway                | `<<proxy>>`            |
| 10       | Email Provider               | Actor (tertiary)       |

> `OwnerVerification` and `UserAccount` are return types only in this communication view. The controller works through repositories and gateways, not by sending messages to entity participants.

## Messages

| #   | From -> To                                  | Message |
| --- | ------------------------------------------- | ------- |
| 1   | System Admin -> AdminUI                     | Verification Review Access |
| 1.1 | AdminUI -> ReviewVerificationController     | `GetPendingSubmissions(out response: List<SubmissionSummaryDto>)` |
| 1.2 | ReviewVerificationController -> IOwnerVerificationRepository | `FindPendingAsync(out records: List<OwnerVerification>)` |
| 1.3 | ReviewVerificationController -> IUserAccountRepository | `FindByIdAsync(in id: Guid, out owner: UserAccount)` |
| 1.4 | AdminUI -> System Admin                     | Pending Submissions List Display |
| 2   | System Admin -> AdminUI                     | Submission Selection |
| 2.1 | AdminUI -> ReviewVerificationController     | `GetSubmissionDetail(in verificationId: Guid, out response: SubmissionDetailResponseDto)` |
| 2.2 | ReviewVerificationController -> IOwnerVerificationRepository | `FindByIdAsync(in id: Guid, out verification: OwnerVerification)` |
| 2.3 | ReviewVerificationController -> IUserAccountRepository | `FindByIdAsync(in id: Guid, out owner: UserAccount)` |
| 2.4 | ReviewVerificationController -> ICloudStorageGateway | `RetrieveDocumentsAsync(in documentRefs: List<string>, out documentUrls: List<string>)` |
| 2.5 | AdminUI -> System Admin                     | Submission Details with Documents Display |
| 3   | System Admin -> AdminUI                     | Approval Decision |
| 3.1 | AdminUI -> ReviewVerificationController     | `ApproveVerification(in verificationId: Guid, in dto: ReviewDecisionDto, out response: AdminDecisionResponseDto)` |
| 3.2 | ReviewVerificationController -> IOwnerVerificationRepository | `FindByIdAsync(in id: Guid, out verification: OwnerVerification)` |
| 3.3 | ReviewVerificationController -> VerificationLogic | `ValidateDecision(in verification: OwnerVerification, out result: ValidationResult)` |
| 3.4 | ReviewVerificationController -> IOwnerVerificationRepository | `UpdateAsync(in entity: OwnerVerification, out persisted: OwnerVerification)` |
| 3.5 | ReviewVerificationController -> IUserAccountRepository | `FindByIdAsync(in id: Guid, out owner: UserAccount)` |
| 3.6 | ReviewVerificationController -> IEmailGateway | `SendAsync(in message: EmailMessage)` |
| 3.7 | IEmailGateway -> Email Provider             | `SendAsync(in message: EmailMessage)` |
| 3.8 | AdminUI -> System Admin                     | Decision Success Message Display |

## Alternative Flow Notes

- `3.1a Reject path` - `RejectVerification(in verificationId: Guid, in dto: ReviewDecisionDto, out response: AdminDecisionResponseDto)` follows the same repository, validation, update, owner lookup, and email dispatch pattern.
- `3.3 Validation fails` - `ValidationResult.IsValid = false`, so the controller returns an error response without updating the verification.
- `3.1a Reject path input rule` - rejection requires a non-empty review note before the controller proceeds.
- `3.6-3.7 Email fails` - notification failure does not roll back the approved or rejected verification status.

## Notes

- `AdminUI` is shown explicitly - the system admin does not interact directly with the backend controller.
- `ReviewVerificationController` is stateless, so the decision sequence re-fetches the verification before validation and update.
- `VerificationLogic` encapsulates `ValidateDecision(...)`.
- `IOwnerVerificationRepository` is the only persistence wrapper that mutates verification state in this use case.
- `IUserAccountRepository` is used to enrich list/detail responses and to resolve the owner email target before dispatch.
- `ICloudStorageGateway` retrieves document URLs from external storage for review.
- `IEmailGateway` dispatches approval or rejection notifications in a fire-and-forget manner.
- The old `OwnerProfile` / `IOwnerProfileRepository` update path is intentionally removed because it does not exist in the actual controller implementation.
