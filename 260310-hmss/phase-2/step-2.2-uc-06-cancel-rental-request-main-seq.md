# Communication Diagram: UC-06 Cancel Rental Request - Analysis Model

## Object Layout

```text
Tenant --- TenantUI --- RentalRequestCoordinator --- RentalRequestRules --- RentalRequest
                                      |
                                      --- EmailProxy --- Email Provider
```

## Participants

| Position | Object                   | Stereotype             | Justification                                                                                                        |
| -------- | ------------------------ | ---------------------- | -------------------------------------------------------------------------------------------------------------------- |
| 1        | Tenant                   | Actor (primary)        | The human actor initiating the use case.                                                                             |
| 2        | TenantUI                 | `<<user interaction>>` | Boundary object receiving physical inputs and displaying information.                                                |
| 3        | RentalRequestCoordinator | `<<coordinator>>`      | Control object that sequences the overall flow of the use case.                                                      |
| 4        | RentalRequestRules       | `<<business logic>>`   | Encapsulates the specific business rules for checking if the request is still pending and eligible for cancellation. |
| 5        | RentalRequest            | `<<entity>>`           | Long-lived data object encapsulating the rental request data and its current status.                                 |
| 6        | EmailProxy               | `<<proxy>>`            | Boundary object that hides the technical details of communicating with the external email system.                    |
| 7        | Email Provider           | Actor (secondary)      | The external system receiving the notification.                                                                      |

## Messages (Main Sequence)

| #   | From -> To                                     | Message / Information Passed     | Use Case Step |
| --- | ---------------------------------------------- | -------------------------------- | ------------- |
| 1   | Tenant -> TenantUI                             | Request Management Access        | Step 1        |
| 1.1 | TenantUI -> RentalRequestCoordinator           | Rental Request List Request      |               |
| 1.2 | RentalRequestCoordinator -> RentalRequest      | Tenant Requests Query            |               |
| 1.3 | RentalRequest -> RentalRequestCoordinator      | Tenant Requests Data             |               |
| 1.4 | RentalRequestCoordinator -> TenantUI           | Rental Requests and Statuses     | Step 2        |
| 1.5 | TenantUI -> Tenant                             | Rental Requests Display          |               |
| 2   | Tenant -> TenantUI                             | Cancellation Selection           | Step 3        |
| 2.1 | TenantUI -> RentalRequestCoordinator           | Cancellation Request             |               |
| 2.2 | RentalRequestCoordinator -> RentalRequestRules | Cancellation Eligibility Check   | Step 4        |
| 2.3 | RentalRequestRules -> RentalRequest            | Request Status Query             |               |
| 2.4 | RentalRequest -> RentalRequestRules            | Request Status Data              |               |
| 2.5 | RentalRequestRules -> RentalRequestCoordinator | Eligibility Result (Eligible)    |               |
| 2.6 | RentalRequestCoordinator -> TenantUI           | Cancellation Confirmation Prompt |               |
| 2.7 | TenantUI -> Tenant                             | Confirmation Prompt Display      |               |
| 3   | Tenant -> TenantUI                             | Cancellation Confirmation        | Step 5        |
| 3.1 | TenantUI -> RentalRequestCoordinator           | Confirmed Cancellation           |               |
| 3.2 | RentalRequestCoordinator -> RentalRequest      | Cancellation Status Update       | Step 6        |
| 3.3 | RentalRequestCoordinator -> EmailProxy         | Owner Notification Request       | Step 7        |
| 3.4 | EmailProxy -> Email Provider                   | Owner Notification               |               |
| 3.5 | RentalRequestCoordinator -> TenantUI           | Cancellation Success             | Step 8        |
| 3.6 | TenantUI -> Tenant                             | Cancellation Success Message     |               |

## Alternative Sequences

| #    | From -> To                                     | Message / Information Passed                   | Use Case Step    |
| ---- | ---------------------------------------------- | ---------------------------------------------- | ---------------- |
| 2.5a | RentalRequestRules -> RentalRequestCoordinator | [Not eligible] Eligibility Result (Ineligible) | Alt Step 4.1     |
| 2.6a | RentalRequestCoordinator -> TenantUI           | Ineligible Cancellation Error                  |                  |
| 2.7a | TenantUI -> Tenant                             | Ineligible Cancellation Display                | Ends             |
| 3.4a | EmailProxy -> RentalRequestCoordinator         | [Provider unavailable] Delivery Failure        | Alt Step 7.1     |
| 3.4b | RentalRequestCoordinator -> RentalRequest      | Failed Notification Record                     | Continues to 3.5 |

## Architectural Notes

- **Explicit Returns vs. Method Signatures**: In analysis modeling, we use messages like `Tenant Requests Data` (Message 1.3) and `Eligibility Result` (Message 2.5) to explicitly show data flowing back to the Coordinator. Later, in the design phase, these explicit return messages will be absorbed into the `out` parameters of synchronous `methodName(in, out)` calls.
- **Separation of Concerns**: The `RentalRequestCoordinator` does not check the status itself. It asks the `RentalRequestRules` (`<<business logic>>`), which queries the `RentalRequest` (`<<entity>>`). This perfectly sets up the design phase, allowing the rules to be encapsulated away from the controller.
- **Noun Phrases**: Interactions crossing the system boundary (Actor ↔ UI) and internal system messages strictly use physical events or data descriptions (e.g., `Owner Notification Request` instead of `sendAsync()`), keeping the focus on what the system is doing before worrying about how to code it.

Use `/drawio-communication-diagram` to generate a visual `.drawio` file from this blueprint.
