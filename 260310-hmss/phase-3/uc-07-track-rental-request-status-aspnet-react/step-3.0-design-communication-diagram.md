# Design Communication Diagram: UC-07 Track Rental Request Status - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: `TenantUI -> TrackRentalRequestController`, then `Controller -> Repository`
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label when a response payload is expected
- Separate reply arrows are intentionally omitted because `out` parameters already represent returned data
- Request flow style: synchronous read-only operations

## Object Layout

```text
Tenant --- TenantUI --- TrackRentalRequestController
                             |--- IRentalRequestRepository --- RentalRequest
```

## Participants

| Position | Object                    | Stereotype             |
| -------- | ------------------------- | ---------------------- |
| 1        | Tenant                    | Actor (primary)        |
| 2        | TenantUI                  | `<<user interaction>>` |
| 3        | TrackRentalRequestController | `<<coordinator>>`      |
| 4        | IRentalRequestRepository  | `<<database wrapper>>` |
| 5        | RentalRequest             | `<<data abstraction>>` |

## Messages

| #   | From -> To                              | Message                                                            |
| --- | --------------------------------------- | ------------------------------------------------------------------ |
| 1   | Tenant -> TenantUI                      | Rental Request Status Access                                        |
| 1.1 | TenantUI -> TrackRentalRequestController | `getTenantRequests(in tenantId: Guid, out response: TenantRequestsResponseDto)` |
| 1.2 | TrackRentalRequestController -> IRentalRequestRepository | `findTenantRequests(in tenantId: Guid, out list: RentalRequestList)` |
| 1.3 | TenantUI -> Tenant                      | Request List and Statuses Display                                   |
| 1a  | TenantUI -> Tenant                      | [No requests] No Request History Display                            |
| 2   | Tenant -> TenantUI                      | Status Detail Selection                                             |
| 2.1 | TenantUI -> TrackRentalRequestController | `getRequestDetail(in requestId: Guid, out response: RequestDetailResponseDto)` |
| 2.2 | TrackRentalRequestController -> IRentalRequestRepository | `findById(in id: Guid, out entity: RentalRequest)`                |
| 2.3 | TenantUI -> Tenant                      | Full Status Details and Actions Display                              |
| 3   | Tenant -> TenantUI                      | Status Detail Review                                                |

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
| ----------------- | -------------- | ----- |
| `1.1` RentalRequestStatusUI -> RentalRequestCoordinator: "Rental Request Status Request" | `1.1` TenantUI -> TrackRentalRequestController: `getTenantRequests(in tenantId: Guid, out response: TenantRequestsResponseDto)` | sync, renamed to code-style |
| `1.2-1.4` RentalRequestCoordinator -> RentalRequestStatusRules -> RentalRequest (status rules chain) | `1.2` TrackRentalRequestController -> IRentalRequestRepository: `findTenantRequests(in tenantId: Guid, out list: RentalRequestList)` | sync, business logic optimized out - controller queries repository directly |
| `1.5-1.6` Return path with status list | (implicit in `out response`) | response embedded in `out` parameter |
| `2.1` RentalRequestStatusUI -> RentalRequestCoordinator: "Status Detail Request" | `2.1` TenantUI -> TrackRentalRequestController: `getRequestDetail(in requestId: Guid, out response: RequestDetailResponseDto)` | sync, renamed to code-style |
| `2.2-2.4` RentalRequestCoordinator -> RentalRequestStatusRules -> RentalRequest (detail chain) | `2.2` TrackRentalRequestController -> IRentalRequestRepository: `findById(in id: Guid, out entity: RentalRequest)` | sync, business logic optimized out |
| `2.5-2.6` Return path with available actions | (implicit in `out response`) | available actions derived via DTO mapping in controller |

## Alternative Flow Notes

- **Step 1a: No submitted requests** - Repository returns empty list in message 1.2, response indicates no request history, UI displays empty state, use case ends successfully
- **Step 2.2: Request not found** - Repository returns null, response contains error, use case ends

## Notes

- `TenantUI` is shown explicitly so the human actor does not interact directly with the backend controller.
- `IRentalRequestRepository` handles read operations and returns domain entities that the controller uses.
- `TrackRentalRequestController` acts as the simplified orchestration point for this read-only use case.
- **Stateless coordinator**: Message 1.1 explicitly includes `in tenantId: Guid` parameter to ensure the controller remains completely stateless. The controller cannot retain the tenant ID from HTTP authentication context between requests.
- **Business logic optimization**: The analysis model's `RentalRequestStatusRules` (`<<business logic>>`) has been optimized out in the design phase. The controller queries the repository directly and handles status-to-available-actions derivation via DTO mapping. This reduces unnecessary pass-through classes while maintaining clear separation of concerns.
- **Available actions derivation**: The controller maps `RentalRequest.status` to available actions during DTO construction:
  - `Pending` → Show "Cancel" button
  - `Accepted` → Hide "Cancel" button
  - `Rejected` → No actions available
  - `Cancelled by Tenant` → No actions available
  - `Revoked by Owner` → No actions available
- This is a read-only use case with no state mutations or external service calls.
- Actor-to-UI messages (1, 2, 3, 1.3, 2.3) use noun phrases because they represent physical user interactions, not code method calls.
