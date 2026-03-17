# Design Communication Diagram: UC-17 Manage User Account Status

## Design Communication Decision

- Diagram level: design phase
- Message style: single directional function messages
- Each function message carries both `in` and `out` parameters in the same label
- Separate reply arrows are intentionally omitted to keep the diagram clean
- Interaction style: synchronous message passing
- MVC mapping: `AdminUI` acts as View, `AdminCoordinator` acts as Controller, and `UserManagementLogic`, `UserAccount`, `UserAccountDB`, `NotificationService`, and `EmailProxy` are model-side collaborators
- The analysis `User` entity is refined into `UserAccount <<data abstraction>>` and `UserAccountDB <<database wrapper>>` because user-account data is long-lived and assumed to be stored in a physical database

## Object Layout

```text
System Admin --- AdminUI --- AdminCoordinator --- UserManagementLogic
                                  |--- UserAccount
                                  |--- UserAccountDB
                                  |--- NotificationService
                                  |--- EmailProxy --- Email Provider
```

## Participants

| Position | Object | Stereotype |
| --- | --- | --- |
| 1 | System Admin | Actor (primary) |
| 2 | AdminUI | `<<user interaction>>` |
| 3 | AdminCoordinator | `<<coordinator>>` |
| 4 | UserManagementLogic | `<<business logic>>` |
| 5 | UserAccount | `<<data abstraction>>` |
| 6 | UserAccountDB | `<<database wrapper>>` |
| 7 | NotificationService | `<<service>>` |
| 8 | EmailProxy | `<<proxy>>` |
| 9 | Email Provider | Actor (secondary) |

## Messages

| # | From -> To | Message |
| --- | --- | --- |
| 1 | System Admin -> AdminUI | `accessUserAccountAdministration(out userAccountList)` |
| 1.1 | AdminUI -> AdminCoordinator | `getUserAccountList(out userAccountList)` |
| 1.2 | AdminCoordinator -> UserManagementLogic | `getUserAccountList(out userAccountList)` |
| 1.3 | UserManagementLogic -> UserAccountDB | `findUserAccountSummaries(out userAccountList)` |
| 2 | System Admin -> AdminUI | `selectUserAccount(in userAccountReference, out userAccountDetail, out availableStatusActions)` |
| 2.1 | AdminUI -> AdminCoordinator | `getUserAccountDetailAndAvailableStatusActions(in userAccountReference, out userAccountDetail, out availableStatusActions)` |
| 2.2 | AdminCoordinator -> UserManagementLogic | `getUserAccountDetailAndAvailableStatusActions(in userAccountReference, out userAccountDetail, out availableStatusActions)` |
| 2.3 | UserManagementLogic -> UserAccountDB | `findUserAccountByReference(in userAccountReference, out userAccount)` |
| 3 | System Admin -> AdminUI | `submitAccountStatusChange(in userAccountReference, in accountStatusAction, out accountStatusChangeOutcome)` |
| 3.1 | AdminUI -> AdminCoordinator | `applyAccountStatusChange(in userAccountReference, in accountStatusAction, out accountStatusChangeOutcome, out deliveryStatus)` |
| 3.2 | AdminCoordinator -> UserManagementLogic | `changeUserAccountStatus(in userAccountReference, in accountStatusAction, out accountStatusChangeOutcome)` |
| 3.3 | UserManagementLogic -> UserAccountDB | `findUserAccountByReference(in userAccountReference, out userAccount)` |
| 3.4 | UserManagementLogic -> UserAccount | `applyStatusTransition(in accountStatusAction, out accountStatusRecord)` |
| 3.5 | UserManagementLogic -> UserAccountDB | `saveUserAccountStatus(in userAccount, out accountStatusRecord)` |
| 3.6 | AdminCoordinator -> NotificationService | `composeUserAccountStatusChangeNotification(in userAccountReference, in accountStatusChangeOutcome, out userNotification)` |
| 3.7 | AdminCoordinator -> EmailProxy | `sendUserAccountStatusChangeNotification(in userNotification, out deliveryStatus)` |
| 3.8 | EmailProxy -> Email Provider | `sendNotification(in userNotification, out deliveryStatus)` |

## Alternative Flow Notes

- At message `2.2`, if the selected account has no further permitted status-management action, `out availableStatusActions` is empty and message group `3` is skipped.
- At messages `3.2` to `3.4`, `UserManagementLogic` revalidates that the requested action is still permitted for the current persisted account status.
- If the requested action is no longer permitted at execution time, message `3.2` yields a failure `accountStatusChangeOutcome`, messages `3.4` to `3.8` are skipped, and `deliveryStatus` is treated as `notAttempted`.
- If the email provider is unavailable, the account-status change still succeeds and `deliveryStatus` reports notification failure.

## Notes

- This is a design-phase communication diagram, so messages are function names rather than analysis-level noun phrases.
- `out` parameters inside the message label already imply returned data, so separate reply arrows are intentionally omitted.
- Persistence details are intentionally hidden behind `UserAccountDB`; the physical database is not shown as a separate participant in this version.
- `UserAccount` is kept as a `<<data abstraction>>` because the business transition is applied to an in-memory account object before the updated state is persisted.
