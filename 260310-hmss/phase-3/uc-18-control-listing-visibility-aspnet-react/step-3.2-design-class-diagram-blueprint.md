# Design Class Diagram Blueprint: UC-18 Control Listing Visibility - ASP.NET Simple Layered Backend

## Scope

- Included classes: `AdminUI`, `ControlListingController`, `IRoomListingRepository`, `IUserAccountRepository`, `ListingControlLogic`, `NotificationService`, `IEmailGateway`, `RoomListing`, `UserAccount`
- Synchronization source:
  - participant set and call structure from `step-3.0-design-communication-diagram.md`
  - class operations derived from implemented controller/service methods

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
  - `+ getVisibleListings(out response: List<AdminListingSummaryDto>)`
  - `+ getListingDetails(in listingId: Guid, out response: AdminListingDetailDto)`
  - `+ disableListing(in listingId: Guid, out response: ControlActionDto)`

### `IRoomListingRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ findByStatusAsync(in status: string, out listings: List<RoomListing>)`
  - `+ findByIdAsync(in id: Guid, out listing: RoomListing)`
  - `+ updateAsync(in entity: RoomListing, out persisted: RoomListing)`

### `IUserAccountRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ findByIdAsync(in id: Guid, out owner: UserAccount)`

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
  - `- status: string`
  - `- imagesRef: string`
- Operations:
  - `+ archive(out result: StatusChangeResult)`

### `UserAccount`

- Stereotype: `<<data abstraction>>`
- Attributes:
  - `- userId: Guid`
  - `- fullName: string`
  - `- email: string`
- Operations:
  - none in current scope

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
  - to: `IUserAccountRepository`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `loads owner info`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ControlListingController`
  - to: `ListingControlLogic`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `validates disable`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ControlListingController`
  - to: `NotificationService`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `creates notice`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ControlListingController`
  - to: `IEmailGateway`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `dispatches email`
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

- association:
  - from: `IUserAccountRepository`
  - to: `UserAccount`
  - source multiplicity: `1`
  - target multiplicity: `0..*`
  - association name: `manages`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

## Generalizations

- none in current scope

## Notes

- `GetVisibleListings(...)` and `GetListingDetails(...)` enrich listing data with owner information from `IUserAccountRepository`.
- The admin disable action is implemented in code as `RoomListing.archive(...)`.
- `NotificationService` composes the email payload after persistence succeeds.
- Email dispatch is async fire-and-forget in the current controller implementation.
- Validation prevents archive-on-already-inactive listings through `ListingControlLogic`.
