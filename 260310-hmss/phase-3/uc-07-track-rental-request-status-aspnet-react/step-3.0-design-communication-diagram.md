# Design Communication Diagram: UC-07 Track Rental Request Status - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: TenantUI -> TenantRentalRequestController, then Controller -> Repository
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label
- Separate reply arrows intentionally omitted — `out` parameters represent returned data
- Request flow style: synchronous read-only operations

## Object Layout

```text
Tenant --- TenantUI --- TenantRentalRequestController
                             |--- IRentalRequestRepository
```

## Participants

| Position | Object                        | Stereotype             |
| -------- | ----------------------------- | ---------------------- |
| 1        | Tenant                        | Actor (primary)        |
| 2        | TenantUI                      | `<<user interaction>>` |
| 3        | TenantRentalRequestController | `<<coordinator>>`      |
| 4        | IRentalRequestRepository      | `<<database wrapper>>` |

> `RentalRequest` removed — return type only, no messages sent to it in this use case.

## Messages

| #   | From -> To                              | Message                                                            |
| --- | --------------------------------------- | ------------------------------------------------------------------ |
| 1   | Tenant -> TenantUI                      | Rental Request Status Access                                        |
| 1.1 | TenantUI -> TenantRentalRequestController | `GetTenantRequests(out response: TenantRequestsResponseDto)` |
| 1.2 | TenantRentalRequestController -> IRentalRequestRepository | `FindByTenantIdAsync(in tenantId: Guid, out list: List<RentalRequest>)` |
| 1.3 | TenantUI -> Tenant                      | Request List and Statuses Display                                   |
| 1a  | TenantUI -> Tenant                      | [No requests] No Request History Display                            |
| 2   | Tenant -> TenantUI                      | Status Detail Selection                                             |
| 2.1 | TenantUI -> TenantRentalRequestController | `GetRequestDetail(in requestId: Guid, out response: RequestDetailResponseDto)` |
| 2.2 | TenantRentalRequestController -> IRentalRequestRepository | `FindByIdAsync(in id: Guid, out entity: RentalRequest)`                |
| 2.3 | TenantUI -> Tenant                      | Full Status Details and Actions Display                              |
| 3   | Tenant -> TenantUI                      | Status Detail Review                                                |

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
|---|---|---|
| `1.1` RentalRequestStatusUI -> RentalRequestCoordinator: "Rental Request Status Request" | `1.1` TenantUI -> TenantRentalRequestController: `GetTenantRequests(...)` | renamed |
| `1.2-1.4` RentalRequestCoordinator -> RentalRequestStatusRules -> RentalRequest | `1.2` TenantRentalRequestController -> IRentalRequestRepository: `FindByTenantIdAsync(...)` | business logic optimized out |
| `2.1` RentalRequestStatusUI -> RentalRequestCoordinator: "Status Detail Request" | `2.1` TenantUI -> TenantRentalRequestController: `GetRequestDetail(...)` | renamed |
| `2.2-2.4` RentalRequestCoordinator -> RentalRequestStatusRules -> RentalRequest | `2.2` TenantRentalRequestController -> IRentalRequestRepository: `FindByIdAsync(...)` | business logic optimized out |

## Alternative Flow Notes

- **Step 1a: No submitted requests** — Repository returns empty list, response indicates no request history, UI displays empty state
- **Step 2.2: Request not found** — Repository returns null, response contains error, use case ends

## Notes

- `TenantUI` shown explicitly — human actor does not interact directly with backend controller.
- `IRentalRequestRepository` handles read operations and returns domain entities.
- `TenantRentalRequestController` acts as stateless orchestration point for this read-only use case.
- **Stateless coordinator**: TenantId comes from JWT claims via `ClaimsHelper.GetUserId(User)`, not from request parameter. Controller remains completely stateless between requests.
- **Business logic optimization**: Analysis model's `RentalRequestStatusRules` optimized out in design. Controller queries repository directly and handles status-to-actions derivation via DTO mapping.
- **Available actions derivation**: Controller maps `RentalRequest.status` to available actions:
  - `Pending` → Show "Cancel" button
  - `Accepted` → Hide "Cancel" button
  - `Rejected`, `Cancelled by Tenant`, `Revoked by Owner` → No actions
- This is a read-only use case with no state mutations or external service calls.
- Actor-to-UI messages (1, 2, 3, 1.3, 2.3) use noun phrases — physical user interactions, not code method calls.
