# Design Communication Diagram: UC-15 Reopen Room Listing - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: OwnerUI -> RoomListingController, then Controller -> Repository, Controller -> ReopenLogic, and Controller -> IEmailGateway
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label
- Separate reply arrows intentionally omitted; `out` parameters represent returned data
- Request flow style: synchronous request handling with two-phase operation and dual entity modification pattern

## Object Layout

```text
Owner --- OwnerUI --- RoomListingController
                       |--- ReopenLogic
                       |--- IRentalRequestRepository
                       |--- IRoomListingRepository
                       |--- IEmailGateway --- Email Provider
```

## Participants

| Position | Object                   | Stereotype             |
| -------- | ------------------------ | ---------------------- |
| 1        | Owner                    | Actor (primary)        |
| 2        | OwnerUI                  | `<<user interaction>>` |
| 3        | RoomListingController    | `<<coordinator>>`      |
| 4        | ReopenLogic              | `<<business logic>>`   |
| 5        | IRentalRequestRepository | `<<database wrapper>>` |
| 6        | IRoomListingRepository   | `<<database wrapper>>` |
| 7        | IEmailGateway            | `<<proxy>>`            |
| 8        | Email Provider           | Actor (secondary)      |

> `RentalRequest` and `RoomListing` removed; return types only, no messages sent to them in this use case.

## Messages

| #   | From -> To                                  | Message                                                            |
| --- | ------------------------------------------- | ------------------------------------------------------------------ |
| 1   | Owner -> OwnerUI                            | Accepted Arrangements Access                                       |
| 1.1 | OwnerUI -> RoomListingController            | `GetReopenOptions(in requestId: Guid, out response: ReopenOptionsResponseDto)` |
| 1.2 | RoomListingController -> IRentalRequestRepository | `FindByIdAsync(in id: Guid, out request: RentalRequest)` |
| 1.3 | OwnerUI -> Owner                            | Reopen Confirmation Prompt                                         |
| 2   | Owner -> OwnerUI                            | Reopen Confirmation                                                |
| 2.1 | OwnerUI -> RoomListingController            | `SubmitReopen(in requestId: Guid, out response: StatusChangeResponseDto)` |
| 2.2 | RoomListingController -> IRentalRequestRepository | `FindByIdAsync(in id: Guid, out request: RentalRequest)` |
| 2.3 | RoomListingController -> ReopenLogic        | `ValidateConcurrencyStatus(in request: RentalRequest, out result: ValidationResult)` |
| 2.4 | RoomListingController -> IRentalRequestRepository | `UpdateAsync(in entity: RentalRequest, out persisted: RentalRequest)` |
| 2.5 | RoomListingController -> IRoomListingRepository | `FindByIdAsync(in id: Guid, out listing: RoomListing)` |
| 2.6 | RoomListingController -> IRoomListingRepository | `UpdateAsync(in entity: RoomListing, out persisted: RoomListing)` |
| 2.7 | RoomListingController -> IEmailGateway      | `SendAsync(in message: EmailMessage)` |
| 2.8 | IEmailGateway -> Email Provider             | `SendAsync(in message: EmailMessage)` |
| 2.9 | OwnerUI -> Owner                            | Reopen Success Message                                             |

## Analysis -> Design Message Mapping

| Analysis message | Design message | Notes |
|---|---|---|
| `1.1` OwnerUI -> ReopenRoomCoordinator: "Accepted Arrangements Query" | `1.1` OwnerUI -> RoomListingController: `GetReopenOptions(...)` | renamed |
| `1.2` ReopenRoomCoordinator -> RentalRequest: "Accepted Arrangements Request" | `1.2` RoomListingController -> IRentalRequestRepository: `FindByIdAsync(...)` | repository query |
| `2.1` OwnerUI -> ReopenRoomCoordinator: "Confirmed Reopen Request" | `2.1` OwnerUI -> RoomListingController: `SubmitReopen(...)` | renamed |
| `2.2-2.5` ReopenRoomCoordinator -> ReopenRules: "Status Concurrency Check" | `2.3` RoomListingController -> ReopenLogic: `ValidateConcurrencyStatus(...)` | business logic |
| `3.2-3.5` ReopenRoomCoordinator -> RentalRequest, RoomListing, EmailProxy | `2.4-2.8` RoomListingController updates both entities and sends email | dual update + notification |

## Alternative Flow Notes

- **Step 2.3: Validation fails** - `ValidationResult.IsValid = false` (for example, request already changed), entities are not updated
- **Step 2.4 or 2.6: Update fails** - Repository exception handled, response contains error
- **Step 2.7-2.8: Email fails** - Exception caught, reopen still succeeds, notification failure is logged

## Notes

- `OwnerUI` shown explicitly; human actor does not interact directly with backend controller.
- `RoomListingController` acts as stateless orchestration point. Sequence 2 re-queries by ID independently.
- `ReopenLogic` encapsulates `ValidateConcurrencyStatus`; checks if request can still be reopened after concurrent changes.
- `IRentalRequestRepository` updates `RentalRequest` entity to revoked-by-owner status.
- `IRoomListingRepository` updates `RoomListing` entity to reopen it and make it available again.
- `IEmailGateway` sends notification to tenant about the reopened listing arrangement.
- **Dual entity modification**: Both `RentalRequest` and `RoomListing` are updated.
- **Implicit DTO mapping**: Controller implicitly maps entities to response DTOs. Not shown as separate message.
- Actor-to-UI messages (1, 1.3, 2, 2.9) use noun phrases; physical user interactions, not code method calls.
