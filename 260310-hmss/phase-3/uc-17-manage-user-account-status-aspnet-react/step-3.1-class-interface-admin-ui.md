# Class Interface Specification: AdminUI

## Class Summary

- Stereotype: `<<user interaction>>`
- Scope: `UC-17 Manage User Account Status - ASP.NET simple layered backend`
- Hidden Information: frontend screen state, form interaction flow, and request dispatch from the admin-facing UI to the backend controller
- Structuring Criterion: user interaction

## Assumptions

- `AdminUI` represents the Next.js or React admin screen for managing user-account status.
- The human actor interacts with the system through this UI object rather than calling the backend directly.

## Anticipated Changes

- Screen composition, component split, or client-side state handling may change without altering the controller contract.
- Additional filters or table interactions may later extend the listing behavior.

## Private Attributes

- None in current scope.

## Invariants

- `AdminUI` does not apply account-status persistence or notification logic directly.
- `AdminUI` forwards status-management requests through `UserAccountAdminController`.

## Collaborators

- `UserAccountAdminController`: backend boundary that handles admin account-management requests

## Operations Provided

### `+ viewUserAccountList()`

- Source communication messages: `1`
- Function: Handles the admin action that opens or refreshes the manageable user-account list view.
- Parameters:
  - none
- Preconditions:
  - The system admin has access to the account-management UI.
- Postconditions:
  - A list request is sent to `UserAccountAdminController`.

### `+ selectUserAccount(in userAccountId: Guid)`

- Source communication messages: `2`
- Function: Handles the admin action that selects a specific user account for detail viewing.
- Parameters:
  - `in userAccountId: Guid`: selected account identifier
- Preconditions:
  - `userAccountId` refers to an account currently shown in the UI list.
- Postconditions:
  - A detail request is sent to `UserAccountAdminController`.

### `+ submitStatusChange(in userAccountId: Guid, in requestedAction: AccountStatusActionDto)`

- Source communication messages: `3`
- Function: Handles the admin action that submits a requested account-status change.
- Parameters:
  - `in userAccountId: Guid`: selected account identifier
  - `in requestedAction: AccountStatusActionDto`: requested status-management action from the UI
- Preconditions:
  - The selected account is present in the current UI context.
  - `requestedAction` is enabled in the current UI state.
- Postconditions:
  - A status-change request is sent to `UserAccountAdminController`.

## Operations Required

- `UserAccountAdminController.getUserAccountList(out response: UserAccountListResponseDto)` from message `1.1`
- `UserAccountAdminController.getUserAccountDetail(in userAccountId: Guid, out response: UserAccountDetailResponseDto)` from message `2.1`
- `UserAccountAdminController.changeUserAccountStatus(in userAccountId: Guid, in request: ChangeUserAccountStatusRequestDto, out response: ChangeUserAccountStatusResponseDto)` from message `3.1`

## Traceability

- Source use case: `UC-17 Manage User Account Status`
- Source design communication messages:
  - `1 System Admin -> AdminUI`
  - `2 System Admin -> AdminUI`
  - `3 System Admin -> AdminUI`
  - `1.1 AdminUI -> UserAccountAdminController`
  - `2.1 AdminUI -> UserAccountAdminController`
  - `3.1 AdminUI -> UserAccountAdminController`
