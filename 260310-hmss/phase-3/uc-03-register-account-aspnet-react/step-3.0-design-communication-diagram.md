# Design Communication Diagram: UC-03 Register Account - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: `VisitorUI -> RegisterAccountController`, then `Controller -> BusinessLogic` and `Controller -> Repository`
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label when a response payload is expected
- Separate reply arrows are intentionally omitted because `out` parameters already represent returned data
- Request flow style: synchronous request handling

## Object Layout

```text
Visitor --- VisitorUI --- RegisterAccountController
                             |--- AuthenticationLogic
                             |--- IUserAccountRepository --- UserAccount
```

## Participants

| Position | Object                    | Stereotype             |
| -------- | ------------------------- | ---------------------- |
| 1        | Visitor                   | Actor (primary)        |
| 2        | VisitorUI                 | `<<user interaction>>` |
| 3        | RegisterAccountController | `<<coordinator>>`      |
| 4        | AuthenticationLogic       | `<<business logic>>`   |
| 5        | IUserAccountRepository    | `<<database wrapper>>` |
| 6        | UserAccount               | `<<data abstraction>>` |

## Messages

| #   | From -> To                               | Message                                                            |
| --- | ---------------------------------------- | ------------------------------------------------------------------ |
| 1   | Visitor -> VisitorUI                     | Registration Access                                                |
| 1.1 | VisitorUI -> RegisterAccountController    | `getRegistrationForm(out response: RegistrationFormResponseDto)`   |
| 2   | Visitor -> VisitorUI                     | Registration Information                                           |
| 2.1 | VisitorUI -> Visitor                     | Registration Review                                                |
| 3   | Visitor -> VisitorUI                     | Registration Confirmation                                          |
| 3.1 | VisitorUI -> RegisterAccountController   | `registerAccount(in request: RegistrationDto, out response: RegistrationResponseDto)` |
| 3.2 | RegisterAccountController -> AuthenticationLogic | `validateRegistration(in request: RegistrationDto, out result: ValidationResult)` |
| 3.3 | RegisterAccountController -> IUserAccountRepository | `save(in entity: UserAccount, out persisted: UserAccount)` |
| 3.4 | VisitorUI -> Visitor                    | Registration Confirmation                                          |

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
| ----------------- | -------------- | ----- |
| `1.1` RegistrationUI -> RegistrationCoordinator: "Registration Request" | `1.1` VisitorUI -> RegisterAccountController: `getRegistrationForm(out response: RegistrationFormResponseDto)` | sync, renamed to code-style |
| `3.1` RegistrationUI -> RegistrationCoordinator: "Registration Request" | `3.1` VisitorUI -> RegisterAccountController: `registerAccount(in request: RegistrationDto, out response: RegistrationResponseDto)` | sync, renamed |
| `3.2` RegistrationCoordinator -> AccountRegistrationRules: "Registration Information" | `3.2` RegisterAccountController -> AuthenticationLogic: `validateRegistration(in request: RegistrationDto, out result: ValidationResult)` | sync, business logic encapsulation |
| `3.4` RegistrationCoordinator -> UserAccount: "Account Information" | (implicit DTO mapping before save) | DTO to entity mapping is implicit |
| `3.5` UserAccount -> RegistrationCoordinator: "Account Record" | `3.3` RegisterAccountController -> IUserAccountRepository: `save(in entity: UserAccount, out persisted: UserAccount)` | sync, repository persists entity |

## Alternative Flow Notes

- **Step 3.2: Validation fails** - `ValidationResult.isValid = false`, `response.errors` populated with specific error messages (incomplete fields, email already exists, weak password), use case ends without saving
- **Step 3.3: Database error on save** - Repository throws exception, response contains error, use case ends

## Notes

- `VisitorUI` is shown explicitly so the human actor does not interact directly with the backend controller.
- `IUserAccountRepository` handles persistence and returns the created `UserAccount` entity with database-generated values.
- `RegisterAccountController` acts as the simplified orchestration point for this use case.
- `AuthenticationLogic` encapsulates the registration business rules: email uniqueness check, password strength validation, required field validation.
- **Implicit DTO mapping**: At message 3.3, the controller implicitly maps data from `RegistrationDto` to the `UserAccount` entity before calling `save()`. This mapping is not shown as a separate message to keep the design clean.
- **Password hashing**: Password hashing is implicitly applied during DTO mapping before persistence; passwords are stored in non-recoverable protected form per security requirements.
- **Initial account status**: Newly created accounts are assigned `accountStatus = Active` by default during entity initialization.
- Actor-to-UI messages (1, 2, 2.1, 3, 3.4) use noun phrases because they represent physical user interactions, not code method calls.
- No secondary actors or external proxies are involved in this use case.
