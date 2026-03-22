# Design Communication Diagram: UC-08a Create Property - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: OwnerUI -> PropertyController, then Controller -> Service and Controller -> Repository
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label
- Separate reply arrows intentionally omitted — `out` parameters represent returned data
- Request flow style: synchronous request handling

## Object Layout

```text
Owner --- OwnerUI --- PropertyController
                       |--- PropertyService
                       |--- IPropertyRepository
```

## Participants

| Position | Object                  | Stereotype             |
| -------- | ----------------------- | ---------------------- |
| 1        | Owner                   | Actor (primary)        |
| 2        | OwnerUI                 | `<<user interaction>>` |
| 3        | PropertyController      | `<<coordinator>>`      |
| 4        | PropertyService         | `<<business logic>>`   |
| 5        | IPropertyRepository     | `<<database wrapper>>` |

## Messages

| #   | From -> To                             | Message                                                           |
| --- | -------------------------------------- | ----------------------------------------------------------------- |
| 1   | Owner -> OwnerUI                       | Property Creation Access                                           |
| 1.1 | OwnerUI -> PropertyController          | `GetCreatePropertyForm(out response: PropertyFormResponseDto)` |
| 2   | Owner -> OwnerUI                       | Property Information Input                                          |
| 2.1 | OwnerUI -> Owner                       | Property Review Display                                            |
| 3   | Owner -> OwnerUI                       | Creation Confirmation                                              |
| 3.1 | OwnerUI -> PropertyController          | `CreateProperty(in request: PropertyDto, out response: PropertyResponseDto)` |
| 3.2 | PropertyController -> PropertyService  | `ValidatePropertyFields(in request: PropertyDto, out result: ValidationResult)` |
| 3.3 | PropertyController -> IPropertyRepository | `SaveAsync(in entity: Property, out persisted: Property)` |
| 3.4 | OwnerUI -> Owner                       | Property Creation Success Message                                   |

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
|---|---|---|
| `1.1` OwnerUI -> CreatePropertyCoordinator: "Property Form Request" | `1.1` OwnerUI -> PropertyController: `GetCreatePropertyForm(...)` | renamed |
| `3.1-3.2` OwnerUI -> CreatePropertyCoordinator -> PropertyService: "Create Property" | `3.2` PropertyController -> PropertyService: `ValidatePropertyFields(...)` | validation |
| `3.3` CreatePropertyCoordinator -> IPropertyRepository: "Save Property" | `3.3` PropertyController -> IPropertyRepository: `SaveAsync(...)` | persist |

## Alternative Flow Notes

- **Step 3.2: Validation fails** — `ValidationResult.IsValid = false`, response includes errors, property not saved
- **Step 3.3: Save fails** — Repository exception handled, response contains error

## Notes

- `OwnerUI` shown explicitly — human actor does not interact directly with backend controller.
- `PropertyController` acts as stateless orchestration point.
- `PropertyService` encapsulates `ValidatePropertyFields` validation logic.
- `IPropertyRepository` persists `Property` entity.
- **Implicit DTO mapping**: Controller implicitly maps entity to response DTO. Not shown as separate message.
- Actor-to-UI messages (1, 2.1, 3, 3.4) use noun phrases — physical user interactions, not code method calls.
