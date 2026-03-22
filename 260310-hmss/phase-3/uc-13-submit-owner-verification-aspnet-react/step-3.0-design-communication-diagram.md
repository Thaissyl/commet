# Design Communication Diagram: UC-13 Submit Owner Verification - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: OwnerUI -> SubmitVerificationController, then Controller -> VerificationLogic, Controller -> ICloudStorageGateway, and Controller -> Repository
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label
- Separate reply arrows intentionally omitted; `out` parameters represent returned data
- Request flow style: synchronous request handling with validation-before-upload review flow

## Object Layout

```text
Owner --- OwnerUI --- SubmitVerificationController
                       |--- VerificationLogic
                       |--- ICloudStorageGateway --- Cloud Storage
                       |--- IOwnerVerificationRepository
```

## Participants

| Position | Object                       | Stereotype             |
| -------- | ---------------------------- | ---------------------- |
| 1        | Owner                        | Actor (primary)        |
| 2        | OwnerUI                      | `<<user interaction>>` |
| 3        | SubmitVerificationController | `<<coordinator>>`      |
| 4        | VerificationLogic            | `<<business logic>>`   |
| 5        | ICloudStorageGateway         | `<<proxy>>`            |
| 6        | Cloud Storage                | Actor (secondary)      |
| 7        | IOwnerVerificationRepository | `<<database wrapper>>` |

> `OwnerVerification` removed; return type only, no messages sent to it in this use case.

## Messages

| #   | From -> To                                  | Message                                                            |
| --- | ------------------------------------------- | ------------------------------------------------------------------ |
| 1   | Owner -> OwnerUI                            | Verification Submission Access                                     |
| 1.1 | OwnerUI -> SubmitVerificationController     | `GetVerificationForm(out response: VerificationFormResponseDto)` |
| 1.2 | OwnerUI -> Owner                            | Verification Form Display                                          |
| 2   | Owner -> OwnerUI                            | Verification Data and Documents Input                              |
| 2.1 | OwnerUI -> SubmitVerificationController     | `ValidateAndUploadDocuments(in request: VerificationSubmissionDto, in documents: IFormFileCollection, out response: VerificationReviewResponseDto)` |
| 2.2 | SubmitVerificationController -> VerificationLogic | `ValidateVerificationData(in request: VerificationSubmissionDto, out result: ValidationResult)` |
| 2.3 | SubmitVerificationController -> ICloudStorageGateway | `UploadImagesAsync(in documents: IFormFileCollection, out documentUrls: List<string>)` |
| 2.4 | ICloudStorageGateway -> Cloud Storage       | `UploadDocuments(in documents: IFormFileCollection, out urls: List<string>)` |
| 2.5 | OwnerUI -> Owner                            | Documents Review Display                                           |
| 3   | Owner -> OwnerUI                            | Submission Confirmation                                            |
| 3.1 | OwnerUI -> SubmitVerificationController     | `SubmitVerification(in request: VerificationSubmissionDto, in documentUrls: List<string>, out response: VerificationResponseDto)` |
| 3.2 | SubmitVerificationController -> IOwnerVerificationRepository | `SaveAsync(in entity: OwnerVerification, out persisted: OwnerVerification)` |
| 3.3 | OwnerUI -> Owner                            | Submission Success Message                                         |

## Analysis -> Design Message Mapping

| Analysis message | Design message | Notes |
|---|---|---|
| `1.1` OwnerUI -> SubmitVerificationCoordinator: "Verification Form Request" | `1.1` OwnerUI -> SubmitVerificationController: `GetVerificationForm(...)` | form retrieval |
| `2.1-2.3` OwnerUI -> SubmitVerificationCoordinator -> VerificationRules: "Validation and Upload Request" | `2.1-2.2` OwnerUI -> SubmitVerificationController -> VerificationLogic | validate required fields first |
| `2.4-2.7` SubmitVerificationCoordinator -> CloudStorageProxy -> Cloud Storage | `2.3-2.4` SubmitVerificationController -> ICloudStorageGateway -> Cloud Storage | upload only after validation succeeds |
| `3.1-3.2` OwnerUI -> SubmitVerificationCoordinator -> OwnerVerification | `3.1-3.2` OwnerUI -> SubmitVerificationController -> IOwnerVerificationRepository | persist final verification record |

## Alternative Flow Notes

- **Step 2.2: Validation fails** - `ValidationResult.IsValid = false`, upload is skipped, response includes errors
- **Step 2.3-2.4: Upload fails** - `ICloudStorageGateway.UploadImagesAsync()` returns empty or partial URLs, review cannot continue
- **Step 3.2: Save fails** - Repository exception handled, response contains error

## Notes

- `OwnerUI` shown explicitly; human actor does not interact directly with backend controller.
- `SubmitVerificationController` acts as stateless orchestration point.
- `VerificationLogic` encapsulates `ValidateVerificationData`; validation runs before any external upload.
- `ICloudStorageGateway` handles document upload to cloud storage after validation succeeds.
- `IOwnerVerificationRepository` persists `OwnerVerification` entity with uploaded document URLs.
- **Three-step process**: get form, validate-and-upload for review, then confirm final submission.
- **Implicit DTO mapping**: Controller implicitly maps data to response DTOs. Not shown as separate message.
- Actor-to-UI messages (1, 1.2, 2, 2.5, 3, 3.3) use noun phrases; physical user interactions, not code method calls.
