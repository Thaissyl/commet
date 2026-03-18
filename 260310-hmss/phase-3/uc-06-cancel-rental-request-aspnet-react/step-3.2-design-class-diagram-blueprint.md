# Design Class Diagram Blueprint: UC-06 Cancel Rental Request - ASP.NET Simple Layered Backend

## Scope

- Included classes: `TenantUI`, `CancelRentalRequestController`, `IRentalRequestRepository`, `RentalRequest`, `RentalRequestLogic`, `IEmailGateway`
- Synchronization source:
  - participant set and call structure from `step-3.0-design-communication-diagram.md`
  - class operations derived from step-3.0 messages

## Class Boxes

### `TenantUI`

- Stereotype: `<<user interaction>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ openRequestManagement()`
  - `+ checkEligibility(in requestId: Guid)`
  - `+ confirmCancellation(in requestId: Guid)`

### `CancelRentalRequestController`

- Stereotype: `<<coordinator>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getTenantRequests(in tenantId: Guid, out response: TenantRequestListResponseDto)`
  - `+ checkCancellationEligibility(in requestId: Guid, out response: EligibilityResponseDto)`
  - `+ submitCancellation(in requestId: Guid, out response: CancellationResponseDto)`

### `IRentalRequestRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ findTenantRequests(in tenantId: Guid, out list: RentalRequestList)`
  - `+ findById(in id: Guid, out entity: RentalRequest)`
  - `+ update(in entity: RentalRequest, out persisted: RentalRequest)`

### `RentalRequest`

- Stereotype: `<<data abstraction>>`
- Attributes:
  - `- requestId: Guid`
  - `- listingId: Guid`
  - `- tenantId: Guid`
  - `- status: RequestStatus`
  - `- submittedAt: DateTime`
- Operations:
  - `+ applyCancellation(out result: StatusChangeResult)`

### `RentalRequestLogic`

- Stereotype: `<<business logic>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ validateCancellationEligibility(in request: RentalRequest, out result: EligibilityResult)`

### `IEmailGateway`

- Stereotype: `<<proxy>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ sendAsync(in message: EmailMessage)`

## Relationships

- association:
  - from: `TenantUI`
  - to: `CancelRentalRequestController`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `initiates cancellation`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `CancelRentalRequestController`
  - to: `IRentalRequestRepository`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `loads and persists`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `CancelRentalRequestController`
  - to: `RentalRequest`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `mutates state`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `CancelRentalRequestController`
  - to: `RentalRequestLogic`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `validates eligibility`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `CancelRentalRequestController`
  - to: `IEmailGateway`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `dispatches notification`
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

- Three-phase pattern: list (1), validation pre-check (2), execution (3)
- Controller is stateless; `findById` called at validation and execution phases
- Separation of mutation and persistence: `applyCancellation` mutates in RAM, then `update` persists
- `RentalRequest.applyCancellation` has no `in` parameter — entity knows its own state transition (Pending → CancelledByTenant)
- Email dispatch is async (fire-and-forget)
- `RentalRequestLogic` validates: only Pending requests are cancellable
