# Class Interface Specification: EmailProxy

## Class Summary

- Stereotype: `<<proxy>>`
- Scope: `UC-17 Manage User Account Status`
- Hidden Information: protocol details for communicating with the external email provider
- Structuring Criterion: proxy

## Assumptions

- Delivery failure is reported back to the coordinator without undoing an already applied account-status change.
- External email-provider behavior stays outside the HMSS design class scope.

## Anticipated Changes

- Retry or fallback-channel logic may be added behind the proxy contract.
- Provider-specific request metadata may change without affecting higher-level classes.

## Private Attributes

- None in current scope.

## Invariants

- The proxy does not decide business success of account-status changes.
- Every send attempt returns a delivery result to the caller.

## Collaborators

- `AdminCoordinator`: submits prepared notifications for delivery

## Operations Provided

### `+ sendUserAccountStatusChangeNotification(in userNotification: NotificationMessage, out deliveryStatus: DeliveryStatus)`

- Source trace: `UC-17 main sequence step 7 and alternative step 7.1; communication messages 3.8-3.11`
- Function: Sends the prepared notification through the external email provider and reports the delivery outcome.
- Parameters:
  - `in userNotification`: composed notification payload to send
  - `out deliveryStatus`: provider-facing delivery result returned to HMSS
- Preconditions:
  - `userNotification` is available and complete for delivery.
- Postconditions:
  - A delivery attempt has been made with the external provider.
  - `deliveryStatus` reports success or failure for the attempted send.
