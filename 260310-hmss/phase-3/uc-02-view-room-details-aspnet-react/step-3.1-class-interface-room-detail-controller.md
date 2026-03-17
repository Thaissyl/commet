# Class Interface Specification: RoomDetailController

## Class Summary

- Stereotype: `<<coordinator>>`
- Scope: `UC-02 View Room Details - ASP.NET simple layered backend`
- Hidden Information: HTTP route binding, ASP.NET model binding, API response translation, DTO mapping logic, and orchestration across repository and map gateway
- Structuring Criterion: coordinator

## Assumptions

- This class maps to an ASP.NET Web API controller dedicated to room detail endpoints.
- No authentication is required; room detail is publicly accessible for visible listings.
- The controller re-uses repository access per request; no cross-request caching is handled here.
- **DTO mapping happens internally**: When repository returns `RoomListing`, controller extracts fields and builds `RoomDetailResponseDto`. When gateway returns `MapData`, controller extracts fields and builds `PropertyMapResponseDto`. These are internal operations, not separate outgoing messages.

## Anticipated Changes

- Caching of room detail responses may be introduced at the controller or middleware level without altering the operation signatures.
- Additional detail fields (e.g., owner contact info, related listings) may be added to `RoomDetailResponseDto` in later releases.

## Private Attributes

- None in current scope.

## Invariants

- The controller must not embed SQL or provider-specific map API details directly.
- The controller must verify listing visibility before returning room detail data.
- API contracts remain stable for the frontend caller.
- DTO mapping from data abstractions to response objects happens within the controller's operation implementation.

## Collaborators

- `VisitorUI`: frontend user-interaction caller
- `IRoomListingRepository`: loads room listing records including property address
- `IGoogleMapsGateway`: queries Google Maps for property location data

## Operations Provided

### `+ getRoomDetail(in listingId: Guid, out response: RoomDetailResponseDto)`

- Source communication messages: `1.1`, `1.2`
- Function: Handles the HTTP request that loads and returns full room detail for a given listing.
- Parameters:
  - `in listingId`: identifier of the requested room listing
  - `out response`: API response payload containing room title, description, price, amenities, capacity, availability status, move-in date, images, property name, property address, and basic owner information
- Preconditions:
  - `listingId` identifies an existing listing whose `status` is publicly visible.
- Postconditions:
  - Internally calls `IRoomListingRepository.findById` to obtain `RoomListing` data abstraction.
  - Internally maps `RoomListing` fields to `RoomDetailResponseDto`.
  - `response` contains the mapped DTO data.
  - If the listing is not found or not publicly visible, `response` contains an appropriate error indicator.

### `+ getPropertyMap(in address: String, out response: PropertyMapResponseDto)`

- Source communication messages: `2.1`, `2.2`
- Function: Handles the HTTP request that retrieves map or location data for a property address by delegating to the map gateway.
- Parameters:
  - `in address`: property address string supplied by the UI from the previously loaded room detail
  - `out response`: API response payload containing map data or an unavailability indicator
- Preconditions:
  - `address` is a non-empty string.
- Postconditions:
  - Internally calls `IGoogleMapsGateway.getLocationData` to obtain `MapData` data abstraction.
  - Internally maps `MapData` fields to `PropertyMapResponseDto`.
  - On success, `response` contains the mapped map data.
  - On gateway failure, `response` contains an unavailability indicator; no exception is propagated to the caller.

## Operations Required

- `IRoomListingRepository.findById(in listingId: Guid, out listing: RoomListing)` from message `1.2`
- `IGoogleMapsGateway.getLocationData(in address: String, out mapData: MapData)` from message `2.2`

## Traceability

- Source use case: `UC-02 View Room Details`
- Source design communication messages:
  - `1.1 VisitorUI -> RoomDetailController`
  - `1.2 RoomDetailController -> IRoomListingRepository`
  - `2.1 VisitorUI -> RoomDetailController`
  - `2.2 RoomDetailController -> IGoogleMapsGateway`
