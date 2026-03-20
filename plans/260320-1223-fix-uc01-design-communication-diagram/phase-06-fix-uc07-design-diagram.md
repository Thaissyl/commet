# Phase 06: Document Fix — Rewrite UC-07 step-3.0-design-communication-diagram.md

**Status:** Ready (no code changes needed — read-only use case)
**Priority:** High
**File:** `C:\Users\welterial\commet\260310-hmss\phase-3\uc-07-track-rental-request-status-aspnet-react\step-3.0-design-communication-diagram.md`

## Context Links

- Use case: `C:\Users\welterial\commet\260310-hmss\step-1.3-uc-07-track-rental-request-status.md`
- Analysis: `C:\Users\welterial\commet\260310-hmss\phase-2\step-2.2-uc-07-track-rental-request-status-main-seq.md`
- Code: `backend/Hmss.Api/Controllers/TenantRentalRequestController.cs`

## Errors Being Fixed

| # | Error |
|---|-------|
| 1 | Participant `TrackRentalRequestController` → `TenantRentalRequestController` (actual class name) |
| 2 | `RentalRequest <<data abstraction>>` participant — remove (no messages go to it; return type only) |
| 3 | Object layout `IRentalRequestRepository --- RentalRequest` line — remove |
| 4 | Msg 1.2 method `findTenantRequests` → `FindByTenantIdAsync` |
| 5 | Msg 1.2 return type `RentalRequestList` → `List<RentalRequest>` |
| 6 | Msg 2.2 method `findById` → `FindByIdAsync` |
| 7 | Note claims `in tenantId: Guid` needed for statelessness — wrong; tenantId comes from JWT (`ClaimsHelper.GetUserId(User)`), not a request parameter |

## Corrected Participants (4 total)

| Position | Object | Stereotype |
|---|---|---|
| 1 | Tenant | Actor (primary) |
| 2 | TenantUI | `<<user interaction>>` |
| 3 | TenantRentalRequestController | `<<coordinator>>` |
| 4 | IRentalRequestRepository | `<<database wrapper>>` |

> `RentalRequest` removed — return type only, no messages sent to it in this use case.

## Corrected Object Layout

```text
Tenant --- TenantUI --- TenantRentalRequestController
                             |--- IRentalRequestRepository
```

## Corrected Messages

| # | From -> To | Message |
|---|---|---|
| 1 | Tenant -> TenantUI | Rental Request Status Access |
| 1.1 | TenantUI -> TenantRentalRequestController | `GetTenantRequests(out response: TenantRequestsResponseDto)` |
| 1.2 | TenantRentalRequestController -> IRentalRequestRepository | `FindByTenantIdAsync(in tenantId: Guid, out list: List<RentalRequest>)` |
| 1.3 | TenantUI -> Tenant | Request List and Statuses Display |
| 1a | TenantUI -> Tenant | [No requests] No Request History Display |
| 2 | Tenant -> TenantUI | Status Detail Selection |
| 2.1 | TenantUI -> TenantRentalRequestController | `GetRequestDetail(in requestId: Guid, out response: RequestDetailResponseDto)` |
| 2.2 | TenantRentalRequestController -> IRentalRequestRepository | `FindByIdAsync(in id: Guid, out entity: RentalRequest)` |
| 2.3 | TenantUI -> Tenant | Full Status Details and Actions Display |
| 3 | Tenant -> TenantUI | Status Detail Review |

## Todo

- [ ] Replace controller name `TrackRentalRequestController` → `TenantRentalRequestController` throughout
- [ ] Remove `RentalRequest` from Participants table
- [ ] Remove `IRentalRequestRepository --- RentalRequest` from Object Layout
- [ ] Fix Msg 1.1: remove `in tenantId: Guid` param
- [ ] Fix Msg 1.2: `findTenantRequests` → `FindByTenantIdAsync`, `RentalRequestList` → `List<RentalRequest>`
- [ ] Fix Msg 2.2: `findById` → `FindByIdAsync`
- [ ] Fix note about tenantId statelessness — tenantId resolved from JWT, not request param

## Success Criteria

- 4 participants (no `RentalRequest`)
- Controller named `TenantRentalRequestController` throughout
- Msg 1.2 uses `FindByTenantIdAsync` with `List<RentalRequest>` return type
- Msg 2.2 uses `FindByIdAsync`
- Msg 1.1 has no `in tenantId` param
