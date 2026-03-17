# Class Interface Specification: RoomSearchController

## Class Summary

- Stereotype: `<<coordinator>>`
- Scope: `UC-01 Search Hostel Room - ASP.NET simple layered backend`
- Hidden Information: HTTP route binding, ASP.NET model binding, API response translation, and simplified use-case orchestration across repository, service, and gateway collaborators
- Structuring Criterion: coordinator

## Assumptions

- This class maps to an ASP.NET Web API controller dedicated to room search endpoints.
- No authentication is required; endpoints are publicly accessible.
- The controller delegates filter logic to `SearchMatchingService` and map data retrieval to `IGoogleMapsGateway`, keeping inline logic minimal.
- When `IGoogleMapsGateway` returns empty or partial location data, the controller includes listings in the response without map information rather than failing the request.

## Anticipated Changes

- Endpoint attributes, route versioning, or caching headers may change without altering use-case orchestration.
- If search logic grows substantially, orchestration may be extracted into a dedicated application service.

## Private Attributes

- None in current scope.

## Invariants

- The controller must not embed SQL or Google Maps API details directly.
- The controller must not perform multi-criteria matching inline; filtering is always delegated to `SearchMatchingService`.
- API contracts remain stable for the frontend caller.

## Collaborators

- `VisitorUI`: frontend user-interaction caller
- `IRoomListingRepository`: loads published room listings from persistence
- `SearchMatchingService`: applies filter criteria and builds listing summaries
- `IGoogleMapsGateway`: fetches location data from Google Maps

## Operations Provided

### `+ getSearchPage(out response: SearchPageResponseDto)`

- Source communication messages: `1.1`, `1.2`, `1.3`, `1.4`, `1.5`
- Function: Handles the HTTP request that loads the search page — retrieves all currently published listings, builds summaries, and fetches location data to populate the initial search form view.
- Parameters:
  - `out response`: API response payload containing published listing summaries and available location data
- Preconditions:
  - No authentication is required.
- Postconditions:
  - The response payload contains all currently published listings with summary data and location data where available.
  - If Google Maps is unavailable, the response contains listings without map information.

### `+ searchRooms(in criteria: SearchCriteriaDto, out response: SearchResponseDto)`

- Source communication messages: `2.1`, `2.2`, `2.3`, `2.4`, `2.5`, `2.6`
- Function: Handles the HTTP request that filters published listings by the submitted criteria, builds summaries for matched listings, and fetches their location data.
- Parameters:
  - `in criteria`: visitor-supplied filter values (location, price range, amenities, availability, move-in date); may be empty
  - `out response`: API response payload containing matched listing summaries with location data, or a zero-result payload
- Preconditions:
  - No authentication is required.
- Postconditions:
  - On match, the response payload contains the filtered listing summaries with location data where available.
  - On zero match, the response payload carries an empty result set so the UI can inform the visitor accordingly.
  - If criteria is empty, all published listings are returned using the default ordering.

### `+ getListingEntryPoint(in listingId: Guid, out response: ListingEntryPointResponseDto)`

- Source communication messages: `3.1`
- Function: Handles the HTTP request triggered when a visitor selects a listing from the search results, returning the entry-point data needed to navigate to the listing detail view.
- Parameters:
  - `in listingId`: identifier of the selected room listing
  - `out response`: API response payload providing the listing detail entry point
- Preconditions:
  - No authentication is required.
  - `listingId` identifies an existing published listing.
- Postconditions:
  - The response payload contains the data required for the frontend to navigate to the listing detail page.

## Operations Required

- `IRoomListingRepository.findPublishedListings(out listings: RoomListingList)` from messages `1.2`, `2.2`
- `SearchMatchingService.buildListingSummaries(in listings: RoomListingList, out summaries: ListingSummaryList)` from messages `1.3`, `2.4`
- `SearchMatchingService.filterByCriteria(in listings: RoomListingList, in criteria: SearchCriteriaDto, out matchedListings: RoomListingList)` from message `2.3`
- `IGoogleMapsGateway.getLocationData(in listings: RoomListingList, out locationData: LocationDataList)` from messages `1.4`, `2.5`
