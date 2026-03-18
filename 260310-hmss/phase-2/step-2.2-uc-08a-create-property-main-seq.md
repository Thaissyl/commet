# Communication Diagram: UC-08a Create Property - Analysis Model

## Object Layout

```text
Owner --- OwnerUI --- CreatePropertyCoordinator --- PropertyRules --- Property
```

## Participants

| Position | Object                   | Stereotype             | Justification                                                                                             |
| -------- | ------------------------ | ---------------------- | --------------------------------------------------------------------------------------------------------- |
| 1        | Owner                    | Actor (primary)        | The human actor initiating the use case.                                                                  |
| 2        | OwnerUI                  | `<<user interaction>>` | Boundary object receiving physical inputs and displaying information.                                     |
| 3        | CreatePropertyCoordinator | `<<coordinator>>`      | Control object sequencing the overall flow of the use case.                                               |
| 4        | PropertyRules            | `<<business logic>>`   | Encapsulates the specific business rules for validating the property fields.                              |
| 5        | Property                 | `<<entity>>`           | Long-lived conceptual data object encapsulating the new property record.                                  |

## Messages (Main Sequence)

| #   | From -> To                               | Message / Information Passed    | Use Case Step |
| --- | ---------------------------------------- | ------------------------------- | ------------- |
| 1   | Owner -> OwnerUI                         | Property Creation Access        | Step 1        |
| 1.1 | OwnerUI -> CreatePropertyCoordinator     | Property Form Request           |               |
| 1.2 | CreatePropertyCoordinator -> OwnerUI     | Property Creation Form          |               |
| 1.3 | OwnerUI -> Owner                         | Property Form Display           | Step 2        |
| 2   | Owner -> OwnerUI                         | Property Information Input      | Step 3        |
| 2.1 | OwnerUI -> Owner                         | Property Review Display         |               |
| 3   | Owner -> OwnerUI                         | Creation Confirmation           | Step 5        |
| 3.1 | OwnerUI -> CreatePropertyCoordinator     | Property Creation Request       |               |
| 3.2 | CreatePropertyCoordinator -> PropertyRules | Required Fields Validation Check | Step 4        |
| 3.3 | PropertyRules -> CreatePropertyCoordinator | Validation Result (Valid)       |               |
| 3.4 | CreatePropertyCoordinator -> Property    | New Property Record             | Step 6        |
| 3.5 | CreatePropertyCoordinator -> OwnerUI     | Creation Success                | Step 7        |
| 3.6 | OwnerUI -> Owner                         | Property Creation Success Message |             |

## Alternative Sequences

| #    | From -> To                               | Message / Information Passed      | Use Case Step       |
| ---- | ---------------------------------------- | --------------------------------- | ------------------- |
| 3.3a | PropertyRules -> CreatePropertyCoordinator | [Invalid fields] Validation Result (Invalid) | Alt Step 4.1 |
| 3.4a | CreatePropertyCoordinator -> OwnerUI     | Correction Prompt                 |                     |
| 3.5a | OwnerUI -> Owner                         | Correction Display                | Returns to Step 3   |

## Architectural Notes

- **Analysis vs. Design**: In this analysis model, messages use descriptive noun phrases (e.g., `New Property Record`) rather than operation signatures (e.g., `createProperty(in, out)`). The focus is on what the system does, not how it's programmed.
- **Separation of Concerns**: The `CreatePropertyCoordinator` delegates validation to `PropertyRules` (`<<business logic>>`), which encapsulates the business rules for validating required fields. This separation will be preserved in the design phase.
- **Explicit Returns**: The analysis model shows explicit data flow (e.g., `Validation Result (Valid)` in Message 3.3). In the design phase, these will be embedded into `out` parameters of synchronous calls.
- **Stateless Coordinator**: `CreatePropertyCoordinator` is a stateless control object that sequences the flow. It does not contain business logic itself.

Use `/drawio-communication-diagram` to generate a visual `.drawio` file from this blueprint.
