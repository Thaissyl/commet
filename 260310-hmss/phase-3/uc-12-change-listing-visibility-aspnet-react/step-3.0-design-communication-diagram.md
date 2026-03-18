# Design Communication Diagram: UC-12 Change Listing Visibility - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: `OwnerUI -> ChangeVisibilityController`, then `Controller -> Repository`, `Controller -> VisibilityLogic`
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label when a response payload is expected
- Separate reply arrows are intentionally omitted because `out` parameters already represent returned data
- Request flow style: synchronous request handling with two-phase operation

## Object Layout

```text
Owner --- OwnerUI --- ChangeVisibilityController
                       |--- IRoomListingRepository --- RoomListing
                       |--- VisibilityLogic
```

## Participants

| Position | Object                 | Stereotype             |
| -------- | ---------------------- | ---------------------- |
| 1        | Owner                  | Actor (primary)        |
| 2        | OwnerUI                | `<<user interaction>>` |
| 3        | ChangeVisibilityController | `<<coordinator>>`      |
| 4        | IRoomListingRepository | `<<database wrapper>>` |
| 5        | RoomListing            | `<<data abstraction>>` |
| 6        | VisibilityLogic        | `<<business logic>>`   |

## Messages

| #   | From -> To                             | Message                                                            |
| --- | -------------------------------------- | ------------------------------------------------------------------ |
| 1   | Owner -> OwnerUI                       | Listing Selection                                                 |
| 1.1 | OwnerUI -> ChangeVisibilityController  | `getListingVisibilityDetails(in listingId: Guid, out response: VisibilityDetailsDto)` |
| 1.2 | ChangeVisibilityController -> IRoomListingRepository | `findById(in id: Guid, out entity: RoomListing)`                 |
| 1.3 | OwnerUI -> Owner                       | Listing Details and Actions Display                                |
| 2   | Owner -> OwnerUI                       | Visibility Action Selection                                       |
| 2.1 | OwnerUI -> ChangeVisibilityController  | `checkActionValidity(in listingId: Guid, in action: String, out response: ValidityResponseDto)` |
| 2.2 | ChangeVisibilityController -> IRoomListingRepository | `findById(in id: Guid, out entity: RoomListing)`                 |
| 2.3 | ChangeVisibilityController -> VisibilityLogic | `validateVisibilityAction(in listing: RoomListing, in action: String, out result: ValidationResult)` |
| 2.4 | OwnerUI -> Owner                       | Visibility Confirmation Prompt Display                             |
| 3   | Owner -> OwnerUI                       | Visibility Change Confirmation                                     |
| 3.1 | OwnerUI -> ChangeVisibilityController  | `submitVisibilityChange(in listingId: Guid, in action: String, out response: StatusChangeResponseDto)` |
| 3.2 | ChangeVisibilityController -> IRoomListingRepository | `findById(in id: Guid, out entity: RoomListing)`                 |
| 3.3 | ChangeVisibilityController -> RoomListing | `changeVisibility(in action: String, out result: StatusChangeResult)` |
| 3.4 | ChangeVisibilityController -> IRoomListingRepository | `update(in entity: RoomListing, out persisted: RoomListing)`     |
| 3.5 | OwnerUI -> Owner                       | Visibility Change Success Message                                 |

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
| ----------------- | -------------- | ----- |
| `1.1` OwnerUI -> ChangeVisibilityCoordinator: "Listing Detail Request" | `1.1` OwnerUI -> ChangeVisibilityController: `getListingVisibilityDetails(in listingId: Guid, out response: VisibilityDetailsDto)` | sync, renamed to code-style |
| `1.2` ChangeVisibilityCoordinator -> RoomListing: "Listing Detail Query" | `1.2` ChangeVisibilityController -> IRoomListingRepository: `findById(in id: Guid, out entity: RoomListing)` | stateless controller fetch |
| `2.1` OwnerUI -> ChangeVisibilityCoordinator: "Visibility Action Request" | `2.1` OwnerUI -> ChangeVisibilityController: `checkActionValidity(in listingId: Guid, in action: String, out response: ValidityResponseDto)` | sync, two-phase: pre-check |
| `2.2` ChangeVisibilityCoordinator -> VisibilityRules: "Action Validity Check" | `2.2` ChangeVisibilityController -> IRoomListingRepository: `findById(in id: Guid, out entity: RoomListing)` then `2.3` validateVisibilityAction(...) | load entity for validation |
| `3.1` OwnerUI -> ChangeVisibilityCoordinator: "Confirmed Visibility Change" | `3.1` OwnerUI -> ChangeVisibilityController: `submitVisibilityChange(in listingId: Guid, in action: String, out response: StatusChangeResponseDto)` | sync, two-phase: execution |
| `3.2` ChangeVisibilityCoordinator -> RoomListing: "Visibility Status Update" | `3.2` ChangeVisibilityController -> IRoomListingRepository: `findById(in id: Guid, out entity: RoomListing)` then `3.3` changeVisibility(...) then `3.4` update(...) | load, mutate, persist pattern |

## Alternative Flow Notes

- **Step 2.3: Validation fails** - `ValidationResult.isValid = false`, response contains invalid action reason, messages 3.1-3.4 are skipped, use case ends unsuccessfully
- **Step 2.2: Listing not found** - Repository returns null/error, response contains not found error, use case ends
- **Step 3.2: Listing not found** - Repository returns null/error, response contains not found error, use case ends
- **Step 3.4: Database error on update** - Repository throws exception, response contains error, use case ends

## Notes

- `OwnerUI` is shown explicitly so the human actor does not interact directly with the backend controller.
- `IRoomListingRepository` handles persistence and returns the updated `RoomListing` entity.
- `ChangeVisibilityController` acts as the simplified orchestration point for this use case.
- `VisibilityLogic` encapsulates the visibility state transition validation business rules: validates which status transitions are permitted (e.g., Published → Hidden ✓, Hidden → Archive ✓, Archived → Published ✗).
- **Two-Phase Operation Pattern**: This use case demonstrates the validation-then-execution pattern:
  - **Phase 1 (Pre-check)**: Sequence 2 `checkActionValidity` validates the requested action without modifying state.
  - **Phase 2 (Execution)**: Sequence 3 `submitVisibilityChange` performs the actual status change.
- **Reactive System Design**: The UI displays a "standard menu of visibility actions" rather than filtering to only valid options. Users can select any action, and the backend validates and rejects invalid actions. This approach is simpler and more maintainable than keeping UI filters synchronized with complex business rules.
- **Stateless Coordinator (Messages 1.2, 2.2, 3.2)**: The controller executes a fresh `findById()` against the database wrapper at the beginning of each sequence. Web controllers must be completely stateless and cannot preserve the `RoomListing` object in memory between user clicks.
- **Separation of State Mutation and Persistence (Messages 3.3 & 3.4)**: Based on the Information Hiding principle, the controller does not alter the status value directly. It invokes `changeVisibility()` on the `RoomListing` (`<<data abstraction>>`) object so that the object mutates its own data safely in RAM. Immediately following this, it calls `update()` on the `IRoomListingRepository` (`<<database wrapper>>`) to guarantee that the RAM mutation is securely persisted to the disk.
- **Action Parameter**: The `action: String` parameter represents the requested visibility change (e.g., "hide", "archive"). At the design level, `String` is simpler and more flexible than defining an enum type. Type enforcement can be applied at implementation level.
- **Implicit DTO mapping**: The controller implicitly maps response data from entities to DTOs. This mapping is not shown as a separate message.
- Actor-to-UI messages (1, 1.3, 2, 2.4, 3, 3.5) use noun phrases because they represent physical user interactions, not code method calls.
