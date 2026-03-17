# Class Interface Specification: VisitorUI

## Class Summary

- Stereotype: `<<user interaction>>`
- Scope: `UC-01 Search Hostel Room - ASP.NET simple layered backend`
- Hidden Information: React component rendering, user input capture, display of search results and map data, navigation to listing detail
- Structuring Criterion: user interaction

## Assumptions

- `VisitorUI` is a React frontend component set that renders the search form and result listing cards.
- No authentication is required; this interface is accessible to any visitor.
- The UI handles the empty-result state by displaying a "no matching room" message received from the API response.

## Anticipated Changes

- Search filter controls (e.g. amenity checkboxes, date pickers) may evolve without changing the backend contract.
- Map rendering library or component may be swapped without affecting the controller interface.

## Private Attributes

- None in current scope.

## Invariants

- `VisitorUI` must not call the backend directly; all data requests go through `RoomSearchController`.
- The search form must remain accessible without a logged-in session.

## Collaborators

- `Visitor`: human actor who initiates search and browses results
- `RoomSearchController`: backend coordinator that handles all data requests

## Operations Provided

### `+ openSearch()`

- Source communication messages: `1`
- Function: Receives the visitor's intent to access the room search function and triggers loading of the search page.
- Parameters: none
- Preconditions:
  - Visitor has access to the system (no login required).
- Postconditions:
  - A request is issued to `RoomSearchController.getSearchPage(...)` and the search form with initial listings is rendered.

### `+ submitSearch(in criteria: SearchCriteriaDto)`

- Source communication messages: `2`
- Function: Captures the search criteria entered by the visitor and dispatches a filtered search request.
- Parameters:
  - `in criteria`: visitor-supplied filter values (location, price range, amenities, availability, move-in date); may be empty
- Preconditions:
  - The search form is displayed.
- Postconditions:
  - A request is issued to `RoomSearchController.searchRooms(...)` and the returned matching listings are displayed.
  - If the response carries a zero-result payload, the UI displays a "no matching room" notice and invites criteria revision.

### `+ selectListing(in listingId: Guid)`

- Source communication messages: `3`
- Function: Captures the visitor's selection of a specific listing and navigates to the listing detail view.
- Parameters:
  - `in listingId`: identifier of the selected room listing
- Preconditions:
  - At least one listing is displayed in the search results.
- Postconditions:
  - A request is issued to `RoomSearchController.getListingEntryPoint(...)` and the visitor is navigated to the listing detail page.

## Operations Required

- `RoomSearchController.getSearchPage(out response: SearchPageResponseDto)` from message `1.1`
- `RoomSearchController.searchRooms(in criteria: SearchCriteriaDto, out response: SearchResponseDto)` from message `2.1`
- `RoomSearchController.getListingEntryPoint(in listingId: Guid, out response: ListingEntryPointResponseDto)` from message `3.1`
