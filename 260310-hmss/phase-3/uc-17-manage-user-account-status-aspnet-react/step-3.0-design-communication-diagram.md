# Design Communication Diagram: UC-17 Manage User Account Status - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: `AdminUI -> Controller`, then `Controller -> Repository` and `Controller -> infrastructure collaborators`
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label when a response payload is expected
- Separate reply arrows are intentionally omitted because `out` parameters already represent returned data
- Request flow style: synchronous request handling with asynchronous email dispatch

## Object Layout

```text
System Admin --- AdminUI --- UserAccountAdminController
                              |--- IUserAccountRepository
                              |--- AccountStatusNotificationService
                              |--- IEmailGateway --- Email Provider
```

## Participants

| Position | Object | Stereotype |
| --- | --- | --- |
| 1 | System Admin | Actor (primary) |
| 2 | AdminUI | `<<user interaction>>` |
| 3 | UserAccountAdminController | `<<boundary>>` |
| 4 | IUserAccountRepository | `<<database wrapper>>` |
| 5 | AccountStatusNotificationService | `<<service>>` |
| 6 | IEmailGateway | `<<proxy>>` |
| 7 | Email Provider | Actor (secondary) |

## Messages

| # | From -> To | Message |
| --- | --- | --- |
| 1 | System Admin -> AdminUI | `viewUserAccountList()` |
| 1.1 | AdminUI -> UserAccountAdminController | `getUserAccountList(out response: UserAccountListResponseDto)` |
| 1.2 | UserAccountAdminController -> IUserAccountRepository | `findManageableUserAccounts(out userAccounts: UserAccountList)` |
| 2 | System Admin -> AdminUI | `selectUserAccount(in userAccountId: Guid)` |
| 2.1 | AdminUI -> UserAccountAdminController | `getUserAccountDetail(in userAccountId: Guid, out response: UserAccountDetailResponseDto)` |
| 2.2 | UserAccountAdminController -> IUserAccountRepository | `findById(in userAccountId: Guid, out userAccountRecord: UserAccountRecord)` |
| 3 | System Admin -> AdminUI | `submitStatusChange(in userAccountId: Guid, in requestedAction: AccountStatusActionDto)` |
| 3.1 | AdminUI -> UserAccountAdminController | `changeUserAccountStatus(in userAccountId: Guid, in request: ChangeUserAccountStatusRequestDto, out response: ChangeUserAccountStatusResponseDto)` |
| 3.2 | UserAccountAdminController -> IUserAccountRepository | `findById(in userAccountId: Guid, out userAccountRecord: UserAccountRecord)` |
| 3.3 | UserAccountAdminController -> IUserAccountRepository | `save(in userAccountRecord: UserAccountRecord, out persistedUserAccountRecord: UserAccountRecord)` |
| 3.4 | UserAccountAdminController -> AccountStatusNotificationService | `composeStatusChangedEmail(in userAccountRecord: UserAccountRecord, in changeResult: AccountStatusChangeResult, out emailMessage: EmailMessage)` |
| 3.5 | UserAccountAdminController -> IEmailGateway | `sendAsync(in emailMessage: EmailMessage)` |
| 3.6 | IEmailGateway -> Email Provider | `sendAsync(in emailMessage: EmailMessage)` |

## Alternative Flow Notes

- At message `2.1`, if no further status-management action is available for the selected account, `response` contains an empty allowed-action set and message group `3` is skipped.
- Between messages `3.2` and `3.3`, the controller validates that the requested action is still permitted for the current account status before persisting the update.
- If the requested action is no longer permitted, the response reports failure and messages `3.3` to `3.6` are skipped.
- If the email provider is unavailable, the asynchronous email-processing path records notification failure separately while the persisted account-status change remains successful.

## Notes

- `AdminUI` is shown explicitly so the human actor does not interact directly with the backend controller.
- `IUserAccountRepository` handles persistence access and returns account records that the controller validates and updates in this simplified ASP.NET-oriented design.
- `UserAccountAdminController` remains a backend boundary object in this stack-specific design, while also acting as the simplified orchestration point for this use case.
- Email dispatch is intentionally asynchronous to avoid blocking the main HTTP request on external provider latency.
