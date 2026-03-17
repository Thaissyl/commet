# Class Interface Specification: AdminCoordinator

## Class Summary

- Stereotype: `<<coordinator>>`
- Scope: `UC-18 Control Listing Visibility`
- Hidden Information: none in current scope; this coordinator is treated as stateless orchestration
- Structuring Criterion: coordinator

## Assumptions

- `AdminCoordinator` is shared by UC-17 and UC-18, but only the listing-control responsibilities are in scope here.
- Notification composition is delegated to `NotificationService`, while outbound email delivery is delegated to `EmailProxy`.

## Anticipated Changes

- Additional administrative moderation use cases may reuse this coordinator and add new orchestration operations.
- Audit logging may be introduced as another collaborator without changing the boundary contract.

## Private Attributes

- None in current scope.

## Invariants

- The coordinator does not persist domain state between requests.
- All listing-control actions are delegated to `RoomListingLogic` before any owner notification is sent.

## Collaborators

- `AdminUI`: source of boundary requests and sink for responses
- `RoomListingLogic`: evaluates and applies listing-visibility control rules
- `NotificationService`: composes the notification payload for the affected owner
- `EmailProxy`: sends the prepared notification to the external email provider

## Operations Provided

### `+ getVisibleListingList(out visibleListingList: VisibleListingSummaryList)`

- Source trace: `UC-18 main sequence steps 1-2; design communication messages 1.1-1.2`
- Function: Retrieves the visible listing list needed by the administration boundary.
- Parameters:
  - `out visibleListingList`: current publicly visible listing summaries for administrative review
- Preconditions:
  - System Admin is signed in.
- Postconditions:
  - The latest visible listing list from `RoomListingLogic` is returned to `AdminUI`.

### `+ getListingDetailAndAvailableControlActions(in listingReference: ListingReference, out listingDetail: ListingDetail, out availableControlActions: ListingControlActionList)`

- Source trace: `UC-18 main sequence steps 3-4; design communication messages 2.1-2.2`
- Function: Obtains current listing information and the permitted control actions for the selected listing.
- Parameters:
  - `in listingReference`: identifies the selected listing
  - `out listingDetail`: current listing information
  - `out availableControlActions`: permitted administrative control actions
- Preconditions:
  - `listingReference` identifies an existing listing.
- Postconditions:
  - `AdminUI` receives the latest detail and action set returned by `RoomListingLogic`.

### `+ applyListingControlAction(in listingReference: ListingReference, in listingControlAction: ListingControlAction, out listingControlOutcome: ListingControlOutcome, out deliveryStatus: DeliveryStatus)`

- Source trace: `UC-18 main sequence steps 5-9 and alternative step 8.1; design communication messages 3.1-3.7`
- Function: Orchestrates the listing-control action, owner-notification preparation, and notification-delivery attempt.
- Parameters:
  - `in listingReference`: identifies the listing to update
  - `in listingControlAction`: requested administrative control action
  - `out listingControlOutcome`: result of the listing-control action
  - `out deliveryStatus`: result of the notification-delivery attempt
- Preconditions:
  - `listingControlAction` is intended for the current visibility state of the selected listing.
- Postconditions:
  - `RoomListingLogic` has either rejected or applied the requested control action.
  - When the control action succeeds, a notification payload has been requested from `NotificationService`.
  - A delivery attempt has been made through `EmailProxy` without rolling back a successful listing-control action when email delivery fails.
