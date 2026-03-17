# Design Class Diagram Blueprint: UC-17 Manage User Account Status

## Scope

- Included classes: `AdminUI`, `AdminCoordinator`, `UserManagementLogic`, `UserAccount`, `UserAccountDB`, `NotificationService`, `EmailProxy`

## Class Boxes

### `AdminUI`

- Stereotype: `<<user interaction>>`
- Attributes:
  - `- displayedUserAccountList: UserAccountSummaryList`
  - `- selectedUserAccountReference: UserAccountReference`
  - `- displayedAvailableStatusActions: AccountStatusActionList`
- Operations:
  - `+ accessUserAccountAdministration(out userAccountList: UserAccountSummaryList)`
  - `+ selectUserAccount(in userAccountReference: UserAccountReference, out userAccountDetail: UserAccountDetail, out availableStatusActions: AccountStatusActionList)`
  - `+ submitAccountStatusChange(in userAccountReference: UserAccountReference, in accountStatusAction: AccountStatusAction, out accountStatusChangeOutcome: AccountStatusChangeOutcome)`

### `AdminCoordinator`

- Stereotype: `<<coordinator>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getUserAccountList(out userAccountList: UserAccountSummaryList)`
  - `+ getUserAccountDetailAndAvailableStatusActions(in userAccountReference: UserAccountReference, out userAccountDetail: UserAccountDetail, out availableStatusActions: AccountStatusActionList)`
  - `+ applyAccountStatusChange(in userAccountReference: UserAccountReference, in accountStatusAction: AccountStatusAction, out accountStatusChangeOutcome: AccountStatusChangeOutcome, out deliveryStatus: DeliveryStatus)`

### `UserManagementLogic`

- Stereotype: `<<business logic>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getUserAccountList(out userAccountList: UserAccountSummaryList)`
  - `+ getUserAccountDetailAndAvailableStatusActions(in userAccountReference: UserAccountReference, out userAccountDetail: UserAccountDetail, out availableStatusActions: AccountStatusActionList)`
  - `+ changeUserAccountStatus(in userAccountReference: UserAccountReference, in accountStatusAction: AccountStatusAction, out accountStatusChangeOutcome: AccountStatusChangeOutcome)`

### `UserAccount`

- Stereotype: `<<data abstraction>>`
- Attributes:
  - `- userId: UserId`
  - `- fullName: FullName`
  - `- email: EmailAddress`
  - `- role: UserRole`
  - `- accountStatus: AccountStatus`
- Operations:
  - `+ applyStatusTransition(in accountStatusAction: AccountStatusAction, out accountStatusRecord: AccountStatusRecord)`

### `UserAccountDB`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ findUserAccountSummaries(out userAccountList: UserAccountSummaryList)`
  - `+ findUserAccountByReference(in userAccountReference: UserAccountReference, out userAccount: UserAccount)`
  - `+ saveUserAccountStatus(in userAccount: UserAccount, out accountStatusRecord: AccountStatusRecord)`

### `NotificationService`

- Stereotype: `<<service>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ composeUserAccountStatusChangeNotification(in userAccountReference: UserAccountReference, in accountStatusChangeOutcome: AccountStatusChangeOutcome, out userNotification: NotificationMessage)`

### `EmailProxy`

- Stereotype: `<<proxy>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ sendUserAccountStatusChangeNotification(in userNotification: NotificationMessage, out deliveryStatus: DeliveryStatus)`

## Relationships

- association:
  - from: `AdminUI`
  - to: `AdminCoordinator`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `submits requests`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`
- association:
  - from: `AdminCoordinator`
  - to: `UserManagementLogic`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `delegates rules`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`
- association:
  - from: `UserManagementLogic`
  - to: `UserAccountDB`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `queries persistence`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`
- association:
  - from: `UserManagementLogic`
  - to: `UserAccount`
  - source multiplicity: `1`
  - target multiplicity: `0..1`
  - association name: `applies transition`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`
- association:
  - from: `UserAccountDB`
  - to: `UserAccount`
  - source multiplicity: `1`
  - target multiplicity: `0..*`
  - association name: `reconstitutes`
  - reading direction: `bottom-to-top`
  - source navigability: `none`
  - target navigability: `navigable`
- association:
  - from: `AdminCoordinator`
  - to: `NotificationService`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `requests notification`
  - reading direction: `top-to-bottom`
  - source navigability: `none`
  - target navigability: `navigable`
- association:
  - from: `AdminCoordinator`
  - to: `EmailProxy`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `dispatches email`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

## Generalizations

- none in current scope

## Notes

- The analysis participant `User` is refined into `UserAccount <<data abstraction>>` plus `UserAccountDB <<database wrapper>>` because user-account data is assumed to be stored in a physical database.
- `UserAccount` encapsulates the in-memory account state during transition evaluation, while `UserAccountDB` hides database retrieval and persistence details.
- The transition policy is treated as `Active <-> Suspended -> Disabled` based on the static model; no separate statechart file currently exists for `UserAccount`.
- Notification delivery failure does not roll back a successfully applied account-status change.
