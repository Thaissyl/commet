# Class Interface Specification: IEmailGateway

## Class Summary

- Stereotype: `<<proxy>>`
- Scope: `UC-17 Manage User Account Status - ASP.NET simple layered backend`
- Hidden Information: provider-specific transport details for sending outbound email
- Structuring Criterion: proxy

## Assumptions

- This abstraction is implemented by infrastructure code such as SMTP or a third-party provider adapter.
- Delivery failure is reported upward without rolling back the account-status update.

## Anticipated Changes

- Provider switching or retry policies may change without affecting the service layer.
- Additional email metadata may later be added to the outbound payload.

## Private Attributes

- None in current scope.

## Invariants

- Each asynchronous send request must be accepted for background processing or reported through infrastructure monitoring.
- The gateway does not contain business rules for account-status transitions.

## Collaborators

- `UserAccountAdminController`: orchestration caller in the simplified design

## Operations Provided

### `+ sendAsync(in emailMessage: EmailMessage)`

- Source communication messages: `3.5`, `3.6`
- Function: Queues or dispatches an outbound email asynchronously without blocking the main request flow.
- Parameters:
  - `in emailMessage`: composed outbound email payload
- Preconditions:
  - `emailMessage` is complete and ready for delivery.
- Postconditions:
  - An asynchronous delivery request has been accepted for background processing.

## Operations Required

- `Email Provider.sendAsync(in emailMessage: EmailMessage)` from message `3.6`

## Traceability

- Source use case: `UC-17 Manage User Account Status`
- Source design communication messages:
  - `3.5 UserAccountAdminController -> IEmailGateway`
  - `3.6 IEmailGateway -> Email Provider`
