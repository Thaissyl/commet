# Design Class Diagram Blueprint: UC-03 Register Account - ASP.NET Simple Layered Backend

## Scope

- Included classes: `VisitorUI`, `RegisterAccountController`, `AuthenticationLogic`, `IUserAccountRepository`, `UserAccount`
- Synchronization source:
  - participant set and call structure from `step-3.0-design-communication-diagram.md`
  - class operations derived from step-3.0 messages

## Class Boxes

### `VisitorUI`

- Stereotype: `<<user interaction>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ openRegistration()`
  - `+ submitRegistration(in request: RegistrationDto)`

### `RegisterAccountController`

- Stereotype: `<<coordinator>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ getRegistrationForm(out response: RegistrationFormResponseDto)`
  - `+ registerAccount(in request: RegistrationDto, out response: RegistrationResponseDto)`

### `AuthenticationLogic`

- Stereotype: `<<business logic>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ validateRegistration(in request: RegistrationDto, out result: ValidationResult)`

### `IUserAccountRepository`

- Stereotype: `<<database wrapper>>`
- Attributes:
  - none in current scope
- Operations:
  - `+ save(in entity: UserAccount, out persisted: UserAccount)`

### `UserAccount`

- Stereotype: `<<data abstraction>>`
- Attributes:
  - `- userId: Guid`
  - `- fullName: string`
  - `- email: string`
  - `- phone: string`
  - `- passwordHash: string`
  - `- role: UserRole`
  - `- accountStatus: AccountStatus`
  - `- createdAt: DateTime`
- Operations:
  - none in current scope

## Relationships

- association:
  - from: `VisitorUI`
  - to: `RegisterAccountController`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `submits registration`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `RegisterAccountController`
  - to: `AuthenticationLogic`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `validates`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `RegisterAccountController`
  - to: `IUserAccountRepository`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `persists`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

- association:
  - from: `IUserAccountRepository`
  - to: `UserAccount`
  - source multiplicity: `1`
  - target multiplicity: `0..*`
  - association name: `manages`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

## Generalizations

- none in current scope

## Notes

- This version uses a simplified orchestration style where `RegisterAccountController` coordinates business logic and repository collaborators.
- Password hashing is applied implicitly during DTO-to-entity mapping before persistence.
- New accounts default to `accountStatus = Active`.
- `AuthenticationLogic` validates email uniqueness, password strength, and required fields.
