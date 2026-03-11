# Communication Diagram: UC-16 Review Owner Verification - Main Sequence (Approve)

## Object Layout

```text
System Admin --- VerificationReviewUI --- VerificationCoordinator --- VerificationLogic --- OwnerVerification
                                                     |
                                                     --- CloudStorageProxy --- Cloud Storage
                                                     |
                                                     --- NotificationService
                                                     |
                                                     --- EmailProxy --- Email Provider
```

## Participants

| Position | Object | Stereotype |
|---|---|---|
| 1 | System Admin | Actor (primary) |
| 2 | VerificationReviewUI | `<<user interaction>>` |
| 3 | VerificationCoordinator | `<<coordinator>>` |
| 4 | VerificationLogic | `<<business logic>>` |
| 5 | OwnerVerification | `<<entity>>` |
| 6 | CloudStorageProxy | `<<proxy>>` |
| 7 | Cloud Storage | Actor (secondary) |
| 8 | NotificationService | `<<service>>` |
| 9 | EmailProxy | `<<proxy>>` |
| 10 | Email Provider | Actor (secondary) |

## Messages

| # | From -> To | Message |
|---|---|---|
| 1 | System Admin -> VerificationReviewUI | Owner Verification Review Access |
| 1.1 | VerificationReviewUI -> VerificationCoordinator | Pending Verification List Request |
| 1.2 | VerificationCoordinator -> VerificationLogic | Pending Verification List Request |
| 1.3 | VerificationLogic -> OwnerVerification | Pending Verification List Request |
| 1.4 | OwnerVerification -> VerificationLogic | Pending Verification List |
| 1.5 | VerificationLogic -> VerificationCoordinator | Pending Verification List |
| 1.6 | VerificationCoordinator -> VerificationReviewUI | Pending Verification List |
| 1.7 | VerificationReviewUI -> System Admin | Pending Verification List |
| 2 | System Admin -> VerificationReviewUI | Verification Submission Selection |
| 2.1 | VerificationReviewUI -> VerificationCoordinator | Verification Submission Detail Request |
| 2.2 | VerificationCoordinator -> VerificationLogic | Verification Submission Detail Request |
| 2.3 | VerificationLogic -> OwnerVerification | Verification Submission Detail Request |
| 2.4 | OwnerVerification -> VerificationLogic | Verification Submission Detail and Document References |
| 2.5 | VerificationLogic -> VerificationCoordinator | Verification Submission Detail and Document References |
| 2.6 | VerificationCoordinator -> CloudStorageProxy | Supporting Documents Request |
| 2.7 | CloudStorageProxy -> Cloud Storage | Supporting Documents Request |
| 2.8 | Cloud Storage -> CloudStorageProxy | Supporting Documents |
| 2.9 | CloudStorageProxy -> VerificationCoordinator | Supporting Documents |
| 2.10 | VerificationCoordinator -> VerificationReviewUI | Verification Submission Detail and Supporting Documents |
| 2.11 | VerificationReviewUI -> System Admin | Verification Submission Detail and Supporting Documents |
| 3 | System Admin -> VerificationReviewUI | Verification Decision |
| 3.1 | VerificationReviewUI -> VerificationCoordinator | Verification Decision |
| 3.2 | VerificationCoordinator -> VerificationLogic | Verification Decision |
| 3.3 | VerificationLogic -> OwnerVerification | Verification Status Record |
| 3.4 | OwnerVerification -> VerificationLogic | Verification Status Record |
| 3.5 | VerificationLogic -> VerificationCoordinator | Verification Decision Result |
| 3.6 | VerificationCoordinator -> NotificationService | Owner Notification Request |
| 3.7 | NotificationService -> VerificationCoordinator | Owner Notification |
| 3.8 | VerificationCoordinator -> EmailProxy | Owner Notification |
| 3.9 | EmailProxy -> Email Provider | Owner Notification |
| 3.10 | Email Provider -> EmailProxy | Notification Delivery Result |
| 3.11 | EmailProxy -> VerificationCoordinator | Notification Delivery Result |
| 3.12 | VerificationCoordinator -> VerificationReviewUI | Verification Review Outcome |
| 3.13 | VerificationReviewUI -> System Admin | Verification Review Confirmation |

## Notes

- Main sequence shows the `Approve` path. The `Reject` path keeps the same structure but records status `Rejected` instead.
- `VerificationCoordinator` obtains supporting documents through `CloudStorageProxy` before the decision is finalized.
- Messages are kept at analysis level and avoid method-style naming.

Use `/drawio` to generate a visual `.drawio` file from this blueprint.
