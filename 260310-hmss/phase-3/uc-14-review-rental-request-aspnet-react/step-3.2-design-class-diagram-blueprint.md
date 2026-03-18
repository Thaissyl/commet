# Design Class Diagram Blueprint: UC-14 Review Rental Request - ASP.NET Simple Layered Backend

## Scope

- Included classes: `OwnerUI`, `ReviewRequestController`, `ReviewRequestLogic`, `IRentalRequestRepository`, `IRoomListingRepository`, `IEmailGateway`, `RentalRequest`, `RoomListing`
- Synchronization source:
  - participant set and call structure from `step-3.0-design-communication-diagram.md`
  - class operations derived from step-3.0 messages

## Class Boxes

### `OwnerUI`

- Stereotype: `<<user interaction>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ openReviewFunction(in roomId: Guid)`
  - `+ selectRequest(in requestId: Guid)`
  - `+ acceptRequest(in requestId: Guid)`

### `ReviewRequestController`

- Stereotype: `<<coordinator>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getRoomRequests(in roomId: Guid, out response: RequestListResponseDto)`
  - `+ getRequestDetail(in requestId: Guid, out response: RequestDetailResponseDto)`
  - `+ acceptRequest(in requestId: Guid, out response: DecisionResponseDto)`

### `IRentalRequestRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ findByRoomId(in id: Guid, out list: RequestList)`
  - `+ findById(in id: Guid, out entity: RentalRequest)`
  - `+ update(in entity: RentalRequest, out persisted: RentalRequest)`

### `IRoomListingRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ findByRequestId(in requestId: Guid, out entity: RoomListing)`
  - `+ update(in entity: RoomListing, out persisted: RoomListing)`

### `ReviewRequestLogic`

- Stereotype: `<<business logic>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ validateAcceptance(in request: RentalRequest, in room: RoomListing, out result: ValidationResult)`

### `IEmailGateway`

- Stereotype: `<<proxy>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ sendAsync(in message: EmailMessage)`

### `RentalRequest`

- Stereotype: `<<data abstraction>>`
- Attributes:
  - `- requestId: Guid`
  - `- listingId: Guid`
  - `- tenantId: Guid`
  - `- status: RequestStatus`
- Operations:
  - `+ accept(out result: StatusChangeResult)`

### `RoomListing`

- Stereotype: `<<data abstraction>>`
- Attributes:
  - `- listingId: Guid`
  - `- title: string`
  - `- status: ListingStatus`
- Operations:
  - `+ lock(out result: StatusChangeResult)`

## Relationships

- association:
  - from: `OwnerUI`
  - to: `ReviewRequestController`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `reviews requests`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ReviewRequestController`
  - to: `IRentalRequestRepository`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `loads and persists`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ReviewRequestController`
  - to: `IRoomListingRepository`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `loads and persists`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ReviewRequestController`
  - to: `ReviewRequestLogic`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `validates`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ReviewRequestController`
  - to: `IEmailGateway`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `dispatches notification`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ReviewRequestController`
  - to: `RentalRequest`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `mutates state`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ReviewRequestController`
  - to: `RoomListing`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `mutates state`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `IRentalRequestRepository`
  - to: `RentalRequest`
  - source multiplicity: `1`
  - target multiplicity: `0..*`
  - association name: `manages`
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

- Dual entity modification: `RentalRequest.accept()` and `RoomListing.lock()` both mutate state
- Both entities loaded and persisted separately in sequence 3
- Email dispatch is async (fire-and-forget)
- Alternative flows: reject (no room modification), keep pending (no state changes)
