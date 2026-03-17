# Example Blueprint

```md
# Design Class Diagram Blueprint: Control Listing Visibility

## Scope

- Included classes: `AdminUI`, `AdminCoordinator`, `RoomListingLogic`, `RoomListing`

## Class Boxes

### `AdminUI`

- Stereotype: `<<user interaction>>`
- Attributes:
  - `- displayedVisibleListingList: VisibleListingList`
  - `- selectedListingReference: RoomListingReference`
- Operations:
  - `+ accessListingAdministration(out visibleListingList: VisibleListingList)`
  - `+ selectListing(in listingReference: RoomListingReference, out listingDetail: ListingDetail, out availableControlActions: ListingControlActionList)`
  - `+ submitListingVisibilityChange(in listingReference: RoomListingReference, in listingControlAction: ListingControlAction, out listingControlResult: ListingControlResult)`

### `AdminCoordinator`

- Stereotype: `<<coordinator>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getVisibleListingList(out visibleListingList: VisibleListingList)`
  - `+ getListingDetailAndAvailableControlActions(in listingReference: RoomListingReference, out listingDetail: ListingDetail, out availableControlActions: ListingControlActionList)`
  - `+ applyListingVisibilityControl(in listingReference: RoomListingReference, in listingControlAction: ListingControlAction, out listingControlResult: ListingControlResult, out deliveryStatus: DeliveryStatus)`

### `RoomListingLogic`

- Stereotype: `<<business logic>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getVisibleListingList(out visibleListingList: VisibleListingList)`
  - `+ getListingDetailAndAvailableControlActions(in listingReference: RoomListingReference, out listingDetail: ListingDetail, out availableControlActions: ListingControlActionList)`
  - `+ changeListingVisibility(in listingReference: RoomListingReference, in listingControlAction: ListingControlAction, out listingControlResult: ListingControlResult)`

### `RoomListing`

- Stereotype: `<<data abstraction>>`
- Attributes:
  - `- status: RoomListingStatus`
  - `- visibility: ListingVisibility`
- Operations:
  - `+ getListingDetail(in listingReference: RoomListingReference, out listingDetail: ListingDetail)`
  - `+ applyAdminDisable(in listingReference: RoomListingReference, in listingControlAction: ListingControlAction, out listingVisibilityRecord: ListingVisibilityRecord)`

## Relationships

- association:
  - from: `AdminUI`
  - to: `AdminCoordinator`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `submits requests`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`
- association:
  - from: `AdminCoordinator`
  - to: `RoomListingLogic`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `delegates rules`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`
- association:
  - from: `RoomListingLogic`
  - to: `RoomListing`
  - source multiplicity: `1`
  - target multiplicity: `1..*`
  - association name: `updates visibility`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

## Generalizations

- none in current scope

## Notes

- RoomListing: visibility changes do not alter listing ownership.
```
