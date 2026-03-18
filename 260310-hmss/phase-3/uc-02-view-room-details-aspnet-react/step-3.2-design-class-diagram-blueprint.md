# Design Class Diagram Blueprint: UC-02 View Room Details - ASP.NET Simple Layered Backend

## Scope

- Included classes: `VisitorUI`, `ViewRoomController`, `IRoomListingRepository`, `RoomListing`, `IGoogleMapsGateway`
- Synchronization source:
  - participant set and call structure from `step-3.0-design-communication-diagram.md`
  - class operations derived from step-3.0 messages

## Class Boxes

### `VisitorUI`

- Stereotype: `<<user interaction>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ selectListing(in listingId: Guid)`
  - `+ requestMap(in locationData: String)`

### `ViewRoomController`

- Stereotype: `<<coordinator>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getRoomDetails(in listingId: Guid, out response: RoomDetailDto)`
  - `+ getMapInformation(in locationData: String, out response: MapDto)`

### `IRoomListingRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ findVisibleListingById(in id: Guid, out entity: RoomListing)`

### `RoomListing`

- Stereotype: `<<data abstraction>>`
- Attributes:
  - `- listingId: Guid`
  - `- propertyId: Guid`
  - `- title: string`
  - `- description: string`
  - `- price: decimal`
  - `- capacity: int`
  - `- amenities: AmenityList`
  - `- availableFrom: DateOnly`
  - `- furnishedStatus: FurnishedStatus`
  - `- privateWCStatus: bool`
  - `- imagesRef: string`
  - `- status: ListingStatus`
  - `- visibility: ListingVisibility`
- Operations:
  - none in current scope

### `IGoogleMapsGateway`

- Stereotype: `<<proxy>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getMapData(in locationData: String, out mapData: MapDto)`

## Relationships

- association:
  - from: `VisitorUI`
  - to: `ViewRoomController`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `requests details`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ViewRoomController`
  - to: `IRoomListingRepository`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `queries listing`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ViewRoomController`
  - to: `IGoogleMapsGateway`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `fetches map data`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `IRoomListingRepository`
  - to: `RoomListing`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `returns`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

## Generalizations

- none in current scope

## Notes

- This version uses a simplified orchestration style where `ViewRoomController` coordinates repository and gateway collaborators directly.
- UC-02 is read-only — no write or mutate operations.
- `RoomListing` includes `visibility` attribute for access control; repository filters by visible status in SQL WHERE clause.
- `IRoomListingRepository` handles SQL JOINs internally to fetch property and owner data for the `RoomDetailDto`.
- `IGoogleMapsGateway` encapsulates the external Google Maps API with graceful timeout handling.
