# Design Class Diagram Blueprint: UC-07 Track Rental Request Status - ASP.NET Simple Layered Backend

## Scope

- Included classes: `TenantUI`, `TrackRentalRequestController`, `IRentalRequestRepository`, `RentalRequest`
- Synchronization source:
  - participant set and call structure from `step-3.0-design-communication-diagram.md`
  - class operations derived from step-3.0 messages

## Class Boxes

### `TenantUI`

- Stereotype: `<<user interaction>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ openRequestTracking()`
  - `+ selectRequestDetail(in requestId: Guid)`
  - `+ reviewStatus()`

### `TrackRentalRequestController`

- Stereotype: `<<coordinator>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getTenantRequests(in tenantId: Guid, out response: TenantRequestsResponseDto)`
  - `+ getRequestDetail(in requestId: Guid, out response: RequestDetailResponseDto)`

### `IRentalRequestRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ findTenantRequests(in tenantId: Guid, out list: RentalRequestList)`
  - `+ findById(in id: Guid, out entity: RentalRequest)`

### `RentalRequest`

- Stereotype: `<<data abstraction>>`
- Attributes:
  - `- requestId: Guid`
  - `- listingId: Guid`
  - `- tenantId: Guid`
  - `- status: RequestStatus`
  - `- submittedAt: DateTime`
  - `- decidedAt: DateTime`
- Operations:
  - none in current scope

## Relationships

- association:
  - from: `TenantUI`
  - to: `TrackRentalRequestController`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `tracks status`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `TrackRentalRequestController`
  - to: `IRentalRequestRepository`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `queries`
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

- UC-07 is read-only — no state mutations or external service calls.
- Business logic optimized out: controller queries repository directly; status-to-actions mapping handled via DTO construction.
- Available actions derived from status: Pending → Cancel button; Accepted/Rejected/Cancelled → no actions.
- Controller is stateless; `tenantId` passed explicitly in request.
