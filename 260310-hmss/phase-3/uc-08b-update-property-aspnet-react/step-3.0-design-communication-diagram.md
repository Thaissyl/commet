# Design Communication Diagram: UC-08b Update Property - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: OwnerUI -> PropertyController, then Controller -> Repository, Controller -> PropertyLogic, and Controller -> Property entity
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label
- Separate reply arrows intentionally omitted — `out` parameters represent returned data
- Request flow style: synchronous request handling

## Object Layout

```text
Owner --- OwnerUI --- PropertyController
                       |--- IPropertyRepository
                       |--- PropertyLogic
                       |--- Property
```

## Participants

| Position | Object                  | Stereotype             |
| -------- | ----------------------- | ---------------------- |
| 1        | Owner                   | Actor (primary)        |
| 2        | OwnerUI                 | `<<user interaction>>` |
| 3        | PropertyController      | `<<coordinator>>`      |
| 4        | IPropertyRepository     | `<<database wrapper>>` |
| 5        | PropertyLogic           | `<<business logic>>`   |
| 6        | Property                | `<<entity>>`           |

## Messages

| #   | From -> To                              | Message                                                            |
| --- | --------------------------------------- | ------------------------------------------------------------------ |
| 1   | Owner -> OwnerUI                        | Property Management Access                                         |
| 1.1 | OwnerUI -> PropertyController           | `GetOwnerProperties(out response: PropertyListResponseDto)` |
| 1.2 | PropertyController -> IPropertyRepository | `FindByOwnerIdAsync(in ownerId: Guid, out list: List<Property>)` |
| 1.3 | OwnerUI -> Owner                        | Properties Display                                                 |
| 2   | Owner -> OwnerUI                        | Property Selection                                                 |
| 2.1 | OwnerUI -> PropertyController           | `GetPropertyForUpdate(in propertyId: Guid, out response: PropertyFormResponseDto)` |
| 2.2 | PropertyController -> IPropertyRepository | `FindByIdAsync(in id: Guid, out entity: Property)` |
| 2.3 | OwnerUI -> Owner                        | Editable Property Form Display                                     |
| 3   | Owner -> OwnerUI                        | Property Information Edit                                          |
| 3.1 | OwnerUI -> Owner                        | Property Review Display                                            |
| 4   | Owner -> OwnerUI                        | Update Confirmation                                                |
| 4.1 | OwnerUI -> PropertyController           | `UpdateProperty(in request: PropertyUpdateDto, out response: PropertyResponseDto)` |
| 4.2 | PropertyController -> IPropertyRepository | `FindByIdAsync(in id: Guid, out entity: Property)` |
| 4.3 | PropertyController -> PropertyLogic     | `ValidateUpdate(in entity: Property, in request: PropertyUpdateDto, out result: ValidationResult)` |
| 4.4 | PropertyController -> Property          | `ApplyUpdates(in request: PropertyUpdateDto, out result: StatusChangeResult)` |
| 4.5 | PropertyController -> IPropertyRepository | `UpdateAsync(in entity: Property, out persisted: Property)` |
| 4.6 | OwnerUI -> Owner                        | Update Success Message                                             |

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
|---|---|---|
| `1.1` OwnerUI -> UpdatePropertyCoordinator: "Property List Request" | `1.1` OwnerUI -> PropertyController: `GetOwnerProperties(...)` | renamed |
| `1.2` UpdatePropertyCoordinator -> IPropertyRepository: "Owner Properties Query" | `1.2` PropertyController -> IPropertyRepository: `FindByOwnerIdAsync(...)` | direct repo call |
| `2.1` OwnerUI -> UpdatePropertyCoordinator: "Property Detail Request" | `2.1` OwnerUI -> PropertyController: `GetPropertyForUpdate(...)` | renamed |
| `2.2` UpdatePropertyCoordinator -> IPropertyRepository: "Property Detail Query" | `2.2` PropertyController -> IPropertyRepository: `FindByIdAsync(...)` | direct repo call |
| `4.1-4.3` OwnerUI -> UpdatePropertyCoordinator -> PropertyLogic: "Update Property" | `4.3` PropertyController -> PropertyLogic: `ValidateUpdate(...)` | validation |
| `4.4-4.5` UpdatePropertyCoordinator -> Property -> IPropertyRepository: "Apply and Persist" | `4.4-4.5` PropertyController -> Property: `ApplyUpdates(...)` + IPropertyRepository: `UpdateAsync(...)` | entity method then persist |

## Alternative Flow Notes

- **Step 4.3: Validation fails** — `ValidationResult.IsValid = false`, response includes errors, property not updated
- **Step 4.4: ApplyUpdates fails** — `StatusChangeResult.Success = false`, response contains error, property not persisted
- **Step 4.5: Update fails** — Repository exception handled, response contains error

## Notes

- `OwnerUI` shown explicitly — human actor does not interact directly with backend controller.
- `PropertyController` acts as stateless orchestration point. Sequence 2 re-queries property by ID independently; no state held from sequence 1.
- **TenantId from JWT**: `GetOwnerProperties` doesn't take `ownerId` parameter — comes from `ClaimsHelper.GetUserId(User)`.
- `PropertyLogic` encapsulates `ValidateUpdate` — validates property update rules before persistence.
- `Property.ApplyUpdates()` called directly on entity — encapsulates business logic for status updates.
- `IPropertyRepository` queries and persists `Property` entity.
- **Implicit DTO mapping**: Controller implicitly maps entity to response DTO. Not shown as separate message.
- Actor-to-UI messages (1, 1.3, 2, 2.3, 3, 3.1, 4, 4.6) use noun phrases — physical user interactions, not code method calls.
