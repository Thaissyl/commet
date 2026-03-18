# Communication Diagram: UC-16 Review Owner Verification - Analysis Model

## Object Layout

```text
System Admin --- AdminUI --- ReviewVerificationCoordinator --- VerificationRules --- OwnerVerification
                                           |                         |
                                           |                         --- OwnerProfile
                                           |
                                           --- CloudStorageProxy --- Cloud Storage
                                           |
                                           --- EmailProxy --- Email Provider
```

## Participants

| Position | Object                    | Stereotype             | Justification                                                                                           |
| -------- | ------------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------- |
| 1        | System Admin              | Actor (primary)        | The human user initiating the review.                                                                  |
| 2        | AdminUI                   | `<<user interaction>>` | Boundary object receiving physical inputs and displaying information.                                   |
| 3        | ReviewVerificationCoordinator | `<<coordinator>>`      | Control object sequencing the overall flow of the use case without holding state.                        |
| 4        | VerificationRules         | `<<business logic>>`   | Encapsulates the business rules for validating administrative decisions.                                 |
| 5        | CloudStorageProxy         | `<<proxy>>`            | Boundary object hiding the technical details of the external document storage API.                       |
| 6        | Cloud Storage             | Actor (secondary)      | The external system storing the physical documents.                                                     |
| 7        | OwnerVerification         | `<<entity>>`           | Conceptual data object encapsulating the pending verification submission record.                        |
| 8        | OwnerProfile              | `<<entity>>`           | Conceptual data object encapsulating the owner's system-wide account status.                             |
| 9        | EmailProxy                | `<<proxy>>`            | Boundary object hiding the external email system API.                                                   |
| 10       | Email Provider            | Actor (secondary)      | The external system dispatching notifications.                                                           |

## Messages (Main Sequence - Approve Path)

| #   | From -> To                                        | Message / Information Passed        | Use Case Step |
| --- | ------------------------------------------------- | ----------------------------------- | ------------- |
| 1   | System Admin -> AdminUI                           | Verification Review Access         | Step 1        |
| 1.1 | AdminUI -> ReviewVerificationCoordinator          | Pending Submissions Query          |               |
| 1.2 | ReviewVerificationCoordinator -> OwnerVerification | Pending Records Request            |               |
| 1.3 | OwnerVerification -> ReviewVerificationCoordinator | Pending Records Data               |               |
| 1.4 | ReviewVerificationCoordinator -> AdminUI         | Pending Submissions List            | Step 2        |
| 1.5 | AdminUI -> System Admin                           | Pending Submissions Display         |               |
| 2   | System Admin -> AdminUI                           | Submission Selection                | Step 3        |
| 2.1 | AdminUI -> ReviewVerificationCoordinator          | Submission Detail Query            |               |
| 2.2 | ReviewVerificationCoordinator -> OwnerVerification | Submission Detail Request         |               |
| 2.3 | OwnerVerification -> ReviewVerificationCoordinator | Submission Detail Data             |               |
| 2.4 | ReviewVerificationCoordinator -> CloudStorageProxy | Document Retrieval Request         | Step 4        |
| 2.5 | CloudStorageProxy -> Cloud Storage                | Document Request                    |               |
| 2.6 | Cloud Storage -> CloudStorageProxy                | Document Data                       |               |
| 2.7 | CloudStorageProxy -> ReviewVerificationCoordinator | Document Files                     |               |
| 2.8 | ReviewVerificationCoordinator -> AdminUI         | Submission Details and Documents    | Step 4        |
| 2.9 | AdminUI -> System Admin                           | Review Interface Display            |               |
| 3   | System Admin -> AdminUI                           | Approval Decision                   | Step 5        |
| 3.1 | AdminUI -> ReviewVerificationCoordinator          | Approval Request                    |               |
| 3.2 | ReviewVerificationCoordinator -> VerificationRules | Decision Validation Check         |               |
| 3.3 | VerificationRules -> ReviewVerificationCoordinator | Validation Result (Valid)         |               |
| 3.4 | ReviewVerificationCoordinator -> OwnerVerification | Approved Status Update             | Step 6        |
| 3.5 | ReviewVerificationCoordinator -> OwnerProfile    | Verified Status Update             | Step 7        |
| 3.6 | ReviewVerificationCoordinator -> EmailProxy       | Owner Notification Request         | Step 8        |
| 3.7 | EmailProxy -> Email Provider                      | Owner Notification                  |               |
| 3.8 | ReviewVerificationCoordinator -> AdminUI         | Decision Success                    | Step 9        |
| 3.9 | AdminUI -> System Admin                           | Success Message Display             |               |

## Alternative Sequences

| #    | From -> To                                        | Message / Information Passed                     | Use Case Step    |
| ---- | ------------------------------------------------- | ---------------------------------------------- | ---------------- |
| 3.1a | AdminUI -> ReviewVerificationCoordinator          | [Reject] Rejection Request                      | Alt Step 5.1     |
| 3.4a | ReviewVerificationCoordinator -> OwnerVerification | Rejected Status Update                         | Alt Step 5.1     |
| 3.5a | ReviewVerificationCoordinator -> OwnerProfile    | Rejected Status Update                          | Continues to 3.6  |
| 3.7a | EmailProxy -> ReviewVerificationCoordinator      | [Provider unavailable] Delivery Failure        | Alt Step 8.1     |
| 3.8a | ReviewVerificationCoordinator -> AdminUI         | Decision Success (notification failed recorded) | Continues to 3.8  |

## Architectural Notes

- **Explicit Approve Path**: The main sequence explicitly describes the "Approve" scenario (primary success). The "Reject" scenario is entirely moved to alternative sequences.
- **Two Entity Updates**: Approving updates BOTH `OwnerVerification` (submission → Approved) AND `OwnerProfile` (overall status → Verified). This verifies the owner account system-wide, enabling UC-11 (Publish Room Listing).
- **External Actor Integration**: Step 4 explicitly retrieves documents from `Cloud Storage` secondary actor via `CloudStorageProxy` before displaying to admin.
- **Analysis vs. Design**: In this analysis model, messages use descriptive noun phrases (e.g., `Approved Status Update`, `Verified Status Update`) rather than operation signatures (e.g., `approveVerification(in, out)`).
- **Separation of Concerns**: The `ReviewVerificationCoordinator` delegates decision validation to `VerificationRules` (`<<business logic>>`), ensuring administrative decisions comply with business policies.

Use `/drawio-communication-diagram` to generate a visual `.drawio` file from this blueprint.
