# Communication Diagram: UC-14 Review Rental Request - Main Sequence (Accept)

## Object Layout

```text
Owner --- RentalRequestReviewUI --- RequestReviewCoordinator --- RentalRequestLogic --- RentalRequest
                                               |                                      |
                                               |                                      --- RoomListing
                                               |
                                               --- NotificationService
                                               |
                                               --- EmailProxy --- Email Provider
```

## Participants

| Position | Object | Stereotype |
|---|---|---|
| 1 | Owner | Actor (primary) |
| 2 | RentalRequestReviewUI | `<<user interaction>>` |
| 3 | RequestReviewCoordinator | `<<coordinator>>` |
| 4 | RentalRequestLogic | `<<business logic>>` |
| 5 | RentalRequest | `<<entity>>` |
| 6 | RoomListing | `<<entity>>` |
| 7 | NotificationService | `<<service>>` |
| 8 | EmailProxy | `<<proxy>>` |
| 9 | Email Provider | Actor (secondary) |

## Messages

| # | From -> To | Message |
|---|---|---|
| 1 | Owner -> RentalRequestReviewUI | Rental Request Review Access |
| 1.1 | RentalRequestReviewUI -> RequestReviewCoordinator | Rental Request List Request |
| 1.2 | RequestReviewCoordinator -> RentalRequestLogic | Rental Request List Request |
| 1.3 | RentalRequestLogic -> RentalRequest | Rental Request List Request |
| 1.4 | RentalRequest -> RentalRequestLogic | Rental Request List |
| 1.5 | RentalRequestLogic -> RequestReviewCoordinator | Rental Request List |
| 1.6 | RequestReviewCoordinator -> RentalRequestReviewUI | Rental Request List |
| 1.7 | RentalRequestReviewUI -> Owner | Rental Request List |
| 2 | Owner -> RentalRequestReviewUI | Rental Request Selection |
| 2.1 | RentalRequestReviewUI -> RequestReviewCoordinator | Rental Request Detail Request |
| 2.2 | RequestReviewCoordinator -> RentalRequestLogic | Rental Request Detail Request |
| 2.3 | RentalRequestLogic -> RentalRequest | Rental Request Detail Request |
| 2.4 | RentalRequest -> RentalRequestLogic | Rental Request Detail |
| 2.5 | RentalRequestLogic -> RequestReviewCoordinator | Rental Request Detail and Decision Options |
| 2.6 | RequestReviewCoordinator -> RentalRequestReviewUI | Rental Request Detail and Decision Options |
| 2.7 | RentalRequestReviewUI -> Owner | Rental Request Detail and Decision Options |
| 3 | Owner -> RentalRequestReviewUI | Rental Request Decision |
| 3.1 | RentalRequestReviewUI -> RequestReviewCoordinator | Rental Request Decision |
| 3.2 | RequestReviewCoordinator -> RentalRequestLogic | Rental Request Decision |
| 3.3 | RentalRequestLogic -> RentalRequest | Rental Request Record |
| 3.4 | RentalRequestLogic -> RoomListing | Room Listing Status Record |
| 3.5 | RentalRequestLogic -> RequestReviewCoordinator | Rental Request Decision Result |
| 3.6 | RequestReviewCoordinator -> NotificationService | Tenant Notification Request |
| 3.7 | NotificationService -> RequestReviewCoordinator | Tenant Notification |
| 3.8 | RequestReviewCoordinator -> EmailProxy | Tenant Notification |
| 3.9 | EmailProxy -> Email Provider | Tenant Notification |
| 3.10 | Email Provider -> EmailProxy | Notification Delivery Result |
| 3.11 | EmailProxy -> RequestReviewCoordinator | Notification Delivery Result |
| 3.12 | RequestReviewCoordinator -> RentalRequestReviewUI | Rental Request Review Outcome |
| 3.13 | RentalRequestReviewUI -> Owner | Rental Request Review Confirmation |

## Notes

- Main sequence shows the `Accept` decision path. The `Reject` path keeps the same structure but omits the room-locking effect on `RoomListing`.
- `RentalRequestLogic` owns both the request-status update and the room-locking rule when the request is accepted.
- Messages are kept at analysis level and avoid method-style naming.

Use `/drawio` to generate a visual `.drawio` file from this blueprint.
