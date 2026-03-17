# Class Interface Specification: UserAccount

## Class Summary

- Stereotype: `<<data abstraction>>`
- Scope: `UC-17 Manage User Account Status`
- Hidden Information: in-memory representation of account identity and status data while the current transition is being evaluated and applied
- Structuring Criterion: data abstraction

## Assumptions

- The analysis participant `User` is normalized to `UserAccount` to match the canonical entity in `step-2.1-static-model.md`.
- Persistent storage concerns are hidden by `UserAccountDB`; `UserAccount` itself does not expose database access.

## Anticipated Changes

- Additional account profile attributes may later be loaded into the in-memory abstraction for richer administration detail.
- Traceability requirements may introduce separate audit objects without changing the encapsulated account state.

## Private Attributes

| Attribute | Type | Purpose |
| --- | --- | --- |
| `- userId` | `UserId` | Stores the stable identifier of the user account. |
| `- fullName` | `FullName` | Stores the account holder's display name for administration and notification. |
| `- email` | `EmailAddress` | Stores the destination email used for notifications. |
| `- role` | `UserRole` | Stores the account role used by the wider HMSS authorization model. |
| `- accountStatus` | `AccountStatus` | Stores the current status used to derive permitted transitions. |

## Invariants

- `accountStatus` must always contain a valid domain status value.
- A status transition must leave the account in exactly one current status.
- A suspended or disabled account must not be considered eligible for protected access in downstream authentication logic.

## Collaborators

- `UserManagementLogic`: requests validated status transitions
- `UserAccountDB`: persists the updated account state after a successful transition

## Operations Provided

### `+ applyStatusTransition(in accountStatusAction: AccountStatusAction, out accountStatusRecord: AccountStatusRecord)`

- Source trace: `UC-17 main sequence step 6 and alternative step 6.1; design communication message 3.4`
- Function: Applies a validated account-status transition to the in-memory account object and returns the resulting status record.
- Parameters:
  - `in accountStatusAction`: validated status-management action to apply
  - `out accountStatusRecord`: resulting status information after the transition attempt
- Preconditions:
  - `accountStatusAction` is permitted for the current `accountStatus`.
- Postconditions:
  - On success, `accountStatus` is updated to the target status defined by the action.
  - On failure, `accountStatus` remains unchanged and the returned record indicates no applied transition.
