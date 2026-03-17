# Design Class Diagram Blueprint: UC-02 View Room Details - ASP.NET Simple Layered Backend

## Scope

- Included classes: `VisitorUI`, `RoomDetailController`, `IRoomListingRepository`, `RoomListing`, `IGoogleMapsGateway`, `MapData`
- Synchronization source:
  - participant set and call structure from `step-3.0-design-communication-diagram.md`
  - class operations and responsibilities from `step-3.1-class-interface-*.md`

## Class Boxes

### `VisitorUI`

- Stereotype: `<<user interaction>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ selectRoomListing(in listingId: Guid)`
  - `+ requestMapLocation()`

### `RoomDetailController`

- Stereotype: `<<coordinator>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getRoomDetail(in listingId: Guid, out response: RoomDetailResponseDto)`
  - `+ getPropertyMap(in address: String, out response: PropertyMapResponseDto)`

### `IRoomListingRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ findById(in listingId: Guid, out listing: RoomListing)`

### `IGoogleMapsGateway`

- Stereotype: `<<proxy>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getLocationData(in address: String, out mapData: MapData)`

### `RoomListing`

- Stereotype: `<<data abstraction>>`
- Attributes:
  - `- listingId: Guid`
  - `- propertyId: Guid`
  - `- title: String`
  - `- description: String`
  - `- price: Decimal`
  - `- capacity: Integer`
  - `- amenities: String`
  - `- availableFrom: Date`
  - `- furnishedStatus: Boolean`
  - `- privateWCStatus: Boolean`
  - `- imagesRef: String`
  - `- status: String`
  - `- propertyName: String`
  - `- propertyAddress: String`
  - `- createdAt: DateTime`
  - `- updatedAt: DateTime`
  - `- publishedAt: DateTime`
- Operations:
  - none in current scope (data is accessed by controller via field extraction/internal mapping)

### `MapData`

- Stereotype: `<<data abstraction>>`
- Attributes:
  - `- rawResponse: String`
  - `- latitude: Decimal`
  - `- longitude: Decimal`
  - `- embedUrl: String`
  - `- isAvailable: Boolean`
- Operations:
  - none in current scope (data is accessed by controller via field extraction/internal mapping)

> **Note**: `RoomListing` and `MapData` are included as class boxes because they are data types that flow through this UC. However, they have **no provided operations** in this UC because the controller accesses their data internally via field extraction to build response DTOs. They are not direct message targets in the communication diagram.

## Relationships

- association:
  - from: `VisitorUI`
  - to: `RoomDetailController`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `calls`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `RoomDetailController`
  - to: `IRoomListingRepository`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `uses`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `RoomDetailController`
  - to: `IGoogleMapsGateway`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `queries`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

## Generalizations

- none in current scope

## Notes

- This version uses a simplified orchestration style where the controller coordinates repository and gateway collaborators directly.
- `VisitorUI` is included to keep the class diagram aligned with the design communication diagram.
- `RoomListing` and `MapData` are included as class boxes to show their structure (attributes) since they are data types that flow through this UC. However, they have no provided operations in this UC because the controller accesses their data internally via field extraction to build response DTOs.
- `IGoogleMapsGateway` uses synchronous call semantics with strict timeout enforcement because the map response must be returned within the same HTTP request; this differs from the asynchronous pattern used for email dispatch gateways in other UCs.
