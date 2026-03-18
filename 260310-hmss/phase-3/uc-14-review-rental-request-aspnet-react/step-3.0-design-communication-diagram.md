# Design Communication Diagram: UC-14 Review Rental Request - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: `OwnerUI -> ReviewRequestController`, then `Controller -> Repository`, `Controller -> ReviewRequestLogic`, and `Controller -> IEmailGateway`
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label when a response payload is expected
- Separate reply arrows are intentionally omitted because `out` parameters already represent returned data
- Request flow style: synchronous request handling with dual entity modification pattern

## Object Layout

```text
Owner --- OwnerUI --- ReviewRequestController
                       |--- ReviewRequestLogic
                       |--- IRentalRequestRepository --- RentalRequest
                       |--- IRoomListingRepository --- RoomListing
                       |--- IEmailGateway --- Email Provider
```

## Participants

| Position | Object                      | Stereotype             |
| -------- | --------------------------- | ---------------------- |
| 1        | Owner                       | Actor (primary)        |
| 2        | OwnerUI                     | `<<user interaction>>` |
| 3        | ReviewRequestController     | `<<coordinator>>`      |
| 4        | ReviewRequestLogic          | `<<business logic>>`   |
| 5        | IRentalRequestRepository    | `<<database wrapper>>` |
| 6        | RentalRequest               | `<<data abstraction>>` |
| 7        | IRoomListingRepository      | `<<database wrapper>>` |
| 8        | RoomListing                 | `<<data abstraction>>` |
| 9        | IEmailGateway               | `<<proxy>>`            |
| 10       | Email Provider              | Actor (secondary)      |

## Messages

| #   | From -> To                                  | Message                                                            |
| --- | ------------------------------------------- | ------------------------------------------------------------------ |
| 1   | Owner -> OwnerUI                            | Review Function Access                                             |
| 1.1 | OwnerUI -> ReviewRequestController           | `getRoomRequests(in roomId: Guid, out response: RequestListResponseDto)` |
| 1.2 | ReviewRequestController -> IRentalRequestRepository | `findByRoomId(in id: Guid, out list: RequestList)`             |
| 1.3 | OwnerUI -> Owner                            | Requests Display                                                   |
| 2   | Owner -> OwnerUI                            | Request Selection                                                  |
| 2.1 | OwnerUI -> ReviewRequestController           | `getRequestDetail(in requestId: Guid, out response: RequestDetailResponseDto)` |
| 2.2 | ReviewRequestController -> IRentalRequestRepository | `findById(in id: Guid, out entity: RentalRequest)`              |
| 2.3 | OwnerUI -> Owner                            | Request Detail Display                                             |
| 3   | Owner -> OwnerUI                            | Acceptance Decision                                                |
| 3.1 | OwnerUI -> ReviewRequestController           | `acceptRequest(in requestId: Guid, out response: DecisionResponseDto)` |
| 3.2 | ReviewRequestController -> IRentalRequestRepository | `findById(in id: Guid, out entity: RentalRequest)`              |
| 3.3 | ReviewRequestController -> IRoomListingRepository | `findByRequestId(in requestId: Guid, out entity: RoomListing)`   |
| 3.4 | ReviewRequestController -> ReviewRequestLogic | `validateAcceptance(in request: RentalRequest, in room: RoomListing, out result: ValidationResult)` |
| 3.5 | ReviewRequestController -> RentalRequest    | `accept(out result: StatusChangeResult)`                           |
| 3.6 | ReviewRequestController -> RoomListing      | `lock(out result: StatusChangeResult)`                             |
| 3.7 | ReviewRequestController -> IRentalRequestRepository | `update(in entity: RentalRequest, out persisted: RentalRequest)` |
| 3.8 | ReviewRequestController -> IRoomListingRepository | `update(in entity: RoomListing, out persisted: RoomListing)`     |
| 3.9 | ReviewRequestController -> IEmailGateway     | `sendAsync(in message: EmailMessage)`                              |
| 3.10| IEmailGateway -> Email Provider              | `sendAsync(in message: EmailMessage)`                              |
| 3.11| OwnerUI -> Owner                            | Decision Success Message                                           |

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
| ----------------- | -------------- | ----- |
| `1.1` OwnerUI -> ReviewRequestCoordinator: "Room Requests Query" | `1.1` OwnerUI -> ReviewRequestController: `getRoomRequests(in roomId: Guid, out response: RequestListResponseDto)` | sync, renamed |
| `1.2` ReviewRequestCoordinator -> RentalRequest: "Room Requests Data Request" | `1.2` ReviewRequestController -> IRentalRequestRepository: `findByRoomId(in id: Guid, out list: RequestList)` | sync |
| `2.1` OwnerUI -> ReviewRequestCoordinator: "Request Detail Query" | `2.1` OwnerUI -> ReviewRequestController: `getRequestDetail(in requestId: Guid, out response: RequestDetailResponseDto)` | sync |
| `2.2` ReviewRequestCoordinator -> RentalRequest: "Request Detail Request" | `2.2` ReviewRequestController -> IRentalRequestRepository: `findById(in id: Guid, out entity: RentalRequest)` | stateless reload |
| `3.1` OwnerUI -> ReviewRequestCoordinator: "Acceptance Request" | `3.1` OwnerUI -> ReviewRequestController: `acceptRequest(in requestId: Guid, out response: DecisionResponseDto)` | sync, renamed |
| `3.2` ReviewRequestCoordinator -> ReviewRequestRules: "Decision Validation Check" | `3.4` ReviewRequestController -> ReviewRequestLogic: `validateAcceptance(in request, in room, out result)` | delegated after fetching both entities |
| `3.4` ReviewRequestCoordinator -> RentalRequest: "Accepted Status Update" | `3.5` ReviewRequestController -> RentalRequest: `accept(out result: StatusChangeResult)` | RAM mutation |
| `3.5` ReviewRequestCoordinator -> RoomListing: "Locked Status Update" | `3.6` ReviewRequestController -> RoomListing: `lock(out result: StatusChangeResult)` | RAM mutation |
| `3.6` ReviewRequestCoordinator -> EmailProxy: "Tenant Notification Request" | `3.9` ReviewRequestController -> IEmailGateway: `sendAsync(in message: EmailMessage)` | async fire-and-forget |

## Alternative Flow Notes

- **Step 3.4: Validation fails** - `ValidationResult.isValid = false`, response contains validation error, messages 3.5-3.10 skipped, use case ends
- **Step 3.2: Request not found** - Repository returns null/error, response contains not found error, use case ends
- **Step 3.3: Room not found** - Repository returns null/error, response contains not found error, use case ends
- **Step 3.5/3.6: Database error on update** - Repository throws exception, response contains error, use case ends
- **Alternative: Reject decision** - Similar flow but uses `rejectRequest(in requestId)` endpoint, calls `reject(out result)` on RentalRequest, skips RoomListing fetch and update
- **Alternative: Keep Pending** - Returns to sequence 1 without state changes
- **Step 3.10: Email Provider unavailable** - Gateway records failure, decision succeeds, continues to step 3.11

## Notes

- `OwnerUI` is shown explicitly so the human actor does not interact directly with the backend controller.
- `IRentalRequestRepository` and `IRoomListingRepository` handle persistence and return the updated entities.
- `ReviewRequestController` acts as the simplified orchestration point.
- `ReviewRequestLogic` encapsulates decision validation: checks if request can be accepted, validates room lock eligibility, ensures no conflicting accepted requests.
- `IEmailGateway` handles asynchronous email dispatch. No `out` parameter because notifications are fire-and-forget.
- **Dual Entity Modification (Messages 3.2 - 3.8)**: Accepting a request modifies two distinct entities:
  - `RentalRequest` status changes to `Accepted` via `accept()` method
  - `RoomListing` status changes to `Locked` via `lock()` method
  - Both mutations occur in RAM (messages 3.5, 3.6) before persistence (messages 3.7, 3.8)
- **Stateless Coordinator Compliance**: The controller executes fresh `findById()` and `findByRequestId()` calls at the beginning of sequence 3. Web controllers must remain stateless and cannot preserve entities between HTTP requests.
- **Separation of State Mutation and Persistence (Messages 3.5, 3.6, 3.7, 3.8)**: Based on the Information Hiding principle, the controller invokes `accept()` on `RentalRequest` and `lock()` on `RoomListing` so that objects mutate their own data safely in RAM. Immediately following, it calls `update()` on each repository to guarantee RAM mutations are persisted to disk.
- **Asynchronous External Proxy (Message 3.9)**: The `IEmailGateway` uses `sendAsync(in message)` with no `out` parameter. The controller fires the notification to a background queue and immediately returns success to the user, preventing UI freeze if the Email Provider is slow or unavailable.
- **Decision Parameter**: The action (accept/reject/keep pending) is implied by the endpoint name (`acceptRequest`, `rejectRequest`). Alternative sequences would show similar patterns for `rejectRequest()` (no room modification) and `keepPendingRequest()` (no state changes).
- **Implicit DTO mapping**: The controller implicitly maps response data from entities to DTOs. This mapping is not shown as a separate message.
- **Alternative decision flows**: Reject decision follows similar pattern but skips `RoomListing` fetch and update (room remains requestable). Keep pending returns to sequence 1 without persisting changes.
- Actor-to-UI messages (1, 1.3, 2, 2.3, 3, 3.11) use noun phrases because they represent physical user interactions, not code method calls.
