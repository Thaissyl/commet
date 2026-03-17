# Class Interface Specification: SearchMatchingService

## Class Summary

- Stereotype: `<<service>>`
- Scope: `UC-01 Search Hostel Room - ASP.NET simple layered backend`
- Hidden Information: Multi-criteria matching algorithm, default ordering strategy, and listing summary construction logic
- Structuring Criterion: service

## Assumptions

- `SearchMatchingService` is a stateless service; it holds no per-request state.
- Filtering is applied in-memory against the `RoomListingList` provided by the controller; the service does not access the repository directly.
- When `criteria` is empty, `filterByCriteria` returns all listings using the default ordering (ordering rule to be finalised per the outstanding question in UC-01).
- Summary construction in `buildListingSummaries` produces only the fields needed for search result cards: title, price, location reference, availability, and listing identifier.

## Anticipated Changes

- Matching algorithm may be extended with new filter dimensions (e.g. rating, room type) without altering the method signature.
- Default ordering strategy will be locked in once the outstanding question in UC-01 is resolved.

## Private Attributes

- None in current scope.

## Invariants

- Must not call `IRoomListingRepository` or any proxy directly; it operates solely on data passed in by the controller.
- Must not perform persistence operations.

## Collaborators

- `RoomSearchController`: sole caller; provides listing data and criteria

## Operations Provided

### `+ filterByCriteria(in listings: RoomListingList, in criteria: SearchCriteriaDto, out matchedListings: RoomListingList)`

- Source communication messages: `2.3`
- Function: Applies the visitor-supplied search criteria against the provided published listings and returns those that satisfy all specified filters. When criteria is empty, returns all listings using the default ordering.
- Parameters:
  - `in listings`: full list of currently published `RoomListing` objects loaded from the repository
  - `in criteria`: visitor-supplied filter values (location, price range, amenities, availability, move-in date); may be empty
  - `out matchedListings`: subset of `listings` that satisfy all non-empty criteria; may be empty
- Preconditions:
  - `listings` is a non-null list (may be empty).
  - `criteria` is a non-null object (individual fields may be absent).
- Postconditions:
  - Every item in `matchedListings` satisfies all non-empty criteria fields.
  - If no listing matches, `matchedListings` is an empty list.
  - If `criteria` is entirely empty, `matchedListings` equals `listings` in default order.

### `+ buildListingSummaries(in listings: RoomListingList, out summaries: ListingSummaryList)`

- Source communication messages: `1.3`, `2.4`
- Function: Constructs lightweight summary representations of the provided listings suitable for display in search result cards.
- Parameters:
  - `in listings`: list of `RoomListing` objects to summarise
  - `out summaries`: list of `ListingSummary` items containing title, price, location reference, availability, and listing identifier
- Preconditions:
  - `listings` is a non-null list (may be empty).
- Postconditions:
  - `summaries` contains one entry per item in `listings`.
  - If `listings` is empty, `summaries` is an empty list.

## Operations Required

- None in current scope.
