# Design Communication Diagram: UC-17 Manage User Account Status - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: `AdminUI -> Controller`, then `Controller -> Repository`, `Controller -> Domain Object`, `Controller -> infrastructure collaborators`
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label when a response payload is expected
- Separate reply arrows are intentionally omitted because `out` parameters already represent returned data
- Request flow style: synchronous request handling with asynchronous email dispatch

## Object Layout

```text
System Admin --- AdminUI --- UserAccountAdminController
                              |--- IUserAccountRepository --- UserAccount
                              |--- AccountStatusNotificationService
                              |--- IEmailGateway --- Email Provider
```

## Participants

| Position | Object | Stereotype |
| --- | --- | --- |
| 1 | System Admin | Actor (primary) |
| 2 | AdminUI | `<<user interaction>>` |
| 3 | UserAccountAdminController | `<<coordinator>>` |
| 4 | IUserAccountRepository | `<<database wrapper>>` |
| 5 | UserAccount | `<<data abstraction>>` |
| 6 | AccountStatusNotificationService | `<<service>>` |
| 7 | IEmailGateway | `<<proxy>>` |
| 8 | Email Provider | Actor (secondary) |

## Messages

| # | From -> To | Message |
| --- | --- | --- |
| 1 | System Admin -> AdminUI | `viewUserAccountList()` |
| 1.1 | AdminUI -> UserAccountAdminController | `getUserAccountList(out response: UserAccountListResponseDto)` |
| 1.2 | UserAccountAdminController -> IUserAccountRepository | `findManageableUserAccounts(out userAccounts: UserAccountList)` |
| 2 | System Admin -> AdminUI | `selectUserAccount(in userAccountId: Guid)` |
| 2.1 | AdminUI -> UserAccountAdminController | `getUserAccountDetail(in userAccountId: Guid, out response: UserAccountDetailResponseDto)` |
| 2.2 | UserAccountAdminController -> IUserAccountRepository | `findById(in userAccountId: Guid, out userAccount: UserAccount)` |
| 3 | System Admin -> AdminUI | `submitStatusChange(in userAccountId: Guid, in requestedAction: AccountStatusActionDto)` |
| 3.1 | AdminUI -> UserAccountAdminController | `changeUserAccountStatus(in userAccountId: Guid, in request: ChangeUserAccountStatusRequestDto, out response: ChangeUserAccountStatusResponseDto)` |
| 3.2 | UserAccountAdminController -> IUserAccountRepository | `findById(in userAccountId: Guid, out userAccount: UserAccount)` |
| 3.3 | UserAccountAdminController -> UserAccount | `applyStatusChange(in action: AccountStatusActionDto, out changeResult: AccountStatusChangeResult)` |
| 3.4 | UserAccountAdminController -> IUserAccountRepository | `save(in userAccount: UserAccount, out persistedUserAccount: UserAccount)` |
| 3.5 | UserAccountAdminController -> AccountStatusNotificationService | `composeStatusChangedEmail(in userAccount: UserAccount, in changeResult: AccountStatusChangeResult, out emailMessage: EmailMessage)` |
| 3.6 | UserAccountAdminController -> IEmailGateway | `sendAsync(in emailMessage: EmailMessage)` |
| 3.7 | IEmailGateway -> Email Provider | `sendAsync(in emailMessage: EmailMessage)` |

## Alternative Flow Notes

- At message `2.1`, if no further status-management action is available for the selected account, `response` contains an empty allowed-action set and message group `3` is skipped.
- At message `3.3`, if the requested action is not permitted for the current account status, `changeResult` reports rejection and messages `3.4` to `3.7` are skipped.
- If the email provider is unavailable, the asynchronous email-processing path records notification failure separately while the persisted account-status change remains successful.

## Notes

- `AdminUI` is shown explicitly so the human actor does not interact directly with the backend controller.
- `IUserAccountRepository` handles persistence only — load and save. It returns a `UserAccount` domain object, not a raw record DTO.
- `UserAccount` (`<<data abstraction>>`) owns the status-change business rule via `applyStatusChange`. The controller does not contain business logic inline.
- `UserAccountAdminController` coordinates: load from repository → delegate mutation to domain object → persist → compose notification → dispatch async.
- Email dispatch is intentionally asynchronous to avoid blocking the main HTTP request on external provider latency.
