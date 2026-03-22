# Design Communication Diagram: UC-14 Review Rental Request - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: OwnerUI -> ReviewRequestController, then Controller -> Repository, Controller -> ReviewRequestLogic, and Controller -> IEmailGateway
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label
- Separate reply arrows intentionally omitted; `out` parameters represent returned data
- Request flow style: synchronous request handling with three-phase review flow and conditional dual entity modification

## Object Layout

```text
Owner --- OwnerUI --- ReviewRequestController
                       |--- ReviewRequestLogic
                       |--- IRentalRequestRepository
                       |--- IRoomListingRepository
                       |--- IEmailGateway --- Email Provider
```

## Participants

| Position | Object                   | Stereotype             |
| -------- | ------------------------ | ---------------------- |
| 1        | Owner                    | Actor (primary)        |
| 2        | OwnerUI                  | `<<user interaction>>` |
| 3        | ReviewRequestController  | `<<coordinator>>`      |
| 4        | ReviewRequestLogic       | `<<business logic>>`   |
| 5        | IRentalRequestRepository | `<<database wrapper>>` |
| 6        | IRoomListingRepository   | `<<database wrapper>>` |
| 7        | IEmailGateway            | `<<proxy>>`            |
| 8        | Email Provider           | Actor (secondary)      |

> `RentalRequest` and `RoomListing` removed; return types only, no messages sent to them in this use case.

## Messages

| #   | From -> To                                  | Message                                                            |
| --- | ------------------------------------------- | ------------------------------------------------------------------ |
| 1   | Owner -> OwnerUI                            | Review Access                                                      |
| 1.1 | OwnerUI -> ReviewRequestController          | `GetPendingRequests(out response: PendingRequestsResponseDto)` |
| 1.2 | ReviewRequestController -> IRentalRequestRepository | `FindPendingByOwnerIdAsync(in ownerId: Guid, out requests: List<RentalRequest>)` |
| 1.3 | OwnerUI -> Owner                            | Request List Display                                               |
| 2   | Owner -> OwnerUI                            | Request Selection                                                  |
| 2.1 | OwnerUI -> ReviewRequestController          | `GetRequestDetail(in requestId: Guid, out response: RequestDetailResponseDto)` |
| 2.2 | ReviewRequestController -> IRentalRequestRepository | `FindByIdAsync(in id: Guid, out request: RentalRequest)` |
| 2.3 | OwnerUI -> Owner                            | Request Details Display                                            |
| 3   | Owner -> OwnerUI                            | Request Decision (Accept/Reject/Keep Pending)                      |
| 3.1 | OwnerUI -> ReviewRequestController          | `ProcessRequestDecision(in requestId: Guid, in decision: RequestDecisionDto, out response: DecisionResponseDto)` |
| 3.2 | ReviewRequestController -> IRentalRequestRepository | `FindByIdAsync(in id: Guid, out request: RentalRequest)` |
| 3.3 | ReviewRequestController -> ReviewRequestLogic | `ValidateDecision(in request: RentalRequest, in decision: string, out result: ValidationResult)` |
| 3.4 | ReviewRequestController -> IRentalRequestRepository | `UpdateAsync(in entity: RentalRequest, out persisted: RentalRequest)` |
| 3.5 | ReviewRequestController -> IRoomListingRepository | `UpdateAsync(in entity: RoomListing, out persisted: RoomListing)` |
| 3.6 | ReviewRequestController -> IEmailGateway     | `SendAsync(in message: EmailMessage)` |
| 3.7 | IEmailGateway -> Email Provider              | `SendAsync(in message: EmailMessage)` |
| 3.8 | OwnerUI -> Owner                            | Decision Confirmation Message                                      |

## Analysis -> Design Message Mapping

| Analysis message | Design message | Notes |
|---|---|---|
| `1.1` OwnerUI -> ReviewRequestCoordinator: "Room Requests Query" | `1.1` OwnerUI -> ReviewRequestController: `GetPendingRequests(...)` | renamed |
| `1.2` ReviewRequestCoordinator -> RentalRequest: "Room Requests Data Request" | `1.2` ReviewRequestController -> IRentalRequestRepository: `FindPendingByOwnerIdAsync(...)` | repository query |
| `2.1` OwnerUI -> ReviewRequestCoordinator: "Request Detail Query" | `2.1` OwnerUI -> ReviewRequestController: `GetRequestDetail(...)` | renamed |
| `3.1-3.3` OwnerUI -> ReviewRequestCoordinator -> ReviewRequestRules: "Request Decision Validation" | `3.2-3.3` ReviewRequestController -> IRentalRequestRepository -> ReviewRequestLogic | stateless re-query plus business validation |
| `3.4-3.7` ReviewRequestCoordinator -> RentalRequest, RoomListing, EmailProxy | `3.4-3.7` ReviewRequestController updates entities and sends email | conditional room update and notification |

## Alternative Flow Notes

- **Step 3.3: Validation fails** - `ValidationResult.IsValid = false` (for example, decision no longer valid), entities are not updated
- **Step 3.4: Reject path** - only `RentalRequest` is updated; room listing is not locked
- **Step 3.4: Keep pending path** - no entity update is applied; flow returns to review list
- **Step 3.5-3.7: Accept path** - room listing is locked and tenant notification is sent
- **Step 3.6-3.7: Email fails** - exception is logged, decision remains successful

## Notes

- `OwnerUI` shown explicitly; human actor does not interact directly with backend controller.
- `ReviewRequestController` acts as stateless orchestration point. Sequence 2 and Sequence 3 re-query by ID independently.
- `ReviewRequestLogic` encapsulates `ValidateDecision`; checks whether accept, reject, or keep-pending is valid for the current request state.
- `IRentalRequestRepository` queries and persists `RentalRequest` entity with the owner's decision.
- `IRoomListingRepository` updates `RoomListing` only when the accepted request should lock the room.
- `IEmailGateway` sends notification to tenant about the owner's decision.
- **Conditional dual entity modification**: Accept updates both `RentalRequest` and `RoomListing`; reject updates only `RentalRequest`; keep pending performs no state change.
- **Implicit DTO mapping**: Controller implicitly maps entities to response DTOs. Not shown as separate message.
- Actor-to-UI messages (1, 1.3, 2, 2.3, 3, 3.8) use noun phrases; physical user interactions, not code method calls.
