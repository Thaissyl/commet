# Design Class Diagram Blueprint: UC-15 Reopen Room Listing - ASP.NET Simple Layered Backend

## Scope

- Included classes: `OwnerUI`, `ReopenRoomController`, `ReopenLogic`, `IRentalRequestRepository`, `IRoomListingRepository`, `IEmailGateway`, `RentalRequest`, `RoomListing`
- Synchronization source:
  - participant set and call structure from `step-3.0-design-communication-diagram.md`
  - class operations derived from step-3.0 messages

## Class Boxes

### `OwnerUI`

- Stereotype: `<<user interaction>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ openReopenFunction()`
  - `+ selectRequest(in requestId: Guid)`
  - `+ confirmReopen(in requestId: Guid)`

### `ReopenRoomController`

- Stereotype: `<<coordinator>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getAcceptedArrangements(in ownerId: Guid, out response: ArrangementListDto)`
  - `+ checkReopenEligibility(in requestId: Guid, out response: EligibilityResponseDto)`
  - `+ submitReopen(in requestId: Guid, out response: StatusChangeResponseDto)`

### `IRentalRequestRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ findAcceptedByOwnerId(in ownerId: Guid, out list: RequestList)`
  - `+ findById(in id: Guid, out entity: RentalRequest)`
  - `+ update(in entity: RentalRequest, out persisted: RentalRequest)`

### `IRoomListingRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ findByRequestId(in requestId: Guid, out entity: RoomListing)`
  - `+ update(in entity: RoomListing, out persisted: RoomListing)`

### `ReopenLogic`

- Stereotype: `<<business logic>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ validateConcurrencyStatus(in request: RentalRequest, out result: ValidationResult)`

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
  - `+ revoke(out result: StatusChangeResult)`

### `RoomListing`

- Stereotype: `<<data abstraction>>`
- Attributes:
  - `- listingId: Guid`
  - `- title: string`
  - `- status: ListingStatus`
- Operations:
  - `+ reopen(out result: StatusChangeResult)`

## Relationships

- association:
  - from: `OwnerUI`
  - to: `ReopenRoomController`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `reopens listing`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ReopenRoomController`
  - to: `IRentalRequestRepository`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `loads and persists`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ReopenRoomController`
  - to: `IRoomListingRepository`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `loads and persists`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ReopenRoomController`
  - to: `ReopenLogic`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `validates concurrency`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ReopenRoomController`
  - to: `IEmailGateway`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `dispatches notification`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ReopenRoomController`
  - to: `RentalRequest`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `mutates state`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `ReopenRoomController`
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

- Dual entity modification: `RentalRequest.revoke()` and `RoomListing.reopen()` both mutate state
- Two-phase: eligibility pre-check (sequence 2), then execution (sequence 3)
- Email dispatch is async (fire-and-forget)
- `findByRequestId` fetches room associated with the rental request
