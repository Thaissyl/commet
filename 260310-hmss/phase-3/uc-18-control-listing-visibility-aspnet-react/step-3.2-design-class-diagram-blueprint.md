# Design Class Diagram Blueprint: UC-18 Control Listing Visibility - ASP.NET Simple Layered Backend

## Scope

- Included classes: `AdminUI`, `ControlListingController`, `ListingControlLogic`, `IRoomListingRepository`, `NotificationService`, `IEmailGateway`, `RoomListing`
- Synchronization source:
  - participant set and call structure from `step-3.0-design-communication-diagram.md`
  - class operations derived from step-3.0 messages

## Class Boxes

### `AdminUI`

- Stereotype: `<<user interaction>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ openListingAdministration()`
  - `+ selectListing(in listingId: Guid)`
  - `+ disableListing(in listingId: Guid)`

### `ControlListingController`

- Stereotype: `<<coordinator>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getVisibleListings(out response: ListingListDto)`
  - `+ getListingDetails(in listingId: Guid, out response: ListingDetailDto)`
  - `+ disableListing(in listingId: Guid, out response: ControlActionDto)`

### `IRoomListingRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ findByStatus(in status: String, out list: ListingList)`
  - `+ findById(in id: Guid, out entity: RoomListing)`
  - `+ update(in entity: RoomListing, out persisted: RoomListing)`

### `ListingControlLogic`

- Stereotype: `<<business logic>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ validateDisableAction(in listing: RoomListing, out result: ValidationResult)`

### `NotificationService`

- Stereotype: `<<application logic>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ createDisableNotification(in listing: RoomListing, out message: EmailMessage)`

### `IEmailGateway`

- Stereotype: `<<proxy>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ sendAsync(in message: EmailMessage)`

### `RoomListing`

- Stereotype: `<<data abstraction>>`
- Attributes:
  - `- listingId: Guid`
  - `- title: string`
  - `- status: ListingStatus`
- Operations:
  - `+ disableByAdmin(out result: StatusChangeResult)`

## Relationships

- association:
  - from: `AdminUI`
  - to: `ControlListingController`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `controls listings`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ControlListingController`
  - to: `IRoomListingRepository`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `loads and persists`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ControlListingController`
  - to: `ListingControlLogic`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `validates action`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ControlListingController`
  - to: `NotificationService`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `requests notification`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ControlListingController`
  - to: `IEmailGateway`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `dispatches notification`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ControlListingController`
  - to: `RoomListing`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `mutates state`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `IRoomListingRepository`
  - to: `RoomListing`
  - source multiplicity: `1`
  - target multiplicity: `0..*`
  - association name: `manages`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

## Generalizations

- none in current scope

## Notes

- Admin override: disable forcibly removes listings from public visibility regardless of current state
- Two-phase: validation pre-check (sequence 2), then execution (sequence 3)
- `NotificationService` composes email payload before passing to gateway
- Email dispatch is async (fire-and-forget)
- Status concurrency check prevents double-disable on already disabled listings
