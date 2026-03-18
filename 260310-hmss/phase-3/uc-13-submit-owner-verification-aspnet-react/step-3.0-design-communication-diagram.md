# Design Communication Diagram: UC-13 Submit Owner Verification - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: `OwnerUI -> SubmitOwnerVerificationController`, then `Controller -> Repository`, `Controller -> VerificationLogic`, and `Controller -> ICloudStorageGateway`
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label when a response payload is expected
- Separate reply arrows are intentionally omitted because `out` parameters already represent returned data
- Request flow style: synchronous request handling

## Object Layout

```text
Owner --- OwnerUI --- SubmitVerificationController
                       |--- IOwnerVerificationRepository --- OwnerVerification
                       |--- VerificationLogic
                       |--- ICloudStorageGateway --- Cloud Storage
```

## Participants

| Position | Object                       | Stereotype             |
| -------- | ---------------------------- | ---------------------- |
| 1        | Owner                        | Actor (primary)        |
| 2        | OwnerUI                      | `<<user interaction>>` |
| 3        | SubmitVerificationController | `<<coordinator>>`      |
| 4        | VerificationLogic           | `<<business logic>>`   |
| 5        | ICloudStorageGateway         | `<<proxy>>`            |
| 6        | Cloud Storage                | Actor (secondary)      |
| 7        | IOwnerVerificationRepository  | `<<database wrapper>>` |
| 8        | OwnerVerification            | `<<data abstraction>>` |

## Messages

| #   | From -> To                                  | Message                                                            |
| --- | ------------------------------------------- | ------------------------------------------------------------------ |
| 1   | Owner -> OwnerUI                            | Verification Access                                                |
| 1.1 | OwnerUI -> SubmitVerificationController      | `getVerificationForm(in ownerId: Guid, out response: VerificationFormDto)` |
| 1.2 | OwnerUI -> Owner                            | Form Display                                                        |
| 2   | Owner -> OwnerUI                            | Information and Documents Input                                    |
| 2.1 | OwnerUI -> SubmitVerificationController      | `processVerificationDetails(in request: VerificationDraftDto, in documents: FileList, out response: ProcessVerificationResponseDto)` |
| 2.2 | SubmitVerificationController -> VerificationLogic | `validateRequiredFields(in request: VerificationDraftDto, out result: ValidationResult)` |
| 2.3 | SubmitVerificationController -> ICloudStorageGateway | `uploadDocuments(in documents: FileList, out documentUrls: List<String>)` |
| 2.4 | ICloudStorageGateway -> Cloud Storage       | `uploadDocuments(in documents: FileList, out documentUrls: List<String>)` |
| 2.5 | OwnerUI -> Owner                            | Verification Review Display                                        |
| 3   | Owner -> OwnerUI                            | Submission Confirmation                                           |
| 3.1 | OwnerUI -> SubmitVerificationController      | `submitVerification(in request: VerificationDraftDto, in documentUrls: List<String>, out response: SubmissionResponseDto)` |
| 3.2 | SubmitVerificationController -> IOwnerVerificationRepository | `save(in entity: OwnerVerification, out persisted: OwnerVerification)` |
| 3.3 | OwnerUI -> Owner                            | Submission Success Message                                         |

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
| ----------------- | -------------- | ----- |
| `1.1` OwnerUI -> SubmitVerificationCoordinator: "Verification Form Request" | `1.1` OwnerUI -> SubmitVerificationController: `getVerificationForm(in ownerId: Guid, out response: VerificationFormDto)` | sync, renamed |
| `2.1` OwnerUI -> SubmitVerificationCoordinator: "Validation and Upload Request" | `2.1` OwnerUI -> SubmitVerificationController: `processVerificationDetails(in request: VerificationDraftDto, in documents: FileList, out response: ProcessVerificationResponseDto)` | sync, renamed |
| `2.2` SubmitVerificationCoordinator -> VerificationRules: "Required Fields Validation Check" | `2.2` SubmitVerificationController -> VerificationLogic: `validateRequiredFields(in request: VerificationDraftDto, out result: ValidationResult)` | sync |
| `2.4` SubmitVerificationCoordinator -> CloudStorageProxy: "Document Upload Request" | `2.3` SubmitVerificationController -> ICloudStorageGateway: `uploadDocuments(in documents: FileList, out documentUrls: List<String>)` | sync with reply |
| `3.1` OwnerUI -> SubmitVerificationCoordinator: "Submission Request" | `3.1` OwnerUI -> SubmitVerificationController: `submitVerification(in request: VerificationDraftDto, in documentUrls: List<String>, out response: SubmissionResponseDto)` | sync, renamed |
| `3.2` SubmitVerificationCoordinator -> OwnerVerification: "New Verification Record" | `3.2` SubmitVerificationController -> IOwnerVerificationRepository: `save(in entity: OwnerVerification, out persisted: OwnerVerification)` | sync, DTO mapping implicit |

## Alternative Flow Notes

- **Step 2.2: Validation fails** - `ValidationResult.isValid = false`, response contains missing fields, messages 2.3-2.4 skipped, returns to step 2
- **Step 2.3: Cloud Storage unavailable** - Gateway returns failure, response contains upload error, returns to step 2
- **Step 3.2: Database error on save** - Repository throws exception, response contains error, use case ends

## Notes

- `OwnerUI` is shown explicitly so the human actor does not interact directly with the backend controller.
- `IOwnerVerificationRepository` handles persistence and returns the created `OwnerVerification` entity.
- `SubmitVerificationController` acts as the simplified orchestration point.
- `VerificationLogic` encapsulates verification field validation: required personal information fields, document completeness check.
- `ICloudStorageGateway` handles synchronous document upload. Returns `documentUrls` in `out` parameter for entity storage and UI preview.
- **Implicit Instantiation (Between 3.1 and 3.2)**: As in standard COMET creation use cases, the `SubmitVerificationController` implicitly instantiates the `OwnerVerification` (`<<data abstraction>>`) object in memory using parameters mapped from the `VerificationDraftDto` and the `documentUrls` before passing it to the database wrapper. Keeping this instantiation implicit prevents visual clutter on the final design diagram.
- **Handling the Proxy Timeout (Alternative Step 4.1)**: Message 2.3 to the `ICloudStorageGateway` involves crossing a network boundary. The `<<proxy>>` object must be programmed with a strict connection timeout limit. If the `Cloud Storage` actor fails to respond, the Proxy will return a failure exception or invalid result to the Controller, fulfilling the second alternative sequence and ensuring the Controller thread is not blocked indefinitely.
- **Stateless Coordinator Compliance**: Because web controllers must remain stateless to support scalability, the Controller operates across two distinct sequences (Validation/Upload in Sequence 2 and Saving in Sequence 3). The UI passes both the `VerificationDraftDto` and the newly acquired `documentUrls` back to the Controller in Sequence 3 (Message 3.1) so that the Controller does not have to unlawfully preserve user state in its memory between HTTP requests.
- **Parameter Forwarding**: `documentUrls` captured in sequence 2 are passed back to the controller in sequence 3 via `submitVerification(in request: VerificationDraftDto, in documentUrls)`. This maintains statelessness while preserving data between the two interactions.
- **Initial verification state**: Newly created verification records have `status = PendingReview` and await admin review.
- Actor-to-UI messages (1, 1.2, 2, 2.5, 3, 3.3) use noun phrases because they represent physical user interactions, not code method calls.
