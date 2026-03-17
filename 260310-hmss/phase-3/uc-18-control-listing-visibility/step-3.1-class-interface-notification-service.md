# Class Interface Specification: NotificationService

## Class Summary

- Stereotype: `<<service>>`
- Scope: `UC-18 Control Listing Visibility`
- Hidden Information: notification-content composition rules for owner-facing listing-control events
- Structuring Criterion: service

## Assumptions

- The service prepares notification content but does not deliver messages directly.
- Notification wording depends on the final listing-control outcome returned by `RoomListingLogic`.

## Anticipated Changes

- Additional notification channels may reuse the same composed message payload.
- Templates may later vary by moderation reason, locale, or listing category.

## Private Attributes

- None in current scope.

## Invariants

- Notification content must correspond to the final applied listing-control outcome.
- Notification preparation must not mutate room-listing state.

## Collaborators

- `AdminCoordinator`: requests notification content after a successful listing-control action

## Operations Provided

### `+ composeOwnerListingControlNotification(in listingReference: ListingReference, in listingControlOutcome: ListingControlOutcome, out ownerNotification: NotificationMessage)`

- Source trace: `UC-18 main sequence step 8; design communication message 3.6`
- Function: Composes the outbound notification payload that informs the owner about the applied administrative listing-control action.
- Parameters:
  - `in listingReference`: identifies the affected listing for notification targeting
  - `in listingControlOutcome`: describes the applied administrative control result
  - `out ownerNotification`: composed notification payload ready for delivery
- Preconditions:
  - `listingControlOutcome` represents a successfully applied listing-control action.
- Postconditions:
  - `ownerNotification` contains content suitable for downstream delivery through `EmailProxy`.
