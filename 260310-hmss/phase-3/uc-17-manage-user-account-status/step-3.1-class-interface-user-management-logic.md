# Class Interface Specification: UserManagementLogic

## Class Summary

- Stereotype: `<<business logic>>`
- Scope: `UC-17 Manage User Account Status`
- Hidden Information: business rules for allowed account-status transitions and derivation of permitted actions from current account status
- Structuring Criterion: business logic

## Assumptions

- The current policy scope follows the static-model note `Active <-> Suspended -> Disabled`.
- User-account data is persisted in a physical database, so persistence access is delegated to `UserAccountDB`.

## Anticipated Changes

- Additional account states such as locked, pending verification, or soft-deleted may extend the transition policy.
- Future authorization rules may restrict which admin roles can apply specific account-status actions.

## Private Attributes

- None in current scope.

## Invariants

- A requested account-status change must be rejected when it is not permitted for the account's current status.
- Permitted actions returned for an account must correspond to the same current status used for transition validation.

## Collaborators

- `AdminCoordinator`: invokes business operations for account management
- `UserAccountDB`: retrieves and persists user-account data
- `UserAccount`: encapsulates the in-memory account state during transition application

## Operations Provided

### `+ getUserAccountList(out userAccountList: UserAccountSummaryList)`

- Source trace: `UC-17 main sequence steps 1-2; communication messages 1.2-1.5`
- Function: Retrieves the user-account summaries needed for the administration list view.
- Parameters:
  - `out userAccountList`: summaries of manageable user accounts and their current statuses
- Preconditions:
  - None beyond the caller's authorization, which is enforced outside this class.
- Postconditions:
  - The returned summaries are loaded through `UserAccountDB`.

### `+ getUserAccountDetailAndAvailableStatusActions(in userAccountReference: UserAccountReference, out userAccountDetail: UserAccountDetail, out availableStatusActions: AccountStatusActionList)`

- Source trace: `UC-17 main sequence steps 3-4; communication messages 2.2-2.5`
- Function: Loads the selected account and derives the status-management actions currently allowed for it.
- Parameters:
  - `in userAccountReference`: identifies the account being managed
  - `out userAccountDetail`: current account information for the selected account
  - `out availableStatusActions`: permitted actions derived from the current status
- Preconditions:
  - `userAccountReference` identifies an existing account.
- Postconditions:
  - `userAccountDetail` reflects the account loaded through `UserAccountDB`.
  - `availableStatusActions` contains only actions valid for the current account status in policy scope.

### `+ changeUserAccountStatus(in userAccountReference: UserAccountReference, in accountStatusAction: AccountStatusAction, out accountStatusChangeOutcome: AccountStatusChangeOutcome)`

- Source trace: `UC-17 main sequence steps 5-6 and alternative step 6.1; communication messages 3.2-3.5`
- Function: Loads the target account, validates the requested action against the current status, applies the corresponding transition, and persists the updated account state.
- Parameters:
  - `in userAccountReference`: identifies the target account
  - `in accountStatusAction`: requested transition action
  - `out accountStatusChangeOutcome`: result containing applied status or rejection information
- Preconditions:
  - `userAccountReference` identifies an existing account.
  - `accountStatusAction` is a defined action in the current transition policy.
- Postconditions:
  - On success, the selected account's status is updated through `UserAccount` and persisted through `UserAccountDB`.
  - On failure, the selected account's persisted status remains unchanged and the outcome indicates rejection.
