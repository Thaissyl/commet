# Design Communication Diagram: UC-18 Control Listing Visibility - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: OwnerUI -> RoomListingController, then Controller -> Repository and Controller -> VisibilityLogic
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label
- Separate reply arrows intentionally omitted — `out` parameters represent returned data
- Request flow style: synchronous request handling with visibility state machine

## Object Layout

```text
Owner --- OwnerUI --- RoomListingController
                       |--- VisibilityLogic
                       |--- IRoomListingRepository
```

## Participants

| Position | Object                   | Stereotype             |
| -------- | ------------------------ | ---------------------- |
| 1        | Owner                    | Actor (primary)        |
| 2        | OwnerUI                  | `<<user interaction>>` |
| 3        | RoomListingController    | `<<coordinator>>`      |
| 4        | VisibilityLogic          | `<<business logic>>`   |
| 5        | IRoomListingRepository   | `<<database wrapper>>` |

## Messages

| #   | From -> To                                  | Message                                                            |
| --- | ------------------------------------------- | ------------------------------------------------------------------ |
| 1   | Owner -> OwnerUI                            | Visibility Control Access                                          |
| 1.1 | OwnerUI -> RoomListingController            | `GetListingVisibilityDetails(in listingId: Guid, out response: VisibilityResponseDto)` |
| 1.2 | RoomListingController -> IRoomListingRepository | `FindByIdAsync(in id: Guid, out entity: RoomListing)` |
| 1.3 | OwnerUI -> Owner                            | Current Visibility Status Display                                 |
| 2   | Owner -> OwnerUI                            | Visibility Change Decision                                         |
| 2.1 | OwnerUI -> RoomListingController            | `ChangeVisibility(in listingId: Guid, in action: string, out response: StatusChangeResponseDto)` |
| 2.2 | RoomListingController -> IRoomListingRepository | `FindByIdAsync(in id: Guid, out entity: RoomListing)` |
| 2.3 | RoomListingController -> VisibilityLogic    | `ValidateVisibilityAction(in listing: RoomListing, in action: string, out result: ValidationResult)` |
| 2.4 | RoomListingController -> IRoomListingRepository | `UpdateAsync(in entity: RoomListing, out persisted: RoomListing)` |
| 2.5 | OwnerUI -> Owner                            | Visibility Change Confirmation Message                            |

## Alternative Flow Notes

- **Step 2.3: Validation fails** — `ValidationResult.IsValid = false` (e.g., cannot hide already hidden), response includes reason
- **Step 2.4: Update fails** — Repository exception handled, response contains error

## Notes

- `OwnerUI` shown explicitly — human actor does not interact directly with backend controller.
- `RoomListingController` acts as stateless orchestration point.
- `VisibilityLogic` encapsulates `ValidateVisibilityAction` state machine validation.
- `IRoomListingRepository` queries and persists `RoomListing` entity with visibility status.
- Visibility state machine: PublishedAvailable ↔ Hidden, Draft states.
- Actor-to-UI messages use noun phrases — physical interactions, not code method calls.
