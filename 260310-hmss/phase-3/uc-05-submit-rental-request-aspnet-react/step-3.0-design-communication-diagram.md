# Design Communication Diagram: UC-05 Submit Rental Request - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: `TenantUI -> SubmitRentalRequestController`, then `Controller -> Repository`, `Controller -> BusinessLogic`, and `Controller -> infrastructure collaborators`
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label when a response payload is expected
- Separate reply arrows are intentionally omitted because `out` parameters already represent returned data
- Request flow style: synchronous request handling with asynchronous email dispatch
- Stateless coordinator: Controller does not retain state across sequences; reloads entities when needed

## Object Layout

```text
Tenant --- TenantUI --- SubmitRentalRequestController
                             |--- IRoomListingRepository --- RoomListing
                             |--- RentalRequestLogic
                             |--- IRentalRequestRepository --- RentalRequest
                             |--- IEmailGateway --- Email Provider
```

## Participants

| Position | Object                        | Stereotype             |
| -------- | ----------------------------- | ---------------------- |
| 1        | Tenant                        | Actor (primary)        |
| 2        | TenantUI                      | `<<user interaction>>` |
| 3        | SubmitRentalRequestController | `<<coordinator>>`      |
| 4        | IRoomListingRepository        | `<<database wrapper>>` |
| 5        | RoomListing                   | `<<data abstraction>>` |
| 6        | RentalRequestLogic            | `<<business logic>>`   |
| 7        | IRentalRequestRepository      | `<<database wrapper>>` |
| 8        | RentalRequest                 | `<<data abstraction>>` |
| 9        | IEmailGateway                 | `<<proxy>>`            |
| 10       | Email Provider                | Actor (secondary)      |

## Messages

| #   | From -> To                                  | Message                                                                  |
| --- | ------------------------------------------- | ------------------------------------------------------------------------ |
| 1   | Tenant -> TenantUI                          | Rental Request Access                                                    |
| 1.1 | TenantUI -> SubmitRentalRequestController   | `getRentalRequestForm(in listingId: Guid, out response: RentalRequestFormResponseDto)` |
| 1.2 | SubmitRentalRequestController -> IRoomListingRepository | `findById(in id: Guid, out entity: RoomListing)`                    |
| 2   | Tenant -> TenantUI                          | Rental Request Information                                               |
| 2.1 | TenantUI -> Tenant                          | Rental Request Review Display                                            |
| 3   | Tenant -> TenantUI                          | Submission Confirmation                                                  |
| 3.1 | TenantUI -> SubmitRentalRequestController   | `submitRentalRequest(in request: RentalRequestDto, out response: SubmissionResponseDto)` |
| 3.2 | SubmitRentalRequestController -> IRoomListingRepository | `findById(in id: Guid, out entity: RoomListing)`                    |
| 3.3 | SubmitRentalRequestController -> RentalRequestLogic | `validateRequestability(in listing: RoomListing, in request: RentalRequestDto, out result: ValidationResult)` |
| 3.4 | SubmitRentalRequestController -> IRentalRequestRepository | `save(in entity: RentalRequest, out persisted: RentalRequest)`     |
| 3.5 | SubmitRentalRequestController -> IEmailGateway | `sendAsync(in message: EmailMessage)`                                  |
| 3.6 | IEmailGateway -> Email Provider             | `sendAsync(in message: EmailMessage)`                                    |
| 3.7 | TenantUI -> Tenant                          | Submission Success                                                      |

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
| ----------------- | -------------- | ----- |
| `1.1` RentalRequestUI -> RentalRequestCoordinator: "Rental Request Form Request" | `1.1` TenantUI -> SubmitRentalRequestController: `getRentalRequestForm(in listingId: Guid, out response: RentalRequestFormResponseDto)` | sync, renamed to code-style |
| `1.2` RentalRequestCoordinator -> RentalRequestRules: "Listing Information Request" | `1.2` SubmitRentalRequestController -> IRoomListingRepository: `findById(in id: Guid, out entity: RoomListing)` | sync, added Repository layer |
| `3.1` RentalRequestUI -> RentalRequestCoordinator: "Rental Request Submission" | `3.1` TenantUI -> SubmitRentalRequestController: `submitRentalRequest(in request: RentalRequestDto, out response: SubmissionResponseDto)` | sync, renamed |
| `3.2` RentalRequestCoordinator -> RentalRequestRules: "Rental Request Information" | `3.3` SubmitRentalRequestController -> RentalRequestLogic: `validateRequestability(in listing: RoomListing, in request: RentalRequestDto, out result: ValidationResult)` | sync, business logic encapsulation |
| `3.3` RentalRequestRules -> RoomListing: "Requestability Check" | (absorbed into RentalRequestLogic.validateRequestability) | business rule encapsulation |
| `3.5` RentalRequestRules -> RentalRequest: "Rental Request Record" | (implicit DTO mapping before save) | DTO to entity mapping is implicit |
| `3.8` RentalRequestCoordinator -> NotificationService: "Owner Notification Request" | (implicit before 3.5) | Email composition is implicit in controller |
| `3.10` RentalRequestCoordinator -> EmailProxy: "Owner Notification" | `3.5-3.6` SubmitRentalRequestController -> IEmailGateway: `sendAsync(in message: EmailMessage)` | async, fire-and-forget |

## Alternative Flow Notes

- **Step 3.3: Requestability validation fails** - `ValidationResult.isValid = false`, `response.errors` populated, use case ends without saving
- **Step 3.5-3.6: Email Provider unavailable** - `IEmailGateway.sendAsync()` fails silently, request submission still succeeds, notification failure logged
- **Step 1.2, 3.2: Listing not found** - Repository returns null, response contains error, use case ends

## Notes

- `TenantUI` is shown explicitly so the human actor does not interact directly with the backend controller.
- `IRoomListingRepository` and `IRentalRequestRepository` handle persistence and return domain entities that the controller uses.
- `SubmitRentalRequestController` acts as the simplified orchestration point for this use case and is stateless.
- **Stateless design**: At message 3.2, the controller calls `findById` again to load `RoomListing` rather than retaining it from message 1.2, ensuring stateless behavior.
- Email dispatch is intentionally asynchronous to avoid blocking the HTTP request. The `sendAsync(in message: EmailMessage)` operation has no `out` parameter.
- `RentalRequestLogic` encapsulates the requestability business rule that validates whether a `RoomListing` can accept new requests.
- **Implicit DTO mapping**: At message 3.4, the controller implicitly maps data from `RentalRequestDto` to the `RentalRequest` entity before calling `save()`. This mapping is not shown as a separate message to keep the design clean.
- **Implicit email composition**: The controller composes the email message content before calling `IEmailGateway.sendAsync()`. This composition is not shown as a separate message.
- Actor-to-UI messages (1, 2, 2.1, 3, 3.7) use noun phrases because they represent physical user interactions, not code method calls.
