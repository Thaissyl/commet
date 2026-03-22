# Design Communication Diagram: UC-05 Submit Rental Request - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: TenantUI -> SubmitRentalRequestController, then Controller -> Repository, Controller -> BusinessLogic, and Controller -> infrastructure collaborators
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label
- Separate reply arrows intentionally omitted — `out` parameters represent returned data
- Request flow style: synchronous request handling with asynchronous email dispatch
- Stateless coordinator: Controller does not retain state across sequences; reloads entities when needed

## Object Layout

```text
Tenant --- TenantUI --- SubmitRentalRequestController
                             |--- IRoomListingRepository
                             |--- RentalRequestLogic
                             |--- IRentalRequestRepository
                             |--- IEmailGateway --- Email Provider
```

## Participants

| Position | Object                        | Stereotype             |
| -------- | ----------------------------- | ---------------------- |
| 1        | Tenant                        | Actor (primary)        |
| 2        | TenantUI                      | `<<user interaction>>` |
| 3        | SubmitRentalRequestController | `<<coordinator>>`      |
| 4        | IRoomListingRepository        | `<<database wrapper>>` |
| 5        | RentalRequestLogic            | `<<business logic>>`   |
| 6        | IRentalRequestRepository      | `<<database wrapper>>` |
| 7        | IEmailGateway                 | `<<proxy>>`            |
| 8        | Email Provider                | Actor (secondary)      |

> `RoomListing` and `RentalRequest` removed — they are entity return types, not message-passing objects. Communication diagrams only show objects that send or receive messages.

## Messages

| #   | From -> To                                  | Message                                                                  |
| --- | ------------------------------------------- | ------------------------------------------------------------------------ |
| 1   | Tenant -> TenantUI                          | Rental Request Access                                                    |
| 1.1 | TenantUI -> SubmitRentalRequestController   | `GetRentalRequestForm(in listingId: Guid, out response: RentalRequestFormResponseDto)` |
| 1.2 | SubmitRentalRequestController -> IRoomListingRepository | `FindByIdAsync(in id: Guid, out entity: RoomListing)`                    |
| 2   | Tenant -> TenantUI                          | Rental Request Information                                               |
| 2.1 | TenantUI -> Tenant                          | Rental Request Review Display                                            |
| 3   | Tenant -> TenantUI                          | Submission Confirmation                                                  |
| 3.1 | TenantUI -> SubmitRentalRequestController   | `SubmitRentalRequest(in request: RentalRequestDto, out response: SubmissionResponseDto)` |
| 3.2 | SubmitRentalRequestController -> IRoomListingRepository | `FindByIdAsync(in id: Guid, out entity: RoomListing)`                    |
| 3.3 | SubmitRentalRequestController -> RentalRequestLogic | `ValidateRequestabilityWithDuplicateCheckAsync(in listing: RoomListing, in tenantId: Guid, out result: ValidationResult)` |
| 3.4 | SubmitRentalRequestController -> IRentalRequestRepository | `SaveAsync(in entity: RentalRequest, out persisted: RentalRequest)`     |
| 3.5 | SubmitRentalRequestController -> IEmailGateway | `SendAsync(in message: EmailMessage)` [to Owner]                         |
| 3.6 | IEmailGateway -> Email Provider             | `SendAsync(in message: EmailMessage)`                                    |
| 3.7 | TenantUI -> Tenant                          | Submission Success                                                       |

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
|---|---|---|
| `1.1` RentalRequestUI -> RentalRequestCoordinator: "Rental Request Form Request" | `1.1` TenantUI -> SubmitRentalRequestController: `GetRentalRequestForm(...)` | renamed |
| `1.2` RentalRequestCoordinator -> RentalRequestRules: "Listing Information Request" | `1.2` SubmitRentalRequestController -> IRoomListingRepository: `FindByIdAsync(...)` | sync, repository layer |
| `3.1` RentalRequestUI -> RentalRequestCoordinator: "Rental Request Submission" | `3.1` TenantUI -> SubmitRentalRequestController: `SubmitRentalRequest(...)` | renamed |
| `3.2` RentalRequestCoordinator -> RentalRequestRules: "Rental Request Information" | `3.3` SubmitRentalRequestController -> RentalRequestLogic: `ValidateRequestabilityWithDuplicateCheckAsync(...)` | business logic encapsulation |
| `3.8` RentalRequestCoordinator -> NotificationService: "Owner Notification Request" | `3.5-3.6` SubmitRentalRequestController -> IEmailGateway: `SendAsync(...)` to Owner | **CORRECTED:** sends to owner, not tenant |

## Alternative Flow Notes

- **Step 3.3: Requestability validation fails** — `ValidationResult.IsValid = false`, response includes errors, request not saved
- **Step 3.4: Duplicate request exists** — `ValidateRequestabilityWithDuplicateCheckAsync` detects existing active request from same tenant, returns invalid
- **Step 3.5-3.6: Email Provider unavailable** — `IEmailGateway.SendAsync()` catches exception, request submission succeeds, notification failure logged
- **Step 1.2, 3.2: Listing not found** — Repository returns null, response contains error, use case ends

## Notes

- `TenantUI` shown explicitly — human actor does not interact directly with backend controller.
- `IRoomListingRepository` and `IRentalRequestRepository` handle persistence and return domain entities.
- `SubmitRentalRequestController` acts as stateless orchestration point for this use case.
- **Stateless design**: At message 3.2, the controller calls `FindByIdAsync` again to load `RoomListing` rather than retaining it from message 1.2, ensuring stateless behavior.
- **Owner notification (Message 3.5)**: Controller notifies the **property owner** (not the tenant) of the new rental request. Message composes `EmailMessage(owner.Email, "New Rental Request Received", ...)` before calling `IEmailGateway.SendAsync()`.
- **Email dispatch asynchronous**: `SendAsync(in message: EmailMessage)` has no `out` parameter — fire-and-forget pattern to avoid blocking HTTP response.
- `RentalRequestLogic` encapsulates `ValidateRequestabilityWithDuplicateCheckAsync` — validates whether listing can accept requests and checks for duplicate active requests from same tenant.
- **Implicit DTO mapping**: Controller implicitly maps `RentalRequestDto` to `RentalRequest` entity before calling `SaveAsync()`. Not shown as separate message.
- Actor-to-UI messages (1, 2, 2.1, 3, 3.7) use noun phrases — physical user interactions, not code method calls.
