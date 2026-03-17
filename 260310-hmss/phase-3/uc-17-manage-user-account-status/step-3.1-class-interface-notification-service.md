# Class Interface Specification: NotificationService

## Class Summary

- Stereotype: `<<service>>`
- Scope: `UC-17 Manage User Account Status`
- Hidden Information: notification-content composition rules for account-status change events
- Structuring Criterion: service

## Assumptions

- The service prepares notification content but does not deliver messages directly.
- Notification wording depends on the final account-status change result returned by `UserManagementLogic`.

## Anticipated Changes

- Additional notification channels may reuse the same composed message payload.
- Templates may later vary by user role, locale, or action type.

## Private Attributes

- None in current scope.

## Invariants

- Notification content must correspond to the final applied account-status outcome.
- Notification preparation must not mutate user-account state.

## Collaborators

- `AdminCoordinator`: requests notification content after a successful status change

## Operations Provided

### `+ composeUserAccountStatusChangeNotification(in userAccountReference: UserAccountReference, in accountStatusChangeOutcome: AccountStatusChangeOutcome, out userNotification: NotificationMessage)`

- Source trace: `UC-17 main sequence step 7; communication messages 3.6-3.7`
- Function: Composes the outbound notification payload that informs the affected user about the account-status change.
- Parameters:
  - `in userAccountReference`: identifies the affected account for notification targeting
  - `in accountStatusChangeOutcome`: describes the applied status change
  - `out userNotification`: composed notification payload ready for delivery
- Preconditions:
  - `accountStatusChangeOutcome` represents a successfully applied status change.
- Postconditions:
  - `userNotification` contains content suitable for downstream delivery through `EmailProxy`.
