# Class Interface Specification: IGoogleMapsGateway

## Class Summary

- Stereotype: `<<proxy>>`
- Scope: `UC-02 View Room Details - ASP.NET simple layered backend`
- Hidden Information: Google Maps API endpoint, HTTP client configuration, API key management, response deserialization, and strict timeout enforcement
- Structuring Criterion: proxy

## Assumptions

- The gateway implementation wraps the Google Maps Geocoding or Maps Embed API; the specific API variant is an implementation detail hidden behind the interface.
- The call is synchronous from the controller's perspective because the map data must be returned in the same HTTP response.
- The gateway enforces a strict timeout (e.g., 3-5 seconds) to prevent indefinite blocking if the external service is degraded.
- The gateway returns a `MapData` data abstraction object (or structured type) to the controller; the controller internally maps this to `PropertyMapResponseDto`.

## Anticipated Changes

- The underlying map provider may be swapped (e.g., OpenStreetMap, Mapbox) without changing the interface contract.
- Additional map query methods (e.g., directions, nearby places) may be added as new use cases require.

## Private Attributes

- None in current scope.

## Invariants

- Must not leak provider-specific API types or error codes through the interface.
- Must enforce a timeout on all external HTTP calls.
- Must always return a structured result; must not propagate network exceptions to the caller.

## Collaborators

- `RoomDetailController`: the sole caller in this UC scope
- `Google Maps`: external map provider called by the implementation

## Operations Provided

### `+ getLocationData(in address: String, out mapData: MapData)`

- Source communication messages: `2.2`
- Function: Queries the external map provider for location data corresponding to a property address and returns structured map data.
- Parameters:
  - `in address`: property address string to resolve
  - `out mapData`: structured map result containing coordinates and embeddable map reference, or an error indicator on failure
- Preconditions:
  - `address` is a non-empty string.
- Postconditions:
  - On success, `mapData` contains coordinates and embed data returned by the provider.
  - On failure (network error, quota exceeded, timeout), `mapData` contains an error indicator; no exception is propagated.
  - The external HTTP call is subject to a strict timeout enforced by the gateway implementation.

## Operations Required

- `Google Maps.getLocationData(in address: String, out rawResponse: String)` — external HTTP call to the Google Maps API

## Traceability

- Source use case: `UC-02 View Room Details`
- Source design communication messages:
  - `2.2 RoomDetailController -> IGoogleMapsGateway`
  - `2.3 IGoogleMapsGateway -> Google Maps`
