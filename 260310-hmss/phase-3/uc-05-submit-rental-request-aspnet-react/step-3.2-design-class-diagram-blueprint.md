# Design Class Diagram Blueprint: UC-05 Submit Rental Request - ASP.NET Simple Layered Backend

## Scope

- Included classes: `TenantUI`, `SubmitRentalRequestController`, `IRoomListingRepository`, `RentalRequestLogic`, `IRentalRequestRepository`, `IEmailGateway`, `RoomListing`, `RentalRequest`
- Synchronization source:
  - participant set and call structure from `step-3.0-design-communication-diagram.md`
  - class operations derived from step-3.0 messages

## Class Boxes

### `TenantUI`

- Stereotype: `<<user interaction>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ openRequestForm(in listingId: Guid)`
  - `+ submitRequest(in request: RentalRequestDto)`

### `SubmitRentalRequestController`

- Stereotype: `<<coordinator>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getRentalRequestForm(in listingId: Guid, out response: RentalRequestFormResponseDto)`
  - `+ submitRentalRequest(in request: RentalRequestDto, out response: SubmissionResponseDto)`

### `IRoomListingRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ findById(in id: Guid, out entity: RoomListing)`

### `RentalRequestLogic`

- Stereotype: `<<business logic>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ validateRequestability(in listing: RoomListing, in request: RentalRequestDto, out result: ValidationResult)`

### `IRentalRequestRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ save(in entity: RentalRequest, out persisted: RentalRequest)`

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
  - `- propertyId: Guid`
  - `- title: string`
  - `- status: ListingStatus`
  - `- visibility: ListingVisibility`
- Operations:
  - none in current scope

### `RentalRequest`

- Stereotype: `<<data abstraction>>`
- Attributes:
  - `- requestId: Guid`
  - `- listingId: Guid`
  - `- tenantId: Guid`
  - `- moveInDate: DateOnly`
  - `- expectedRentalDuration: int`
  - `- occupantCount: int`
  - `- occupationCategory: OccupationCategory`
  - `- budgetExpectation: decimal`
  - `- contactPhone: string`
  - `- preferredContactMethod: ContactMethod`
  - `- specialNotes: string`
  - `- status: RequestStatus`
  - `- submittedAt: DateTime`
- Operations:
  - none in current scope

## Relationships

- association:
  - from: `TenantUI`
  - to: `SubmitRentalRequestController`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `submits request`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `SubmitRentalRequestController`
  - to: `IRoomListingRepository`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `loads listing`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `SubmitRentalRequestController`
  - to: `RentalRequestLogic`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `validates`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `SubmitRentalRequestController`
  - to: `IRentalRequestRepository`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `persists`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `SubmitRentalRequestController`
  - to: `IEmailGateway`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `dispatches notification`
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
  - from: `IRentalRequestRepository`
  - to: `RentalRequest`
  - source multiplicity: `1`
  - target multiplicity: `0..*`
  - association name: `manages`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

## Generalizations

- none in current scope

## Notes

- Controller is stateless; `findById` is called again at submission time rather than retaining the listing from form load.
- Email dispatch is asynchronous (fire-and-forget) to avoid blocking the HTTP request.
- `RentalRequestLogic` validates whether the listing can accept new requests (status, visibility, existing requests).
- DTO-to-entity mapping is implicit before `save()` call.
