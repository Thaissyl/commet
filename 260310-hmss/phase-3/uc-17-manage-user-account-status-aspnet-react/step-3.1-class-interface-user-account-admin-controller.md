# Class Interface Specification: UserAccountAdminController

## Class Summary

- Stereotype: `<<coordinator>>`
- Scope: `UC-17 Manage User Account Status - ASP.NET simple layered backend`
- Hidden Information: HTTP route binding, ASP.NET model binding, API response translation, and simplified use-case orchestration across repository and infrastructure collaborators
- Structuring Criterion: coordinator

## Assumptions

- This class maps to an ASP.NET Web API controller dedicated to admin account-management endpoints.
- Authorization is enforced at the controller or middleware boundary.
- This simplified design intentionally lets the controller coordinate repository access, transition validation, notification composition, and asynchronous email dispatch.

## Anticipated Changes

- Endpoint attributes, versioning, or authorization policies may change without altering use-case orchestration.
- If the use-case logic grows substantially later, orchestration may be extracted into a dedicated service.

## Private Attributes

- None in current scope.

## Invariants

- The controller must not embed SQL or provider-specific email details directly.
- The controller must validate status transitions consistently before persisting state changes.
- API contracts remain stable for the frontend caller.

## Collaborators

- `AdminUI`: frontend user-interaction caller
- `IUserAccountRepository`: loads and persists account data
- `AccountStatusNotificationService`: composes outbound email content
- `IEmailGateway`: queues outbound email asynchronously

## Operations Provided

### `+ getUserAccountList(out response: UserAccountListResponseDto)`

- Source communication messages: `1.1`, `1.2`
- Function: Handles the HTTP request that retrieves user accounts and their current statuses.
- Parameters:
  - `out response`: API response payload for the frontend
- Preconditions:
  - The current caller is authorized as a system admin.
- Postconditions:
  - The response payload is populated from repository data.

### `+ getUserAccountDetail(in userAccountId: Guid, out response: UserAccountDetailResponseDto)`

- Source communication messages: `2.1`, `2.2`
- Function: Handles the HTTP request that retrieves selected-account detail and allowed actions.
- Parameters:
  - `in userAccountId`: selected account identifier
  - `out response`: API response payload for the frontend
- Preconditions:
  - The current caller is authorized as a system admin.
  - `userAccountId` identifies an existing account.
- Postconditions:
  - The response payload contains account detail and allowed actions derived from the loaded account record.

### `+ changeUserAccountStatus(in userAccountId: Guid, in request: ChangeUserAccountStatusRequestDto, out response: ChangeUserAccountStatusResponseDto)`

- Source communication messages: `3.1`, `3.2`, `3.3`, `3.4`, `3.5`
- Function: Handles the HTTP request that validates and applies a user-account status change using the loaded account record.
- Parameters:
  - `in userAccountId`: selected account identifier
  - `in request`: requested status-change action
  - `out response`: API response payload describing the result
- Preconditions:
  - The current caller is authorized as a system admin.
  - `request` contains a defined status-management action.
- Postconditions:
  - On success, the account status is persisted and the response payload reports the applied transition.
  - On success, an asynchronous email-dispatch request is issued.
  - On failure, the persisted account status remains unchanged and the response payload reports rejection.

## Operations Required

- `IUserAccountRepository.findManageableUserAccounts(out userAccounts: UserAccountList)` from message `1.2`
- `IUserAccountRepository.findById(in userAccountId: Guid, out userAccountRecord: UserAccountRecord)` from messages `2.2`, `3.2`
- `IUserAccountRepository.save(in userAccountRecord: UserAccountRecord, out persistedUserAccountRecord: UserAccountRecord)` from message `3.3`
- `AccountStatusNotificationService.composeStatusChangedEmail(in userAccountRecord: UserAccountRecord, in changeResult: AccountStatusChangeResult, out emailMessage: EmailMessage)` from message `3.4`
- `IEmailGateway.sendAsync(in emailMessage: EmailMessage)` from message `3.5`

## Traceability

- Source use case: `UC-17 Manage User Account Status`
- Source design communication messages:
  - `1.1 AdminUI -> UserAccountAdminController`
  - `1.2 UserAccountAdminController -> IUserAccountRepository`
  - `2.1 AdminUI -> UserAccountAdminController`
  - `2.2 UserAccountAdminController -> IUserAccountRepository`
  - `3.1 AdminUI -> UserAccountAdminController`
  - `3.2 UserAccountAdminController -> IUserAccountRepository`
  - `3.3 UserAccountAdminController -> IUserAccountRepository`
  - `3.4 UserAccountAdminController -> AccountStatusNotificationService`
  - `3.5 UserAccountAdminController -> IEmailGateway`
