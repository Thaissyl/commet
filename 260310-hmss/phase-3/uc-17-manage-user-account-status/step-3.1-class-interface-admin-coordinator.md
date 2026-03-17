# Class Interface Specification: AdminCoordinator

## Class Summary

- Stereotype: `<<coordinator>>`
- Scope: `UC-17 Manage User Account Status`
- Hidden Information: none in current scope; this coordinator is treated as stateless orchestration
- Structuring Criterion: coordinator

## Assumptions

- `AdminCoordinator` is shared by UC-17 and UC-18, but only the account-management responsibilities are in scope here.
- Notification composition is delegated to `NotificationService`, while outbound email delivery is delegated to `EmailProxy`.

## Anticipated Changes

- Additional administrative use cases may reuse this coordinator and add new orchestration operations.
- Audit logging may be introduced as another collaborator without changing the boundary contract.

## Private Attributes

- None in current scope.

## Invariants

- The coordinator does not persist domain state between requests.
- All account-status changes are delegated to `UserManagementLogic` before any user notification is sent.

## Collaborators

- `AdminUI`: source of boundary requests and sink for responses
- `UserManagementLogic`: evaluates and applies account-status rules
- `NotificationService`: composes the notification payload for the affected user
- `EmailProxy`: sends the prepared notification to the external email provider

## Operations Provided

### `+ getUserAccountList(out userAccountList: UserAccountSummaryList)`

- Source trace: `UC-17 main sequence steps 1-2; communication messages 1.1-1.6`
- Function: Retrieves the account list needed by the administration boundary.
- Parameters:
  - `out userAccountList`: current user-account summaries with statuses
- Preconditions:
  - System Admin is signed in.
- Postconditions:
  - The latest account list from `UserManagementLogic` is returned to `AdminUI`.

### `+ getUserAccountDetailAndAvailableStatusActions(in userAccountReference: UserAccountReference, out userAccountDetail: UserAccountDetail, out availableStatusActions: AccountStatusActionList)`

- Source trace: `UC-17 main sequence steps 3-4; communication messages 2.1-2.6`
- Function: Obtains current account information and the permitted status-management actions for the selected account.
- Parameters:
  - `in userAccountReference`: identifies the selected account
  - `out userAccountDetail`: current account information
  - `out availableStatusActions`: permitted account-status actions
- Preconditions:
  - `userAccountReference` identifies an existing user account.
- Postconditions:
  - `AdminUI` receives the latest detail and action set returned by `UserManagementLogic`.

### `+ applyAccountStatusChange(in userAccountReference: UserAccountReference, in accountStatusAction: AccountStatusAction, out accountStatusChangeOutcome: AccountStatusChangeOutcome, out deliveryStatus: DeliveryStatus)`

- Source trace: `UC-17 main sequence steps 5-8; communication messages 3.1-3.12`
- Function: Orchestrates the account-status change, notification preparation, and notification delivery attempt.
- Parameters:
  - `in userAccountReference`: identifies the account to update
  - `in accountStatusAction`: requested account-status action
  - `out accountStatusChangeOutcome`: result of the account-status update
  - `out deliveryStatus`: result of the notification delivery attempt
- Preconditions:
  - `accountStatusAction` is intended for the current status of the selected account.
- Postconditions:
  - `UserManagementLogic` has either rejected or applied the requested transition.
  - When the status change succeeds, a notification payload has been requested from `NotificationService`.
  - A delivery attempt has been made through `EmailProxy` without rolling back a successful status change when email delivery fails.
