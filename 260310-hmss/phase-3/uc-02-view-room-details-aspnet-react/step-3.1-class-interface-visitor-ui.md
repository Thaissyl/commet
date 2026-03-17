# Class Interface Specification: VisitorUI

## Class Summary

- Stereotype: `<<user interaction>>`
- Scope: `UC-02 View Room Details - ASP.NET simple layered backend`
- Hidden Information: React component state, routing logic, UI rendering, and translation of user gestures into HTTP requests
- Structuring Criterion: user interaction

## Assumptions

- The visitor has already navigated to a room listing page (e.g., from UC-01 search results or a direct URL).
- The `listingId` is available from the route parameter or link state when the page loads.
- After loading room detail, the UI retains the property address string in component state for use in the map request.

## Anticipated Changes

- The set of room-detail fields displayed may be refined in later releases.
- Map display may be embedded directly on the page rather than triggered by a separate user action.

## Private Attributes

- None in current scope.

## Invariants

- Must not expose raw domain objects to the view layer; always renders from the response DTO received from the controller.

## Collaborators

- `RoomDetailController`: backend controller that handles room detail and map queries

## Operations Provided

### `+ selectRoomListing(in listingId: Guid)`

- Source communication messages: `1`
- Function: Initiates a room detail page load when the visitor selects or navigates to a specific listing.
- Parameters:
  - `in listingId`: identifier of the selected room listing
- Preconditions:
  - The listing page is accessible via the provided `listingId`.
- Postconditions:
  - A `getRoomDetail` request is issued to `RoomDetailController` with the given `listingId`.

### `+ requestMapLocation()`

- Source communication messages: `2`
- Function: Triggers a map data fetch when the visitor requests location information for the property.
- Parameters:
  - none
- Preconditions:
  - Room detail has been successfully loaded and the property address is available in UI state.
- Postconditions:
  - A `getPropertyMap` request is issued to `RoomDetailController` with the address string from UI state.

## Operations Required

- `RoomDetailController.getRoomDetail(in listingId: Guid, out response: RoomDetailResponseDto)` from message `1.1`
- `RoomDetailController.getPropertyMap(in address: String, out response: PropertyMapResponseDto)` from message `2.1`

## Traceability

- Source use case: `UC-02 View Room Details`
- Source design communication messages:
  - `1 Visitor -> VisitorUI`
  - `2 Visitor -> VisitorUI`
