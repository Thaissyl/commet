# Communication Diagram: UC-17 Manage User Account Status - Analysis Model

## Object Layout

```text
System Admin --- AdminUI --- AdminCoordinator --- UserManagementLogic --- User
                                       |
                                       --- NotificationService
                                       |
                                       --- EmailProxy --- Email Provider
```

## Participants

| Position | Object              | Stereotype              | Justification                                                                                     |
| -------- | ------------------- | ----------------------- | ------------------------------------------------------------------------------------------------- |
| 1        | System Admin        | Actor (primary)         | The human user initiating the management action.                                                  |
| 2        | AdminUI             | `<<user interaction>>`  | Boundary object receiving inputs and displaying information.                                        |
| 3        | AdminCoordinator    | `<<coordinator>>`       | Control object sequencing the overall flow of the use case.                                          |
| 4        | UserManagementLogic | `<<business logic>>`    | Encapsulates the business rules for status transitions.                                             |
| 5        | User                | `<<entity>>`            | Conceptual data object encapsulating the user account record.                                        |
| 6        | NotificationService | `<<application logic>>` | Encapsulates the rules for formatting notification content.                                         |
| 7        | EmailProxy          | `<<proxy>>`             | Boundary object hiding the external email system API.                                               |
| 8        | Email Provider       | Actor (secondary)       | The external system receiving the notification.                                                     |

## Messages (Main Sequence - Active → Suspended)

| #   | From -> To                                   | Message / Information Passed         |
| --- | -------------------------------------------- | ------------------------------------ |
| 1   | System Admin -> AdminUI                     | Account Management Access            |
| 1.1 | AdminUI -> AdminCoordinator                | User Account List Request            |
| 1.2 | AdminCoordinator -> UserManagementLogic     | User Account List Request             |
| 1.3 | UserManagementLogic -> User                | User Account List Query               |
| 1.4 | User -> UserManagementLogic                | User Account List Data                |
| 1.5 | UserManagementLogic -> AdminCoordinator    | User Account List Data                |
| 1.6 | AdminCoordinator -> AdminUI                | User Account List                     |
| 1.7 | AdminUI -> System Admin                    | User Account List Display             |
| 2   | System Admin -> AdminUI                     | User Account Selection                |
| 2.1 | AdminUI -> AdminCoordinator                | User Account Detail Request           |
| 2.2 | AdminCoordinator -> UserManagementLogic     | User Account Detail Request           |
| 2.3 | UserManagementLogic -> User                | User Account Detail Query             |
| 2.4 | User -> UserManagementLogic                | User Account Data                     |
| 2.5 | UserManagementLogic -> AdminCoordinator    | User Account Detail and Available Status Actions |
| 2.6 | AdminCoordinator -> AdminUI                | User Account Detail and Available Status Actions |
| 2.7 | AdminUI -> System Admin                    | Detail and Available Actions Display  |
| 3   | System Admin -> AdminUI                     | Account Status Change Decision (Suspend) |
| 3.1 | AdminUI -> AdminCoordinator                | Account Status Change Request         |
| 3.2 | AdminCoordinator -> UserManagementLogic     | Account Status Transition Check       |
| 3.3 | UserManagementLogic -> User                | Account Status Transition Update      |
| 3.4 | User -> UserManagementLogic                | Account Status Record Confirmation    |
| 3.5 | UserManagementLogic -> AdminCoordinator    | Account Status Change Result          |
| 3.6 | AdminCoordinator -> NotificationService    | User Notification Request             |
| 3.7 | NotificationService -> AdminCoordinator    | User Notification Payload             |
| 3.8 | AdminCoordinator -> EmailProxy             | User Notification Dispatch            |
| 3.9 | EmailProxy -> Email Provider               | User Notification                    |
| 3.10 | Email Provider -> EmailProxy              | Notification Delivery Result         |
| 3.11 | EmailProxy -> AdminCoordinator            | Notification Delivery Result         |
| 3.12 | AdminCoordinator -> AdminUI                | Account Status Change Outcome         |
| 3.13 | AdminUI -> System Admin                    | Account Status Change Confirmation   |

## Alternative Sequences

| #    | From -> To                                   | Message / Information Passed                          |
| ---- | -------------------------------------------- | ---------------------------------------------------- |
| 2.5a | UserManagementLogic -> AdminCoordinator    | [No actions available] No Available Actions           |
| 2.6a | AdminCoordinator -> AdminUI                | No Actions Available Error                           |
| 2.7a | AdminUI -> System Admin                    | Error Display (Ends unsuccessfully)                   |
| 3.3a | UserManagementLogic -> AdminCoordinator    | [Transition not permitted] Invalid Transition Result |
| 3.4a | AdminCoordinator -> AdminUI                | Invalid Transition Error                             |
| 3.5a | AdminUI -> System Admin                    | Error Display (Ends unsuccessfully)                   |
| 3.11a | EmailProxy -> AdminCoordinator            | [Provider unavailable] Delivery Failure              |
| 3.12a | AdminCoordinator -> AdminUI                | Account Status Change Outcome (notification failed)  |

## Architectural Notes

- **Explicit Status Transition**: Main sequence explicitly describes "Active → Suspended" transition. Other valid transitions (Enable, Disable) follow the same pattern and would be shown as alternative sequences or separate use case instances.
- **Stateless Coordinator**: The `AdminCoordinator` does not keep the selected User object in memory between sequences. Each sequence starts with an explicit database query to maintain statelessness.
- **Data Persistence Separation**: In analysis, `UserManagementLogic` updates the User entity directly. In design, this will separate into: (1) User `<<data abstraction>>` mutates in RAM, (2) IUserRepository `<<database wrapper>>` executes SQL UPDATE for ACID durability.
- **Asynchronous External Proxy**: Messages 3.9-3.11 show synchronous waiting for email delivery. In design, this will optimize to fire-and-forget async dispatch to prevent blocking the admin's UI thread.
- **Analysis vs. Design**: This analysis model uses descriptive noun phrases (e.g., `Account Status Transition Update`) rather than operation signatures (e.g., `suspendAccount(in, out)`).

Use `/drawio-communication-diagram` to generate a visual `.drawio` file from this blueprint.
