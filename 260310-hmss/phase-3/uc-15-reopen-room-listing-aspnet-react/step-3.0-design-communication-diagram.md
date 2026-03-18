# Design Communication Diagram: UC-15 Reopen Room Listing - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: `OwnerUI -> ReopenRoomController`, then `Controller -> Repository`, `Controller -> ReopenLogic`, and `Controller -> IEmailGateway`
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label when a response payload is expected
- Separate reply arrows are intentionally omitted because `out` parameters already represent returned data
- Request flow style: synchronous request handling with two-phase operation and dual entity modification pattern

## Object Layout

```text
Owner --- OwnerUI --- ReopenRoomController
                       |--- ReopenLogic
                       |--- IRentalRequestRepository --- RentalRequest
                       |--- IRoomListingRepository --- RoomListing
                       |--- IEmailGateway --- Email Provider
```

## Participants

| Position | Object                   | Stereotype             |
| -------- | ------------------------ | ---------------------- |
| 1        | Owner                    | Actor (primary)        |
| 2        | OwnerUI                  | `<<user interaction>>` |
| 3        | ReopenRoomController     | `<<coordinator>>`      |
| 4        | ReopenLogic              | `<<business logic>>`   |
| 5        | IRentalRequestRepository | `<<database wrapper>>` |
| 6        | RentalRequest            | `<<data abstraction>>` |
| 7        | IRoomListingRepository   | `<<database wrapper>>` |
| 8        | RoomListing              | `<<data abstraction>>` |
| 9        | IEmailGateway            | `<<proxy>>`            |
| 10       | Email Provider           | Actor (secondary)      |

## Messages

| #   | From -> To                                  | Message                                                            |
| --- | ------------------------------------------- | ------------------------------------------------------------------ |
| 1   | Owner -> OwnerUI                            | Accepted Arrangements Access                                       |
| 1.1 | OwnerUI -> ReopenRoomController             | `getAcceptedArrangements(in ownerId: Guid, out response: ArrangementListDto)` |
| 1.2 | ReopenRoomController -> IRentalRequestRepository | `findAcceptedByOwnerId(in ownerId: Guid, out list: RequestList)` |
| 1.3 | OwnerUI -> Owner                            | Arrangements Display                                               |
| 2   | Owner -> OwnerUI                            | Arrangement Selection                                              |
| 2.1 | OwnerUI -> ReopenRoomController             | `checkReopenEligibility(in requestId: Guid, out response: EligibilityResponseDto)` |
| 2.2 | ReopenRoomController -> IRentalRequestRepository | `findById(in id: Guid, out entity: RentalRequest)`              |
| 2.3 | ReopenRoomController -> ReopenLogic         | `validateConcurrencyStatus(in request: RentalRequest, out result: ValidationResult)` |
| 2.4 | OwnerUI -> Owner                            | Reopen Action Prompt Display                                       |
| 3   | Owner -> OwnerUI                            | Reopen Confirmation                                                |
| 3.1 | OwnerUI -> ReopenRoomController             | `submitReopen(in requestId: Guid, out response: StatusChangeResponseDto)` |
| 3.2 | ReopenRoomController -> IRentalRequestRepository | `findById(in id: Guid, out entity: RentalRequest)`              |
| 3.3 | ReopenRoomController -> IRoomListingRepository | `findByRequestId(in requestId: Guid, out entity: RoomListing)`   |
| 3.4 | ReopenRoomController -> RentalRequest       | `revoke(out result: StatusChangeResult)`                           |
| 3.5 | ReopenRoomController -> RoomListing         | `reopen(out result: StatusChangeResult)`                           |
| 3.6 | ReopenRoomController -> IRentalRequestRepository | `update(in entity: RentalRequest, out persisted: RentalRequest)` |
| 3.7 | ReopenRoomController -> IRoomListingRepository | `update(in entity: RoomListing, out persisted: RoomListing)`     |
| 3.8 | ReopenRoomController -> IEmailGateway       | `sendAsync(in message: EmailMessage)`                              |
| 3.9 | IEmailGateway -> Email Provider             | `sendAsync(in message: EmailMessage)`                              |
| 3.10| OwnerUI -> Owner                            | Reopen Success Message                                             |

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
| ----------------- | -------------- | ----- |
| `1.1` OwnerUI -> ReopenRoomCoordinator: "Accepted Arrangements Query" | `1.1` OwnerUI -> ReopenRoomController: `getAcceptedArrangements(in ownerId: Guid, out response: ArrangementListDto)` | sync, renamed |
| `1.2` ReopenRoomCoordinator -> RentalRequest: "Accepted Arrangements Request" | `1.2` ReopenRoomController -> IRentalRequestRepository: `findAcceptedByOwnerId(in ownerId: Guid, out list: RequestList)` | sync, repository query |
| `2.1` OwnerUI -> ReopenRoomCoordinator: "Arrangement Selection Request" | `2.1` OwnerUI -> ReopenRoomController: `checkReopenEligibility(in requestId: Guid, out response: EligibilityResponseDto)` | sync, two-phase: pre-check |
| `2.2` ReopenRoomCoordinator -> ReopenRules: "Status Concurrency Check" | `2.2` ReopenRoomController -> IRentalRequestRepository: `findById(in id: Guid, out entity: RentalRequest)` then `2.3` validateConcurrencyStatus(...) | load entity for validation |
| `3.1` OwnerUI -> ReopenRoomCoordinator: "Confirmed Reopen Request" | `3.1` OwnerUI -> ReopenRoomController: `submitReopen(in requestId: Guid, out response: StatusChangeResponseDto)` | sync, two-phase: execution |
| `3.2` ReopenRoomCoordinator -> RentalRequest: "Revoked Status Update" | `3.2` ReopenRoomController -> IRentalRequestRepository: `findById(in id: Guid, out entity: RentalRequest)` then `3.4` revoke(...) | load, mutate, persist pattern |
| `3.3` ReopenRoomCoordinator -> RoomListing: "Published Available Status Update" | `3.3` ReopenRoomController -> IRoomListingRepository: `findByRequestId(in requestId: Guid, out entity: RoomListing)` then `3.5` reopen(...) | fetch room, mutate, persist |
| `3.4` ReopenRoomCoordinator -> EmailProxy: "Tenant Notification Request" | `3.8` ReopenRoomController -> IEmailGateway: `sendAsync(in message: EmailMessage)` | async fire-and-forget |

## Alternative Flow Notes

- **Step 2.3: Validation fails** - `ValidationResult.isValid = false`, response contains invalid status reason, messages 3.1-3.9 skipped, use case ends
- **Step 2.2: Request not found** - Repository returns null/error, response contains not found error, use case ends
- **Step 3.2: Request not found** - Repository returns null/error, response contains not found error, use case ends
- **Step 3.3: Room not found** - Repository returns null/error, response contains not found error, use case ends
- **Step 3.6/3.7: Database error on update** - Repository throws exception, response contains error, use case ends
- **Step 3.9: Email Provider unavailable** - Gateway records failure, reopen action succeeds, continues to step 3.10

## Notes

- `OwnerUI` is shown explicitly so the human actor does not interact directly with the backend controller.
- `IRentalRequestRepository` and `IRoomListingRepository` handle persistence and return the updated entities.
- `ReopenRoomController` acts as the simplified orchestration point.
- `ReopenLogic` encapsulates reopen eligibility validation: checks if request is still in Accepted status, validates concurrency status, ensures no conflicting state changes.
- `IEmailGateway` handles asynchronous email dispatch. No `out` parameter because notifications are fire-and-forget.
- **Dual Entity Modification (Messages 3.2 - 3.7)**: Revoking a finalized arrangement modifies two distinct entities:
  - `RentalRequest` status changes to `Revoked by Owner` via `revoke()` method
  - `RoomListing` status changes to `Published Available` via `reopen()` method
  - Both mutations occur in RAM (messages 3.4, 3.5) before persistence (messages 3.6, 3.7)
- **Two-Phase Operation Pattern**: This use case demonstrates the validation-then-execution pattern:
  - **Phase 1 (Pre-check)**: Sequence 2 `checkReopenEligibility` validates concurrency status without modifying state.
  - **Phase 2 (Execution)**: Sequence 3 `submitReopen` performs the actual status changes.
- **Stateless Coordinator Compliance (Messages 1.2, 2.2, 3.2, 3.3)**: The controller executes fresh repository queries at the beginning of each sequence. Web controllers must remain stateless and cannot preserve entities in memory between user clicks. This explicitly solves the concurrency flaw identified in requirements modeling.
- **Separation of State Mutation and Persistence (Messages 3.4, 3.5, 3.6, 3.7)**: Based on the Information Hiding principle, the controller invokes `revoke()` on `RentalRequest` and `reopen()` on `RoomListing` so that objects mutate their own data safely in RAM. Immediately following, it calls `update()` on each repository to guarantee RAM mutations are persisted to disk.
- **Asynchronous External Proxy (Message 3.8)**: The `IEmailGateway` uses `sendAsync(in message)` with no `out` parameter. The controller fires the notification to a background queue and immediately returns success to the user, preventing UI freeze if the Email Provider is slow or unavailable.
- **Repository Query Patterns**:
  - `findAcceptedByOwnerId(in ownerId: Guid)` - Fetches all accepted requests for an owner (sequence 1)
  - `findById(in id: Guid)` - Fetches single entity by ID (sequences 2, 3)
  - `findByRequestId(in requestId: Guid)` - Fetches associated room by request ID (sequence 3)
- **Implicit DTO mapping**: The controller implicitly maps response data from entities to DTOs. This mapping is not shown as a separate message.
- Actor-to-UI messages (1, 1.3, 2, 2.4, 3, 3.10) use noun phrases because they represent physical user interactions, not code method calls.
