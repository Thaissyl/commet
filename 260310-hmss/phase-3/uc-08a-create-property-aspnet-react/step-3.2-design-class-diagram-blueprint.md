# Design Class Diagram Blueprint: UC-08a Create Property - ASP.NET Simple Layered Backend

## Scope

- Included classes: `OwnerUI`, `CreatePropertyController`, `PropertyService`, `IPropertyRepository`, `Property`
- Synchronization source:
  - participant set and call structure from `step-3.0-design-communication-diagram.md`
  - class operations derived from step-3.0 messages

## Class Boxes

### `OwnerUI`

- Stereotype: `<<user interaction>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ openPropertyCreation()`
  - `+ submitProperty(in request: PropertyDto)`

### `CreatePropertyController`

- Stereotype: `<<coordinator>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getCreatePropertyForm(out response: PropertyFormResponseDto)`
  - `+ createProperty(in request: PropertyDto, out response: PropertyResponseDto)`

### `PropertyService`

- Stereotype: `<<service>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ validatePropertyFields(in request: PropertyDto, out result: ValidationResult)`

### `IPropertyRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ save(in entity: Property, out persisted: Property)`

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
  - `- createdAt: DateTime`
  - `- updatedAt: DateTime`
- Operations:
  - none in current scope

## Relationships

- association:
  - from: `OwnerUI`
  - to: `CreatePropertyController`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `creates property`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `CreatePropertyController`
  - to: `PropertyService`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `validates`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `CreatePropertyController`
  - to: `IPropertyRepository`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `persists`
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

- `PropertyService` validates required fields (name, address), format validation, and policy constraints.
- DTO-to-entity mapping is implicit before `save()` call.
- `ownerId` is set from authenticated owner's context during DTO mapping.
- No external actors or proxies involved in this use case.
