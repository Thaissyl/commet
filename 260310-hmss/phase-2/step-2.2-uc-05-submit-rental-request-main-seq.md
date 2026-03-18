# Communication Diagram: UC-05 Submit Rental Request - Analysis Model

## Object Layout

```text
Tenant --- TenantUI --- RentalRequestCoordinator --- RentalRequestRules --- RoomListing
                                      |                         |
                                      |                         --- RentalRequest
                                      |
                                      --- EmailProxy --- Email Provider
```

## Participants

| Position | Object                   | Stereotype             | Justification                                                                                           |
| -------- | ------------------------ | ---------------------- | ------------------------------------------------------------------------------------------------------- |
| 1        | Tenant                   | Actor (primary)        | The human actor initiating the use case.                                                                |
| 2        | TenantUI                 | `<<user interaction>>` | Boundary object receiving physical inputs and displaying information.                                   |
| 3        | RentalRequestCoordinator | `<<coordinator>>`      | Control object that sequences the overall flow of the use case.                                         |
| 4        | RentalRequestRules       | `<<business logic>>`   | Encapsulates the specific business rules for validating required fields and checking room availability. |
| 5        | RoomListing              | `<<entity>>`           | Long-lived data object encapsulating the room's summary and requestable status.                         |
| 6        | RentalRequest            | `<<entity>>`           | Long-lived data object encapsulating the newly submitted rental request data.                           |
| 7        | EmailProxy               | `<<proxy>>`            | Boundary object that hides the technical details of communicating with the external email system.       |
| 8        | Email Provider           | Actor (secondary)      | The external system receiving the notification.                                                         |

## Messages (Main Sequence)

| #   | From -> To                                     | Message / Information Passed         | Use Case Step |
| --- | ---------------------------------------------- | ------------------------------------ | ------------- |
| 1   | Tenant -> TenantUI                             | Rental Request Access                | Step 1        |
| 1.1 | TenantUI -> RentalRequestCoordinator           | Room Summary Request                 |               |
| 1.2 | RentalRequestCoordinator -> RoomListing        | Room Information Request             |               |
| 1.3 | RoomListing -> RentalRequestCoordinator        | Room Summary Data                    |               |
| 1.4 | RentalRequestCoordinator -> TenantUI           | Rental Request Form and Room Summary | Step 2        |
| 1.5 | TenantUI -> Tenant                             | Rental Request Form Display          |               |
| 2   | Tenant -> TenantUI                             | Rental Request Information           | Step 3        |
| 2.1 | TenantUI -> RentalRequestCoordinator           | Rental Request Information           |               |
| 2.2 | RentalRequestCoordinator -> RentalRequestRules | Request Validation Check             | Step 4        |
| 2.3 | RentalRequestRules -> RoomListing              | Room Status Request                  |               |
| 2.4 | RoomListing -> RentalRequestRules              | Room Status Data                     |               |
| 2.5 | RentalRequestRules -> RentalRequestCoordinator | Validation Result                    |               |
| 2.6 | RentalRequestCoordinator -> TenantUI           | Review Prompt                        |               |
| 2.7 | TenantUI -> Tenant                             | Rental Request Review Display        | Step 5        |
| 3   | Tenant -> TenantUI                             | Submission Confirmation              | Step 5        |
| 3.1 | TenantUI -> RentalRequestCoordinator           | Submission Confirmation              |               |
| 3.2 | RentalRequestCoordinator -> RentalRequest      | New Rental Request Record            | Step 6        |
| 3.3 | RentalRequestCoordinator -> EmailProxy         | Owner Notification                   | Step 7        |
| 3.4 | EmailProxy -> Email Provider                   | Owner Notification                   |               |
| 3.5 | RentalRequestCoordinator -> TenantUI           | Submission Success                   | Step 8        |
| 3.6 | TenantUI -> Tenant                             | Submission Success Message           |               |

## Alternative Sequences

| #    | From -> To                                     | Message / Information Passed                           | Use Case Step    |
| ---- | ---------------------------------------------- | ------------------------------------------------------ | ---------------- |
| 2.5a | RentalRequestRules -> RentalRequestCoordinator | [Room not requestable] Validation Result (Unavailable) | Alt Step 4.1     |
| 2.6a | RentalRequestCoordinator -> TenantUI           | Room Unavailable Error                                 |                  |
| 2.7a | TenantUI -> Tenant                             | Room Unavailable Display                               | Ends             |
| 2.5b | RentalRequestRules -> RentalRequestCoordinator | [Invalid Fields] Validation Result (Invalid)           | Alt Step 4.1     |
| 2.6b | RentalRequestCoordinator -> TenantUI           | Correction Prompt                                      |                  |
| 2.7b | TenantUI -> Tenant                             | Correction Display                                     | Returns to 2     |
| 3.4a | EmailProxy -> RentalRequestCoordinator         | [Provider unavailable] Delivery Failure                | Alt Step 7.1     |
| 3.4b | RentalRequestCoordinator -> RentalRequest      | Failed Notification Record                             | Continues to 3.5 |

## Architectural Notes

- **Noun Phrases**: Messages use descriptive noun phrases (e.g., "New Rental Request Record") rather than operation signatures (e.g., `createRentalRequest(in, out)`). This keeps the focus on what the system does, not how it's programmed.
- **Explicit Returns**: The analysis model uses explicit return messages (e.g., Messages 1.3, 2.4, 2.5) to clearly show data flowing back up to the coordinator.
- **Stateless Coordinator**: `RentalRequestCoordinator` will act as a Façade in the design phase, delegating validation to `RentalRequestRules` and persistence to repository wrappers.

Use `/drawio-communication-diagram` to generate a visual `.drawio` file from this blueprint.
