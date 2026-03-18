# Communication Diagram: UC-15 Reopen Room Listing - Analysis Model

## Object Layout

```text
Owner --- OwnerUI --- ReopenRoomCoordinator --- ReopenRules --- RentalRequest
                                      |                     |
                                      |                     --- RoomListing
                                      |
                                      --- EmailProxy --- Email Provider
```

## Participants

| Position | Object                | Stereotype             | Justification                                                                                           |
| -------- | --------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------- |
| 1        | Owner                 | Actor (primary)        | The human user initiating the reopening.                                                                |
| 2        | OwnerUI               | `<<user interaction>>` | Boundary object receiving physical inputs and displaying information.                                   |
| 3        | ReopenRoomCoordinator | `<<coordinator>>`      | Control object sequencing the overall flow of the use case without holding state.                         |
| 4        | ReopenRules           | `<<business logic>>`   | Encapsulates the specific business rules for validating status concurrency and eligibility.              |
| 5        | RentalRequest         | `<<entity>>`           | Conceptual data object encapsulating the rental request record.                                          |
| 6        | RoomListing           | `<<entity>>`           | Conceptual data object encapsulating the locked room record.                                             |
| 7        | EmailProxy            | `<<proxy>>`            | Boundary object hiding the technical details of the external email system API.                           |
| 8        | Email Provider        | Actor (secondary)      | The external system receiving notifications.                                                             |

## Messages (Main Sequence)

| #   | From -> To                                   | Message / Information Passed        | Use Case Step     |
| --- | -------------------------------------------- | ----------------------------------- | ----------------- |
| 1   | Owner -> OwnerUI                             | Accepted Arrangements Access        | Step 1            |
| 1.1 | OwnerUI -> ReopenRoomCoordinator            | Accepted Arrangements Query         |                   |
| 1.2 | ReopenRoomCoordinator -> RentalRequest      | Accepted Arrangements Request       |                   |
| 1.3 | RentalRequest -> ReopenRoomCoordinator      | Accepted Arrangements Data          |                   |
| 1.4 | ReopenRoomCoordinator -> OwnerUI            | Accepted Arrangements and Room Info | Step 2            |
| 1.5 | OwnerUI -> Owner                             | Arrangements Display                |                   |
| 2   | Owner -> OwnerUI                             | Arrangement Selection               | Step 3            |
| 2.1 | OwnerUI -> ReopenRoomCoordinator            | Arrangement Selection Request       |                   |
| 2.2 | ReopenRoomCoordinator -> ReopenRules        | Status Concurrency Check            | Step 4            |
| 2.3 | ReopenRules -> RentalRequest                | Request Status Query                |                   |
| 2.4 | RentalRequest -> ReopenRules                | Request Status Data                 |                   |
| 2.5 | ReopenRules -> ReopenRoomCoordinator        | Validation Result (Valid)           |                   |
| 2.6 | ReopenRoomCoordinator -> OwnerUI            | Reopen Action Prompt and Consequences | Step 5          |
| 2.7 | OwnerUI -> Owner                             | Prompt Display                      |                   |
| 3   | Owner -> OwnerUI                             | Reopen Confirmation                | Step 6 (Orig. 5)  |
| 3.1 | OwnerUI -> ReopenRoomCoordinator            | Confirmed Reopen Request            |                   |
| 3.2 | ReopenRoomCoordinator -> RentalRequest      | Revoked Status Update               | Step 7 (Orig. 6)  |
| 3.3 | ReopenRoomCoordinator -> RoomListing        | Published Available Status Update   | Step 8 (Orig. 7)  |
| 3.4 | ReopenRoomCoordinator -> EmailProxy         | Tenant Notification Request         | Step 9 (Orig. 8)  |
| 3.5 | EmailProxy -> Email Provider                | Tenant Notification                 |                   |
| 3.6 | ReopenRoomCoordinator -> OwnerUI            | Reopen Success                      | Step 10 (Orig. 9) |
| 3.7 | OwnerUI -> Owner                             | Reopen Success Message              |                   |

## Alternative Sequences

| #    | From -> To                                   | Message / Information Passed                    | Use Case Step        |
| ---- | -------------------------------------------- | ---------------------------------------------- | -------------------- |
| 2.5a | ReopenRules -> ReopenRoomCoordinator         | [Status changed] Validation Result (Invalid)    | Alt Step 3.1         |
| 2.6a | ReopenRoomCoordinator -> OwnerUI             | Invalid Status Error Prompt                     |                      |
| 2.7a | OwnerUI -> Owner                             | Error Display                                   | Ends unsuccessfully   |
| 3.5a | EmailProxy -> ReopenRoomCoordinator         | [Provider unavailable] Delivery Failure         | Alt Step 8.1         |
| 3.5b | ReopenRoomCoordinator -> RentalRequest       | Failed Notification Record                      | Continues to 3.6      |

## Architectural Notes

- **Explicit Concurrency Check**: Step 4 (Status Concurrency Check) was inserted to validate that the selected request is still in Accepted status. This handles the edge case where status changes between Step 2 (display) and Step 3 (selection) due to concurrency.
- **Two Entity Updates**: Reopening updates BOTH `RentalRequest` (to Revoked by Owner) AND `RoomListing` (to Published Available). This reverses the locking that occurred in UC-14 (Review Rental Request).
- **Analysis vs. Design**: In this analysis model, messages use descriptive noun phrases (e.g., `Revoked Status Update`, `Published Available Status Update`) rather than operation signatures (e.g., `reopenListing(in, out)`).
- **Separation of Concerns**: The `ReopenRoomCoordinator` delegates status validation to `ReopenRules` (`<<business logic>>`), ensuring the request is still in Accepted status before proceeding.
- **Explicit Returns**: The analysis model shows explicit data flow (e.g., `Request Status Data` in Message 2.4). In the design phase, these will be embedded into `out` parameters of synchronous calls.

Use `/drawio-communication-diagram` to generate a visual `.drawio` file from this blueprint.
