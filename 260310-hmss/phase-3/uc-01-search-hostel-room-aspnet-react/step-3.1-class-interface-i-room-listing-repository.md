# Class Interface Specification: IRoomListingRepository

## Class Summary

- Stereotype: `<<database wrapper>>`
- Scope: `UC-01 Search Hostel Room - ASP.NET simple layered backend`
- Hidden Information: EF Core queries, SQL filtering, database connection management, and persistence-layer details
- Structuring Criterion: database wrapper

## Assumptions

- This interface is implemented by a concrete EF Core repository; the controller depends only on the interface.
- `findPublishedListings` returns only listings whose `status` equals `Published Available`.
- Ordering when no criteria are supplied follows a default ordering rule to be finalized per the outstanding question in UC-01.

## Anticipated Changes

- Default ordering strategy may be configured externally once finalized.
- Additional query methods (e.g. paginated load) may be added without changing existing signatures.

## Private Attributes

- None in current scope.

## Invariants

- Must not embed business-matching logic; filtering by criteria is the responsibility of `SearchMatchingService`.
- Must not expose raw SQL or EF Core types to callers.

## Collaborators

- `RoomSearchController`: sole caller in this use case scope
- `RoomListing`: domain object returned by load operations

## Operations Provided

### `+ findPublishedListings(out listings: RoomListingList)`

- Source communication messages: `1.2`, `2.2`
- Function: Loads all room listings whose status is `Published Available` from the data store and returns them as a list of `RoomListing` domain objects.
- Parameters:
  - `out listings`: list of currently published `RoomListing` domain objects
- Preconditions:
  - Database connection is available.
- Postconditions:
  - `listings` contains all records with `status = Published Available`; the list may be empty if no published listings exist.

## Operations Required

- None in current scope.
