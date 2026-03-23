# Communication Diagram: UC-18 Control Listing Visibility - Analysis Model

## Object Layout

```text
System Admin --- AdminUI --- ControlListingCoordinator --- RoomListing
                                       |
                                       --- UserAccount
                                       |
                                       --- EmailProxy --- Email Provider
```

## Participants

| Position | Object                    | Stereotype             | Justification |
| -------- | ------------------------- | ---------------------- | ------------- |
| 1        | System Admin              | Actor (primary)        | The human user initiating the listing-control action. |
| 2        | AdminUI                   | `<<user interaction>>` | Boundary object receiving admin input and displaying listing-control information. |
| 3        | ControlListingCoordinator | `<<coordinator>>`      | Control object sequencing the overall flow of the use case without holding long-lived state. |
| 4        | RoomListing               | `<<entity>>`           | Conceptual data object encapsulating the room listing and its current visibility state. |
| 5        | UserAccount               | `<<entity>>`           | Conceptual data object representing owner identity and contact information used for list/detail enrichment and notification. |
| 6        | EmailProxy                | `<<proxy>>`            | Boundary object hiding the technical details of the external email system API. |
| 7        | Email Provider            | Actor (secondary)      | The external system dispatching owner-notification emails. |

## Messages (Main Sequence - Disable Action)

| #   | From -> To                             | Message / Information Passed | Use Case Step |
| --- | -------------------------------------- | ---------------------------- | ------------- |
| 1   | System Admin -> AdminUI                | Listing Administration Access | Step 1 |
| 1.1 | AdminUI -> ControlListingCoordinator   | Visible Listings Query | |
| 1.2 | ControlListingCoordinator -> RoomListing | Visible Listings Query | |
| 1.3 | RoomListing -> ControlListingCoordinator | Visible Listings Data | |
| 1.4 | ControlListingCoordinator -> UserAccount | Owner Account Summary Query | |
| 1.5 | UserAccount -> ControlListingCoordinator | Owner Account Summary Data | |
| 1.6 | ControlListingCoordinator -> AdminUI   | Visible Listings with Associated Information | Step 2 |
| 1.7 | AdminUI -> System Admin                | Visible Listings Display | |
| 2   | System Admin -> AdminUI                | Listing Selection | Step 3 |
| 2.1 | AdminUI -> ControlListingCoordinator   | Listing Detail Query | |
| 2.2 | ControlListingCoordinator -> RoomListing | Listing Detail Query | |
| 2.3 | RoomListing -> ControlListingCoordinator | Listing Detail Data | |
| 2.4 | ControlListingCoordinator -> UserAccount | Owner Account Detail Query | |
| 2.5 | UserAccount -> ControlListingCoordinator | Owner Account Detail Data | |
| 2.6 | ControlListingCoordinator -> AdminUI   | Listing Details and Disable Action | Step 4 |
| 2.7 | AdminUI -> System Admin                | Details and Disable Action Display | |
| 3   | System Admin -> AdminUI                | Disable Action Decision | Step 5 |
| 3.1 | AdminUI -> ControlListingCoordinator   | Disable Action Request | |
| 3.2 | ControlListingCoordinator -> RoomListing | Disable Eligibility Check | Step 6 |
| 3.3 | RoomListing -> ControlListingCoordinator | Eligibility Result (Valid) | |
| 3.4 | ControlListingCoordinator -> RoomListing | Apply Disable Action | Step 7 |
| 3.5 | ControlListingCoordinator -> EmailProxy | Owner Notification Request | Step 8 |
| 3.6 | EmailProxy -> Email Provider           | Owner Notification | |
| 3.7 | ControlListingCoordinator -> AdminUI   | Action Success | Step 9 |
| 3.8 | AdminUI -> System Admin                | Action Success Message Display | |

## Alternative Sequences

| #    | From -> To                             | Message / Information Passed | Use Case Step |
| ---- | -------------------------------------- | ---------------------------- | ------------- |
| 3.3a | RoomListing -> ControlListingCoordinator | [Listing cannot be disabled] Invalid Listing State Result | Alt Step 6.1 |
| 3.4a | ControlListingCoordinator -> AdminUI   | Invalid Listing State Error | |
| 3.5a | AdminUI -> System Admin                | Error Display (Ends unsuccessfully) | |

## Architectural Notes

- **Use-Case-and-Code Balanced Analysis**: This analysis remains business-oriented but reflects the current implemented workflow more closely than the earlier version.
- **Owner Data Enrichment**: `UserAccount` is included because the implemented system loads owner information when building list and detail responses.
- **Business Action vs. Implementation Detail**: The analysis keeps the business action name `Disable`. In the current implementation, that action is realized as an archive operation on the listing.
- **Validation Scope**: The message name `Disable Eligibility Check` avoids overstating the exact rule as "still publicly visible" when the current implementation uses a weaker status-validity check.
- **Notification Boundary**: Notification is represented as a direct boundary crossing through `EmailProxy` to the `Email Provider`. Internal payload-composition helpers are intentionally omitted from analysis.
- **Delivery Failure Gap**: The use case description mentions provider-unavailable handling, but the current controller sends email asynchronously and does not expose synchronous delivery feedback in its request flow.

Use `/drawio-communication-diagram` to generate a visual `.drawio` file from this blueprint.
