# Communication Diagram: UC-13 Submit Owner Verification - Main Sequence

## Object Layout

```text
Owner --- VerificationSubmissionUI --- VerificationCoordinator --- VerificationLogic --- OwnerVerification
                                                 |
                                                 --- CloudStorageProxy --- Cloud Storage
```

## Participants

| Position | Object | Stereotype |
|---|---|---|
| 1 | Owner | Actor (primary) |
| 2 | VerificationSubmissionUI | `<<user interaction>>` |
| 3 | VerificationCoordinator | `<<coordinator>>` |
| 4 | VerificationLogic | `<<business logic>>` |
| 5 | OwnerVerification | `<<entity>>` |
| 6 | CloudStorageProxy | `<<proxy>>` |
| 7 | Cloud Storage | Actor (secondary) |

## Messages

| # | From -> To | Message |
|---|---|---|
| 1 | Owner -> VerificationSubmissionUI | Owner Verification Submission Access |
| 1.1 | VerificationSubmissionUI -> VerificationCoordinator | Verification Submission Form Request |
| 1.2 | VerificationCoordinator -> VerificationLogic | Verification Requirements Request |
| 1.3 | VerificationLogic -> VerificationCoordinator | Verification Requirements |
| 1.4 | VerificationCoordinator -> VerificationSubmissionUI | Verification Submission Form |
| 1.5 | VerificationSubmissionUI -> Owner | Verification Submission Form |
| 2 | Owner -> VerificationSubmissionUI | Verification Information and Documents |
| 2.1 | VerificationSubmissionUI -> VerificationCoordinator | Verification Information and Documents |
| 2.2 | VerificationCoordinator -> CloudStorageProxy | Verification Documents |
| 2.3 | CloudStorageProxy -> Cloud Storage | Verification Documents |
| 2.4 | Cloud Storage -> CloudStorageProxy | Document References |
| 2.5 | CloudStorageProxy -> VerificationCoordinator | Document References |
| 2.6 | VerificationCoordinator -> VerificationSubmissionUI | Verification Submission Review |
| 2.7 | VerificationSubmissionUI -> Owner | Verification Submission Review |
| 3 | Owner -> VerificationSubmissionUI | Verification Submission Confirmation |
| 3.1 | VerificationSubmissionUI -> VerificationCoordinator | Verification Submission Request |
| 3.2 | VerificationCoordinator -> VerificationLogic | Verification Submission Information |
| 3.3 | VerificationLogic -> OwnerVerification | Owner Verification Record |
| 3.4 | OwnerVerification -> VerificationLogic | Owner Verification Record |
| 3.5 | VerificationLogic -> VerificationCoordinator | Verification Submission Result |
| 3.6 | VerificationCoordinator -> VerificationSubmissionUI | Verification Submission Outcome |
| 3.7 | VerificationSubmissionUI -> Owner | Verification Submission Confirmation |

## Notes

- `VerificationCoordinator` handles document storage through `CloudStorageProxy` before the submission is confirmed.
- `VerificationLogic` encapsulates verification-submission rules and records the resulting `OwnerVerification`.
- Messages are kept at analysis level and avoid method-style naming.

Use `/drawio` to generate a visual `.drawio` file from this blueprint.
