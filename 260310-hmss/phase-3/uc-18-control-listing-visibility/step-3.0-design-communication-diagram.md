# Design Communication Diagram: UC-18 Control Listing Visibility

## Design Communication Decision

- Diagram level: design phase
- Message style: single directional function messages
- Each function message carries both `in` and `out` parameters in the same label
- Separate reply arrows are intentionally omitted to keep the diagram clean
- Interaction style: synchronous message passing
- MVC mapping: `AdminUI` acts as View, `AdminCoordinator` acts as Controller, and `RoomListingLogic`, `RoomListing`, `RoomListingDB`, `NotificationService`, and `EmailProxy` are model-side collaborators
- The analysis `RoomListing` entity is refined into `RoomListing <<data abstraction>>` and `RoomListingDB <<database wrapper>>` because listing data is long-lived and assumed to be stored in a physical database

## Object Layout

```text
System Admin --- AdminUI --- AdminCoordinator --- RoomListingLogic
                                  |--- RoomListing
                                  |--- RoomListingDB
                                  |--- NotificationService
                                  |--- EmailProxy --- Email Provider
```

## Participants

| Position | Object | Stereotype |
| --- | --- | --- |
| 1 | System Admin | Actor (primary) |
| 2 | AdminUI | `<<user interaction>>` |
| 3 | AdminCoordinator | `<<coordinator>>` |
| 4 | RoomListingLogic | `<<business logic>>` |
| 5 | RoomListing | `<<data abstraction>>` |
| 6 | RoomListingDB | `<<database wrapper>>` |
| 7 | NotificationService | `<<service>>` |
| 8 | EmailProxy | `<<proxy>>` |
| 9 | Email Provider | Actor (secondary) |

## Messages

| # | From -> To | Message |
| --- | --- | --- |
| 1 | System Admin -> AdminUI | `accessListingAdministration(out visibleListingList)` |
| 1.1 | AdminUI -> AdminCoordinator | `getVisibleListingList(out visibleListingList)` |
| 1.2 | AdminCoordinator -> RoomListingLogic | `getVisibleListingList(out visibleListingList)` |
| 1.3 | RoomListingLogic -> RoomListingDB | `findVisibleListingSummaries(out visibleListingList)` |
| 2 | System Admin -> AdminUI | `selectListingForReview(in listingReference, out listingDetail, out availableControlActions)` |
| 2.1 | AdminUI -> AdminCoordinator | `getListingDetailAndAvailableControlActions(in listingReference, out listingDetail, out availableControlActions)` |
| 2.2 | AdminCoordinator -> RoomListingLogic | `getListingDetailAndAvailableControlActions(in listingReference, out listingDetail, out availableControlActions)` |
| 2.3 | RoomListingLogic -> RoomListingDB | `findListingByReference(in listingReference, out roomListing)` |
| 3 | System Admin -> AdminUI | `submitListingControlAction(in listingReference, in listingControlAction, out listingControlOutcome)` |
| 3.1 | AdminUI -> AdminCoordinator | `applyListingControlAction(in listingReference, in listingControlAction, out listingControlOutcome, out deliveryStatus)` |
| 3.2 | AdminCoordinator -> RoomListingLogic | `applyAdministrativeListingControl(in listingReference, in listingControlAction, out listingControlOutcome)` |
| 3.3 | RoomListingLogic -> RoomListingDB | `findListingByReference(in listingReference, out roomListing)` |
| 3.4 | RoomListingLogic -> RoomListing | `applyAdministrativeListingControl(in listingControlAction, out listingVisibilityRecord)` |
| 3.5 | RoomListingLogic -> RoomListingDB | `saveListingVisibility(in roomListing, out listingVisibilityRecord)` |
| 3.6 | AdminCoordinator -> NotificationService | `composeOwnerListingControlNotification(in listingReference, in listingControlOutcome, out ownerNotification)` |
| 3.7 | AdminCoordinator -> EmailProxy | `sendOwnerListingControlNotification(in ownerNotification, out deliveryStatus)` |
| 3.8 | EmailProxy -> Email Provider | `sendNotification(in ownerNotification, out deliveryStatus)` |

## Alternative Flow Notes

- At message `2.2`, if the selected listing has no permitted administrative control action, `out availableControlActions` is empty and message group `3` is skipped.
- At messages `3.2` to `3.4`, `RoomListingLogic` revalidates that the requested action is still permitted for the current persisted listing state.
- If the requested action is no longer permitted at execution time, message `3.2` yields a failure `listingControlOutcome`, messages `3.4` to `3.8` are skipped, and `deliveryStatus` is treated as `notAttempted`.
- If the email provider is unavailable, the listing-control action still succeeds and `deliveryStatus` reports notification failure.

## Notes

- This is a design-phase communication diagram, so messages are function names rather than analysis-level noun phrases.
- `out` parameters inside the message label already imply returned data, so separate reply arrows are intentionally omitted.
- Persistence details are intentionally hidden behind `RoomListingDB`; the physical database is not shown as a separate participant in this version.
- `RoomListing` is kept as a `<<data abstraction>>` because the administrative visibility transition is applied to an in-memory listing object before the updated state is persisted.
