# Design Communication Diagram: UC-08a Create Property - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: `OwnerUI -> CreatePropertyController`, then `Controller -> Service` and `Controller -> Repository`
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label when a response payload is expected
- Separate reply arrows are intentionally omitted because `out` parameters already represent returned data
- Request flow style: synchronous request handling

## Object Layout

```text
Owner --- OwnerUI --- CreatePropertyController
                       |--- PropertyService
                       |--- IPropertyRepository --- Property
```

## Participants

| Position | Object                  | Stereotype             |
| -------- | ----------------------- | ---------------------- |
| 1        | Owner                   | Actor (primary)        |
| 2        | OwnerUI                 | `<<user interaction>>` |
| 3        | CreatePropertyController | `<<coordinator>>`      |
| 4        | PropertyService         | `<<service>>`          |
| 5        | IPropertyRepository     | `<<database wrapper>>` |
| 6        | Property                | `<<data abstraction>>` |

## Messages

| #   | From -> To                             | Message                                                           |
| --- | -------------------------------------- | ----------------------------------------------------------------- |
| 1   | Owner -> OwnerUI                       | Property Creation Access                                           |
| 1.1 | OwnerUI -> CreatePropertyController    | `getCreatePropertyForm(out response: PropertyFormResponseDto)`     |
| 2   | Owner -> OwnerUI                       | Property Information Input                                          |
| 2.1 | OwnerUI -> Owner                       | Property Review Display                                            |
| 3   | Owner -> OwnerUI                       | Creation Confirmation                                              |
| 3.1 | OwnerUI -> CreatePropertyController    | `createProperty(in request: PropertyDto, out response: PropertyResponseDto)` |
| 3.2 | CreatePropertyController -> PropertyService | `validatePropertyFields(in request: PropertyDto, out result: ValidationResult)` |
| 3.3 | CreatePropertyController -> IPropertyRepository | `save(in entity: Property, out persisted: Property)`         |
| 3.4 | OwnerUI -> Owner                       | Property Creation Success Message                                   |

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
| ----------------- | -------------- | ----- |
| `1.1` OwnerUI -> CreatePropertyCoordinator: "Property Form Request" | `1.1` OwnerUI -> CreatePropertyController: `getCreatePropertyForm(out response: PropertyFormResponseDto)` | sync, renamed to code-style |
| `3.1` OwnerUI -> CreatePropertyCoordinator: "Property Creation Request" | `3.1` OwnerUI -> CreatePropertyController: `createProperty(in request: PropertyDto, out response: PropertyResponseDto)` | sync, renamed |
| `3.2` CreatePropertyCoordinator -> PropertyRules: "Required Fields Validation Check" | `3.2` CreatePropertyController -> PropertyService: `validatePropertyFields(in request: PropertyDto, out result: ValidationResult)` | sync, service handles validation |
| `3.4` CreatePropertyCoordinator -> Property: "New Property Record" | `3.3` CreatePropertyController -> IPropertyRepository: `save(in entity: Property, out persisted: Property)` | sync, DTO mapping implicit before save |

## Alternative Flow Notes

- **Step 3.2: Validation fails** - `ValidationResult.isValid = false`, response contains field error details, use case ends without saving
- **Step 3.3: Database error on save** - Repository throws exception, response contains error, use case ends

## Notes

- `OwnerUI` is shown explicitly so the human actor does not interact directly with the backend controller.
- `IPropertyRepository` handles persistence and returns the created `Property` entity with database-generated values.
- `CreatePropertyController` acts as the simplified orchestration point for this use case.
- `PropertyService` encapsulates the property field validation business rules: required fields (name, address), format validation (address structure, map location), and policy constraints.
- **Implicit DTO mapping**: At message 3.3, the controller implicitly maps data from `PropertyDto` to the `Property` entity before calling `save()`. This mapping is not shown as a separate message to keep the design clean.
- **Owner association**: The `ownerId` field is implicitly set from the authenticated owner's context during DTO mapping before persistence.
- **Initial property state**: Newly created properties have no listings and are ready for listing creation in subsequent use cases.
- Actor-to-UI messages (1, 2, 2.1, 3, 3.4) use noun phrases because they represent physical user interactions, not code method calls.
- No external actors or proxies are involved in this use case.
