# Phase 05: Fix UC-06 — Code Bug + Design Diagram

**Status:** Ready
**Priority:** High

## Context Links

- Use case: `C:\Users\welterial\commet\260310-hmss\step-1.3-uc-06-cancel-rental-request.md`
- Analysis: `C:\Users\welterial\commet\260310-hmss\phase-2\step-2.2-uc-06-cancel-rental-request-main-seq.md`
- Design diagram: `C:\Users\welterial\commet\260310-hmss\phase-3\uc-06-cancel-rental-request-aspnet-react\step-3.0-design-communication-diagram.md`
- Code: `backend/Hmss.Api/Controllers/TenantRentalRequestController.cs`
- Code: `backend/Hmss.Api/Logic/RentalRequestLogic.cs`
- Code: `backend/Hmss.Api/Entities/RentalRequest.cs`

## Code Bug — Wrong Email Recipient

**Use case step 7:** "System sends a notification of the cancellation **to the Owner**."

**Actual code** (`SubmitCancellation`, line 102–104) sends to `tenant.Email` — owner is never notified.

### Fix in TenantRentalRequestController.cs

Replace:
```csharp
// WRONG: sends to tenant
var tenant = await _userRepo.FindByIdAsync(tenantId);
if (tenant != null)
    _email.SendAsync(new EmailMessage(tenant.Email, "Request Cancelled", "Your rental request has been cancelled."));
```

With:
```csharp
// CORRECT: notify owner of cancellation
var listing = request.Listing;
if (listing?.Property?.OwnerId != null)
{
    var owner = await _userRepo.FindByIdAsync(listing.Property.OwnerId);
    if (owner != null)
        _email.SendAsync(new EmailMessage(owner.Email, "Rental Request Cancelled",
            $"A tenant has cancelled their rental request for your listing: {listing.Title}."));
}
```

Note: verify `FindByIdAsync` on `IRentalRequestRepository` includes `Listing.Property` navigation, or add `.Include(x => x.Listing).ThenInclude(x => x.Property)` in the repo.

## Document Errors to Fix

| # | Error |
|---|-------|
| 1 | Participant `CancelRentalRequestController` → rename to `TenantRentalRequestController` (throughout all tables, messages, notes) |
| 2 | Msg 1.2 method `findTenantRequests` → `FindByTenantIdAsync` |
| 3 | Msg 1.2 return type `RentalRequestList` → `List<RentalRequest>` |
| 4 | Msg 2.2 and 3.2 method `findById` → `FindByIdAsync` |
| 5 | Msg 3.4 method `update` → `UpdateAsync` |

## Todo

- [ ] Fix `TenantRentalRequestController.SubmitCancellation` — send email to owner, not tenant
- [ ] Verify `FindByIdAsync` includes `Listing.Property` navigation (needed for `OwnerId`)
- [ ] Run `dotnet build` — zero errors
- [ ] Fix participant name `CancelRentalRequestController` → `TenantRentalRequestController` in diagram
- [ ] Fix Msg 1.2: method `findTenantRequests` → `FindByTenantIdAsync`, return type `RentalRequestList` → `List<RentalRequest>`
- [ ] Fix Msg 2.2, 3.2: `findById` → `FindByIdAsync`
- [ ] Fix Msg 3.4: `update` → `UpdateAsync`

## Success Criteria

- Email sent to owner with "Rental Request Cancelled" subject
- `dotnet build` passes
- Diagram participant is `TenantRentalRequestController`
- Msg 1.2 uses `FindByTenantIdAsync` with `List<RentalRequest>` return type
- Msg 2.2, 3.2 use `FindByIdAsync`
- Msg 3.4 uses `UpdateAsync`
