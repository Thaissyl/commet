# Class Interface Specification: RoomListingDB

## Class Summary

- Stereotype: `<<database wrapper>>`
- Scope: `UC-18 Control Listing Visibility`
- Hidden Information: persistence schema, query details, and update statements used to load and save room-listing data
- Structuring Criterion: database wrapper

## Assumptions

- Room listings are long-lived records and are stored in a physical database.
- Query and persistence mechanics are intentionally hidden behind this wrapper rather than exposed to `RoomListingLogic`.

## Anticipated Changes

- Query optimization or moderation-specific indexing may alter the retrieval strategy without changing the public contract.
- Future audit-trace persistence may be added in the same persistence layer or a separate wrapper.

## Private Attributes

- None in current scope.

## Invariants

- Every retrieval operation must return data consistent with the currently stored room-listing records.
- Save operations must persist the latest listing state produced by `RoomListing`.

## Collaborators

- `RoomListingLogic`: requests room-listing retrieval and persistence services
- `RoomListing`: is reconstituted from or flattened into persisted listing data

## Operations Provided

### `+ findVisibleListingSummaries(out visibleListingList: VisibleListingSummaryList)`

- Source trace: `UC-18 main sequence step 2; design communication message 1.3`
- Function: Loads the summaries of currently publicly visible listings needed for the administration list.
- Parameters:
  - `out visibleListingList`: summaries of visible listings with associated review information
- Preconditions:
  - None in current scope.
- Postconditions:
  - `visibleListingList` reflects the currently persisted listings that are still eligible for public search.

### `+ findListingByReference(in listingReference: ListingReference, out roomListing: RoomListing)`

- Source trace: `UC-18 main sequence steps 4 and 7; design communication messages 2.3 and 3.3`
- Function: Loads the selected listing as a design-level `RoomListing` abstraction.
- Parameters:
  - `in listingReference`: identifies the target listing
  - `out roomListing`: reconstituted in-memory listing abstraction
- Preconditions:
  - `listingReference` identifies an existing stored listing.
- Postconditions:
  - `roomListing` contains the current persisted listing state.

### `+ saveListingVisibility(in roomListing: RoomListing, out listingVisibilityRecord: ListingVisibilityRecord)`

- Source trace: `UC-18 main sequence step 7; design communication message 3.5`
- Function: Persists the updated listing visibility state produced by the in-memory `RoomListing` abstraction.
- Parameters:
  - `in roomListing`: updated in-memory listing abstraction
  - `out listingVisibilityRecord`: persisted visibility record after saving
- Preconditions:
  - `roomListing` contains a valid post-control listing state.
- Postconditions:
  - The latest listing visibility state is persisted.
  - `listingVisibilityRecord` reflects the saved listing visibility state.
