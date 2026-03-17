# Class Interface Specification: IGoogleMapsGateway

## Class Summary

- Stereotype: `<<proxy>>`
- Scope: `UC-01 Search Hostel Room - ASP.NET simple layered backend`
- Hidden Information: Google Maps API authentication, HTTP transport details, request serialisation, response parsing, and error handling for provider unavailability
- Structuring Criterion: proxy

## Assumptions

- `IGoogleMapsGateway` is an interface; the concrete implementation wraps the Google Maps API HTTP client.
- Location data is fetched synchronously in this use case because the search response depends on it.
- When the Google Maps service is unavailable or returns an error, the gateway returns an empty or partial `locationData` rather than throwing; the controller includes listings in the response without map information.

## Anticipated Changes

- Google Maps API version or authentication scheme may change without altering the interface.
- A fallback or caching strategy for provider unavailability may be added to the concrete implementation.

## Private Attributes

- None in current scope.

## Invariants

- Must not expose Google Maps API keys or transport-level details to callers.
- Must not invoke filtering or business logic; it returns raw location data as received from the external provider.
- `SearchMatchingService` must never call this gateway directly (COMET rule: business logic / service never calls proxy).

## Collaborators

- `RoomSearchController`: sole caller in this use case scope
- `Google Maps`: external actor providing location data

## Operations Provided

### `+ getLocationData(in listings: RoomListingList, out locationData: LocationDataList)`

- Source communication messages: `1.4`, `1.5`, `2.5`, `2.6`
- Function: Requests location and map data from the Google Maps external service for the provided set of room listings and returns the results. Returns empty or partial data gracefully when the provider is unavailable.
- Parameters:
  - `in listings`: list of `RoomListing` objects whose map location data is needed
  - `out locationData`: list of `LocationData` entries corresponding to the provided listings; may be empty if the provider is unavailable
- Preconditions:
  - `listings` is a non-null list (may be empty).
- Postconditions:
  - On success, `locationData` contains one entry per listing with map coordinates and display data.
  - On provider unavailability, `locationData` is empty or partial; no exception is propagated to the controller.

## Operations Required

- `Google Maps.getLocationData(in listings: RoomListingList, out locationData: LocationDataList)` from messages `1.5`, `2.6`
