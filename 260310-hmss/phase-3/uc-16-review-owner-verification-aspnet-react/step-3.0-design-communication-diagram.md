# Design Communication Diagram: UC-16 Review Owner Verification - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: `AdminUI -> ReviewVerificationController`, then `Controller -> Repository`, `Controller -> VerificationLogic`, `Controller -> ICloudStorageGateway`, and `Controller -> IEmailGateway`
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label when a response payload is expected
- Separate reply arrows are intentionally omitted because `out` parameters already represent returned data
- Request flow style: synchronous request handling with dual entity modification pattern

## Object Layout

```text
System Admin --- AdminUI --- ReviewVerificationController
                              |--- VerificationLogic
                              |--- IOwnerVerificationRepository --- OwnerVerification
                              |--- IOwnerProfileRepository --- OwnerProfile
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
| 6        | OwnerVerification             | `<<data abstraction>>` |
| 7        | IOwnerProfileRepository       | `<<database wrapper>>` |
| 8        | OwnerProfile                  | `<<data abstraction>>` |
| 9        | ICloudStorageGateway          | `<<proxy>>`            |
| 10       | Cloud Storage                 | Actor (secondary)      |
| 11       | IEmailGateway                 | `<<proxy>>`            |
| 12       | Email Provider                | Actor (secondary)      |

## Messages

| #   | From -> To                                  | Message                                                            |
| --- | ------------------------------------------- | ------------------------------------------------------------------ |
| 1   | System Admin -> AdminUI                     | Verification Review Access                                         |
| 1.1 | AdminUI -> ReviewVerificationController      | `getPendingSubmissions(out response: SubmissionListResponseDto)`   |
| 1.2 | ReviewVerificationController -> IOwnerVerificationRepository | `findPending(out list: VerificationList)`                     |
| 1.3 | AdminUI -> System Admin                     | Pending Submissions Display                                        |
| 2   | System Admin -> AdminUI                     | Submission Selection                                               |
| 2.1 | AdminUI -> ReviewVerificationController      | `getSubmissionDetail(in verificationId: Guid, out response: SubmissionDetailResponseDto)` |
| 2.2 | ReviewVerificationController -> IOwnerVerificationRepository | `findById(in id: Guid, out entity: OwnerVerification)`          |
| 2.3 | ReviewVerificationController -> ICloudStorageGateway | `retrieveDocuments(in documentRefs: List<String>, out documents: FileList)` |
| 2.4 | ICloudStorageGateway -> Cloud Storage       | `retrieveDocuments(in documentRefs: List<String>, out documents: FileList)` |
| 2.5 | AdminUI -> System Admin                     | Review Interface Display                                           |
| 3   | System Admin -> AdminUI                     | Approval Decision                                                  |
| 3.1 | AdminUI -> ReviewVerificationController      | `approveVerification(in verificationId: Guid, in reviewNote: String, out response: DecisionResponseDto)` |
| 3.2 | ReviewVerificationController -> IOwnerVerificationRepository | `findById(in id: Guid, out entity: OwnerVerification)`          |
| 3.3 | ReviewVerificationController -> IOwnerProfileRepository | `findByVerificationId(in verificationId: Guid, out entity: OwnerProfile)` |
| 3.4 | ReviewVerificationController -> VerificationLogic | `validateDecision(in verification: OwnerVerification, out result: ValidationResult)` |
| 3.5 | ReviewVerificationController -> OwnerVerification | `approve(in reviewNote: String, out result: StatusChangeResult)` |
| 3.6 | ReviewVerificationController -> OwnerProfile | `verify(out result: StatusChangeResult)`                          |
| 3.7 | ReviewVerificationController -> IOwnerVerificationRepository | `update(in entity: OwnerVerification, out persisted: OwnerVerification)` |
| 3.8 | ReviewVerificationController -> IOwnerProfileRepository | `update(in entity: OwnerProfile, out persisted: OwnerProfile)` |
| 3.9 | ReviewVerificationController -> IEmailGateway | `sendAsync(in message: EmailMessage)`                              |
| 3.10| IEmailGateway -> Email Provider             | `sendAsync(in message: EmailMessage)`                              |
| 3.11| AdminUI -> System Admin                     | Decision Success Message                                           |

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
| ----------------- | -------------- | ----- |
| `1.1` AdminUI -> ReviewVerificationCoordinator: "Pending Submissions Query" | `1.1` AdminUI -> ReviewVerificationController: `getPendingSubmissions(out response: SubmissionListResponseDto)` | sync, renamed |
| `1.2` ReviewVerificationCoordinator -> OwnerVerification: "Pending Records Request" | `1.2` ReviewVerificationController -> IOwnerVerificationRepository: `findPending(out list: VerificationList)` | sync |
| `2.1` AdminUI -> ReviewVerificationCoordinator: "Submission Detail Query" | `2.1` AdminUI -> ReviewVerificationController: `getSubmissionDetail(in verificationId: Guid, out response: SubmissionDetailResponseDto)` | sync |
| `2.2` ReviewVerificationCoordinator -> OwnerVerification: "Submission Detail Request" | `2.2` ReviewVerificationController -> IOwnerVerificationRepository: `findById(in id: Guid, out entity: OwnerVerification)` | stateless reload |
| `2.4` ReviewVerificationCoordinator -> CloudStorageProxy: "Document Retrieval Request" | `2.3` ReviewVerificationController -> ICloudStorageGateway: `retrieveDocuments(in documentRefs: List<String>, out documents: FileList)` | sync with reply |
| `3.1` AdminUI -> ReviewVerificationCoordinator: "Approval Request" | `3.1` AdminUI -> ReviewVerificationController: `approveVerification(in verificationId: Guid, in reviewNote: String, out response: DecisionResponseDto)` | sync, renamed |
| `3.2` ReviewVerificationCoordinator -> VerificationRules: "Decision Validation Check" | `3.4` ReviewVerificationController -> VerificationLogic: `validateDecision(in verification, out result)` | delegated after fetching entities |
| `3.4` ReviewVerificationCoordinator -> OwnerVerification: "Approved Status Update" | `3.5` ReviewVerificationController -> OwnerVerification: `approve(in reviewNote: String, out result: StatusChangeResult)` | RAM mutation |
| `3.5` ReviewVerificationCoordinator -> OwnerProfile: "Verified Status Update" | `3.6` ReviewVerificationController -> OwnerProfile: `verify(out result: StatusChangeResult)` | RAM mutation |
| `3.6` ReviewVerificationCoordinator -> EmailProxy: "Owner Notification Request" | `3.9` ReviewVerificationController -> IEmailGateway: `sendAsync(in message: EmailMessage)` | async fire-and-forget |

## Alternative Flow Notes

- **Step 3.4: Validation fails** - `ValidationResult.isValid = false`, response contains validation error, messages 3.5-3.10 skipped, use case ends
- **Step 3.2: Verification not found** - Repository returns null/error, response contains not found error, use case ends
- **Step 3.3: Owner profile not found** - Repository returns null/error, response contains not found error, use case ends
- **Step 3.7/3.8: Database error on update** - Repository throws exception, response contains error, use case ends
- **Alternative: Reject decision** - Similar flow but uses `rejectVerification(in verificationId, in reviewNote, in rejectionReason)` endpoint, calls `reject(in reviewNote, in rejectionReason)` on OwnerVerification and `unverify()` on OwnerProfile
- **Step 2.3: Cloud Storage unavailable** - Gateway returns failure, response contains document retrieval error, use case continues without documents
- **Step 3.10: Email Provider unavailable** - Gateway records failure, decision succeeds, continues to step 3.11

## Notes

- `AdminUI` is shown explicitly so the human actor does not interact directly with the backend controller.
- `IOwnerVerificationRepository` and `IOwnerProfileRepository` handle persistence and return the updated entities.
- `ReviewVerificationController` acts as the simplified orchestration point.
- `VerificationLogic` encapsulates decision validation: verifies pending status, validates required fields completeness, ensures no conflicting verification states.
- `ICloudStorageGateway` handles synchronous document retrieval from external storage. Returns document files in `out` parameter for admin review.
- `IEmailGateway` handles asynchronous email dispatch. No `out` parameter because notifications are fire-and-forget.
- **Dual Entity Modification (Messages 3.2 - 3.8)**: Approving a verification modifies two distinct entities:
  - `OwnerVerification` status changes to `Approved` via `approve(in reviewNote)` method
  - `OwnerProfile` verification status changes to `Verified` via `verify()` method
  - Both mutations occur in RAM (messages 3.5, 3.6) before persistence (messages 3.7, 3.8)
- **Stateless Coordinator Compliance (Messages 1.2, 2.2, 3.2, 3.3)**: The controller executes fresh repository queries at the beginning of each sequence. Web controllers must remain stateless and cannot preserve entities in memory between user clicks.
- **Separation of State Mutation and Persistence (Messages 3.5, 3.6, 3.7, 3.8)**: Based on the Information Hiding principle, the controller invokes `approve()` on `OwnerVerification` and `verify()` on `OwnerProfile` so that objects mutate their own data safely in RAM. Immediately following, it calls `update()` on each repository to guarantee RAM mutations are persisted to disk.
- **Document Retrieval (Message 2.3)**: The `ICloudStorageGateway` retrieves documents synchronously because the admin UI must display them before making a decision. The `out documents: FileList` parameter provides the file data for display.
- **Asynchronous External Proxy (Message 3.9)**: The `IEmailGateway` uses `sendAsync(in message)` with no `out` parameter. The controller fires the notification to a background queue and immediately returns success to the user, preventing UI freeze if the Email Provider is slow or unavailable.
- **Decision Parameters**: The action (approve/reject) is implied by the endpoint name (`approveVerification`, `rejectVerification`). The `reviewNote` parameter captures admin comments, and rejection would additionally require `rejectionReason`.
- **Repository Query Patterns**:
  - `findPending(out list)` - Fetches all pending verification submissions (sequence 1)
  - `findById(in id: Guid)` - Fetches single entity by ID (sequences 2, 3)
  - `findByVerificationId(in verificationId: Guid)` - Fetches associated owner profile by verification ID (sequence 3)
- **Implicit DTO mapping**: The controller implicitly maps response data from entities to DTOs. This mapping is not shown as a separate message.
- Actor-to-UI messages (1, 1.3, 2, 2.5, 3, 3.11) use noun phrases because they represent physical user interactions, not code method calls.
