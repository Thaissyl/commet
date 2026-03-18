# Design Communication Diagram: UC-18 Control Listing Visibility - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: `AdminUI -> ControlListingController`, then `Controller -> Repository`, `Controller -> ListingControlLogic`, `Controller -> NotificationService`, and `Controller -> IEmailGateway`
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label when a response payload is expected
- Separate reply arrows are intentionally omitted because `out` parameters already represent returned data
- Request flow style: synchronous request handling with two-phase operation pattern

## Object Layout

```text
System Admin --- AdminUI --- ControlListingController
                              |--- ListingControlLogic
                              |--- IRoomListingRepository --- RoomListing
                              |--- NotificationService
                              |--- IEmailGateway --- Email Provider
```

## Participants

| Position | Object                   | Stereotype               |
| -------- | ------------------------ | ------------------------ |
| 1        | System Admin             | Actor (primary)          |
| 2        | AdminUI                  | `<<user interaction>>`   |
| 3        | ControlListingController | `<<coordinator>>`        |
| 4        | IRoomListingRepository   | `<<database wrapper>>`   |
| 5        | RoomListing              | `<<data abstraction>>`   |
| 6        | ListingControlLogic      | `<<business logic>>`     |
| 7        | NotificationService      | `<<application logic>>`  |
| 8        | IEmailGateway            | `<<proxy>>`              |
| 9        | Email Provider           | Actor (secondary)        |

## Messages

| #   | From -> To                                  | Message                                                            |
| --- | ------------------------------------------- | ------------------------------------------------------------------ |
| 1   | System Admin -> AdminUI                     | Listing Administration Access                                      |
| 1.1 | AdminUI -> ControlListingController         | `getVisibleListings(out response: ListingListDto)`                 |
| 1.2 | ControlListingController -> IRoomListingRepository | `findByStatus(in status: String, out list: ListingList)`        |
| 1.3 | AdminUI -> System Admin                     | Visible Listings Display                                           |
| 2   | System Admin -> AdminUI                     | Listing Selection                                                  |
| 2.1 | AdminUI -> ControlListingController         | `getListingDetails(in listingId: Guid, out response: ListingDetailDto)` |
| 2.2 | ControlListingController -> IRoomListingRepository | `findById(in id: Guid, out entity: RoomListing)`                |
| 2.3 | AdminUI -> System Admin                     | Details and Disable Action Display                                 |
| 3   | System Admin -> AdminUI                     | Disable Action Decision                                            |
| 3.1 | AdminUI -> ControlListingController         | `disableListing(in listingId: Guid, out response: ControlActionDto)` |
| 3.2 | ControlListingController -> IRoomListingRepository | `findById(in id: Guid, out entity: RoomListing)`                |
| 3.3 | ControlListingController -> ListingControlLogic | `validateDisableAction(in listing: RoomListing, out result: ValidationResult)` |
| 3.4 | ControlListingController -> RoomListing      | `disableByAdmin(out result: StatusChangeResult)`                   |
| 3.5 | ControlListingController -> IRoomListingRepository | `update(in entity: RoomListing, out persisted: RoomListing)`     |
| 3.6 | ControlListingController -> NotificationService | `createDisableNotification(in listing: RoomListing, out message: EmailMessage)` |
| 3.7 | ControlListingController -> IEmailGateway   | `sendAsync(in message: EmailMessage)`                              |
| 3.8 | IEmailGateway -> Email Provider              | `sendAsync(in message: EmailMessage)`                              |
| 3.9 | AdminUI -> System Admin                     | Action Success Message                                             |

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
| ----------------- | -------------- | ----- |
| `1.1` AdminUI -> ControlListingCoordinator: "Visible Listings Query" | `1.1` AdminUI -> ControlListingController: `getVisibleListings(out response: ListingListDto)` | sync, renamed |
| `1.2` ControlListingCoordinator -> RoomListing: "Visible Listings Request" | `1.2` ControlListingController -> IRoomListingRepository: `findByStatus(in status: String, out list: ListingList)` | sync with status filter |
| `2.1` AdminUI -> ControlListingCoordinator: "Listing Detail Query" | `2.1` AdminUI -> ControlListingController: `getListingDetails(in listingId: Guid, out response: ListingDetailDto)` | sync |
| `2.2` ControlListingCoordinator -> RoomListing: "Listing Detail Request" | `2.2` ControlListingController -> IRoomListingRepository: `findById(in id: Guid, out entity: RoomListing)` | stateless reload |
| `3.1` AdminUI -> ControlListingCoordinator: "Disable Action Request" | `3.1` AdminUI -> ControlListingController: `disableListing(in listingId: Guid, out response: ControlActionDto)` | sync, renamed |
| `3.2` ControlListingCoordinator -> ListingControlRules: "Status Concurrency Check" | `3.3` ControlListingController -> ListingControlLogic: `validateDisableAction(in listing, out result)` | delegated after fetching entity |
| `3.6` ControlListingCoordinator -> RoomListing: "Disabled Status Update" | `3.4` ControlListingController -> RoomListing: `disableByAdmin(out result: StatusChangeResult)` | RAM mutation |
| `3.7-3.10` ControlListingCoordinator -> NotificationService -> EmailProxy: "Owner Notification Request/Payload/Dispatch" | `3.6` ControlListingController -> NotificationService: `createDisableNotification(in listing, out message)` then `3.7` sendAsync(...) | service composes email, async dispatch |

## Alternative Flow Notes

- **Step 3.3: Validation fails** - `ValidationResult.isValid = false`, response contains not publicly visible reason, messages 3.4-3.8 skipped, use case ends
- **Step 3.2: Listing not found** - Repository returns null/error, response contains not found error, use case ends
- **Step 3.5: Database error on update** - Repository throws exception, response contains error, use case ends
- **Step 3.8: Email Provider unavailable** - Gateway records failure, disable action succeeds, continues to step 3.9

## Notes

- `AdminUI` is shown explicitly so the human actor does not interact directly with the backend controller.
- `IRoomListingRepository` handles persistence and returns the updated entity.
- `ControlListingController` acts as the simplified orchestration point.
- `ListingControlLogic` encapsulates admin control validation: validates listing is still publicly visible before disable, ensures status concurrency, prevents double-disable on already disabled listings.
- `NotificationService` (`<<application logic>>`) decouples email formatting from network dispatch: composes subject line, message body, and recipient email before passing payload to gateway.
- `IEmailGateway` handles asynchronous email dispatch. No `out` parameter because notifications are fire-and-forget.
- **Two-Phase Operation Pattern**: This use case demonstrates the validation-then-execution pattern:
  - **Phase 1 (Pre-check)**: Sequence 2 `getListingDetails` retrieves listing for review.
  - **Phase 2 (Execution)**: Sequence 3 `disableListing` performs validation and executes the disable action.
- **Stateless Coordinator Compliance (Messages 1.2, 2.2, 3.2)**: The controller executes fresh repository queries at the beginning of each sequence. Web controllers must remain stateless and cannot preserve the `RoomListing` object in memory between user clicks. This explicitly solves the concurrency flaw where owners may hide or delete listings during admin review.
- **Separation of State Mutation and Persistence (Messages 3.4, 3.5)**: Based on the Information Hiding principle, the controller invokes `disableByAdmin()` on the `RoomListing` (`<<data abstraction>>`) object so that the object mutates its own data safely in RAM. Immediately following, it calls `update()` on the `IRoomListingRepository` (`<<database wrapper>>`) to guarantee that the RAM mutation is securely persisted to the disk.
- **Asynchronous External Proxy (Message 3.7)**: The `IEmailGateway` uses `sendAsync(in message)` with no `out` parameter. The controller fires the notification to a background queue and immediately returns success to the user (Message 3.9), preventing UI freeze if the Email Provider is slow or unavailable.
- **Admin Override**: Unlike UC-12 (Change Listing Visibility) where owners can only transition between certain states, the admin disable action forcibly removes listings from public visibility regardless of the listing's current state (Published Available, Locked, etc.).
- **Repository Query Patterns**:
  - `findByStatus(in status: String, out list)` - Fetches listings by status filter (sequence 1, status = "Visible")
  - `findById(in id: Guid, out entity)` - Fetches single listing by ID (sequences 2, 3)
- **Application Logic Notification Builder (Message 3.6)**: Aligning with architectural optimizations from UC-17, `NotificationService` (`<<application logic>>`) explicitly formats the email payload (subject lines, text templates) before passing to the proxy that actually dispatches it over the network.
- **Implicit DTO mapping**: The controller implicitly maps response data from entities to DTOs. This mapping is not shown as a separate message.
- Actor-to-UI messages (1, 1.3, 2, 2.3, 3, 3.9) use noun phrases because they represent physical user interactions, not code method calls.
