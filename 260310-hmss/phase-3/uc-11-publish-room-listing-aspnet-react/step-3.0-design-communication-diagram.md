# Design Communication Diagram: UC-11 Publish Room Listing - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: `OwnerUI -> PublishListingController`, then `Controller -> Repository`, `Controller -> PublishListingLogic`
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label when a response payload is expected
- Separate reply arrows are intentionally omitted because `out` parameters already represent returned data
- Request flow style: synchronous request handling with two-phase operation

## Object Layout

```text
Owner --- OwnerUI --- PublishListingController
                       |--- IRoomListingRepository --- RoomListing
                       |--- IOwnerRepository --- OwnerProfile
                       |--- PublishListingLogic
```

## Participants

| Position | Object                  | Stereotype             |
| -------- | ----------------------- | ---------------------- |
| 1        | Owner                   | Actor (primary)        |
| 2        | OwnerUI                 | `<<user interaction>>` |
| 3        | PublishListingController | `<<coordinator>>`      |
| 4        | IRoomListingRepository  | `<<database wrapper>>` |
| 5        | RoomListing             | `<<data abstraction>>` |
| 6        | IOwnerRepository        | `<<database wrapper>>` |
| 7        | OwnerProfile            | `<<data abstraction>>` |
| 8        | PublishListingLogic     | `<<business logic>>`   |

## Messages

| #   | From -> To                             | Message                                                            |
| --- | -------------------------------------- | ------------------------------------------------------------------ |
| 1   | Owner -> OwnerUI                       | Publication Access                                                |
| 1.1 | OwnerUI -> PublishListingController    | `getPublicationForm(in listingId: Guid, out response: PublicationFormDto)` |
| 1.2 | PublishListingController -> IRoomListingRepository | `findById(in id: Guid, out entity: RoomListing)`                 |
| 1.3 | OwnerUI -> Owner                       | Listing and Checklist Display                                      |
| 2   | Owner -> OwnerUI                       | Publication Request                                               |
| 2.1 | OwnerUI -> PublishListingController    | `checkPublicationEligibility(in listingId: Guid, in ownerId: Guid, out response: EligibilityResponseDto)` |
| 2.2 | PublishListingController -> IRoomListingRepository | `findById(in id: Guid, out entity: RoomListing)`                 |
| 2.3 | PublishListingController -> IOwnerRepository | `findById(in id: Guid, out entity: OwnerProfile)`                 |
| 2.4 | PublishListingController -> PublishListingLogic | `validateEligibility(in listing: RoomListing, in owner: OwnerProfile, out result: ValidationResult)` |
| 2.5 | OwnerUI -> Owner                       | Publication Confirmation Prompt Display                            |
| 3   | Owner -> OwnerUI                       | Publication Confirmation                                          |
| 3.1 | OwnerUI -> PublishListingController    | `submitPublication(in listingId: Guid, out response: PublicationResponseDto)` |
| 3.2 | PublishListingController -> IRoomListingRepository | `findById(in id: Guid, out entity: RoomListing)`                 |
| 3.3 | PublishListingController -> RoomListing | `publish(out result: StatusChangeResult)`                          |
| 3.4 | PublishListingController -> IRoomListingRepository | `update(in entity: RoomListing, out persisted: RoomListing)`     |
| 3.5 | OwnerUI -> Owner                       | Publication Success Message                                       |

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
| ----------------- | -------------- | ----- |
| `1.1` OwnerUI -> PublishListingCoordinator: "Listing Detail Request" | `1.1` OwnerUI -> PublishListingController: `getPublicationForm(in listingId: Guid, out response: PublicationFormDto)` | sync, renamed to code-style |
| `1.2` PublishListingCoordinator -> RoomListing: "Listing Detail Query" | `1.2` PublishListingController -> IRoomListingRepository: `findById(in id: Guid, out entity: RoomListing)` | stateless controller fetch |
| `2.1` OwnerUI -> PublishListingCoordinator: "Publication Evaluation Request" | `2.1` OwnerUI -> PublishListingController: `checkPublicationEligibility(in listingId: Guid, in ownerId: Guid, out response: EligibilityResponseDto)` | sync, two-phase: pre-check |
| `2.2` PublishListingCoordinator -> PublicationRules: "Eligibility Check (Listing & Owner Data)" | `2.2` PublishListingController -> IRoomListingRepository: `findById(in id: Guid, out entity: RoomListing)` then `2.3` findById for OwnerProfile then `2.4` validateEligibility(...) | load both entities for validation |
| `3.1` OwnerUI -> PublishListingCoordinator: "Confirmed Publication" | `3.1` OwnerUI -> PublishListingController: `submitPublication(in listingId: Guid, out response: PublicationResponseDto)` | sync, two-phase: execution |
| `3.2` PublishListingCoordinator -> RoomListing: "Published Status Update" | `3.2` PublishListingController -> IRoomListingRepository: `findById(in id: Guid, out entity: RoomListing)` then `3.3` publish(...) then `3.4` update(...) | load, mutate, persist pattern |

## Alternative Flow Notes

- **Step 2.4: Validation fails** - `ValidationResult.isValid = false`, response contains ineligibility reason (unverified owner, incomplete listing, no images), messages 3.1-3.4 are skipped, use case returns to step 2
- **Step 2.2: Listing not found** - Repository returns null/error, response contains not found error, use case ends
- **Step 2.3: OwnerProfile not found** - Repository returns null/error, response contains error, use case ends
- **Step 3.2: Listing not found** - Repository returns null/error, response contains not found error, use case ends
- **Step 3.4: Database error on update** - Repository throws exception, response contains error, use case ends

## Notes

- `OwnerUI` is shown explicitly so the human actor does not interact directly with the backend controller.
- `IRoomListingRepository` and `IOwnerRepository` handle persistence and return domain entities.
- `PublishListingController` acts as the simplified orchestration point for this use case.
- `PublishListingLogic` encapsulates the publishing eligibility business rules: owner verification status check, listing completeness validation (required fields), and image availability check (at least one image).
- **Two-Phase Operation Pattern**: This use case demonstrates the validation-then-execution pattern:
  - **Phase 1 (Pre-check)**: Sequence 2 `checkPublicationEligibility` validates eligibility without modifying state.
  - **Phase 2 (Execution)**: Sequence 3 `submitPublication` performs the actual status change.
- **Explicit ownerId Parameter (Message 2.1)**: The `checkPublicationEligibility` method receives both `listingId` and `ownerId` as explicit parameters. This makes the data flow traceable and allows the controller to load the `OwnerProfile` entity for verification status checking.
- **Stateless Coordinator (Sequence 2)**: The controller loads both `RoomListing` (via 2.2) and `OwnerProfile` (via 2.3) entities via `findById()` before passing them to business logic for eligibility validation. The `RoomListing` entity holds `ownerId` as a foreign key, but the actual verification status resides in `OwnerProfile`.
- **Stateless Coordinator (Sequence 3)**: The controller reloads the `RoomListing` entity at message 3.2 before applying the status change, ensuring data accuracy at time of publication.
- **Separation of State Mutation and Persistence (Messages 3.3 & 3.4)**:
  - Message 3.3: `publish(out result: StatusChangeResult)` on `RoomListing` (`<<data abstraction>>`) mutates the status from Draft to Published Available in RAM. The domain object knows its own transition logic — no `in` parameter needed for the new state.
  - Message 3.4: `update(in entity: RoomListing, out persisted: RoomListing)` on `IRoomListingRepository` (`<<database wrapper>>`) executes the SQL UPDATE statement to persist the mutated state, satisfying the ACID Durability requirement.
- **Domain Self-Containment**: The `publish(out result)` method on `RoomListing` takes no `in` parameter for the new status. The domain object owns its state transition logic and knows that Draft → Published Available is the valid path.
- **Critical Business Rules**: Owner verification, listing completeness, and image availability are evaluated as business rules during the use case (Step 4), NOT as Preconditions. Preconditions are only: (1) Owner is signed in, (2) Listing exists in Draft/unpublished state.
- **Implicit DTO mapping**: The controller implicitly maps response data from entities to DTOs. This mapping is not shown as a separate message.
- Actor-to-UI messages (1, 1.3, 2, 2.5, 3, 3.5) use noun phrases because they represent physical user interactions, not code method calls.
