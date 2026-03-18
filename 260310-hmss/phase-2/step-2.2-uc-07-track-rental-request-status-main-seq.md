# Communication Diagram: UC-07 Track Rental Request Status - Analysis Model

## Object Layout

```text
Tenant --- RentalRequestStatusUI --- RentalRequestCoordinator --- RentalRequestStatusRules --- RentalRequest
```

## Participants

| Position | Object                   | Stereotype             | Justification                                                                                               |
| -------- | ------------------------ | ---------------------- | ----------------------------------------------------------------------------------------------------------- |
| 1        | Tenant                   | Actor (primary)        | The human actor initiating the use case to check their request status.                                      |
| 2        | RentalRequestStatusUI    | `<<user interaction>>` | Boundary object receiving physical inputs and displaying the lists/details.                                  |
| 3        | RentalRequestCoordinator | `<<coordinator>>`      | Control object that sequences the overall flow of the status tracking use case.                             |
| 4        | RentalRequestStatusRules | `<<business logic>>`   | Encapsulates the conceptual rules for determining which actions are available based on the current status.  |
| 5        | RentalRequest            | `<<entity>>`           | Long-lived data object encapsulating the rental request data and its current status.                        |

## Messages (Main Sequence)

| #   | From -> To                                      | Message / Information Passed           | Use Case Step |
| --- | ----------------------------------------------- | -------------------------------------- | ------------- |
| 1   | Tenant -> RentalRequestStatusUI                 | Rental Request Status Access           | Step 1        |
| 1.1 | RentalRequestStatusUI -> RentalRequestCoordinator | Rental Request Status Request         |               |
| 1.2 | RentalRequestCoordinator -> RentalRequestStatusRules | Rental Request Status Request         |               |
| 1.3 | RentalRequestStatusRules -> RentalRequest       | Rental Request Status List Request     |               |
| 1.4 | RentalRequest -> RentalRequestStatusRules       | Rental Request Status List             |               |
| 1.5 | RentalRequestStatusRules -> RentalRequestCoordinator | Rental Request Status List           |               |
| 1.6 | RentalRequestCoordinator -> RentalRequestStatusUI | Rental Request Status List            | Step 2        |
| 1.7 | RentalRequestStatusUI -> Tenant                 | Request List and Statuses Display      |               |
| 2   | Tenant -> RentalRequestStatusUI                 | Status Detail Selection                | Step 3        |
| 2.1 | RentalRequestStatusUI -> RentalRequestCoordinator | Status Detail Request                  |               |
| 2.2 | RentalRequestCoordinator -> RentalRequestStatusRules | Status Detail Request                 |               |
| 2.3 | RentalRequestStatusRules -> RentalRequest       | Status Detail Request                  |               |
| 2.4 | RentalRequest -> RentalRequestStatusRules       | Status Detail                          | Step 4        |
| 2.5 | RentalRequestStatusRules -> RentalRequestCoordinator | Status Detail and Available Actions   |               |
| 2.6 | RentalRequestCoordinator -> RentalRequestStatusUI | Status Detail and Available Actions    |               |
| 2.7 | RentalRequestStatusUI -> Tenant                 | Full Status Details Display            |               |
| 3   | Tenant -> RentalRequestStatusUI                 | Status Detail Review                   | Step 5        |

## Alternative Sequences

| #    | From -> To                                    | Message / Information Passed      | Use Case Step    |
| ---- | --------------------------------------------- | --------------------------------- | ---------------- |
| 1.4a | RentalRequest -> RentalRequestStatusRules     | [No submitted requests] Empty Status List | Alt Step 2.1     |
| 1.5a | RentalRequestStatusRules -> RentalRequestCoordinator | Empty Status List            |                  |
| 1.6a | RentalRequestCoordinator -> RentalRequestStatusUI | No Request History Message     |                  |
| 1.7a | RentalRequestStatusUI -> Tenant               | No Request History Display       | Ends             |

## Architectural Notes

- **Alignment with Mapping Table**: This message flow directly matches the Analysis message column. Messages 1.1 through 1.6 map to the list sequence, and 2.1 through 2.6 map to the detailed selection sequence.
- **Explicit Returns**: In this analysis model, we use explicit return arrows (Messages 1.4, 1.5, 1.6 and 2.4, 2.5, 2.6) to show data flowing back up to the UI. When transitioning to the Design Communication Diagram, these independent return arrows will be eliminated and seamlessly embedded into the `out` parameters of synchronous operation calls (e.g., `out response: TenantRequestListResponseDto`).
- **The Role of the Business Logic Object**: In this conceptual phase, `RentalRequestStatusRules` receives the `Status Detail` (Message 2.4) and translates it into `Status Detail and Available Actions` (Message 2.5). Conceptually, this shows that there are business rules dictating what a tenant can do (e.g., if status is "Pending", show "Cancel" button; if "Accepted", hide "Cancel" button).
- **Preparing for Design Optimization**: During the transition to the Design Phase, the `RentalRequestStatusRules` object can be optimized out (bypassed). The `<<coordinator>>` will directly query the `<<database wrapper>>` (`IRentalRequestRepository`) and handle the simple status-to-action derivation itself or via DTO mapping. This demonstrates the difference between Analysis (focusing on strict conceptual responsibilities) and Design (focusing on software efficiency and reducing unnecessary pass-through classes).

Use `/drawio-communication-diagram` to generate a visual `.drawio` file from this blueprint.
