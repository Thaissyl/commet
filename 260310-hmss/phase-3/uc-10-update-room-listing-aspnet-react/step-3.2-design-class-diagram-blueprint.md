# Design Class Diagram Blueprint: UC-10 Update Room Listing - ASP.NET Simple Layered Backend

## Scope

- Included classes: `OwnerUI`, `UpdateRoomListingController`, `IRoomListingRepository`, `RoomListingLogic`, `ICloudStorageGateway`, `RoomListing`
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
  - `+ processUpdates(in request: RoomListingUpdateDto, in newImages: FileList)`
  - `+ submitUpdate(in request: RoomListingUpdateDto, in newImageUrls: List<String>)`

### `UpdateRoomListingController`

- Stereotype: `<<coordinator>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getListingForUpdate(in listingId: Guid, out response: ListingFormResponseDto)`
  - `+ processListingUpdates(in request: RoomListingUpdateDto, in newImages: FileList, out response: ProcessUpdateResponseDto)`
  - `+ submitListingUpdate(in request: RoomListingUpdateDto, in newImageUrls: List<String>, out response: ListingResponseDto)`

### `IRoomListingRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ findById(in id: Guid, out entity: RoomListing)`
  - `+ update(in entity: RoomListing, out persisted: RoomListing)`

### `RoomListingLogic`

- Stereotype: `<<business logic>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ validateUpdates(in entity: RoomListing, in request: RoomListingUpdateDto, out result: ValidationResult)`

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
  - `- imagesRef: string`
  - `- status: ListingStatus`
- Operations:
  - `+ applyUpdates(in request: RoomListingUpdateDto, in newImageUrls: List<String>, out result: StatusChangeResult)`

## Relationships

- association:
  - from: `OwnerUI`
  - to: `UpdateRoomListingController`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `updates listing`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `UpdateRoomListingController`
  - to: `IRoomListingRepository`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `loads and persists`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `UpdateRoomListingController`
  - to: `RoomListingLogic`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `validates`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `UpdateRoomListingController`
  - to: `ICloudStorageGateway`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `uploads images`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `UpdateRoomListingController`
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

- Three-phase: load (1), validate + upload (2), submit update (3)
- Controller is stateless; `findById` called at sequences 2 and 3
- Conditional image upload: only called if `newImages` is not empty
- `newImageUrls` parameter forwarded from sequence 2 to sequence 3
- Separation of mutation and persistence: `applyUpdates` then `update`
