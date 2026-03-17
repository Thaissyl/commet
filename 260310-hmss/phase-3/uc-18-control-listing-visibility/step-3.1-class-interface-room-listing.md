# Class Interface Specification: RoomListing

## Class Summary

- Stereotype: `<<data abstraction>>`
- Scope: `UC-18 Control Listing Visibility`
- Hidden Information: in-memory representation of listing identity, presentation data, and visibility state while the current administrative control action is being evaluated and applied
- Structuring Criterion: data abstraction

## Assumptions

- The analysis participant `RoomListing` is refined to a design `<<data abstraction>>`, while persistence concerns are hidden by `RoomListingDB`.
- The current scope treats admin disable as a forced visibility-control outcome on `RoomListing` using the existing listing-state model, not as a separate persistent status outside that model.
- No dedicated `RoomListing` statechart is currently available, so lifecycle-sensitive transition statements remain provisional assumptions.

## Anticipated Changes

- Additional moderation metadata such as disable reason or review note may later be loaded into the in-memory abstraction.
- Future listing-policy refinements may split the current `status` semantics into separate visibility and moderation fields.

## Private Attributes

| Attribute | Type | Purpose |
| --- | --- | --- |
| `- listingId` | `ListingId` | Stores the stable identifier of the room listing. |
| `- propertyId` | `PropertyId` | Stores the parent property reference for traceability to ownership and location context. |
| `- title` | `ListingTitle` | Stores the listing title shown to administrators during review. |
| `- description` | `ListingDescription` | Stores the descriptive content displayed during listing review. |
| `- price` | `ListingPrice` | Stores the price information associated with the listing. |
| `- status` | `ListingStatus` | Stores the current listing status used to derive permitted administrative controls. |
| `- publishedAt` | `PublishedTimestamp` | Stores when the listing became publicly visible. |
| `- updatedAt` | `UpdatedTimestamp` | Stores the latest persisted update time for the listing. |

## Invariants

- `status` must always contain a valid domain listing-status value.
- A listing that is not publicly visible must not be considered eligible for public search.
- Applying an administrative control action must leave the listing in exactly one resulting visibility state.

## Collaborators

- `RoomListingLogic`: requests validated administrative control transitions
- `RoomListingDB`: persists the updated listing state after a successful control action

## Operations Provided

### `+ applyAdministrativeListingControl(in listingControlAction: ListingControlAction, out listingVisibilityRecord: ListingVisibilityRecord)`

- Source trace: `UC-18 main sequence step 7; design communication message 3.4`
- Function: Applies a validated administrative control action to the in-memory listing object and returns the resulting visibility record.
- Parameters:
  - `in listingControlAction`: validated administrative control action to apply
  - `out listingVisibilityRecord`: resulting listing-visibility information after the control attempt
- Preconditions:
  - `listingControlAction` is permitted for the current `status`.
  - In the current scope, `listingControlAction` represents the admin disable action.
- Postconditions:
  - On success, `status` is updated to the resulting non-public state defined by the current policy assumptions.
  - On failure, `status` remains unchanged and the returned record indicates no applied transition.
