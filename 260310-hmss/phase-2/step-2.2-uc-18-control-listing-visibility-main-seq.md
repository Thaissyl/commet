# Communication Diagram: UC-18 Control Listing Visibility - Analysis Model

## Object Layout

```text
System Admin --- AdminUI --- ControlListingCoordinator --- ListingControlRules --- RoomListing
                                       |
                                       --- NotificationService
                                       |
                                       --- EmailProxy --- Email Provider
```

## Participants

| Position | Object                 | Stereotype              | Justification                                                                                           |
| -------- | ---------------------- | ----------------------- | ------------------------------------------------------------------------------------------------------- |
| 1        | System Admin           | Actor (primary)         | The human user initiating the control action.                                                          |
| 2        | AdminUI                | `<<user interaction>>`  | Boundary object receiving physical inputs and displaying information.                                  |
| 3        | ControlListingCoordinator | `<<coordinator>>`      | Control object sequencing the overall flow of the use case without holding state.                        |
| 4        | ListingControlRules    | `<<business logic>>`    | Encapsulates the business rules for validating admin actions and checking status concurrency.           |
| 5        | RoomListing            | `<<entity>>`            | Conceptual data object encapsulating the room listing record.                                           |
| 6        | NotificationService    | `<<application logic>>` | Encapsulates the rules for formatting the owner notification payload.                                    |
| 7        | EmailProxy             | `<<proxy>>`             | Boundary object hiding the external email system API.                                                  |
| 8        | Email Provider         | Actor (secondary)       | The external system dispatching notifications.                                                         |

## Messages (Main Sequence - Disable Action)

| #   | From -> To                                     | Message / Information Passed     | Use Case Step |
| --- | ---------------------------------------------- | -------------------------------- | ------------- |
| 1   | System Admin -> AdminUI                        | Listing Administration Access    | Step 1        |
| 1.1 | AdminUI -> ControlListingCoordinator           | Visible Listings Query           |               |
| 1.2 | ControlListingCoordinator -> RoomListing       | Visible Listings Request         |               |
| 1.3 | RoomListing -> ControlListingCoordinator       | Visible Listings Data            |               |
| 1.4 | ControlListingCoordinator -> AdminUI           | Visible Listings List            | Step 2        |
| 1.5 | AdminUI -> System Admin                        | Visible Listings Display         |               |
| 2   | System Admin -> AdminUI                        | Listing Selection                | Step 3        |
| 2.1 | AdminUI -> ControlListingCoordinator           | Listing Detail Query             |               |
| 2.2 | ControlListingCoordinator -> RoomListing       | Listing Detail Request           |               |
| 2.3 | RoomListing -> ControlListingCoordinator       | Listing Detail Data              |               |
| 2.4 | ControlListingCoordinator -> AdminUI           | Listing Details and Control Actions | Step 4       |
| 2.5 | AdminUI -> System Admin                        | Details and Disable Action Display |               |
| 3   | System Admin -> AdminUI                        | Disable Action Decision          | Step 5        |
| 3.1 | AdminUI -> ControlListingCoordinator           | Disable Action Request           |               |
| 3.2 | ControlListingCoordinator -> ListingControlRules | Status Concurrency Check         | Step 6        |
| 3.3 | ListingControlRules -> RoomListing             | Listing Status Query             |               |
| 3.4 | RoomListing -> ListingControlRules             | Listing Status Data              |               |
| 3.5 | ListingControlRules -> ControlListingCoordinator | Validation Result (Valid)       |               |
| 3.6 | ControlListingCoordinator -> RoomListing       | Disabled Status Update           | Step 7        |
| 3.7 | ControlListingCoordinator -> NotificationService | Owner Notification Request     | Step 8        |
| 3.8 | NotificationService -> ControlListingCoordinator | Owner Notification Payload    |               |
| 3.9 | ControlListingCoordinator -> EmailProxy        | Owner Notification Dispatch      |               |
| 3.10 | EmailProxy -> Email Provider                  | Owner Notification               |               |
| 3.11 | EmailProxy -> ControlListingCoordinator       | Notification Delivery Result    |               |
| 3.12 | ControlListingCoordinator -> AdminUI           | Action Success                   | Step 9        |
| 3.13 | AdminUI -> System Admin                        | Action Success Message Display   |               |

## Alternative Sequences

| #    | From -> To                                     | Message / Information Passed               | Use Case Step       |
| ---- | ---------------------------------------------- | ------------------------------------------ | ------------------- |
| 3.5a | ListingControlRules -> ControlListingCoordinator | [Status changed] Validation Result (Invalid) | Alt Step 6.1       |
| 3.6a | ControlListingCoordinator -> AdminUI           | Invalid Status Error                       |                     |
| 3.7a | AdminUI -> System Admin                        | Error Display (Ends unsuccessfully)         |                     |
| 3.11a | EmailProxy -> ControlListingCoordinator       | [Provider unavailable] Delivery Failure    | Alt Step 8.1        |
| 3.12a | ControlListingCoordinator -> AdminUI           | Action Success (notification failed recorded) | Continues to 3.12 |

## Architectural Notes

- **Precondition vs. Business Logic**: Removed "The target listing is currently publicly visible" from Preconditions. The system queries and filters for visible listings during the use case (Step 2), making this business logic, not a precondition. Only valid precondition: "System Admin is signed in."
- **Explicit Concurrency Check**: Step 6 (Status Concurrency Check) validates that the selected listing is still publicly visible before applying the Disable action. This handles the edge case where the Owner concurrently hid or deleted the listing during admin review (between Step 4 and Step 5).
- **Analysis vs. Design**: In this analysis model, messages use descriptive noun phrases (e.g., `Disabled Status Update`) rather than operation signatures (e.g., `disableListing(in, out)`).
- **Separation of Concerns**: The `ControlListingCoordinator` delegates status validation to `ListingControlRules` (`<<business logic>>`), ensuring the listing is still in a valid state before mutation.
- **Asynchronous Notification**: Messages 3.9-3.11 show synchronous email delivery. In design, this will optimize to fire-and-forget async dispatch to prevent blocking the admin's UI thread.

Use `/drawio-communication-diagram` to generate a visual `.drawio` file from this blueprint.
