# Communication Diagram: UC-13 Submit Owner Verification - Analysis Model

## Object Layout

```text
Owner --- OwnerUI --- SubmitVerificationCoordinator --- VerificationRules --- OwnerVerification
                                      |
                                      --- CloudStorageProxy --- Cloud Storage
```

## Participants

| Position | Object                      | Stereotype             | Justification                                                                                                   |
| -------- | --------------------------- | ---------------------- | --------------------------------------------------------------------------------------------------------------- |
| 1        | Owner                       | Actor (primary)        | The human user initiating the verification submission.                                                          |
| 2        | OwnerUI                     | `<<user interaction>>` | Boundary object receiving physical inputs and displaying information.                                          |
| 3        | SubmitVerificationCoordinator | `<<coordinator>>`      | Control object sequencing the overall flow of the use case without holding state.                                |
| 4        | VerificationRules           | `<<business logic>>`   | Encapsulates the specific business rules for validating required personal information and document completeness. |
| 5        | CloudStorageProxy           | `<<proxy>>`            | Boundary object serving as the local representative of the external storage system, hiding technical details.     |
| 6        | Cloud Storage               | Actor (secondary)      | The external system actor receiving the uploaded documents.                                                     |
| 7        | OwnerVerification           | `<<entity>>`           | Conceptual data object encapsulating the newly submitted verification record.                                    |

## Messages (Main Sequence)

| #   | From -> To                                        | Message / Information Passed    | Use Case Step |
| --- | ------------------------------------------------- | ------------------------------- | ------------- |
| 1   | Owner -> OwnerUI                                  | Verification Access             | Step 1        |
| 1.1 | OwnerUI -> SubmitVerificationCoordinator           | Verification Form Request       |               |
| 1.2 | SubmitVerificationCoordinator -> OwnerUI           | Verification Form               |               |
| 1.3 | OwnerUI -> Owner                                  | Form Display                    | Step 2        |
| 2   | Owner -> OwnerUI                                  | Information and Documents Input  | Step 3        |
| 2.1 | OwnerUI -> SubmitVerificationCoordinator           | Validation and Upload Request    |               |
| 2.2 | SubmitVerificationCoordinator -> VerificationRules | Required Fields Validation Check | Step 4        |
| 2.3 | VerificationRules -> SubmitVerificationCoordinator | Validation Result (Valid)        |               |
| 2.4 | SubmitVerificationCoordinator -> CloudStorageProxy | Document Upload Request         | Step 4        |
| 2.5 | CloudStorageProxy -> Cloud Storage                | Document Upload                 |               |
| 2.6 | Cloud Storage -> CloudStorageProxy                | Upload Confirmation              |               |
| 2.7 | CloudStorageProxy -> SubmitVerificationCoordinator | Upload Result (Success)         |               |
| 2.8 | SubmitVerificationCoordinator -> OwnerUI           | Review Prompt                   |               |
| 2.9 | OwnerUI -> Owner                                  | Verification Review Display      | Step 5        |
| 3   | Owner -> OwnerUI                                  | Submission Confirmation          | Step 5        |
| 3.1 | OwnerUI -> SubmitVerificationCoordinator           | Submission Request               |               |
| 3.2 | SubmitVerificationCoordinator -> OwnerVerification | New Verification Record         | Step 6        |
| 3.3 | SubmitVerificationCoordinator -> OwnerUI           | Submission Success               | Step 7        |
| 3.4 | OwnerUI -> Owner                                  | Success Message                  |               |

## Alternative Sequences

| #    | From -> To                                        | Message / Information Passed      | Use Case Step    |
| ---- | ------------------------------------------------- | -------------------------------- | ---------------- |
| 2.3a | VerificationRules -> SubmitVerificationCoordinator | [Missing fields] Validation Result (Invalid) | Alt Step 4.1 |
| 2.4a | SubmitVerificationCoordinator -> OwnerUI         | Correction Prompt                |                  |
| 2.5a | OwnerUI -> Owner                                  | Correction Display               | Returns to 2     |
| 2.7b | CloudStorageProxy -> SubmitVerificationCoordinator | [Storage unavailable] Upload Result (Failure) | Alt Step 4.1 |
| 2.8b | SubmitVerificationCoordinator -> OwnerUI         | Upload Error Prompt              |                  |
| 2.9b | OwnerUI -> Owner                                  | Upload Error Display             | Returns to 2     |

## Architectural Notes

- **Explicit Validation Step**: Step 4 now explicitly includes validation before document upload. This ensures the alternative sequences for "missing fields" have a logical branching point. The system validates completeness before attempting external operations.
- **Analysis vs. Design**: In this analysis model, messages use descriptive noun phrases (e.g., `New Verification Record`) rather than operation signatures (e.g., `submitVerification(in, out)`).
- **External Service Integration**: Similar to UC-09/UC-10, this use case integrates with `Cloud Storage` external actor via `CloudStorageProxy` (`<<proxy>>`).
- **Separation of Concerns**: The `SubmitVerificationCoordinator` delegates: (1) validation to `VerificationRules` (`<<business logic>>`), (2) document upload to `CloudStorageProxy` (`<<proxy>>`), and (3) persistence to `OwnerVerification` (`<<entity>>`).
- **Explicit Returns**: The analysis model shows explicit data flow (e.g., `Upload Confirmation` in Message 2.6, `Upload Result (Success)` in Message 2.7). In the design phase, these will be embedded into `out` parameters of synchronous calls.

Use `/drawio-communication-diagram` to generate a visual `.drawio` file from this blueprint.
