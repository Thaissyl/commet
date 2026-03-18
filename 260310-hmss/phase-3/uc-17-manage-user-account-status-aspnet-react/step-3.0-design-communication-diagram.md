# Design Communication Diagram: UC-17 Manage User Account Status - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: `AdminUI -> ManageAccountStatusController`, then `Controller -> Repository`, `Controller -> UserManagementLogic`, and `Controller -> IEmailGateway`
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label when a response payload is expected
- Separate reply arrows are intentionally omitted because `out` parameters already represent returned data
- Request flow style: synchronous request handling with two-phase operation pattern

## Object Layout

```text
System Admin --- AdminUI --- ManageAccountStatusController
                              |--- UserManagementLogic
                              |--- IUserAccountRepository --- UserAccount
                              |--- IEmailGateway --- Email Provider
```

## Participants

| Position | Object                     | Stereotype             |
| -------- | -------------------------- | ---------------------- |
| 1        | System Admin               | Actor (primary)        |
| 2        | AdminUI                    | `<<user interaction>>` |
| 3        | ManageAccountStatusController | `<<coordinator>>`     |
| 4        | UserManagementLogic        | `<<business logic>>`   |
| 5        | IUserAccountRepository     | `<<database wrapper>>` |
| 6        | UserAccount                | `<<data abstraction>>` |
| 7        | IEmailGateway              | `<<proxy>>`            |
| 8        | Email Provider             | Actor (secondary)      |

## Messages

| #   | From -> To                                  | Message                                                            |
| --- | ------------------------------------------- | ------------------------------------------------------------------ |
| 1   | System Admin -> AdminUI                     | Account Management Access                                          |
| 1.1 | AdminUI -> ManageAccountStatusController    | `getAccountList(out response: AccountListResponseDto)`             |
| 1.2 | ManageAccountStatusController -> IUserAccountRepository | `findAll(out list: AccountList)`                             |
| 1.3 | AdminUI -> System Admin                     | Account List Display                                               |
| 2   | System Admin -> AdminUI                     | User Account Selection                                             |
| 2.1 | AdminUI -> ManageAccountStatusController    | `getAccountDetail(in accountId: Guid, out response: AccountDetailResponseDto)` |
| 2.2 | ManageAccountStatusController -> IUserAccountRepository | `findById(in id: Guid, out entity: UserAccount)`                |
| 2.3 | ManageAccountStatusController -> UserManagementLogic | `getAvailableActions(in account: UserAccount, out actions: List<String>)` |
| 2.4 | AdminUI -> System Admin                     | Detail and Available Actions Display                               |
| 3   | System Admin -> AdminUI                     | Account Status Change Decision (Suspend)                           |
| 3.1 | AdminUI -> ManageAccountStatusController    | `suspendAccount(in accountId: Guid, out response: StatusChangeResponseDto)` |
| 3.2 | ManageAccountStatusController -> IUserAccountRepository | `findById(in id: Guid, out entity: UserAccount)`                |
| 3.3 | ManageAccountStatusController -> UserManagementLogic | `validateStatusTransition(in account: UserAccount, in action: String, out result: ValidationResult)` |
| 3.4 | ManageAccountStatusController -> UserAccount | `suspend(out result: StatusChangeResult)`                          |
| 3.5 | ManageAccountStatusController -> IUserAccountRepository | `update(in entity: UserAccount, out persisted: UserAccount)`  |
| 3.6 | ManageAccountStatusController -> IEmailGateway | `sendAsync(in message: EmailMessage)`                              |
| 3.7 | IEmailGateway -> Email Provider             | `sendAsync(in message: EmailMessage)`                              |
| 3.8 | AdminUI -> System Admin                     | Account Status Change Confirmation                                 |

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
| ----------------- | -------------- | ----- |
| `1.1` AdminUI -> AdminCoordinator: "User Account List Request" | `1.1` AdminUI -> ManageAccountStatusController: `getAccountList(out response: AccountListResponseDto)` | sync, renamed |
| `1.2-1.4` AdminCoordinator -> UserManagementLogic -> User: "User Account List Request/Query/Data" | `1.2` ManageAccountStatusController -> IUserAccountRepository: `findAll(out list: AccountList)` | direct repository read |
| `2.1` AdminUI -> AdminCoordinator: "User Account Detail Request" | `2.1` AdminUI -> ManageAccountStatusController: `getAccountDetail(in accountId: Guid, out response: AccountDetailResponseDto)` | sync |
| `2.2-2.5` AdminCoordinator -> UserManagementLogic -> User: "User Account Detail Request/Query/Data" | `2.2` ManageAccountStatusController -> IUserAccountRepository: `findById(in id: Guid, out entity: UserAccount)` then `2.3` getAvailableActions(...) | load entity, determine actions |
| `3.1` AdminUI -> AdminCoordinator: "Account Status Change Request" | `3.1` AdminUI -> ManageAccountStatusController: `suspendAccount(in accountId: Guid, out response: StatusChangeResponseDto)` | sync, action-specific |
| `3.2-3.4` AdminCoordinator -> UserManagementLogic -> User: "Account Status Transition Check/Update" | `3.3` ManageAccountStatusController -> UserManagementLogic: `validateStatusTransition(in account, in action, out result)` then `3.4` suspend(...) | validate, mutate in RAM |
| `3.6-3.11` AdminCoordinator -> NotificationService -> EmailProxy -> EmailProvider: "User Notification Request/Dispatch/Delivery" | `3.6` ManageAccountStatusController -> IEmailGateway: `sendAsync(in message: EmailMessage)` | async fire-and-forget |

## Alternative Flow Notes

- **Step 2.3: No actions available** - `actions` list is empty, response contains no available actions, messages 3.1-3.7 skipped, use case ends
- **Step 3.3: Validation fails** - `ValidationResult.isValid = false`, response contains invalid transition reason, messages 3.4-3.7 skipped, use case ends
- **Step 3.2: Account not found** - Repository returns null/error, response contains not found error, use case ends
- **Step 3.5: Database error on update** - Repository throws exception, response contains error, use case ends
- **Alternative: Enable action** - Similar flow but uses `enableAccount(in accountId)` endpoint, calls `enable(out result)` on UserAccount (Suspended → Active)
- **Alternative: Disable action** - Similar flow but uses `disableAccount(in accountId)` endpoint, calls `disable(out result)` on UserAccount (any status → Disabled)
- **Step 3.7: Email Provider unavailable** - Gateway records failure, status change succeeds, continues to step 3.8

## Notes

- `AdminUI` is shown explicitly so the human actor does not interact directly with the backend controller.
- `IUserAccountRepository` handles persistence and returns the updated entity.
- `ManageAccountStatusController` acts as the simplified orchestration point.
- `UserManagementLogic` encapsulates status transition validation: validates which status transitions are permitted (e.g., Active → Suspend ✓, Suspend → Enable ✓, any status → Disable ✓, Disabled → Enable ✗ without admin intervention).
- `IEmailGateway` handles asynchronous email dispatch. No `out` parameter because notifications are fire-and-forget.
- **Two-Phase Operation Pattern**: This use case demonstrates the validation-then-execution pattern:
  - **Phase 1 (Pre-check)**: Sequence 2 `getAccountDetail` retrieves account and determines available actions.
  - **Phase 2 (Execution)**: Sequence 3 `suspendAccount` (or `enableAccount`, `disableAccount`) performs the actual status change.
- **Stateless Coordinator Compliance (Messages 1.2, 2.2, 3.2)**: The controller executes fresh repository queries at the beginning of each sequence. Web controllers must remain stateless and cannot preserve the `UserAccount` object in memory between user clicks.
- **Separation of State Mutation and Persistence (Messages 3.4, 3.5)**: Based on the Information Hiding principle, the controller invokes `suspend()` on the `UserAccount` (`<<data abstraction>>`) object so that the object mutates its own data safely in RAM. Immediately following, it calls `update()` on the `IUserAccountRepository` (`<<database wrapper>>`) to guarantee that the RAM mutation is securely persisted to the disk.
- **Asynchronous External Proxy (Message 3.6)**: The `IEmailGateway` uses `sendAsync(in message)` with no `out` parameter. The controller fires the notification to a background queue and immediately returns success to the user, preventing UI freeze if the Email Provider is slow or unavailable.
- **Action-Specific Endpoints**: The controller provides action-specific endpoints (`suspendAccount`, `enableAccount`, `disableAccount`) rather than a generic `changeStatus` endpoint. This aligns with action-based controller naming and makes the API more explicit.
- **Available Actions Query (Message 2.3)**: The `getAvailableActions(in account, out actions)` method returns a list of permitted status transition actions (e.g., ["Suspend", "Disable"] for Active accounts, ["Enable"] for Suspended accounts). This allows the UI to display only relevant actions or a reactive menu as per design choice.
- **Repository Query Patterns**:
  - `findAll(out list)` - Fetches all user accounts (sequence 1)
  - `findById(in id: Guid)` - Fetches single account by ID (sequences 2, 3)
- **Implicit DTO mapping**: The controller implicitly maps response data from entities to DTOs. This mapping is not shown as a separate message.
- **NotificationService**: In the analysis model, a separate `NotificationService` (`<<application logic>>`) composes notification content. In design, this functionality is implicit—the controller composes the email message directly before passing it to `IEmailGateway`.
- Actor-to-UI messages (1, 1.3, 2, 2.4, 3, 3.8) use noun phrases because they represent physical user interactions, not code method calls.
