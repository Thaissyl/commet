# Phase 14: Fix UC-15 — Code Bug + Design Diagram

**Status:** Ready
**Code:** `backend/Hmss.Api/Controllers/RoomListingController.cs`
**Doc:** `C:\Users\welterial\commet\260310-hmss\phase-3\uc-15-reopen-room-listing-aspnet-react\step-3.0-design-communication-diagram.md`

## Context Links

- Use case: `C:\Users\welterial\commet\260310-hmss\step-1.3-uc-15-reopen-room-listing.md`
- Analysis: `C:\Users\welterial\commet\260310-hmss\phase-2\step-2.2-uc-15-reopen-room-listing-main-seq.md`

## Code Bug

### Bug — Email sent to hardcoded address instead of tenant

In `SubmitReopen`:
```csharp
_email.SendAsync(new EmailMessage("tenant@hmss.local", "Arrangement Revoked", ...));
```

Fix — use actual tenant email:
```csharp
var tenant = request.Tenant;
if (tenant != null)
    _email.SendAsync(new EmailMessage(tenant.Email, "Arrangement Revoked", $"The owner has revoked your accepted request for {request.Listing?.Title}."));
```

## Document Errors

| # | Error |
|---|-------|
| 1 | Participant `ReopenRoomController` → `RoomListingController` (UC-15 methods are in `RoomListingController`, no separate controller) |
| 2 | Object layout `IRentalRequestRepository --- RentalRequest` — remove; add `RentalRequest` directly under controller (`request.Revoke()` called directly) |
| 3 | Object layout `IRoomListingRepository --- RoomListing` — remove; add `RoomListing` directly under controller (`listing.Reopen()` called directly) |
| 4 | Msg 1.1: remove `in ownerId: Guid` (comes from JWT) |
| 5 | Msg 1.2: `findAcceptedByOwnerId` → `FindAcceptedByOwnerIdAsync`; `out list: RequestList` — `RequestList` is invented, change to `out requests: List<RentalRequest>` |
| 6 | Msg 2.2: `findById` → `FindByIdAsync` |
| 7 | Msg 3.2: `findById` → `FindByIdAsync` |
| 8 | Add msg after 3.2: `RoomListingController -> ReopenLogic: ValidateConcurrencyStatus(in request: RentalRequest, out result: ValidationResult)` — called in `SubmitReopen` but not shown in diagram |
| 9 | Msg 3.3: `findByRequestId(in requestId: Guid, ...)` — no such method; code calls `FindByIdAsync(request.ListingId)` — fix to `FindByIdAsync(in listingId: Guid, out entity: RoomListing)` |
| 10 | Msg 3.6: `update` → `UpdateAsync` |
| 11 | Msg 3.7: `update` → `UpdateAsync` |

## Corrected Object Layout

```text
Owner --- OwnerUI --- RoomListingController
                       |--- IRentalRequestRepository
                       |--- IRoomListingRepository
                       |--- ReopenLogic
                       |--- RentalRequest
                       |--- RoomListing
                       |--- IEmailGateway --- Email Provider
```

## Todo

- [ ] Fix `SubmitReopen`: send email to `request.Tenant.Email` not hardcoded address
- [ ] Run `dotnet build` — zero errors
- [ ] Rename `ReopenRoomController` → `RoomListingController` throughout diagram
- [ ] Fix object layout: remove `IRentalRequestRepository --- RentalRequest`; add `RentalRequest` under controller
- [ ] Fix object layout: remove `IRoomListingRepository --- RoomListing`; add `RoomListing` under controller
- [ ] Fix Msg 1.1: remove `in ownerId: Guid`
- [ ] Fix Msg 1.2: `FindAcceptedByOwnerIdAsync`; `List<RentalRequest>`
- [ ] Fix Msg 2.2: `FindByIdAsync`
- [ ] Fix Msg 3.2: `FindByIdAsync`
- [ ] Add msg after 3.2: `ValidateConcurrencyStatus(in request: RentalRequest, out result: ValidationResult)`
- [ ] Fix Msg 3.3: `FindByIdAsync(in listingId: Guid)`
- [ ] Fix Msg 3.6, 3.7: `UpdateAsync`

## Success Criteria

- Email sent to `request.Tenant.Email`
- `dotnet build` passes
- Diagram shows `RoomListingController`
- Both entity objects directly under controller in layout
- `ValidateConcurrencyStatus` shown in both seq 2 and seq 3
- Msg 3.3 uses `FindByIdAsync(in listingId: Guid)`
- All repo methods with Async suffix
