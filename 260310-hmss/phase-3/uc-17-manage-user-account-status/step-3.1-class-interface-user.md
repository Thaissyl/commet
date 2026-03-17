# Class Interface Specification: User

## Class Summary

- Stereotype: `<<data abstraction>>`
- Scope: `manage-user-account-status`
- Hidden Information: internal representation of user account data and enforcement of valid `accountStatus` transitions in memory
- Structuring Criterion: data abstraction

## Assumptions

- a conceptual `accountReference` can be resolved to a concrete user account in the current scope.
- Administrative listing and lookup are supported directly by the `User` entity in the current model because no separate repository class exists in the supplied analysis artifacts.

## Anticipated Changes

- Add explicit audit fields for administrative status changes.
- Extract repository or query services in a later design refinement if the persistence model becomes more detailed.

## Private Attributes

| Attribute | Type | Purpose |
| --- | --- | --- |
| `- email` | `EmailAddress` | identifies the user account in the current scope |
| `- passwordHash` | `PasswordHash` | stores credential data without exposing raw passwords |
| `- role` | `UserRole` | stores access role used by other subsystems |
| `- accountStatus` | `AccountStatus` | stores the current lifecycle state of the account |
| `- createdAt` | `DateTime` | stores account creation time for traceability |

## Invariants

- `accountStatus` must be one of `Active`, `Suspended`, or `Disabled`
- direct `Active -> Disabled` transition is not permitted in the current scope
- `Disabled` has no outgoing transition in the current scope
- a `Suspended` or `Disabled` account cannot access protected system functions

## Collaborators

- `UserManagementLogic`: requests account list and detail data and invokes status transitions

## Operations Provided

### `+ getUserAccountList(out userAccountList: UserAccountList)`

- Source trace: `UC-17` steps `1-2`; communication messages `1.3`, `1.4`
- Function: provide the current list of managed user accounts and their statuses
- Parameters:
  - `out userAccountList`: current collection of user accounts available for management
- Preconditions:
  - user account data is available in the current subsystem
- Postconditions:
  - `userAccountList` has been returned to `UserManagementLogic`

### `+ getUserAccountDetail(in accountReference: UserAccountReference, out userAccountDetail: UserAccountDetail)`

- Source trace: `UC-17` steps `3-4`; communication messages `2.3`, `2.4`
- Function: provide current account detail for the selected account
- Parameters:
  - `in accountReference`: selected account identifier
  - `out userAccountDetail`: current detail of the selected account, including current `accountStatus`
- Preconditions:
  - an account with `accountReference` exists
- Postconditions:
  - `userAccountDetail` has been returned to `UserManagementLogic`

### `+ applyAccountStatusTransition(in accountReference: UserAccountReference, in statusAction: StatusManagementAction, out userAccountRecord: UserAccountRecord)`

- Source trace: `UC-17` steps `5-8`; communication messages `3.3`, `3.4`; statechart transitions `T2`, `T3`, `T4`
- Function: apply a permitted administrative status transition to the selected user account
- Parameters:
  - `in accountReference`: account selected for management
  - `in statusAction`: requested transition action
  - `out userAccountRecord`: updated account record after the transition is applied
- Preconditions:
  - an account with `accountReference` exists
  - if `statusAction = Suspend`, current `accountStatus = Active`
  - if `statusAction = Enable`, current `accountStatus = Suspended`
  - if `statusAction = Disable`, current `accountStatus = Suspended`
- Postconditions:
  - if `statusAction = Suspend`, `accountStatus = Suspended`
  - if `statusAction = Enable`, `accountStatus = Active`
  - if `statusAction = Disable`, `accountStatus = Disabled`
  - `userAccountRecord` has been returned to `UserManagementLogic`
