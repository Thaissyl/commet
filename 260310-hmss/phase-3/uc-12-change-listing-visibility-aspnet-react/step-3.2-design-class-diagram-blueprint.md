# Design Class Diagram Blueprint: UC-12 Change Listing Visibility - ASP.NET Simple Layered Backend

## Scope

- Included classes: `OwnerUI`, `ChangeVisibilityController`, `IRoomListingRepository`, `RoomListing`, `VisibilityLogic`
- Synchronization source:
  - participant set and call structure from `step-3.0-design-communication-diagram.md`
  - class operations derived from step-3.0 messages

## Class Boxes

### `OwnerUI`

- Stereotype: `<<user interaction>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ selectListing(in listingId: Guid)`
  - `+ checkAction(in listingId: Guid, in action: String)`
  - `+ confirmChange(in listingId: Guid, in action: String)`

### `ChangeVisibilityController`

- Stereotype: `<<coordinator>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getListingVisibilityDetails(in listingId: Guid, out response: VisibilityDetailsDto)`
  - `+ checkActionValidity(in listingId: Guid, in action: String, out response: ValidityResponseDto)`
  - `+ submitVisibilityChange(in listingId: Guid, in action: String, out response: StatusChangeResponseDto)`

### `IRoomListingRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ findById(in id: Guid, out entity: RoomListing)`
  - `+ update(in entity: RoomListing, out persisted: RoomListing)`

### `RoomListing`

- Stereotype: `<<data abstraction>>`
- Attributes:
  - `- listingId: Guid`
  - `- title: string`
  - `- status: ListingStatus`
- Operations:
  - `+ changeVisibility(in action: String, out result: StatusChangeResult)`

### `VisibilityLogic`

- Stereotype: `<<business logic>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ validateVisibilityAction(in listing: RoomListing, in action: String, out result: ValidationResult)`

## Relationships

- association:
  - from: `OwnerUI`
  - to: `ChangeVisibilityController`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `changes visibility`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ChangeVisibilityController`
  - to: `IRoomListingRepository`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `loads and persists`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ChangeVisibilityController`
  - to: `RoomListing`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `mutates state`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ChangeVisibilityController`
  - to: `VisibilityLogic`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `validates action`
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

- Two-phase: action validity pre-check (sequence 2), then execution (sequence 3)
- `action: String` parameter for flexibility (hide, archive, etc.)
- Reactive design: UI shows all actions, backend validates and rejects invalid ones
- `RoomListing.changeVisibility` validates permitted transitions internally
