# Design Class Diagram Blueprint: UC-17 Manage User Account Status - ASP.NET Simple Layered Backend

## Scope

- Included classes: `AdminUI`, `UserAccountAdminController`, `IUserAccountRepository`, `AccountStatusNotificationService`, `IEmailGateway`, `UserAccount`
- Synchronization source:
  - participant set and call structure from `step-3.0-design-communication-diagram.md`
  - class operations derived from implemented controller/service methods

## Class Boxes

### `AdminUI`

- Stereotype: `<<user interaction>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ openAccountManagement()`
  - `+ selectUser(in userId: Guid)`
  - `+ suspendAccount(in userId: Guid)`
  - `+ enableAccount(in userId: Guid)`
  - `+ disableAccount(in userId: Guid)`

### `UserAccountAdminController`

- Stereotype: `<<coordinator>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getUserAccountList(out response: IEnumerable<UserAccountSummaryDto>)`
  - `+ getUserAccountDetail(in userId: Guid, out response: UserAccountDetailResponseDto)`
  - `+ suspendAccount(in userId: Guid, out response: ChangeUserAccountStatusResponseDto)`
  - `+ enableAccount(in userId: Guid, out response: ChangeUserAccountStatusResponseDto)`
  - `+ disableAccount(in userId: Guid, out response: ChangeUserAccountStatusResponseDto)`

### `IUserAccountRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ findManageableUserAccountsAsync(out users: List<UserAccount>)`
  - `+ findByIdAsync(in id: Guid, out user: UserAccount)`
  - `+ updateAsync(in entity: UserAccount, out persisted: UserAccount)`

### `AccountStatusNotificationService`

- Stereotype: `<<application logic>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ composeStatusChangedEmail(in account: UserAccount, in newStatus: string, out message: EmailMessage)`

### `IEmailGateway`

- Stereotype: `<<proxy>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ sendAsync(in message: EmailMessage)`

### `UserAccount`

- Stereotype: `<<data abstraction>>`
- Attributes:
  - `- userId: Guid`
  - `- fullName: string`
  - `- email: string`
  - `- role: string`
  - `- accountStatus: string`
- Operations:
  - `+ changeStatus(in action: string, out result: StatusChangeResult)`

## Relationships

- association:
  - from: `AdminUI`
  - to: `UserAccountAdminController`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `manages accounts`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `UserAccountAdminController`
  - to: `IUserAccountRepository`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `loads and persists`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `UserAccountAdminController`
  - to: `AccountStatusNotificationService`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `composes email`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `UserAccountAdminController`
  - to: `IEmailGateway`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `dispatches email`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `IUserAccountRepository`
  - to: `UserAccount`
  - source multiplicity: `1`
  - target multiplicity: `0..*`
  - association name: `manages`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

## Generalizations

- none in current scope

## Notes

- Available actions depend on `UserAccount.accountStatus`, and `Disable` is removed for the currently signed-in admin when rendering detail.
- The controller re-fetches `UserAccount` before status mutation to stay stateless across request phases.
- Transition enforcement is implemented by `UserAccount.ChangeStatus(...)`, not a separate `UserAccountLogic` class.
- Notification composition is delegated to `AccountStatusNotificationService`.
- Email dispatch is async fire-and-forget in the current controller implementation.
