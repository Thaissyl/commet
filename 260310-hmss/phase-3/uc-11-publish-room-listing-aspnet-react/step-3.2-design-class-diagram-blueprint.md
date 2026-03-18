# Design Class Diagram Blueprint: UC-11 Publish Room Listing - ASP.NET Simple Layered Backend

## Scope

- Included classes: `OwnerUI`, `PublishListingController`, `IRoomListingRepository`, `IOwnerRepository`, `PublishListingLogic`, `RoomListing`, `OwnerProfile`
- Synchronization source:
  - participant set and call structure from `step-3.0-design-communication-diagram.md`
  - class operations derived from step-3.0 messages

## Class Boxes

### `OwnerUI`

- Stereotype: `<<user interaction>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ openPublication(in listingId: Guid)`
  - `+ checkEligibility(in listingId: Guid, in ownerId: Guid)`
  - `+ confirmPublication(in listingId: Guid)`

### `PublishListingController`

- Stereotype: `<<coordinator>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getPublicationForm(in listingId: Guid, out response: PublicationFormDto)`
  - `+ checkPublicationEligibility(in listingId: Guid, in ownerId: Guid, out response: EligibilityResponseDto)`
  - `+ submitPublication(in listingId: Guid, out response: PublicationResponseDto)`

### `IRoomListingRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ findById(in id: Guid, out entity: RoomListing)`
  - `+ update(in entity: RoomListing, out persisted: RoomListing)`

### `IOwnerRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ findById(in id: Guid, out entity: OwnerProfile)`

### `PublishListingLogic`

- Stereotype: `<<business logic>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ validateEligibility(in listing: RoomListing, in owner: OwnerProfile, out result: ValidationResult)`

### `RoomListing`

- Stereotype: `<<data abstraction>>`
- Attributes:
  - `- listingId: Guid`
  - `- propertyId: Guid`
  - `- title: string`
  - `- status: ListingStatus`
  - `- imagesRef: string`
  - `- publishedAt: DateTime`
- Operations:
  - `+ publish(out result: StatusChangeResult)`

### `OwnerProfile`

- Stereotype: `<<data abstraction>>`
- Attributes:
  - `- ownerId: Guid`
  - `- fullName: string`
  - `- verificationStatus: VerificationStatus`
- Operations:
  - none in current scope

## Relationships

- association:
  - from: `OwnerUI`
  - to: `PublishListingController`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `publishes listing`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `PublishListingController`
  - to: `IRoomListingRepository`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `loads and persists`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `PublishListingController`
  - to: `IOwnerRepository`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `loads owner`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `PublishListingController`
  - to: `PublishListingLogic`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `validates eligibility`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `PublishListingController`
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

- association:
  - from: `IOwnerRepository`
  - to: `OwnerProfile`
  - source multiplicity: `1`
  - target multiplicity: `0..*`
  - association name: `manages`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

## Generalizations

- none in current scope

## Notes

- Two-phase operation: eligibility pre-check (sequence 2), then execution (sequence 3)
- `ownerId` passed explicitly to load `OwnerProfile` for verification check
- `RoomListing.publish` has no `in` parameter — entity knows its own transition (Draft → Published Available)
- Critical business rules: owner verified, listing complete, images available — evaluated at runtime, not preconditions
