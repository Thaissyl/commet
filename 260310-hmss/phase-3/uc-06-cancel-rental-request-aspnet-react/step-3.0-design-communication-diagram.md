# Design Communication Diagram: UC-06 Cancel Rental Request - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: `TenantUI -> CancelRentalRequestController`, then `Controller -> Repository`, `Controller -> BusinessLogic`, and `Controller -> infrastructure collaborators`
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label when a response payload is expected
- Separate reply arrows are intentionally omitted because `out` parameters already represent returned data
- Request flow style: synchronous request handling with asynchronous email dispatch

## Object Layout

```text
Tenant --- TenantUI --- CancelRentalRequestController
                             |--- IRentalRequestRepository --- RentalRequest
                             |--- RentalRequestLogic
                             |--- IEmailGateway --- Email Provider
```

## Participants

| Position | Object                       | Stereotype             |
| -------- | ---------------------------- | ---------------------- |
| 1        | Tenant                       | Actor (primary)        |
| 2        | TenantUI                     | `<<user interaction>>` |
| 3        | CancelRentalRequestController | `<<coordinator>>`      |
| 4        | IRentalRequestRepository     | `<<database wrapper>>` |
| 5        | RentalRequest                | `<<data abstraction>>` |
| 6        | RentalRequestLogic           | `<<business logic>>`   |
| 7        | IEmailGateway                | `<<proxy>>`            |
| 8        | Email Provider               | Actor (secondary)      |

## Messages

| #   | From -> To                               | Message                                                               |
| --- | ---------------------------------------- | --------------------------------------------------------------------- |
| 1   | Tenant -> TenantUI                       | Request Management Access                                             |
| 1.1 | TenantUI -> CancelRentalRequestController | `getTenantRequests(in tenantId: Guid, out response: TenantRequestListResponseDto)` |
| 1.2 | CancelRentalRequestController -> IRentalRequestRepository | `findTenantRequests(in tenantId: Guid, out list: RentalRequestList)` |
| 1.3 | TenantUI -> Tenant                       | Rental Requests Display                                               |
| 2   | Tenant -> TenantUI                       | Cancellation Selection                                                |
| 2.1 | TenantUI -> CancelRentalRequestController | `checkCancellationEligibility(in requestId: Guid, out response: EligibilityResponseDto)` |
| 2.2 | CancelRentalRequestController -> IRentalRequestRepository | `findById(in id: Guid, out entity: RentalRequest)`                |
| 2.3 | CancelRentalRequestController -> RentalRequestLogic | `validateCancellationEligibility(in request: RentalRequest, out result: EligibilityResult)` |
| 2.4 | TenantUI -> Tenant                       | Cancellation Confirmation Prompt Display                               |
| 3   | Tenant -> TenantUI                       | Cancellation Confirmation                                             |
| 3.1 | TenantUI -> CancelRentalRequestController | `submitCancellation(in requestId: Guid, out response: CancellationResponseDto)` |
| 3.2 | CancelRentalRequestController -> IRentalRequestRepository | `findById(in id: Guid, out entity: RentalRequest)`                |
| 3.3 | CancelRentalRequestController -> RentalRequest | `applyCancellation(out result: StatusChangeResult)`                |
| 3.4 | CancelRentalRequestController -> IRentalRequestRepository | `update(in entity: RentalRequest, out persisted: RentalRequest)` |
| 3.5 | CancelRentalRequestController -> IEmailGateway | `sendAsync(in message: EmailMessage)`                              |
| 3.6 | IEmailGateway -> Email Provider           | `sendAsync(in message: EmailMessage)`                                |
| 3.7 | TenantUI -> Tenant                       | Cancellation Success Message                                          |

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
| ----------------- | -------------- | ----- |
| `1.1` TenantUI -> RentalRequestCoordinator: "Rental Request List Request" | `1.1` TenantUI -> CancelRentalRequestController: `getTenantRequests(in tenantId: Guid, out response: TenantRequestListResponseDto)` | sync, renamed to code-style |
| `1.2` RentalRequestCoordinator -> RentalRequest: "Tenant Requests Query" | `1.2` CancelRentalRequestController -> IRentalRequestRepository: `findTenantRequests(in tenantId: Guid, out list: RentalRequestList)` | sync, added Repository layer |
| `2.1` TenantUI -> RentalRequestCoordinator: "Cancellation Request" | `2.1` TenantUI -> CancelRentalRequestController: `checkCancellationEligibility(in requestId: Guid, out response: EligibilityResponseDto)` | sync, validation endpoint |
| `2.2` RentalRequestCoordinator -> RentalRequestRules: "Cancellation Eligibility Check" | `2.3` CancelRentalRequestController -> RentalRequestLogic: `validateCancellationEligibility(in request: RentalRequest, out result: EligibilityResult)` | sync, business logic encapsulation |
| `3.1` TenantUI -> RentalRequestCoordinator: "Confirmed Cancellation" | `3.1` TenantUI -> CancelRentalRequestController: `submitCancellation(in requestId: Guid, out response: CancellationResponseDto)` | sync, execution endpoint |
| `3.2` RentalRequestCoordinator -> RentalRequest: "Cancellation Status Update" | `3.3` CancelRentalRequestController -> RentalRequest: `applyCancellation(out result: StatusChangeResult)` | sync, state change on domain object (no `in` parameter - entity knows its own transition) |
| `3.3` RentalRequestCoordinator -> EmailProxy: "Owner Notification Request" | `3.5-3.6` CancelRentalRequestController -> IEmailGateway: `sendAsync(in message: EmailMessage)` | async, fire-and-forget |

## Alternative Flow Notes

- **Step 2.3: Request not eligible** - `EligibilityResult.isEligible = false`, response contains reason (already Accepted/Rejected/Cancelled), use case ends
- **Step 3.5-3.6: Email Provider unavailable** - `IEmailGateway.sendAsync()` fails silently, cancellation still succeeds, notification failure logged
- **Step 1.2, 2.2, 3.2: Request not found** - Repository returns null, response contains error, use case ends

## Notes

- `TenantUI` is shown explicitly so the human actor does not interact directly with the backend controller.
- `IRentalRequestRepository` handles persistence and returns domain entities that the controller uses.
- `CancelRentalRequestController` acts as the simplified orchestration point for this use case.
- **Stateless design**: At messages 2.2 and 3.2, the controller calls `findById` to load `RentalRequest` rather than retaining it from message 1.2, ensuring stateless behavior.
- **Separation of mutation and persistence**: Message 3.3 mutates the domain object in RAM using `applyCancellation(out result: StatusChangeResult)`. Message 3.4 immediately persists the mutated state using `update(in entity: RentalRequest, out persisted: RentalRequest)`. This guarantees system durability.
- Email dispatch is intentionally asynchronous to avoid blocking the HTTP request. The `sendAsync(in message: EmailMessage)` operation has no `out` parameter.
- `RentalRequestLogic` encapsulates the cancellation eligibility business rule: a request can only be cancelled if its current status is `Pending`.
- **Domain self-containment**: `RentalRequest.applyCancellation(out result: StatusChangeResult)` has no `in` parameter because the domain object knows its own state transition logic (Pending → CancelledByTenant).
- The use case has three phases: listing (message 1), validation pre-check (message 2), and execution (message 3). The validation phase allows the UI to check eligibility before the user confirms.
- **Implicit email composition**: The controller composes the cancellation notification email content before calling `IEmailGateway.sendAsync()`. This composition is not shown as a separate message.
- Actor-to-UI messages (1, 2, 2.4, 3, 3.7) use noun phrases because they represent physical user interactions, not code method calls.
