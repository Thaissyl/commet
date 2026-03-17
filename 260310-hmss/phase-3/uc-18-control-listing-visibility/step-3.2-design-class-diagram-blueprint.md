# Design Class Diagram Blueprint: UC-18 Control Listing Visibility

## Scope

- Included classes: `AdminUI`, `AdminCoordinator`, `RoomListingLogic`, `RoomListing`, `RoomListingDB`, `NotificationService`, `EmailProxy`
- Source artifacts: `step-2.1-static-model.md`, `step-1.3-uc-18-control-listing-visibility.md`, `step-2.2-uc-18-control-listing-visibility-main-seq.md`, `step-3.0-design-communication-diagram.md`

## Class Boxes

### `AdminUI`

- Stereotype: `<<user interaction>>`
- Attributes:
  - `- displayedVisibleListingList: VisibleListingSummaryList`
  - `- selectedListingReference: ListingReference`
  - `- displayedAvailableControlActions: ListingControlActionList`
- Operations:
  - `+ accessListingAdministration(out visibleListingList: VisibleListingSummaryList)`
  - `+ selectListingForReview(in listingReference: ListingReference, out listingDetail: ListingDetail, out availableControlActions: ListingControlActionList)`
  - `+ submitListingControlAction(in listingReference: ListingReference, in listingControlAction: ListingControlAction, out listingControlOutcome: ListingControlOutcome)`

### `AdminCoordinator`

- Stereotype: `<<coordinator>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getVisibleListingList(out visibleListingList: VisibleListingSummaryList)`
  - `+ getListingDetailAndAvailableControlActions(in listingReference: ListingReference, out listingDetail: ListingDetail, out availableControlActions: ListingControlActionList)`
  - `+ applyListingControlAction(in listingReference: ListingReference, in listingControlAction: ListingControlAction, out listingControlOutcome: ListingControlOutcome, out deliveryStatus: DeliveryStatus)`

### `RoomListingLogic`

- Stereotype: `<<business logic>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getVisibleListingList(out visibleListingList: VisibleListingSummaryList)`
  - `+ getListingDetailAndAvailableControlActions(in listingReference: ListingReference, out listingDetail: ListingDetail, out availableControlActions: ListingControlActionList)`
  - `+ applyAdministrativeListingControl(in listingReference: ListingReference, in listingControlAction: ListingControlAction, out listingControlOutcome: ListingControlOutcome)`

### `RoomListing`

- Stereotype: `<<data abstraction>>`
- Attributes:
  - `- listingId: ListingId`
  - `- propertyId: PropertyId`
  - `- title: ListingTitle`
  - `- description: ListingDescription`
  - `- price: ListingPrice`
  - `- status: ListingStatus`
  - `- publishedAt: PublishedTimestamp`
  - `- updatedAt: UpdatedTimestamp`
- Operations:
  - `+ applyAdministrativeListingControl(in listingControlAction: ListingControlAction, out listingVisibilityRecord: ListingVisibilityRecord)`

### `RoomListingDB`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ findVisibleListingSummaries(out visibleListingList: VisibleListingSummaryList)`
  - `+ findListingByReference(in listingReference: ListingReference, out roomListing: RoomListing)`
  - `+ saveListingVisibility(in roomListing: RoomListing, out listingVisibilityRecord: ListingVisibilityRecord)`

### `NotificationService`

- Stereotype: `<<service>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ composeOwnerListingControlNotification(in listingReference: ListingReference, in listingControlOutcome: ListingControlOutcome, out ownerNotification: NotificationMessage)`

### `EmailProxy`

- Stereotype: `<<proxy>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ sendOwnerListingControlNotification(in ownerNotification: NotificationMessage, out deliveryStatus: DeliveryStatus)`

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
  - to: `RoomListingDB`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `queries persistence`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`
- association:
  - from: `RoomListingLogic`
  - to: `RoomListing`
  - source multiplicity: `1`
  - target multiplicity: `0..1`
  - association name: `applies control`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`
- association:
  - from: `RoomListingDB`
  - to: `RoomListing`
  - source multiplicity: `1`
  - target multiplicity: `0..*`
  - association name: `reconstitutes`
  - reading direction: `bottom-to-top`
  - source navigability: `none`
  - target navigability: `navigable`
- association:
  - from: `AdminCoordinator`
  - to: `NotificationService`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `requests notification`
  - reading direction: `top-to-bottom`
  - source navigability: `none`
  - target navigability: `navigable`
- association:
  - from: `AdminCoordinator`
  - to: `EmailProxy`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `dispatches email`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

## Generalizations

- none in current scope

## Notes

- The analysis participant `RoomListing` is refined into `RoomListing <<data abstraction>>` plus `RoomListingDB <<database wrapper>>` because listing data is assumed to be stored in a physical database.
- `RoomListing` encapsulates the in-memory listing state during administrative control evaluation, while `RoomListingDB` hides database retrieval and persistence details.
- The current scope treats the admin control action as a forced removal from public search using the existing listing-state model; no separate listing statechart file currently exists, so lifecycle-sensitive transition statements remain provisional assumptions.
- Notification delivery failure does not roll back a successfully applied listing-control action.
