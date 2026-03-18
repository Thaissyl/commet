# Design Communication Diagram: UC-08b Update Property - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: `OwnerUI -> UpdatePropertyController`, then `Controller -> Repository`, `Controller -> PropertyLogic`, and `Controller -> Property`
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label when a response payload is expected
- Separate reply arrows are intentionally omitted because `out` parameters already represent returned data
- Request flow style: synchronous request handling

## Object Layout

```text
Owner --- OwnerUI --- UpdatePropertyController
                       |--- IPropertyRepository --- Property / PropertyList
                       |--- PropertyLogic
```

## Participants

| Position | Object                    | Stereotype             |
| -------- | ------------------------- | ---------------------- |
| 1        | Owner                     | Actor (primary)        |
| 2        | OwnerUI                   | `<<user interaction>>` |
| 3        | UpdatePropertyController  | `<<coordinator>>`      |
| 4        | IPropertyRepository       | `<<database wrapper>>` |
| 5        | Property / PropertyList   | `<<data abstraction>>` |
| 6        | PropertyLogic             | `<<business logic>>`   |

## Messages

| #   | From -> To                              | Message                                                            |
| --- | --------------------------------------- | ------------------------------------------------------------------ |
| 1   | Owner -> OwnerUI                        | Property Management Access                                         |
| 1.1 | OwnerUI -> UpdatePropertyController     | `getOwnerProperties(in ownerId: Guid, out response: PropertyListResponseDto)` |
| 1.2 | UpdatePropertyController -> IPropertyRepository | `findByOwnerId(in ownerId: Guid, out list: PropertyList)`        |
| 1.3 | OwnerUI -> Owner                        | Properties Display                                                 |
| 2   | Owner -> OwnerUI                        | Property Selection                                                 |
| 2.1 | OwnerUI -> UpdatePropertyController     | `getPropertyForUpdate(in propertyId: Guid, out response: PropertyFormResponseDto)` |
| 2.2 | UpdatePropertyController -> IPropertyRepository | `findById(in id: Guid, out entity: Property)`                     |
| 2.3 | OwnerUI -> Owner                        | Editable Property Form Display                                     |
| 3   | Owner -> OwnerUI                        | Property Information Edit                                          |
| 3.1 | OwnerUI -> Owner                        | Property Review Display                                            |
| 4   | Owner -> OwnerUI                        | Update Confirmation                                                |
| 4.1 | OwnerUI -> UpdatePropertyController     | `updateProperty(in request: PropertyUpdateDto, out response: PropertyResponseDto)` |
| 4.2 | UpdatePropertyController -> IPropertyRepository | `findById(in id: Guid, out entity: Property)`                     |
| 4.3 | UpdatePropertyController -> PropertyLogic | `validateUpdate(in entity: Property, in request: PropertyUpdateDto, out result: ValidationResult)` |
| 4.4 | UpdatePropertyController -> Property    | `applyUpdates(in request: PropertyUpdateDto, out result: StatusChangeResult)` |
| 4.5 | UpdatePropertyController -> IPropertyRepository | `update(in entity: Property, out persisted: Property)`            |
| 4.6 | OwnerUI -> Owner                        | Update Success Message                                             |

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
| ----------------- | -------------- | ----- |
| `1.1` OwnerUI -> UpdatePropertyCoordinator: "Owner Properties Request" | `1.1` OwnerUI -> UpdatePropertyController: `getOwnerProperties(in ownerId: Guid, out response: PropertyListResponseDto)` | sync, renamed to code-style |
| `1.2` UpdatePropertyCoordinator -> Property: "Owner Properties Query" | `1.2` UpdatePropertyController -> IPropertyRepository: `findByOwnerId(in ownerId: Guid, out list: PropertyList)` | direct repository read |
| `1.3` Property -> UpdatePropertyCoordinator: "Owner Properties Data" | embedded in `1.2` out parameter | reply via `out list` |
| `1.4` UpdatePropertyCoordinator -> OwnerUI: "Owner Properties List" | implicit in `1.1` response | display data returned |
| `2.1` OwnerUI -> UpdatePropertyCoordinator: "Property Detail Request" | `2.1` OwnerUI -> UpdatePropertyController: `getPropertyForUpdate(in propertyId: Guid, out response: PropertyFormResponseDto)` | sync, renamed |
| `2.2` UpdatePropertyCoordinator -> Property: "Property Detail Query" | `2.2` UpdatePropertyController -> IPropertyRepository: `findById(in id: Guid, out entity: Property)` | stateless controller fetch |
| `2.3` Property -> UpdatePropertyCoordinator: "Property Detail Data" | embedded in `2.2` out parameter | reply via `out entity` |
| `2.4` UpdatePropertyCoordinator -> OwnerUI: "Editable Property Form" | implicit in `2.1` response | form data returned |
| `4.1` OwnerUI -> UpdatePropertyCoordinator: "Property Update Request" | `4.1` OwnerUI -> UpdatePropertyController: `updateProperty(in request: PropertyUpdateDto, out response: PropertyResponseDto)` | sync, renamed |
| `4.2` UpdatePropertyCoordinator -> PropertyRules: "Required Fields Validation Check" | `4.3` UpdatePropertyController -> PropertyLogic: `validateUpdate(in entity: Property, in request: PropertyUpdateDto, out result: ValidationResult)` | sync, business logic handles validation |
| `4.4` UpdatePropertyCoordinator -> Property: "Property Update Record" | `4.4` UpdatePropertyController -> Property: `applyUpdates(in request: PropertyUpdateDto, out result: StatusChangeResult)` | RAM-only state mutation |
| `4.5` UpdatePropertyCoordinator -> OwnerUI: "Update Success" | `4.6` OwnerUI -> Owner | success confirmation |

## Alternative Flow Notes

- **Step 4.3: Validation fails** - `ValidationResult.isValid = false`, response contains field error details, messages 4.4 and 4.5 are skipped, use case ends without updating
- **Step 4.2: Property not found** - Repository returns null/error, response contains not found error, use case ends
- **Step 4.5: Database error on update** - Repository throws exception, response contains error, use case ends

## Notes

- `OwnerUI` is shown explicitly so the human actor does not interact directly with the backend controller.
- `IPropertyRepository` handles persistence with SQL operations and returns domain entities.
- `UpdatePropertyController` acts as the simplified orchestration point for this use case.
- `PropertyLogic` encapsulates the property field validation business rules: required fields (name, address), format validation (address structure, map location), and policy constraints.
- **Stateless Coordinator (Message 4.2)**: Because the controller must be stateless, it does not retain the `Property` object from Sequence 2 when the Owner submits the update in Sequence 4. It issues a fresh `findById()` call to fetch the latest state from the database before applying updates.
- **Separation of State Mutation and Persistence (Messages 4.4 & 4.5)**:
  - Message 4.4: `applyUpdates()` on `Property` (`<<data abstraction>>`) mutates the internal state in RAM securely. The domain object handles its own state mutation.
  - Message 4.5: `update()` on `IPropertyRepository` (`<<database wrapper>>`) executes the SQL UPDATE statement to persist the mutated state, satisfying the ACID Durability requirement.
- **Implicit DTO mapping**: The controller implicitly maps data from `PropertyUpdateDto` to the `Property` entity attributes. This mapping is not shown as a separate message.
- **Two-query pattern**: Message 1.2 retrieves the owner's property list via `findByOwnerId()`. Message 2.2 retrieves details for the selected property via `findById()`. These are separate operations because the user first views the list, then selects a specific property to edit.
- Actor-to-UI messages (1, 1.3, 2, 2.3, 3, 3.1, 4, 4.6) use noun phrases because they represent physical user interactions, not code method calls.
- No external actors or proxies are involved in this use case.
