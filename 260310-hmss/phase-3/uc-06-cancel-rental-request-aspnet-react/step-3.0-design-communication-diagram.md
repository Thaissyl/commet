# Design Communication Diagram: UC-06 Cancel Rental Request - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: TenantUI -> TenantRentalRequestController, then Controller -> Repository, Controller -> BusinessLogic, and Controller -> infrastructure collaborators
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label
- Separate reply arrows intentionally omitted — `out` parameters represent returned data
- Request flow style: synchronous request handling with asynchronous email dispatch

## Object Layout

```text
Tenant --- TenantUI --- TenantRentalRequestController
                             |--- IRentalRequestRepository
                             |--- RentalRequestLogic
                             |--- IEmailGateway --- Email Provider
```

## Participants

| Position | Object                        | Stereotype             |
| -------- | ----------------------------- | ---------------------- |
| 1        | Tenant                        | Actor (primary)        |
| 2        | TenantUI                      | `<<user interaction>>` |
| 3        | TenantRentalRequestController | `<<coordinator>>`      |
| 4        | IRentalRequestRepository      | `<<database wrapper>>` |
| 5        | RentalRequestLogic            | `<<business logic>>`   |
| 6        | IEmailGateway                 | `<<proxy>>`            |
| 7        | Email Provider                | Actor (secondary)      |

> `RentalRequest` removed — it is an entity return type, not a message-passing object. Communication diagrams only show objects that send or receive messages.

## Messages

| #   | From -> To                               | Message                                                               |
| --- | ---------------------------------------- | --------------------------------------------------------------------- |
| 1   | Tenant -> TenantUI                       | Request Management Access                                             |
| 1.1 | TenantUI -> TenantRentalRequestController | `GetTenantRequests(in tenantId: Guid, out response: TenantRequestListResponseDto)` |
| 1.2 | TenantRentalRequestController -> IRentalRequestRepository | `FindByTenantIdAsync(in tenantId: Guid, out list: List<RentalRequest>)` |
| 1.3 | TenantUI -> Tenant                       | Rental Requests Display                                               |
| 2   | Tenant -> TenantUI                       | Cancellation Selection                                                |
| 2.1 | TenantUI -> TenantRentalRequestController | `CheckCancellationEligibility(in requestId: Guid, out response: EligibilityResponseDto)` |
| 2.2 | TenantRentalRequestController -> IRentalRequestRepository | `FindByIdAsync(in id: Guid, out entity: RentalRequest)`                |
| 2.3 | TenantRentalRequestController -> RentalRequestLogic | `ValidateCancellationEligibility(in request: RentalRequest, out result: EligibilityResult)` |
| 2.4 | TenantUI -> Tenant                       | Cancellation Confirmation Prompt Display                               |
| 3   | Tenant -> TenantUI                       | Cancellation Confirmation                                             |
| 3.1 | TenantUI -> TenantRentalRequestController | `SubmitCancellation(in requestId: Guid, out response: CancellationResponseDto)` |
| 3.2 | TenantRentalRequestController -> IRentalRequestRepository | `FindByIdAsync(in id: Guid, out entity: RentalRequest)` |
| 3.3 | TenantRentalRequestController -> RentalRequestLogic | `ValidateCancellationEligibility(in request: RentalRequest, out result: EligibilityResult)` |
| 3.4 | TenantRentalRequestController -> IRentalRequestRepository | `UpdateAsync(in entity: RentalRequest, out persisted: RentalRequest)` |
| 3.5 | TenantRentalRequestController -> IEmailGateway | `SendAsync(in message: EmailMessage)` [to Owner] |
| 3.6 | IEmailGateway -> Email Provider           | `SendAsync(in message: EmailMessage)` |
| 3.7 | TenantUI -> Tenant                       | Cancellation Success Message                                          |

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
|---|---|---|
| `1.1` TenantUI -> CancelRentalRequestCoordinator: "Request Management Request" | `1.1` TenantUI -> TenantRentalRequestController: `GetTenantRequests(...)` | renamed |
| `1.2` CancelRentalRequestCoordinator -> RentalRequest: "Tenant Requests Query" | `1.2` TenantRentalRequestController -> IRentalRequestRepository: `FindByTenantIdAsync(...)` | repository layer |
| `2.1` TenantUI -> CancelRentalRequestCoordinator: "Cancellation Eligibility Check" | `2.1` TenantUI -> TenantRentalRequestController: `CheckCancellationEligibility(...)` | renamed |
| `2.2-2.3` CancelRentalRequestCoordinator -> RentalRequestRules: "Eligibility Validation" | `2.3` TenantRentalRequestController -> RentalRequestLogic: `ValidateCancellationEligibility(...)` | business logic |
| `3.1` TenantUI -> CancelRentalRequestCoordinator: "Cancellation Submission" | `3.1` TenantUI -> TenantRentalRequestController: `SubmitCancellation(...)` | renamed |
| `3.5-3.7` CancelRentalRequestCoordinator -> NotificationService -> EmailProxy -> Email: "Owner Notification" | `3.5-3.6` TenantRentalRequestController -> IEmailGateway: `SendAsync(...)` to Owner | **CORRECTED:** sends to owner, not tenant |

## Alternative Flow Notes

- **Step 2.3: Ineligible for cancellation** — `ValidateCancellationEligibility` returns invalid (e.g., already cancelled or accepted), response includes reason, use case ends
- **Step 3.3: Status change fails** — `ApplyCancellation()` returns failure, request not persisted
- **Step 3.5-3.6: Email Provider unavailable** — `IEmailGateway.SendAsync()` catches exception, cancellation succeeds, notification failure logged
- **Step 2.2, 3.2: Request not found or unauthorized** — Repository returns null or tenant ID doesn't match, response contains error

## Notes

- `TenantUI` shown explicitly — human actor does not interact directly with backend controller.
- `TenantRentalRequestController` handles both "get my requests" (sequence 1) and "cancel request" (sequences 2-3) operations.
- **Owner notification (Message 3.5)**: Controller notifies the **property owner** (not the tenant) of the cancellation. Message composes `EmailMessage(owner.Email, "Rental Request Cancelled", ...)` before calling `IEmailGateway.SendAsync()`.
- **Email dispatch asynchronous**: `SendAsync(in message: EmailMessage)` has no `out` parameter — fire-and-forget pattern.
- `RentalRequestLogic` provides `ValidateCancellationEligibility` — checks if request status allows cancellation (must be Pending).
- Entity method `RentalRequest.ApplyCancellation()` called directly in controller after validation — updates status to "Cancelled". Not shown as separate message.
- **Implicit DTO mapping**: Controller implicitly maps entity data to response DTOs. Not shown as separate message.
- Actor-to-UI messages (1, 1.3, 2, 2.4, 3, 3.7) use noun phrases — physical user interactions, not code method calls.
