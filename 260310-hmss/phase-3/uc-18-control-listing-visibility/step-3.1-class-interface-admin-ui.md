# Class Interface Specification: AdminUI

## Class Summary

- Stereotype: `<<user interaction>>`
- Scope: `UC-18 Control Listing Visibility`
- Hidden Information: UI state for the currently displayed visible-listing list, selected listing, and permitted listing-control actions
- Structuring Criterion: boundary

## Assumptions

- `AdminUI` is the shared administration boundary already identified in `step-2.1-static-model.md`.
- The UI does not evaluate listing-control policy directly; it only collects admin input and renders outputs returned by `AdminCoordinator`.

## Anticipated Changes

- The listing-administration screen may later expose search filters, moderation reasons, or bulk actions without changing the coordinator contract.
- Additional policy-review details may later be displayed before the admin confirms the control action.

## Private Attributes

| Attribute | Type | Purpose |
| --- | --- | --- |
| `- displayedVisibleListingList` | `VisibleListingSummaryList` | Stores the currently displayed publicly visible listings and associated information. |
| `- selectedListingReference` | `ListingReference` | Tracks which listing is being reviewed in the current interaction. |
| `- displayedAvailableControlActions` | `ListingControlActionList` | Stores the control actions permitted for the selected listing. |

## Invariants

- `selectedListingReference` must belong to a listing in `displayedVisibleListingList` before a control-action request is submitted.
- `displayedAvailableControlActions` must reflect the latest selected-listing detail currently shown on screen.

## Collaborators

- `AdminCoordinator`: receives all UI requests and returns application results.

## Operations Provided

### `+ accessListingAdministration(out visibleListingList: VisibleListingSummaryList)`

- Source trace: `UC-18 main sequence steps 1-2; design communication message 1`
- Function: Requests the current list of publicly visible listings for display in the administration screen.
- Parameters:
  - `out visibleListingList`: the visible-listing summaries to be rendered for review
- Preconditions:
  - System Admin is signed in.
- Postconditions:
  - `displayedVisibleListingList` is refreshed from the coordinator response.

### `+ selectListingForReview(in listingReference: ListingReference, out listingDetail: ListingDetail, out availableControlActions: ListingControlActionList)`

- Source trace: `UC-18 main sequence steps 3-4; design communication message 2`
- Function: Requests the selected listing detail and the administrative control actions currently permitted for it.
- Parameters:
  - `in listingReference`: identifies the listing chosen by the admin
  - `out listingDetail`: current information about the selected listing
  - `out availableControlActions`: currently permitted administrative control actions
- Preconditions:
  - `listingReference` identifies an existing listing.
- Postconditions:
  - `selectedListingReference` is updated to `listingReference`.
  - `displayedAvailableControlActions` is updated from the coordinator response.

### `+ submitListingControlAction(in listingReference: ListingReference, in listingControlAction: ListingControlAction, out listingControlOutcome: ListingControlOutcome)`

- Source trace: `UC-18 main sequence steps 5-9 and alternative step 8.1; design communication message 3`
- Function: Submits the admin's confirmed listing-control action and receives the overall outcome to present.
- Parameters:
  - `in listingReference`: identifies the listing to control
  - `in listingControlAction`: the permitted control action selected by the admin
  - `out listingControlOutcome`: business result of the requested control action
- Preconditions:
  - `listingReference` matches the selected listing currently displayed.
  - `listingControlAction` belongs to `displayedAvailableControlActions`.
- Postconditions:
  - The UI shows success or failure feedback returned by the coordinator.
  - When the action succeeds, the displayed listing visibility is refreshed to the resulting non-public state in the outcome.
