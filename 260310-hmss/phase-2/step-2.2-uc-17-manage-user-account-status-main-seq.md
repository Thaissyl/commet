# Communication Diagram: UC-17 Manage User Account Status - Analysis Model

## Object Layout

```text
System Admin --- AdminUI --- AdminCoordinator --- UserAccount
                                       |
                                       --- EmailProxy --- Email Provider
```

## Participants

| Position | Object           | Stereotype             | Justification                                                                                 |
| -------- | ---------------- | ---------------------- | --------------------------------------------------------------------------------------------- |
| 1        | System Admin     | Actor (primary)        | The human user initiating the account-management action.                                      |
| 2        | AdminUI          | `<<user interaction>>` | Boundary object receiving admin input and displaying account-management information.           |
| 3        | AdminCoordinator | `<<coordinator>>`      | Control object sequencing the overall flow of the use case without holding long-lived state.  |
| 4        | UserAccount      | `<<entity>>`           | Conceptual data object encapsulating the selected user account and its current status.        |
| 5        | EmailProxy       | `<<proxy>>`            | Boundary object hiding the technical details of the external email system API.                |
| 6        | Email Provider   | Actor (secondary)      | The external system dispatching user-notification emails.                                     |

## Messages (Main Sequence - Active -> Suspended)

| #   | From -> To                         | Message / Information Passed                    | Use Case Step |
| --- | ---------------------------------- | ----------------------------------------------- | ------------- |
| 1   | System Admin -> AdminUI            | Account Management Access                       | Step 1        |
| 1.1 | AdminUI -> AdminCoordinator        | User Account List Request                       |               |
| 1.2 | AdminCoordinator -> UserAccount    | User Account List Query                         |               |
| 1.3 | UserAccount -> AdminCoordinator    | User Account List Data                          |               |
| 1.4 | AdminCoordinator -> AdminUI        | User Account List                               | Step 2        |
| 1.5 | AdminUI -> System Admin            | User Account List Display                       |               |
| 2   | System Admin -> AdminUI            | User Account Selection                          | Step 3        |
| 2.1 | AdminUI -> AdminCoordinator        | User Account Detail Request                     |               |
| 2.2 | AdminCoordinator -> UserAccount    | User Account Detail Query                       |               |
| 2.3 | UserAccount -> AdminCoordinator    | User Account Detail and Available Status Actions |               |
| 2.4 | AdminCoordinator -> AdminUI        | User Account Detail and Available Status Actions | Step 4        |
| 2.5 | AdminUI -> System Admin            | Detail and Available Actions Display            |               |
| 3   | System Admin -> AdminUI            | Account Status Change Decision (Suspend)        | Step 5        |
| 3.1 | AdminUI -> AdminCoordinator        | Account Status Change Request                   |               |
| 3.2 | AdminCoordinator -> UserAccount    | Status Transition Validation and Update         | Step 6        |
| 3.3 | UserAccount -> AdminCoordinator    | Account Status Change Result                    |               |
| 3.4 | AdminCoordinator -> EmailProxy     | User Notification Request                       | Step 7        |
| 3.5 | EmailProxy -> Email Provider       | User Notification                               |               |
| 3.6 | AdminCoordinator -> AdminUI        | Account Status Change Outcome                   | Step 8        |
| 3.7 | AdminUI -> System Admin            | Account Status Change Confirmation              |               |

## Alternative Sequences

| #    | From -> To                      | Message / Information Passed                        | Use Case Step |
| ---- | ------------------------------- | --------------------------------------------------- | ------------- |
| 2.3a | UserAccount -> AdminCoordinator | [No actions available] No Available Actions         | Alt Step 4.1  |
| 2.4a | AdminCoordinator -> AdminUI     | No Actions Available Error                          |               |
| 2.5a | AdminUI -> System Admin         | Error Display (Ends unsuccessfully)                 |               |
| 3.3a | UserAccount -> AdminCoordinator | [Transition not permitted] Invalid Transition Result | Alt Step 6.1 |
| 3.4a | AdminCoordinator -> AdminUI     | Invalid Transition Error                            |               |
| 3.5a | AdminUI -> System Admin         | Error Display (Ends unsuccessfully)                 |               |
| 3.5b | EmailProxy -> AdminCoordinator  | [Provider unavailable] Delivery Failure             | Alt Step 7.1  |
| 3.6b | AdminCoordinator -> AdminUI     | Account Status Change Outcome (notification failed) | Continues to 3.7 |

## Architectural Notes

- **Use-Case-First Analysis**: This analysis follows the use case description directly. The flow is modeled around account lookup, status update, and notification, without introducing extra intermediate service objects that are not required to understand the business behavior.
- **Status Management Scope**: `UserAccount` is the conceptual entity that both exposes the current status and absorbs the status transition request in the analysis model.
- **Notification Boundary**: Notification is represented as a direct boundary crossing through `EmailProxy` to the `Email Provider`. Any notification-content composition can be introduced later in design if needed.
- **Stateless Coordination**: `AdminCoordinator` explicitly requests account data when the admin needs list or detail information instead of assuming conversational state across steps.
- **Analysis vs. Design**: Message labels stay as descriptive business messages such as `Status Transition Validation and Update`, not code-level operation signatures.

Use `/drawio-communication-diagram` to generate a visual `.drawio` file from this blueprint.
