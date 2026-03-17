# Class Interface Specification: EmailProxy

## Class Summary

- Stereotype: `<<proxy>>`
- Scope: `UC-18 Control Listing Visibility`
- Hidden Information: protocol details for communicating with the external email provider
- Structuring Criterion: proxy

## Assumptions

- Delivery failure is reported back to the coordinator without undoing an already applied listing-control action.
- External email-provider behavior stays outside the HMSS design class scope.

## Anticipated Changes

- Retry or fallback-channel logic may be added behind the proxy contract.
- Provider-specific request metadata may change without affecting higher-level classes.

## Private Attributes

- None in current scope.

## Invariants

- The proxy does not decide business success of listing-control actions.
- Every send attempt returns a delivery result to the caller.

## Collaborators

- `AdminCoordinator`: submits prepared owner notifications for delivery

## Operations Provided

### `+ sendOwnerListingControlNotification(in ownerNotification: NotificationMessage, out deliveryStatus: DeliveryStatus)`

- Source trace: `UC-18 main sequence step 8 and alternative step 8.1; design communication messages 3.7-3.8`
- Function: Sends the prepared owner notification through the external email provider and reports the delivery outcome.
- Parameters:
  - `in ownerNotification`: composed notification payload to send
  - `out deliveryStatus`: provider-facing delivery result returned to HMSS
- Preconditions:
  - `ownerNotification` is available and complete for delivery.
- Postconditions:
  - A delivery attempt has been made with the external provider.
  - `deliveryStatus` reports success or failure for the attempted send.
