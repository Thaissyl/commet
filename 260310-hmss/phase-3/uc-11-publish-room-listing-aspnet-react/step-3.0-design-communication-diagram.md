# Design Communication Diagram: UC-11 Publish Room Listing - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: OwnerUI -> PublishListingController, then Controller -> Repository, Controller -> PublishListingLogic
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label
- Separate reply arrows intentionally omitted — `out` parameters represent returned data
- Request flow style: synchronous request handling with two-phase operation

## Object Layout

```text
Owner --- OwnerUI --- PublishListingController
                       |--- IRoomListingRepository
                       |--- PublishListingLogic
```

## Participants

| Position | Object                  | Stereotype             |
| -------- | ----------------------- | ---------------------- |
| 1        | Owner                   | Actor (primary)        |
| 2        | OwnerUI                 | `<<user interaction>>` |
| 3        | PublishListingController | `<<coordinator>>`      |
| 4        | IRoomListingRepository  | `<<database wrapper>>` |
| 5        | PublishListingLogic     | `<<business logic>>`   |

> `RoomListing` and `OwnerProfile` removed — return types only, no messages sent to them in this use case.

## Messages

| #   | From -> To                             | Message                                                            |
| --- | -------------------------------------- | ------------------------------------------------------------------ |
| 1   | Owner -> OwnerUI                       | Publication Access                                                |
| 1.1 | OwnerUI -> PublishListingController    | `GetPublicationForm(in listingId: Guid, out response: PublicationFormDto)` |
| 1.2 | PublishListingController -> IRoomListingRepository | `FindByIdAsync(in id: Guid, out entity: RoomListing)` |
| 1.3 | OwnerUI -> Owner                       | Publication Eligibility Check Display                             |
| 2   | Owner -> OwnerUI                       | Publication Confirmation                                          |
| 2.1 | OwnerUI -> PublishListingController    | `SubmitPublication(in listingId: Guid, out response: ListingResponseDto)` |
| 2.2 | PublishListingController -> IRoomListingRepository | `FindByIdAsync(in id: Guid, out entity: RoomListing)` |
| 2.3 | PublishListingController -> PublishListingLogic | `ValidateEligibility(in listing: RoomListing, in isVerified: bool, out result: ValidationResult)` |
| 2.4 | PublishListingController -> IRoomListingRepository | `UpdateAsync(in entity: RoomListing, out persisted: RoomListing)` |
| 2.5 | OwnerUI -> Owner                       | Publication Success Message                                       |

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
|---|---|---|
| `1.1` OwnerUI -> PublishListingCoordinator: "Publication Form Request" | `1.1` OwnerUI -> PublishListingController: `GetPublicationForm(...)` | renamed |
| `1.2` PublishListingCoordinator -> RoomListing: "Listing Query" | `1.2` PublishListingController -> IRoomListingRepository: `FindByIdAsync(...)` | direct DB query |
| `2.1` OwnerUI -> PublishListingCoordinator: "Publication Submission" | `2.1` OwnerUI -> PublishListingController: `SubmitPublication(...)` | renamed |
| `2.2-2.3` PublishListingCoordinator -> PublishListingRules: "Verification Check" | `2.3` PublishListingController -> PublishListingLogic: `ValidateEligibility(...)` | business logic |
| `2.4` PublishListingCoordinator -> RoomListing: "Publish Listing" | `2.4` PublishListingController -> IRoomListingRepository: `UpdateAsync(...)` | persist published state |

## Alternative Flow Notes

- **Step 2.3: Eligibility validation fails** — `ValidationResult.IsValid = false` (not verified or blockers), response includes errors, listing not published
- **Step 2.4: Update fails** — Repository exception handled, response contains error

## Notes

- `OwnerUI` shown explicitly — human actor does not interact directly with backend controller.
- `PublishListingController` acts as stateless orchestration point. Sequence 2 re-queries listing by ID independently.
- `PublishListingLogic` encapsulates `ValidateEligibility` — checks owner verification status and listing readiness.
- `IRoomListingRepository` queries and persists `RoomListing` entity with published state.
- **Two-phase operation**: Phase 1 checks eligibility; Phase 2 validates and publishes.
- **Implicit DTO mapping**: Controller implicitly maps entity to response DTO. Not shown as separate message.
- Actor-to-UI messages (1, 1.3, 2, 2.5) use noun phrases — physical user interactions, not code method calls.
