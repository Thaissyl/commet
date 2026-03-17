# Class Interface Specification: RoomListingLogic

## Class Summary

- Stereotype: `<<business logic>>`
- Scope: `UC-18 Control Listing Visibility`
- Hidden Information: business rules for visible-listing retrieval, administrative control eligibility, and mapping an admin disable decision to a non-public listing outcome
- Structuring Criterion: business logic

## Assumptions

- In the current project terminology, a publicly visible listing is treated as a listing in `Published Available` status.
- The current scope treats the admin control action as `Disable`; if moderation later distinguishes more admin actions, the action set can expand without changing the main orchestration shape.
- Room-listing data is persisted in a physical database, so persistence access is delegated to `RoomListingDB`.
- No dedicated `RoomListing` statechart is currently available, so lifecycle-sensitive statements remain provisional assumptions derived from the use cases and static-model notes.

## Anticipated Changes

- Future moderation policy may require explicit disable reasons, review notes, or time-bounded takedowns.
- Listing-visibility rules may later separate publication status, moderation status, and requestability into different policy dimensions.

## Private Attributes

- None in current scope.

## Invariants

- A requested administrative control action must be rejected when it is not permitted for the listing's current visibility state.
- The visible-listing list returned for administration must contain only listings that are currently eligible for public search.

## Collaborators

- `AdminCoordinator`: invokes business operations for admin listing control
- `RoomListingDB`: retrieves and persists room-listing data
- `RoomListing`: encapsulates the in-memory listing state during control evaluation and application

## Operations Provided

### `+ getVisibleListingList(out visibleListingList: VisibleListingSummaryList)`

- Source trace: `UC-18 main sequence steps 1-2; design communication messages 1.2-1.3`
- Function: Retrieves the publicly visible listing summaries needed for the administration list view.
- Parameters:
  - `out visibleListingList`: summaries of publicly visible listings and associated review information
- Preconditions:
  - None beyond the caller's authorization, which is enforced outside this class.
- Postconditions:
  - The returned summaries are loaded through `RoomListingDB`.

### `+ getListingDetailAndAvailableControlActions(in listingReference: ListingReference, out listingDetail: ListingDetail, out availableControlActions: ListingControlActionList)`

- Source trace: `UC-18 main sequence steps 3-4; design communication messages 2.2-2.3`
- Function: Loads the selected listing and derives the administrative control actions currently allowed for it.
- Parameters:
  - `in listingReference`: identifies the listing being reviewed
  - `out listingDetail`: current information about the selected listing
  - `out availableControlActions`: permitted control actions derived from the current listing state
- Preconditions:
  - `listingReference` identifies an existing listing.
- Postconditions:
  - `listingDetail` reflects the listing loaded through `RoomListingDB`.
  - `availableControlActions` contains only actions valid for the current listing state in policy scope.

### `+ applyAdministrativeListingControl(in listingReference: ListingReference, in listingControlAction: ListingControlAction, out listingControlOutcome: ListingControlOutcome)`

- Source trace: `UC-18 main sequence steps 5-7; design communication messages 3.2-3.5`
- Function: Loads the target listing, validates the requested administrative control action against the current state, applies the corresponding visibility transition, and persists the updated listing state.
- Parameters:
  - `in listingReference`: identifies the target listing
  - `in listingControlAction`: requested administrative control action
  - `out listingControlOutcome`: result containing the applied visibility outcome or rejection information
- Preconditions:
  - `listingReference` identifies an existing listing.
  - `listingControlAction` is a defined action in the current moderation-policy scope.
  - Under the current assumption set, the target listing is publicly visible before the action is applied.
- Postconditions:
  - On success, the selected listing is no longer eligible for public search and the resulting visibility record is persisted through `RoomListingDB`.
  - On failure, the selected listing's persisted visibility state remains unchanged and the outcome indicates rejection.
