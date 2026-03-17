# Class Interface Specification: AdminUI

## Class Summary

- Stereotype: `<<user interaction>>`
- Scope: `UC-17 Manage User Account Status`
- Hidden Information: UI state for the currently displayed account list, selected account, and permitted account-status actions
- Structuring Criterion: boundary

## Assumptions

- `AdminUI` is the shared administration boundary already identified in `step-2.1-static-model.md`.
- The UI does not apply account-status rules directly; it only collects admin input and renders outputs returned by `AdminCoordinator`.

## Anticipated Changes

- The account-management screen may later expose additional filters or bulk actions without changing the coordinator contract.
- The displayed account detail may later include audit-trace data for administrative accountability.

## Private Attributes

| Attribute | Type | Purpose |
| --- | --- | --- |
| `- displayedUserAccountList` | `UserAccountSummaryList` | Stores the account list currently shown to the admin. |
| `- selectedUserAccountReference` | `UserAccountReference` | Tracks which account is being managed in the current interaction. |
| `- displayedAvailableStatusActions` | `AccountStatusActionList` | Stores the permitted actions returned for the selected account. |

## Invariants

- `selectedUserAccountReference` must belong to an account in `displayedUserAccountList` before a status-change request is submitted.
- `displayedAvailableStatusActions` must reflect the latest selected account detail currently shown on screen.

## Collaborators

- `AdminCoordinator`: receives all UI requests and returns application results.

## Operations Provided

### `+ accessUserAccountAdministration(out userAccountList: UserAccountSummaryList)`

- Source trace: `UC-17 main sequence steps 1-2; communication messages 1.1-1.7`
- Function: Requests the initial list of user accounts and their current statuses for display.
- Parameters:
  - `out userAccountList`: the account summaries to be rendered on the administration screen
- Preconditions:
  - System Admin is signed in.
- Postconditions:
  - `displayedUserAccountList` is refreshed from the coordinator response.

### `+ selectUserAccount(in userAccountReference: UserAccountReference, out userAccountDetail: UserAccountDetail, out availableStatusActions: AccountStatusActionList)`

- Source trace: `UC-17 main sequence steps 3-4; communication messages 2.1-2.7`
- Function: Requests the selected account detail and the status-management actions permitted for its current state.
- Parameters:
  - `in userAccountReference`: identifies the account chosen by the admin
  - `out userAccountDetail`: the current account information to display
  - `out availableStatusActions`: the permitted actions for the selected account
- Preconditions:
  - `userAccountReference` identifies an existing user account.
- Postconditions:
  - `selectedUserAccountReference` is updated to `userAccountReference`.
  - `displayedAvailableStatusActions` is updated from the coordinator response.

### `+ submitAccountStatusChange(in userAccountReference: UserAccountReference, in accountStatusAction: AccountStatusAction, out accountStatusChangeOutcome: AccountStatusChangeOutcome)`

- Source trace: `UC-17 main sequence steps 5-8; communication messages 3.1-3.13`
- Function: Submits the admin's chosen account-status action and receives the overall outcome to present.
- Parameters:
  - `in userAccountReference`: identifies the account to update
  - `in accountStatusAction`: the permitted status-management action selected by the admin
  - `out accountStatusChangeOutcome`: business result of the requested account-status change
- Preconditions:
  - `userAccountReference` matches the selected account currently displayed.
  - `accountStatusAction` belongs to `displayedAvailableStatusActions`.
- Postconditions:
  - The UI shows success or failure feedback returned by the coordinator.
  - When the change succeeds, the displayed account status is refreshed to the new value in the outcome.
