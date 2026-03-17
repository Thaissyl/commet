# Design Class Diagram Blueprint: UC-17 Manage User Account Status - ASP.NET Simple Layered Backend

## Scope

- Included classes: `AdminUI`, `UserAccountAdminController`, `IUserAccountRepository`, `AccountStatusNotificationService`, `IEmailGateway`
- Synchronization source:
  - participant set and call structure from `step-3.0-design-communication-diagram.md`
  - class operations and responsibilities from `step-3.1-class-interface-*.md`

## Class Boxes

### `AdminUI`

- Stereotype: `<<user interaction>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ viewUserAccountList()`
  - `+ selectUserAccount(in userAccountId: Guid)`
  - `+ submitStatusChange(in userAccountId: Guid, in requestedAction: AccountStatusActionDto)`

### `UserAccountAdminController`

- Stereotype: `<<coordinator>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getUserAccountList(out response: UserAccountListResponseDto)`
  - `+ getUserAccountDetail(in userAccountId: Guid, out response: UserAccountDetailResponseDto)`
  - `+ changeUserAccountStatus(in userAccountId: Guid, in request: ChangeUserAccountStatusRequestDto, out response: ChangeUserAccountStatusResponseDto)`

### `IUserAccountRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ findManageableUserAccounts(out userAccounts: UserAccountList)`
  - `+ findById(in userAccountId: Guid, out userAccountRecord: UserAccountRecord)`
  - `+ save(in userAccountRecord: UserAccountRecord, out persistedUserAccountRecord: UserAccountRecord)`

### `AccountStatusNotificationService`

- Stereotype: `<<service>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ composeStatusChangedEmail(in userAccountRecord: UserAccountRecord, in changeResult: AccountStatusChangeResult, out emailMessage: EmailMessage)`

### `IEmailGateway`

- Stereotype: `<<proxy>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ sendAsync(in emailMessage: EmailMessage)`

## Relationships

- association:
  - from: `AdminUI`
  - to: `UserAccountAdminController`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `submits requests`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`
- association:
  - from: `UserAccountAdminController`
  - to: `IUserAccountRepository`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `loads and saves`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`
- association:
  - from: `UserAccountAdminController`
  - to: `AccountStatusNotificationService`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `composes email`
  - reading direction: `top-to-bottom`
  - source navigability: `none`
  - target navigability: `navigable`
- association:
  - from: `UserAccountAdminController`
  - to: `IEmailGateway`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `sends email`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

## Generalizations

- none in current scope

## Notes

- This version intentionally uses a simplified orchestration style where the controller coordinates repository access and infrastructure collaborators directly.
- `AdminUI` is included to keep the class diagram aligned with the design communication diagram, where the human actor interacts through a user-interaction object rather than calling the backend directly.
- This class diagram is synchronized with the current `step-3.1` interface specifications for `AdminUI`, `UserAccountAdminController`, `IUserAccountRepository`, `AccountStatusNotificationService`, and `IEmailGateway`.
- `IUserAccountRepository` hides persistence concerns such as EF Core or SQL access and exposes account records to the controller.
- Notification composition and outbound delivery are still separated from the controller to keep responsibilities focused even in the simplified design.
- Outbound email is designed as asynchronous background work so the main HTTP request does not block on provider latency.
