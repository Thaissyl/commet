# Design Class Diagram Blueprint: UC-08b Update Property - ASP.NET Simple Layered Backend

## Scope

- Included classes: `OwnerUI`, `UpdatePropertyController`, `IPropertyRepository`, `Property`, `PropertyLogic`
- Synchronization source:
  - participant set and call structure from `step-3.0-design-communication-diagram.md`
  - class operations derived from step-3.0 messages

## Class Boxes

### `OwnerUI`

- Stereotype: `<<user interaction>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ openPropertyManagement()`
  - `+ selectProperty(in propertyId: Guid)`
  - `+ submitUpdate(in request: PropertyUpdateDto)`

### `UpdatePropertyController`

- Stereotype: `<<coordinator>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getOwnerProperties(in ownerId: Guid, out response: PropertyListResponseDto)`
  - `+ getPropertyForUpdate(in propertyId: Guid, out response: PropertyFormResponseDto)`
  - `+ updateProperty(in request: PropertyUpdateDto, out response: PropertyResponseDto)`

### `IPropertyRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ findByOwnerId(in ownerId: Guid, out list: PropertyList)`
  - `+ findById(in id: Guid, out entity: Property)`
  - `+ update(in entity: Property, out persisted: Property)`

### `Property`

- Stereotype: `<<data abstraction>>`
- Attributes:
  - `- propertyId: Guid`
  - `- ownerId: Guid`
  - `- name: string`
  - `- address: string`
  - `- mapLocation: string`
  - `- description: string`
  - `- generalPolicies: string`
  - `- updatedAt: DateTime`
- Operations:
  - `+ applyUpdates(in request: PropertyUpdateDto, out result: StatusChangeResult)`

### `PropertyLogic`

- Stereotype: `<<business logic>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ validateUpdate(in entity: Property, in request: PropertyUpdateDto, out result: ValidationResult)`

## Relationships

- association:
  - from: `OwnerUI`
  - to: `UpdatePropertyController`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `manages properties`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `UpdatePropertyController`
  - to: `IPropertyRepository`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `loads and persists`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `UpdatePropertyController`
  - to: `Property`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `mutates state`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `UpdatePropertyController`
  - to: `PropertyLogic`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `validates`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `IPropertyRepository`
  - to: `Property`
  - source multiplicity: `1`
  - target multiplicity: `0..*`
  - association name: `manages`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

## Generalizations

- none in current scope

## Notes

- Three-phase: list properties (1), select for edit (2), submit update (3)
- Controller is stateless; `findById` called again at update time
- Separation of mutation and persistence: `applyUpdates` mutates in RAM, then `update` persists
- `Property.applyUpdates` takes `in request` parameter to apply changes to entity
