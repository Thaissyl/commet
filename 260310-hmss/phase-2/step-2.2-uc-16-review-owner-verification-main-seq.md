# Communication Diagram: UC-16 Review Owner Verification - Analysis Model

## Object Layout

```text
System Admin --- AdminUI --- ReviewVerificationCoordinator --- OwnerVerification
                                           |
                                           --- CloudStorageProxy --- Cloud Storage
                                           |
                                           --- EmailProxy --- Email Provider
```

## Participants

| Position | Object                         | Stereotype             | Justification                                                                                   |
| -------- | ------------------------------ | ---------------------- | ----------------------------------------------------------------------------------------------- |
| 1        | System Admin                   | Actor (primary)        | The human user initiating the verification review.                                             |
| 2        | AdminUI                        | `<<user interaction>>` | Boundary object receiving admin input and displaying review information.                        |
| 3        | ReviewVerificationCoordinator  | `<<coordinator>>`      | Control object sequencing the review flow without holding long-lived conversational state.      |
| 4        | OwnerVerification              | `<<entity>>`           | Conceptual data object encapsulating pending verification submissions and their review status.   |
| 5        | CloudStorageProxy              | `<<proxy>>`            | Boundary object hiding the technical details of the external document storage API.              |
| 6        | Cloud Storage                  | Actor (secondary)      | The external system storing supporting documents.                                               |
| 7        | EmailProxy                     | `<<proxy>>`            | Boundary object hiding the technical details of the external email system API.                  |
| 8        | Email Provider                 | Actor (secondary)      | The external system dispatching notification emails.                                           |

## Messages (Main Sequence - Approve Path)

| Seq No. | Sender -> Receiver                               | Message Label (Simple Message)   | Use Case Step |
| ------- | ------------------------------------------------ | -------------------------------- | ------------- |
| V1      | System Admin -> AdminUI                          | Verification Review Access       | Step 1        |
| V1.1    | AdminUI -> ReviewVerificationCoordinator         | Get Pending Submissions          |               |
| V1.2    | ReviewVerificationCoordinator -> OwnerVerification | Read Pending Submissions       |               |
| V1.3    | OwnerVerification -> ReviewVerificationCoordinator | Pending Submissions Data       |               |
| V1.4    | ReviewVerificationCoordinator -> AdminUI        | Pending Submissions Data         | Step 2        |
| V1.5    | AdminUI -> System Admin                          | Display Pending Submissions      |               |
| V2      | System Admin -> AdminUI                          | Select Submission                | Step 3        |
| V2.1    | AdminUI -> ReviewVerificationCoordinator         | Get Submission Details           |               |
| V2.2    | ReviewVerificationCoordinator -> CloudStorageProxy | Retrieve Documents Request     | Step 4        |
| V2.3    | CloudStorageProxy -> Cloud Storage               | Request Documents                |               |
| V2.4    | Cloud Storage -> CloudStorageProxy               | Documents Data                   |               |
| V2.5    | CloudStorageProxy -> ReviewVerificationCoordinator | Documents Data                 |               |
| V2.6    | ReviewVerificationCoordinator -> OwnerVerification | Read Submission Data           |               |
| V2.7    | OwnerVerification -> ReviewVerificationCoordinator | Submission Data                |               |
| V2.8    | ReviewVerificationCoordinator -> AdminUI        | Submission Details & Documents   | Step 4        |
| V2.9    | AdminUI -> System Admin                          | Display Review Interface         |               |
| V3      | System Admin -> AdminUI                          | Approve Submission               | Step 5        |
| V3.1    | AdminUI -> ReviewVerificationCoordinator         | Approval Request                 |               |
| V3.2    | ReviewVerificationCoordinator -> OwnerVerification | Update Status (Approved)       | Step 6, 7     |
| V3.3    | ReviewVerificationCoordinator -> EmailProxy      | Send Notification Request        | Step 8        |
| V3.4    | EmailProxy -> Email Provider                     | Send Email Notification          |               |
| V3.5    | ReviewVerificationCoordinator -> AdminUI        | Approval Success                 | Step 9        |
| V3.6    | AdminUI -> System Admin                          | Display Success Message          |               |

## Alternative Sequences

| Seq No. | Sender -> Receiver                               | Message Label (Simple Message)                         | Use Case Step |
| ------- | ------------------------------------------------ | ------------------------------------------------------ | ------------- |
| V3.1a   | AdminUI -> ReviewVerificationCoordinator         | [Reject] Rejection Request                             | Alt Step 5.1  |
| V3.2a   | ReviewVerificationCoordinator -> OwnerVerification | Update Status (Rejected)                             | Alt Step 5.1  |
| V3.4a   | EmailProxy -> ReviewVerificationCoordinator      | [Provider unavailable] Delivery Failure                | Alt Step 8.1  |
| V3.5a   | ReviewVerificationCoordinator -> AdminUI        | Review Success (notification failed recorded)          | Continues to V3.6 |

## Architectural Notes

- **Direct Review Flow**: This revised analysis keeps the review centered on `OwnerVerification`. The coordinator reads pending submissions, loads submission details, updates the submission status, and triggers notification without separate `VerificationRules` or `OwnerProfile` participants.
- **Cloud Storage Integration**: Step V2 explicitly retrieves supporting documents from the `Cloud Storage` secondary actor through `CloudStorageProxy` before the admin reviews the submission.
- **Status Update Scope**: Step V3.2 captures the approved decision and verified-status update on the verification submission in one simple analysis message.
- **Notification Separation**: Notification dispatch is still modeled as a boundary crossing through `EmailProxy` to the external `Email Provider`.
- **Analysis vs. Design**: This analysis model uses descriptive message labels such as `Get Submission Details` and `Update Status (Approved)` rather than code-level operation signatures.

Use `/drawio-communication-diagram` to generate a visual `.drawio` file from this blueprint.
