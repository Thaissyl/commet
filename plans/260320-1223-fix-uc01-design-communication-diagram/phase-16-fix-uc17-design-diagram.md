# Phase 16: Document Fix — Rewrite UC-17 step-3.0-design-communication-diagram.md

**Status:** Ready (no code changes needed)
**File:** `C:\Users\welterial\commet\260310-hmss\phase-3\uc-17-manage-user-account-status-aspnet-react\step-3.0-design-communication-diagram.md`

## Context Links

- Use case: `C:\Users\welterial\commet\260310-hmss\step-1.3-uc-17-manage-user-account-status.md`
- Analysis: `C:\Users\welterial\commet\260310-hmss\phase-2\step-2.2-uc-17-manage-user-account-status-main-seq.md`
- Code: `backend/Hmss.Api/Controllers/UserAccountAdminController.cs`

## Errors Being Fixed

| # | Error |
|---|-------|
| 1 | Participant `ManageAccountStatusController` → `UserAccountAdminController` |
| 2 | Participant `UserManagementLogic` — remove entirely; no such class in code; available actions determined inline via switch expression; validation handled inside `UserAccount.ChangeStatus()` |
| 3 | Add participant `AccountStatusNotificationService <<application logic>>` (explicitly called via `_notificationService.ComposeStatusChangedEmail(...)`) |
| 4 | Object layout: `IUserAccountRepository --- UserAccount` — remove; add `UserAccount` directly under controller (`user.ChangeStatus()` called directly) |
| 5 | Object layout: remove `UserManagementLogic` from layout |
| 6 | Add `AccountStatusNotificationService` under controller in layout |
| 7 | Msg 1.2: `findAll` → `FindManageableUserAccountsAsync`; `out list: AccountList` — `AccountList` invented; change to `out users: List<UserAccount>` |
| 8 | Msg 2.2: `findById` → `FindByIdAsync` |
| 9 | Msg 2.3: remove `getAvailableActions(UserManagementLogic, ...)` — no such call; actions determined inline in `GetUserAccountDetail` via switch expression on `user.AccountStatus`; not a separate object interaction |
| 10 | Msg 3.2: `findById` → `FindByIdAsync` |
| 11 | Msg 3.3: remove `validateStatusTransition(UserManagementLogic, ...)` — no such call; validation is internal to `UserAccount.ChangeStatus()` |
| 12 | Msg 3.4: `suspend(out result)` → `ChangeStatus(in action: String, out result: StatusChangeResult)` — unified method handles all transitions (Suspend/Enable/Disable); no separate `suspend/enable/disable` methods on entity |
| 13 | Add msg before email: `ComposeStatusChangedEmail(in user: UserAccount, in newStatus: String, out message: EmailMessage)` → `AccountStatusNotificationService` |
| 14 | Msg 3.5: `update` → `UpdateAsync` |

## Corrected Object Layout

```text
System Admin --- AdminUI --- UserAccountAdminController
                              |--- IUserAccountRepository
                              |--- AccountStatusNotificationService
                              |--- IEmailGateway --- Email Provider
                              |--- UserAccount
```

## Corrected Seq 3 Flow

- 3.1: `suspendAccount(in userId: Guid, out response: ChangeUserAccountStatusResponseDto)`
- 3.2: `FindByIdAsync(in id: Guid, out entity: UserAccount)` → IUserAccountRepository
- 3.3: `ChangeStatus(in action: String, out result: StatusChangeResult)` → UserAccount
- 3.4: `UpdateAsync(in entity: UserAccount)` → IUserAccountRepository
- 3.5: `ComposeStatusChangedEmail(in user: UserAccount, in newStatus: String, out message: EmailMessage)` → AccountStatusNotificationService
- 3.6: `SendAsync(in message: EmailMessage)` → IEmailGateway
- 3.7: IEmailGateway → Email Provider

## Todo

- [ ] Rename `ManageAccountStatusController` → `UserAccountAdminController` throughout
- [ ] Remove `UserManagementLogic` from participants table
- [ ] Add `AccountStatusNotificationService <<application logic>>` to participants table
- [ ] Fix object layout: remove `IUserAccountRepository --- UserAccount`; add `UserAccount` directly under controller
- [ ] Remove `UserManagementLogic` from layout
- [ ] Add `AccountStatusNotificationService` under controller in layout
- [ ] Fix Msg 1.2: `FindManageableUserAccountsAsync`; `List<UserAccount>`
- [ ] Fix Msg 2.2: `FindByIdAsync`
- [ ] Remove Msg 2.3 `getAvailableActions(UserManagementLogic)`
- [ ] Fix Msg 3.2: `FindByIdAsync`
- [ ] Remove Msg 3.3 `validateStatusTransition(UserManagementLogic)`
- [ ] Fix Msg 3.4: `ChangeStatus(in action: String, out result: StatusChangeResult)` on `UserAccount`
- [ ] Add msg: `AccountStatusNotificationService.ComposeStatusChangedEmail(...)`
- [ ] Fix Msg 3.5: `UpdateAsync`
- [ ] Renumber remaining messages accordingly

## Success Criteria

- Controller named `UserAccountAdminController`
- No `UserManagementLogic` participant
- `AccountStatusNotificationService` present in layout and participants
- `UserAccount` directly under controller in layout
- Msg uses `ChangeStatus(in action: String)` not `suspend/enable/disable`
- `FindManageableUserAccountsAsync` in msg 1.2
- `ComposeStatusChangedEmail` shown before `SendAsync`
- All repo methods with Async suffix
