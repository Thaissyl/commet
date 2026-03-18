# Communication Diagram: UC-12 Change Listing Visibility - Analysis Model

## Object Layout

```text
Owner --- OwnerUI --- ChangeVisibilityCoordinator --- VisibilityRules --- RoomListing
```

## Participants

| Position | Object                    | Stereotype             | Justification                                                                                           |
| -------- | ------------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------- |
| 1        | Owner                     | Actor (primary)        | The human actor initiating the use case.                                                                |
| 2        | OwnerUI                   | `<<user interaction>>` | Boundary object receiving physical inputs and displaying information.                                   |
| 3        | ChangeVisibilityCoordinator | `<<coordinator>>`      | Control object sequencing the overall flow of the use case.                                             |
| 4        | VisibilityRules           | `<<business logic>>`   | Encapsulates the business rules for validating status changes (e.g., Published → Hidden is valid, Hidden → Archive is valid, but Archive → Published is not). |
| 5        | RoomListing               | `<<entity>>`           | Conceptual data object encapsulating the room listing record.                                            |

## Messages (Main Sequence)

| #   | From -> To                                     | Message / Information Passed    | Use Case Step |
| --- | ---------------------------------------------- | ------------------------------- | ------------- |
| 1   | Owner -> OwnerUI                               | Listing Selection               | Step 1        |
| 1.1 | OwnerUI -> ChangeVisibilityCoordinator         | Listing Detail Request          |               |
| 1.2 | ChangeVisibilityCoordinator -> RoomListing     | Listing Detail Query            |               |
| 1.3 | RoomListing -> ChangeVisibilityCoordinator     | Listing Data                    |               |
| 1.4 | ChangeVisibilityCoordinator -> OwnerUI         | Listing Data and Visibility Actions | Step 2        |
| 1.5 | OwnerUI -> Owner                               | Listing Details and Actions Display |             |
| 2   | Owner -> OwnerUI                               | Visibility Action Selection     | Step 3        |
| 2.1 | OwnerUI -> ChangeVisibilityCoordinator         | Visibility Action Request       |               |
| 2.2 | ChangeVisibilityCoordinator -> VisibilityRules | Action Validity Check           | Step 4        |
| 2.3 | VisibilityRules -> ChangeVisibilityCoordinator | Validity Result (Valid)         |               |
| 2.4 | ChangeVisibilityCoordinator -> OwnerUI         | Visibility Confirmation Prompt  |               |
| 2.5 | OwnerUI -> Owner                               | Confirmation Prompt Display     |               |
| 3   | Owner -> OwnerUI                               | Visibility Change Confirmation  | Step 5        |
| 3.1 | OwnerUI -> ChangeVisibilityCoordinator         | Confirmed Visibility Change     |               |
| 3.2 | ChangeVisibilityCoordinator -> RoomListing     | Visibility Status Update        | Step 6        |
| 3.3 | ChangeVisibilityCoordinator -> OwnerUI         | Visibility Change Success       | Step 7        |
| 3.4 | OwnerUI -> Owner                               | Visibility Success Message       |               |

## Alternative Sequences

| #    | From -> To                                     | Message / Information Passed          | Use Case Step        |
| ---- | ---------------------------------------------- | ------------------------------------ | -------------------- |
| 2.3a | VisibilityRules -> ChangeVisibilityCoordinator | [Invalid action] Validity Result (Invalid) | Alt Step 4.1       |
| 2.4a | ChangeVisibilityCoordinator -> OwnerUI         | Invalid Action Error Prompt          |                      |
| 2.5a | OwnerUI -> Owner                               | Error Display                        | Ends unsuccessfully  |

## Architectural Notes

- **Reactive System Design (Option B)**: The UI displays a "standard menu of visibility actions" rather than filtering to only valid options. This allows users to select invalid actions, which the backend then validates and rejects in `VisibilityRules`. This approach is simpler and more maintainable than trying to keep UI filters perfectly synchronized with complex business rules.
- **Analysis vs. Design**: In this analysis model, messages use descriptive noun phrases (e.g., `Visibility Status Update`) rather than operation signatures (e.g., `changeVisibility(in, out)`).
- **State Transition Validation**: `VisibilityRules` encapsulates the state machine logic (e.g., Published → Hidden ✓, Hidden → Archive ✓, Archived → Published ✗). This ensures only valid state transitions are permitted.
- **Explicit Returns**: The analysis model shows explicit data flow (e.g., `Listing Data` in Message 1.3, `Validity Result (Valid)` in Message 2.3). In the design phase, these will be embedded into `out` parameters of synchronous calls.

Use `/drawio-communication-diagram` to generate a visual `.drawio` file from this blueprint.
