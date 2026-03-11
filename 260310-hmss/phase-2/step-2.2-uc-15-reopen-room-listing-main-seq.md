# Communication Diagram: UC-15 Reopen Room Listing - Main Sequence

## Object Layout

```text
Owner --- ReopenArrangementUI --- RequestReviewCoordinator --- RentalRequestLogic --- RentalRequest
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
| 2 | ReopenArrangementUI | `<<user interaction>>` |
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
| 1 | Owner -> ReopenArrangementUI | Accepted Arrangement Management Access |
| 1.1 | ReopenArrangementUI -> RequestReviewCoordinator | Accepted Arrangement List Request |
| 1.2 | RequestReviewCoordinator -> RentalRequestLogic | Accepted Arrangement List Request |
| 1.3 | RentalRequestLogic -> RentalRequest | Accepted Arrangement List Request |
| 1.4 | RentalRequest -> RentalRequestLogic | Accepted Arrangement List |
| 1.5 | RentalRequestLogic -> RequestReviewCoordinator | Accepted Arrangement List and Room Information |
| 1.6 | RequestReviewCoordinator -> ReopenArrangementUI | Accepted Arrangement List |
| 1.7 | ReopenArrangementUI -> Owner | Accepted Arrangement List |
| 2 | Owner -> ReopenArrangementUI | Accepted Arrangement Selection |
| 2.1 | ReopenArrangementUI -> RequestReviewCoordinator | Accepted Arrangement Detail Request |
| 2.2 | RequestReviewCoordinator -> RentalRequestLogic | Accepted Arrangement Detail Request |
| 2.3 | RentalRequestLogic -> RentalRequest | Accepted Arrangement Detail Request |
| 2.4 | RentalRequest -> RentalRequestLogic | Accepted Arrangement Detail |
| 2.5 | RentalRequestLogic -> RequestReviewCoordinator | Reopen Detail and Business Consequence |
| 2.6 | RequestReviewCoordinator -> ReopenArrangementUI | Reopen Detail and Business Consequence |
| 2.7 | ReopenArrangementUI -> Owner | Reopen Detail and Business Consequence |
| 3 | Owner -> ReopenArrangementUI | Reopen Confirmation |
| 3.1 | ReopenArrangementUI -> RequestReviewCoordinator | Reopen Request |
| 3.2 | RequestReviewCoordinator -> RentalRequestLogic | Reopen Request |
| 3.3 | RentalRequestLogic -> RentalRequest | Rental Request Record |
| 3.4 | RentalRequestLogic -> RoomListing | Room Listing Status Record |
| 3.5 | RentalRequestLogic -> RequestReviewCoordinator | Reopen Result |
| 3.6 | RequestReviewCoordinator -> NotificationService | Tenant Notification Request |
| 3.7 | NotificationService -> RequestReviewCoordinator | Tenant Notification |
| 3.8 | RequestReviewCoordinator -> EmailProxy | Tenant Notification |
| 3.9 | EmailProxy -> Email Provider | Tenant Notification |
| 3.10 | Email Provider -> EmailProxy | Notification Delivery Result |
| 3.11 | EmailProxy -> RequestReviewCoordinator | Notification Delivery Result |
| 3.12 | RequestReviewCoordinator -> ReopenArrangementUI | Reopen Outcome |
| 3.13 | ReopenArrangementUI -> Owner | Reopen Confirmation |

## Notes

- `RentalRequestLogic` owns both the request revocation and the room reopening rule.
- The notification path is coordinated after the reopen result is recorded.
- Messages are kept at analysis level and avoid method-style naming.

Use `/drawio` to generate a visual `.drawio` file from this blueprint.
