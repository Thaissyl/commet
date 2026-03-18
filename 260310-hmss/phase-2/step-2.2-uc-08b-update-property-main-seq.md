# Communication Diagram: UC-08b Update Property - Analysis Model

## Object Layout

```text
Owner --- OwnerUI --- UpdatePropertyCoordinator --- PropertyRules --- Property
```

## Participants

| Position | Object                   | Stereotype             | Justification                                                                                             |
| -------- | ------------------------ | ---------------------- | --------------------------------------------------------------------------------------------------------- |
| 1        | Owner                    | Actor (primary)        | The human actor initiating the use case.                                                                  |
| 2        | OwnerUI                  | `<<user interaction>>` | Boundary object receiving physical inputs and displaying information.                                     |
| 3        | UpdatePropertyCoordinator | `<<coordinator>>`      | Control object sequencing the overall flow of the use case.                                               |
| 4        | PropertyRules            | `<<business logic>>`   | Encapsulates the specific business rules for validating property updates.                                  |
| 5        | Property                 | `<<entity>>`           | Long-lived conceptual data object encapsulating the property records.                                      |

## Messages (Main Sequence)

| #   | From -> To                               | Message / Information Passed    | Use Case Step |
| --- | ---------------------------------------- | ------------------------------- | ------------- |
| 1   | Owner -> OwnerUI                         | Property Management Access      | Step 1        |
| 1.1 | OwnerUI -> UpdatePropertyCoordinator     | Owner Properties Request        |               |
| 1.2 | UpdatePropertyCoordinator -> Property    | Owner Properties Query          |               |
| 1.3 | Property -> UpdatePropertyCoordinator    | Owner Properties Data           |               |
| 1.4 | UpdatePropertyCoordinator -> OwnerUI     | Owner Properties List           | Step 2        |
| 1.5 | OwnerUI -> Owner                         | Properties Display              |               |
| 2   | Owner -> OwnerUI                         | Property Selection              | Step 3        |
| 2.1 | OwnerUI -> UpdatePropertyCoordinator     | Property Detail Request         |               |
| 2.2 | UpdatePropertyCoordinator -> Property    | Property Detail Query           |               |
| 2.3 | Property -> UpdatePropertyCoordinator    | Property Detail Data            |               |
| 2.4 | UpdatePropertyCoordinator -> OwnerUI     | Editable Property Form          | Step 4        |
| 2.5 | OwnerUI -> Owner                         | Editable Property Form Display  |               |
| 3   | Owner -> OwnerUI                         | Property Information Edit       | Step 5        |
| 3.1 | OwnerUI -> Owner                         | Property Review Display         |               |
| 4   | Owner -> OwnerUI                         | Update Confirmation             | Step 7        |
| 4.1 | OwnerUI -> UpdatePropertyCoordinator     | Property Update Request         |               |
| 4.2 | UpdatePropertyCoordinator -> PropertyRules | Required Fields Validation Check | Step 6        |
| 4.3 | PropertyRules -> UpdatePropertyCoordinator | Validation Result (Valid)       |               |
| 4.4 | UpdatePropertyCoordinator -> Property    | Property Update Record          | Step 8        |
| 4.5 | UpdatePropertyCoordinator -> OwnerUI     | Update Success                  | Step 9        |
| 4.6 | OwnerUI -> Owner                         | Update Success Message          |               |

## Alternative Sequences

| #    | From -> To                               | Message / Information Passed      | Use Case Step       |
| ---- | ---------------------------------------- | --------------------------------- | ------------------- |
| 4.3a | PropertyRules -> UpdatePropertyCoordinator | [Invalid fields] Validation Result (Invalid) | Alt Step 6.1 |
| 4.4a | UpdatePropertyCoordinator -> OwnerUI     | Correction Prompt                 |                     |
| 4.5a | OwnerUI -> Owner                         | Correction Display                | Returns to Step 5   |

## Architectural Notes

- **Analysis vs. Design**: In this analysis model, messages use descriptive noun phrases (e.g., `Property Update Record`) rather than operation signatures (e.g., `updateProperty(in, out)`). The focus is on what the system does, not how it's programmed.
- **Separation of Concerns**: The `UpdatePropertyCoordinator` delegates validation to `PropertyRules` (`<<business logic>>`), which encapsulates the business rules for validating required fields. This separation will be preserved in the design phase.
- **Explicit Returns**: The analysis model shows explicit data flow (e.g., `Owner Properties Data` in Message 1.3, `Property Detail Data` in Message 2.3). In the design phase, these will be embedded into `out` parameters of synchronous calls.
- **Stateless Coordinator**: `UpdatePropertyCoordinator` is a stateless control object that sequences the flow. It does not contain business logic itself.

Use `/drawio-communication-diagram` to generate a visual `.drawio` file from this blueprint.
