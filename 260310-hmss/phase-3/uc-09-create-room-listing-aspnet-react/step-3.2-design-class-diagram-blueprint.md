# Design Class Diagram Blueprint: UC-09 Create Room Listing - ASP.NET Simple Layered Backend

## Scope

- Included classes: `OwnerUI`, `CreateRoomListingController`, `IRoomListingRepository`, `RoomListingLogic`, `ICloudStorageGateway`, `RoomListing`
- Synchronization source:
  - participant set and call structure from `step-3.0-design-communication-diagram.md`
  - class operations derived from step-3.0 messages

## Class Boxes

### `OwnerUI`

- Stereotype: `<<user interaction>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ openListingCreation(in propertyId: Guid)`
  - `+ processDetails(in request: RoomListingDraftDto, in images: FileList)`
  - `+ saveDraft(in request: RoomListingDraftDto, in imageUrls: List<String>)`

### `CreateRoomListingController`

- Stereotype: `<<coordinator>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getRoomListingForm(in propertyId: Guid, out response: RoomListingFormResponseDto)`
  - `+ processListingDetails(in request: RoomListingDraftDto, in images: FileList, out response: ProcessListingResponseDto)`
  - `+ saveDraftListing(in request: RoomListingDraftDto, in imageUrls: List<String>, out response: ListingResponseDto)`

### `IRoomListingRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ save(in entity: RoomListing, out persisted: RoomListing)`

### `RoomListingLogic`

- Stereotype: `<<business logic>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ validateRequiredFields(in request: RoomListingDraftDto, out result: ValidationResult)`

### `ICloudStorageGateway`

- Stereotype: `<<proxy>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ uploadImages(in images: FileList, out imageUrls: List<String>)`

### `RoomListing`

- Stereotype: `<<data abstraction>>`
- Attributes:
  - `- listingId: Guid`
  - `- propertyId: Guid`
  - `- title: string`
  - `- description: string`
  - `- price: decimal`
  - `- capacity: int`
  - `- status: ListingStatus`
  - `- imagesRef: string`
- Operations:
  - none in current scope

## Relationships

- association:
  - from: `OwnerUI`
  - to: `CreateRoomListingController`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `creates listing`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `CreateRoomListingController`
  - to: `IRoomListingRepository`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `persists`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `CreateRoomListingController`
  - to: `RoomListingLogic`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `validates`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `CreateRoomListingController`
  - to: `ICloudStorageGateway`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `uploads images`
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

- Two-phase operation: validation + upload (sequence 2), then save (sequence 3)
- `imageUrls` parameter forwarded from sequence 2 to sequence 3 (stateless pattern)
- New listings have `status = Draft`
- Image upload is synchronous with reply — URLs returned for preview and embedding
