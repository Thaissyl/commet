# Design Communication Diagram: UC-17 Manage User Account Status - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: AdminUI -> UserAccountController, then Controller -> Repository and Controller -> UserAccountLogic
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label
- Separate reply arrows intentionally omitted — `out` parameters represent returned data
- Request flow style: synchronous request handling with status state machine

## Object Layout

```text
System Admin --- AdminUI --- UserAccountController
                              |--- UserAccountLogic
                              |--- IUserAccountRepository
```

## Participants

| Position | Object                   | Stereotype             |
| -------- | ------------------------ | ---------------------- |
| 1        | System Admin             | Actor (primary)        |
| 2        | AdminUI                  | `<<user interaction>>` |
| 3        | UserAccountController    | `<<coordinator>>`      |
| 4        | UserAccountLogic         | `<<business logic>>`   |
| 5        | IUserAccountRepository   | `<<database wrapper>>` |

## Messages

| #   | From -> To                                  | Message                                                            |
| --- | ------------------------------------------- | ------------------------------------------------------------------ |
| 1   | System Admin -> AdminUI                     | Account Management Access                                          |
| 1.1 | AdminUI -> UserAccountController            | `GetUserAccounts(out response: UserAccountsResponseDto)` |
| 1.2 | UserAccountController -> IUserAccountRepository | `FindAllAsync(out users: List<UserAccount>)` |
| 1.3 | AdminUI -> System Admin                     | User Accounts List Display                                         |
| 2   | System Admin -> AdminUI                     | Account Selection                                                 |
| 2.1 | AdminUI -> UserAccountController            | `GetAccountDetail(in userId: Guid, out response: AccountDetailResponseDto)` |
| 2.2 | UserAccountController -> IUserAccountRepository | `FindByIdAsync(in id: Guid, out user: UserAccount)` |
| 2.3 | AdminUI -> System Admin                     | Account Details Display                                           |
| 3   | System Admin -> AdminUI                     | Status Change Decision                                             |
| 3.1 | AdminUI -> UserAccountController            | `ChangeAccountStatus(in userId: Guid, in newStatus: string, out response: StatusChangeResponseDto)` |
| 3.2 | UserAccountController -> UserAccountLogic   | `ValidateStatusChange(in user: UserAccount, in newStatus: string, out result: ValidationResult)` |
| 3.3 | UserAccountController -> IUserAccountRepository | `UpdateAsync(in entity: UserAccount, out persisted: UserAccount)` |
| 3.4 | AdminUI -> System Admin                     | Status Change Confirmation Message                                |

## Alternative Flow Notes

- **Step 3.2: Validation fails** — `ValidationResult.IsValid = false` (invalid transition), response includes reason
- **Step 3.3: Update fails** — Repository exception handled, response contains error

## Notes

- `AdminUI` shown explicitly — system admin does not interact directly with backend controller.
- `UserAccountController` acts as stateless orchestration point.
- `UserAccountLogic` encapsulates `ValidateStatusChange` state machine validation.
- `IUserAccountRepository` queries and persists `UserAccount` entity with status.
- Status transitions follow state machine rules (e.g., cannot reactivate permanently deleted).
- Actor-to-AdminUI messages use noun phrases — physical interactions.
