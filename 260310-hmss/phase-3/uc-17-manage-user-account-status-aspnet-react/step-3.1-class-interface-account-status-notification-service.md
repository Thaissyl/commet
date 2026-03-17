# Class Interface Specification: AccountStatusNotificationService

## Class Summary

- Stereotype: `<<service>>`
- Scope: `UC-17 Manage User Account Status - ASP.NET simple layered backend`
- Hidden Information: email-template composition rules for account-status change notifications
- Structuring Criterion: service

## Assumptions

- Notification composition is kept separate from `UserAccountAdminController` to preserve single responsibility even in the simplified design.
- This service produces transport-agnostic email content for the outbound gateway.

## Anticipated Changes

- Localization, branding, or role-specific templates may later extend notification composition.
- Additional notification channels may reuse the same business event.

## Private Attributes

- None in current scope.

## Invariants

- The composed notification must reflect the final applied status change.
- Notification composition must not mutate the loaded account record.

## Collaborators

- `UserAccountAdminController`: orchestration caller in the simplified design

## Operations Provided

### `+ composeStatusChangedEmail(in userAccountRecord: UserAccountRecord, in changeResult: AccountStatusChangeResult, out emailMessage: EmailMessage)`

- Source communication messages: `3.4`
- Function: Creates the outbound email content for a successfully applied account-status change.
- Parameters:
  - `in userAccountRecord`: account whose status changed
  - `in changeResult`: applied transition result
  - `out emailMessage`: composed outbound email message
- Preconditions:
  - `changeResult` represents a successful account-status change.
- Postconditions:
  - `emailMessage` is ready for outbound delivery.

## Operations Required

- none in current scope

## Traceability

- Source use case: `UC-17 Manage User Account Status`
- Source design communication messages:
  - `3.4 UserAccountAdminController -> AccountStatusNotificationService`
