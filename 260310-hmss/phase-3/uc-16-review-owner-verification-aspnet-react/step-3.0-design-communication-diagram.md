# Design Communication Diagram: UC-16 Review Owner Verification - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: AdminUI -> ReviewVerificationController, then Controller -> Repository, Controller -> VerificationLogic, and supporting gateways
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label
- Separate reply arrows intentionally omitted — `out` parameters represent returned data
- Request flow style: synchronous request handling with dual entity modification pattern

## Object Layout

```text
System Admin --- AdminUI --- ReviewVerificationController
                              |--- VerificationLogic
                              |--- IOwnerVerificationRepository
                              |--- IOwnerProfileRepository
                              |--- ICloudStorageGateway --- Cloud Storage
                              |--- IEmailGateway --- Email Provider
```

## Participants

| Position | Object                        | Stereotype             |
| -------- | ----------------------------- | ---------------------- |
| 1        | System Admin                  | Actor (primary)        |
| 2        | AdminUI                       | `<<user interaction>>` |
| 3        | ReviewVerificationController  | `<<coordinator>>`      |
| 4        | VerificationLogic             | `<<business logic>>`   |
| 5        | IOwnerVerificationRepository  | `<<database wrapper>>` |
| 6        | IOwnerProfileRepository       | `<<database wrapper>>` |
| 7        | ICloudStorageGateway          | `<<proxy>>`            |
| 8        | Cloud Storage                 | Actor (secondary)      |
| 9        | IEmailGateway                 | `<<proxy>>`            |
| 10       | Email Provider                | Actor (tertiary)       |

> `OwnerVerification` and `OwnerProfile` removed — return types only, no messages sent to them in this use case.

## Messages

| #   | From -> To                                  | Message                                                            |
| --- | ------------------------------------------- | ------------------------------------------------------------------ |
| 1   | System Admin -> AdminUI                     | Verification Review Access                                         |
| 1.1 | AdminUI -> ReviewVerificationController     | `GetPendingVerifications(out response: PendingVerificationsResponseDto)` |
| 1.2 | ReviewVerificationController -> IOwnerVerificationRepository | `FindPendingAsync(out records: List<OwnerVerification>)` |
| 1.3 | AdminUI -> System Admin                     | Pending Verifications List Display                                |
| 2   | System Admin -> AdminUI                     | Verification Selection                                            |
| 2.1 | AdminUI -> ReviewVerificationController     | `GetVerificationDetail(in verificationId: Guid, out response: VerificationDetailResponseDto)` |
| 2.2 | ReviewVerificationController -> IOwnerVerificationRepository | `FindByIdAsync(in id: Guid, out record: OwnerVerification)` |
| 2.3 | ReviewVerificationController -> ICloudStorageGateway | `GetDocumentUrlsAsync(in documentUrls: List<string>, out docs: List<DocumentDto>)` |
| 2.4 | AdminUI -> System Admin                     | Verification Details with Documents Display                       |
| 3   | System Admin -> AdminUI                     | Verification Decision (Approve/Reject)                            |
| 3.1 | AdminUI -> ReviewVerificationController     | `ProcessVerificationDecision(in verificationId: Guid, in decision: DecisionDto, out response: DecisionResponseDto)` |
| 3.2 | ReviewVerificationController -> VerificationLogic | `ValidateVerificationReview(in record: OwnerVerification, in decision: string, out result: ValidationResult)` |
| 3.3 | ReviewVerificationController -> IOwnerVerificationRepository | `UpdateAsync(in entity: OwnerVerification, out persisted: OwnerVerification)` |
| 3.4 | ReviewVerificationController -> IOwnerProfileRepository | `UpdateAsync(in entity: OwnerProfile, out persisted: OwnerProfile)` |
| 3.5 | ReviewVerificationController -> IEmailGateway | `SendAsync(in message: EmailMessage)` |
| 3.6 | IEmailGateway -> Email Provider             | `SendAsync(in message: EmailMessage)` |
| 3.7 | AdminUI -> System Admin                     | Decision Confirmation Message                                     |

## Alternative Flow Notes

- **Step 3.2: Validation fails** — `ValidationResult.IsValid = false`, response includes reason
- **Step 3.3-3.4: Update fails** — Repository exception handled
- **Step 3.5-3.6: Email fails** — Exception caught, decision still successful

## Notes

- `AdminUI` shown explicitly — system admin does not interact directly with backend controller.
- `ReviewVerificationController` acts as stateless orchestration point.
- `VerificationLogic` encapsulates `ValidateVerificationReview` validation.
- `IOwnerVerificationRepository` updates verification record status.
- `IOwnerProfileRepository` updates owner verification flag if approved.
- `ICloudStorageGateway` provides access to uploaded verification documents.
- `IEmailGateway` notifies owner of verification decision.
- Actor-to-AdminUI messages use noun phrases — physical interactions, not code method calls.
