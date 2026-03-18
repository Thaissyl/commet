# Communication Diagram: UC-14 Review Rental Request - Analysis Model

## Object Layout

```text
Owner --- OwnerUI --- ReviewRequestCoordinator --- ReviewRequestRules --- RentalRequest
                                      |                         |
                                      |                         --- RoomListing
                                      |
                                      --- EmailProxy --- Email Provider
```

## Participants

| Position | Object                  | Stereotype             | Justification                                                                                           |
| -------- | ----------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------- |
| 1        | Owner                   | Actor (primary)        | The human user initiating the review.                                                                   |
| 2        | OwnerUI                 | `<<user interaction>>` | Boundary object receiving physical inputs and displaying information.                                   |
| 3        | ReviewRequestCoordinator | `<<coordinator>>`      | Control object sequencing the overall flow of the use case.                                             |
| 4        | ReviewRequestRules      | `<<business logic>>`   | Encapsulates the business rules for validating decisions and ensuring room lock eligibility.            |
| 5        | RentalRequest           | `<<entity>>`           | Conceptual data object encapsulating the rental request record.                                          |
| 6        | RoomListing             | `<<entity>>`           | Conceptual data object encapsulating the room listing record.                                            |
| 7        | EmailProxy              | `<<proxy>>`            | Boundary object hiding the external email system API.                                                    |
| 8        | Email Provider          | Actor (secondary)      | The external system receiving notifications.                                                             |

## Messages (Main Sequence - Accept Path)

| #   | From -> To                                     | Message / Information Passed  | Use Case Step |
| --- | ---------------------------------------------- | ----------------------------- | ------------- |
| 1   | Owner -> OwnerUI                               | Review Function Access         | Step 1        |
| 1.1 | OwnerUI -> ReviewRequestCoordinator            | Room Requests Query            |               |
| 1.2 | ReviewRequestCoordinator -> RentalRequest      | Room Requests Data Request     |               |
| 1.3 | RentalRequest -> ReviewRequestCoordinator      | Room Requests Data             |               |
| 1.4 | ReviewRequestCoordinator -> OwnerUI            | Room Requests List             | Step 2        |
| 1.5 | OwnerUI -> Owner                               | Requests Display               |               |
| 2   | Owner -> OwnerUI                               | Request Selection              | Step 3        |
| 2.1 | OwnerUI -> ReviewRequestCoordinator            | Request Detail Query           |               |
| 2.2 | ReviewRequestCoordinator -> RentalRequest      | Request Detail Request         |               |
| 2.3 | RentalRequest -> ReviewRequestCoordinator      | Request Detail Data            |               |
| 2.4 | ReviewRequestCoordinator -> OwnerUI            | Request Detail and Options      | Step 4        |
| 2.5 | OwnerUI -> Owner                               | Request Detail Display         |               |
| 3   | Owner -> OwnerUI                               | Acceptance Decision            | Step 5        |
| 3.1 | OwnerUI -> ReviewRequestCoordinator            | Acceptance Request             |               |
| 3.2 | ReviewRequestCoordinator -> ReviewRequestRules | Decision Validation Check     |               |
| 3.3 | ReviewRequestRules -> ReviewRequestCoordinator | Validation Result (Valid)      |               |
| 3.4 | ReviewRequestCoordinator -> RentalRequest      | Accepted Status Update         | Step 6        |
| 3.5 | ReviewRequestCoordinator -> RoomListing        | Locked Status Update           | Step 7        |
| 3.6 | ReviewRequestCoordinator -> EmailProxy         | Tenant Notification Request    | Step 8        |
| 3.7 | EmailProxy -> Email Provider                   | Tenant Notification            |               |
| 3.8 | ReviewRequestCoordinator -> OwnerUI            | Decision Success               | Step 9        |
| 3.9 | OwnerUI -> Owner                               | Success Message Display        |               |

## Alternative Sequences

| #    | From -> To                                     | Message / Information Passed                           | Use Case Step           |
| ---- | ---------------------------------------------- | ---------------------------------------------------- | ----------------------- |
| 3.1a | OwnerUI -> ReviewRequestCoordinator            | [Reject] Rejection Request                            | Alt Step 5.1            |
| 3.4a | ReviewRequestCoordinator -> RentalRequest      | Rejected Status Update (Skips room locking)            | Continues to 3.6        |
| 3.1b | OwnerUI -> ReviewRequestCoordinator            | [Keep Pending] Pending Request                        | Alt Step 5.1            |
| 3.2b | ReviewRequestCoordinator -> OwnerUI            | Pending Preserved (Returns to Sequence 1)             | Returns to Step 2       |
| 3.7a | EmailProxy -> ReviewRequestCoordinator         | [Provider unavailable] Delivery Failure               | Alt Step 8.1            |
| 3.8a | ReviewRequestCoordinator -> OwnerUI            | Decision Success (notification failed recorded)        | Continues to 3.8        |

## Architectural Notes

- **Explicit Accept Path**: The main sequence explicitly describes the "Accept" scenario, as it is the primary transaction that finalizes the use case and locks the room. Other decisions (Reject, Keep Pending) are entirely moved to alternative sequences.
- **Analysis vs. Design**: In this analysis model, messages use descriptive noun phrases (e.g., `Accepted Status Update`, `Locked Status Update`) rather than operation signatures (e.g., `acceptRequest(in, out)`).
- **Two Entity Updates**: Accepting a request updates BOTH `RentalRequest` (to Accepted) AND `RoomListing` (to Locked). This is captured in Messages 3.4 and 3.5. Rejecting only updates `RentalRequest` (see 3.4a).
- **Separation of Concerns**: The `ReviewRequestCoordinator` delegates decision validation to `ReviewRequestRules` (`<<business logic>>`), ensuring room lock eligibility before applying state changes.
- **Explicit Returns**: The analysis model shows explicit data flow (e.g., `Room Requests Data` in Message 1.3). In the design phase, these will be embedded into `out` parameters of synchronous calls.

Use `/drawio-communication-diagram` to generate a visual `.drawio` file from this blueprint.
