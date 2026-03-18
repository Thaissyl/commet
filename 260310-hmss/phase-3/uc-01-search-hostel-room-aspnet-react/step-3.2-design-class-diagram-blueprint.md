# Design Class Diagram Blueprint: UC-01 Search Hostel Room - ASP.NET Simple Layered Backend

## Scope

- Included classes: `VisitorUI`, `RoomSearchController`, `IRoomListingRepository`, `RoomListing`, `SearchMatchingService`, `IGoogleMapsGateway`
- Synchronization source:
  - participant set and call structure from `step-3.0-design-communication-diagram.md`
  - class operations and responsibilities from `step-3.1-class-interface-*.md`

## Class Boxes

### `VisitorUI`

- Stereotype: `<<user interaction>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ openSearch()`
  - `+ submitSearch(in criteria: SearchCriteriaDto)`
  - `+ selectListing(in listingId: Guid)`

### `RoomSearchController`

- Stereotype: `<<coordinator>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getSearchPage(out response: SearchPageResponseDto)`
  - `+ searchRooms(in criteria: SearchCriteriaDto, out response: SearchResponseDto)`
  - `+ getListingEntryPoint(in listingId: Guid, out response: ListingEntryPointResponseDto)`

### `IRoomListingRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ findPublishedListings(out listings: RoomListingList)`

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
  - `- publishedAt: DateTime`
- Operations:
  - none in current scope

### `SearchMatchingService`

- Stereotype: `<<service>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ filterByCriteria(in listings: RoomListingList, in criteria: SearchCriteriaDto, out matchedListings: RoomListingList)`
  - `+ buildListingSummaries(in listings: RoomListingList, out summaries: ListingSummaryList)`

### `IGoogleMapsGateway`

- Stereotype: `<<proxy>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getLocationData(in listings: RoomListingList, out locationData: LocationDataList)`

## Relationships

- association:
  - from: `VisitorUI`
  - to: `RoomSearchController`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `submits requests`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `RoomSearchController`
  - to: `IRoomListingRepository`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `loads listings`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `RoomSearchController`
  - to: `SearchMatchingService`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `filters and summarises`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `RoomSearchController`
  - to: `IGoogleMapsGateway`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `fetches location data`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `IRoomListingRepository`
  - to: `RoomListing`
  - source multiplicity: `1`
  - target multiplicity: `0..*`
  - association name: `returns`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `SearchMatchingService`
  - to: `RoomListing`
  - source multiplicity: `1`
  - target multiplicity: `0..*`
  - association name: `filters and summarises`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `IGoogleMapsGateway`
  - to: `RoomListing`
  - source multiplicity: `1`
  - target multiplicity: `0..*`
  - association name: `retrieves map coordinates for`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

## Generalizations

- none in current scope

## Notes

- This version uses a simplified orchestration style where `RoomSearchController` coordinates repository, service, and gateway collaborators directly.
- `VisitorUI` is included to keep the class diagram aligned with the design communication diagram.
- UC-01 is read-only — no write, mutate, or `applyXxxChange` operations exist in this diagram.
- `RoomListing` (`<<data abstraction>>`) carries domain attributes but provides no behaviour operations in this scope; it acts as a data carrier.
- `SearchMatchingService` owns all multi-criteria filter matching and summary construction logic.
- `IGoogleMapsGateway` encapsulates the external Google Maps API; neither `SearchMatchingService` nor `IRoomListingRepository` may call it directly (COMET rule: business logic / service never calls proxy).
- Map data fetch is modelled as synchronous because the search response depends on it; graceful degradation (empty location data) is handled inside the gateway implementation.
- This class diagram is synchronised with the current `step-3.1` interface specifications.
