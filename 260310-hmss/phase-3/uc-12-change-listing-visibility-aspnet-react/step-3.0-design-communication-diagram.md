# Design Communication Diagram: UC-12 Change Listing Visibility - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: OwnerUI -> RoomListingController, then Controller -> Repository, Controller -> VisibilityLogic
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label
- Separate reply arrows intentionally omitted — `out` parameters represent returned data
- Request flow style: synchronous request handling with two-phase operation

## Object Layout

```text
Owner --- OwnerUI --- RoomListingController
                       |--- IRoomListingRepository
                       |--- VisibilityLogic
```

## Participants

| Position | Object                 | Stereotype             |
| -------- | ---------------------- | ---------------------- |
| 1        | Owner                  | Actor (primary)        |
| 2        | OwnerUI                | `<<user interaction>>` |
| 3        | RoomListingController  | `<<coordinator>>`      |
| 4        | IRoomListingRepository | `<<database wrapper>>` |
| 5        | VisibilityLogic        | `<<business logic>>`   |

> `RoomListing` removed — return type only, no messages sent to it in this use case.

## Messages

| #   | From -> To                             | Message                                                            |
| --- | -------------------------------------- | ------------------------------------------------------------------ |
| 1   | Owner -> OwnerUI                       | Visibility Management Access                                       |
| 1.1 | OwnerUI -> RoomListingController       | `GetListingVisibilityDetails(in listingId: Guid, out response: VisibilityResponseDto)` |
| 1.2 | RoomListingController -> IRoomListingRepository | `FindByIdAsync(in id: Guid, out entity: RoomListing)` |
| 1.3 | OwnerUI -> Owner                       | Visibility Status Display with Available Actions                  |
| 2   | Owner -> OwnerUI                       | Visibility Action Confirmation                                    |
| 2.1 | OwnerUI -> RoomListingController       | `SubmitVisibilityChange(in listingId: Guid, in action: VisibilityActionRequest, out response: ListingResponseDto)` |
| 2.2 | RoomListingController -> IRoomListingRepository | `FindByIdAsync(in id: Guid, out entity: RoomListing)` |
| 2.3 | RoomListingController -> VisibilityLogic | `ValidateVisibilityAction(in listing: RoomListing, in action: string, out result: ValidationResult)` |
| 2.4 | RoomListingController -> IRoomListingRepository | `UpdateAsync(in entity: RoomListing, out persisted: RoomListing)` |
| 2.5 | OwnerUI -> Owner                       | Visibility Change Success Message                                 |

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
|---|---|---|
| `1.1` OwnerUI -> VisibilityCoordinator: "Listing Visibility Request" | `1.1` OwnerUI -> RoomListingController: `GetListingVisibilityDetails(...)` | renamed |
| `1.2` VisibilityCoordinator -> RoomListing: "Listing Detail Query" | `1.2` RoomListingController -> IRoomListingRepository: `FindByIdAsync(...)` | direct DB query |
| `2.1` OwnerUI -> VisibilityCoordinator: "Visibility Action Submission" | `2.1` OwnerUI -> RoomListingController: `SubmitVisibilityChange(...)` | renamed |
| `2.2-2.3` VisibilityCoordinator -> VisibilityRules: "Action Validation" | `2.3` RoomListingController -> VisibilityLogic: `ValidateVisibilityAction(...)` | business logic |
| `2.4` VisibilityCoordinator -> RoomListing: "Apply Visibility Change" | `2.4` RoomListingController -> IRoomListingRepository: `UpdateAsync(...)` | persist state |

## Alternative Flow Notes

- **Step 2.3: Validation fails** — `ValidationResult.IsValid = false` (e.g., cannot hide already hidden), response includes reason, entity not updated
- **Step 2.4: Update fails** — Repository exception handled, response contains error

## Notes

- `OwnerUI` shown explicitly — human actor does not interact directly with backend controller.
- `RoomListingController` acts as stateless orchestration point. Sequence 2 re-queries listing by ID independently.
- `VisibilityLogic` encapsulates `ValidateVisibilityAction` — checks if action is valid for current status (e.g., cannot hide already hidden).
- `IRoomListingRepository` queries and persists `RoomListing` entity with visibility state.
- **Two-phase operation**: Phase 1 shows current state and available actions; Phase 2 validates and applies change.
- **Implicit DTO mapping**: Controller implicitly maps entity to response DTO. Not shown as separate message.
- Actor-to-UI messages (1, 1.3, 2, 2.5) use noun phrases — physical user interactions, not code method calls.
