# Design Communication Diagram: UC-17 Manage User Account Status - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend aligned to the implemented ASP.NET controller
- Main flow: `AdminUI -> UserAccountAdminController`, then controller -> repository and email gateway
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label
- Separate reply arrows intentionally omitted; returned data is represented by `out` parameters in the request label
- Request flow style: stateless controller orchestration with fire-and-forget notification dispatch
- View simplification: internal email-composition helper is omitted from the communication view to keep the interaction focused on the main collaborators

## Object Layout

```text
System Admin --- AdminUI --- UserAccountAdminController
                              |--- IUserAccountRepository
                              |--- IEmailGateway --- Email Provider
```

## Participants

| Position | Object                     | Stereotype             |
| -------- | -------------------------- | ---------------------- |
| 1        | System Admin               | Actor (primary)        |
| 2        | AdminUI                    | `<<user interaction>>` |
| 3        | UserAccountAdminController | `<<coordinator>>`      |
| 4        | IUserAccountRepository     | `<<database wrapper>>` |
| 5        | IEmailGateway              | `<<proxy>>`            |
| 6        | Email Provider             | Actor (secondary)      |

## Messages

| #   | From -> To                              | Message |
| --- | --------------------------------------- | ------- |
| 1   | System Admin -> AdminUI                 | Account Management Access |
| 1.1 | AdminUI -> UserAccountAdminController   | `GetUserAccountList(out response: IEnumerable<UserAccountSummaryDto>)` |
| 1.2 | UserAccountAdminController -> IUserAccountRepository | `FindManageableUserAccountsAsync(out users: List<UserAccount>)` |
| 1.3 | AdminUI -> System Admin                 | User Account List Display |
| 2   | System Admin -> AdminUI                 | User Account Selection |
| 2.1 | AdminUI -> UserAccountAdminController   | `GetUserAccountDetail(in userId: Guid, out response: UserAccountDetailResponseDto)` |
| 2.2 | UserAccountAdminController -> IUserAccountRepository | `FindByIdAsync(in id: Guid, out user: UserAccount)` |
| 2.3 | AdminUI -> System Admin                 | Account Details Display |
| 3   | System Admin -> AdminUI                 | Status Change Decision |
| 3.1 | AdminUI -> UserAccountAdminController   | `SuspendAccount(in userId: Guid, out response: ChangeUserAccountStatusResponseDto)` |
| 3.2 | UserAccountAdminController -> IUserAccountRepository | `FindByIdAsync(in id: Guid, out user: UserAccount)` |
| 3.3 | UserAccountAdminController -> IUserAccountRepository | `UpdateAsync(in entity: UserAccount, out persisted: UserAccount)` |
| 3.4 | UserAccountAdminController -> IEmailGateway | `SendAsync(in notification: EmailMessage)` |
| 3.5 | IEmailGateway -> Email Provider         | Send Email Notification |
| 3.6 | AdminUI -> System Admin                 | Account Status Change Confirmation |

## Alternative Flow Notes

- **Step 2.2: User not found** - controller returns `NotFound()`
- **Step 3.1: Other transitions** - `EnableAccount(...)` and `DisableAccount(...)` follow the same orchestration pattern as `SuspendAccount(...)`
- **Step 3.1: Self-disable attempt** - `DisableAccount(...)` returns `BadRequest` when `userId == currentAdminId`
- **Step 3.3: Transition invalid** - `UserAccount.ChangeStatus(action)` returns failure and the controller responds with `BadRequest`
- **Step 3.5: Email delivery** - `_email.SendAsync(...)` is invoked without awaiting a delivery result; notification failure is outside the synchronous success path of the request

## Notes

- `AdminUI` is shown explicitly; the human actor never calls backend endpoints directly.
- `UserAccountAdminController` is the real orchestration point in the implemented system.
- No separate `UserAccountLogic` object exists in the current code for UC-17. Transition enforcement is split between `UserAccountAdminController` and the `UserAccount.ChangeStatus(...)` entity method.
- `GetUserAccountDetail(...)` computes available actions inline and removes `Disable` for the currently signed-in admin.
- `AccountStatusNotificationService` still exists in the codebase as a helper that composes email content, but it is intentionally omitted from this communication view.
- `IEmailGateway` is the design-level boundary to the external email system, and `Email Provider` is shown explicitly as the secondary actor behind that boundary.
- Actor-to-UI messages remain noun phrases because they represent physical interaction, not function calls.
