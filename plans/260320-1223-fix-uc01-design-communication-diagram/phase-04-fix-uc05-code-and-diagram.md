# Phase 04: Fix UC-05 — Code Bug + Design Diagram

**Status:** Ready
**Priority:** High

## Context Links

- Use case: `C:\Users\welterial\commet\260310-hmss\step-1.3-uc-05-submit-rental-request.md`
- Analysis: `C:\Users\welterial\commet\260310-hmss\phase-2\step-2.2-uc-05-submit-rental-request-main-seq.md`
- Design diagram: `C:\Users\welterial\commet\260310-hmss\phase-3\uc-05-submit-rental-request-aspnet-react\step-3.0-design-communication-diagram.md`
- Code: `backend/Hmss.Api/Controllers/SubmitRentalRequestController.cs`
- Code: `backend/Hmss.Api/Logic/RentalRequestLogic.cs`

## Code Bug — Wrong Email Recipient

**Use case step 7:** "System sends a notification that a new rental request has been received **to the Owner**."

**Actual code** sends email to `tenant.Email` ("Your rental request has been submitted") — owner is never notified.

### Fix in SubmitRentalRequestController.cs

Replace the email block:
```csharp
// WRONG: sends to tenant
var tenant = await _userRepo.FindByIdAsync(tenantId);
if (tenant != null)
{
    _email.SendAsync(new EmailMessage(tenant.Email, "Rental Request Submitted",
        $"Your rental request for {listing.Title} has been submitted."));
}
```

With:
```csharp
// CORRECT: notify owner of new request
if (listing.Property?.OwnerId != null)
{
    var owner = await _userRepo.FindByIdAsync(listing.Property.OwnerId);
    if (owner != null)
        _email.SendAsync(new EmailMessage(owner.Email, "New Rental Request Received",
            $"A new rental request has been submitted for your listing: {listing.Title}."));
}
```

Note: `listing.Property` is populated via `Include(x => x.Property)` in `FindByIdAsync` — verify this includes Property, or switch to `FindByIdAsync` that does include it.

## Document Errors to Fix

| # | Error |
|---|-------|
| 1 | `RoomListing <<data abstraction>>` participant — remove (return type, not message-passing) |
| 2 | `RentalRequest <<data abstraction>>` participant — remove (same) |
| 3 | Object layout lines `IRoomListingRepository --- RoomListing` and `IRentalRequestRepository --- RentalRequest` — remove |
| 4 | Msg 3.3: `validateRequestability(in listing, in request, out result)` → `ValidateRequestabilityWithDuplicateCheckAsync(in listing: RoomListing, in tenantId: Guid, out result: ValidationResult)` |
| 5 | Msg 3.5-3.6 label "Owner Notification" correct in intent — but fix `sendAsync` target to owner after code fix |
| 6 | Method casing: `findById` → `FindByIdAsync`, `save` → `SaveAsync` |

## Corrected Participants (8 → 6)

| Position | Object | Stereotype |
|---|---|---|
| 1 | Tenant | Actor (primary) |
| 2 | TenantUI | `<<user interaction>>` |
| 3 | SubmitRentalRequestController | `<<coordinator>>` |
| 4 | IRoomListingRepository | `<<database wrapper>>` |
| 5 | RentalRequestLogic | `<<business logic>>` |
| 6 | IRentalRequestRepository | `<<database wrapper>>` |
| 7 | IEmailGateway | `<<proxy>>` |
| 8 | Email Provider | Actor (secondary) |

## Corrected Object Layout

```text
Tenant --- TenantUI --- SubmitRentalRequestController
                             |--- IRoomListingRepository
                             |--- RentalRequestLogic
                             |--- IRentalRequestRepository
                             |--- IEmailGateway --- Email Provider
```

## Corrected Messages (sequence 3 only — 1 & 2 unchanged)

| # | From -> To | Message |
|---|---|---|
| 3 | Tenant -> TenantUI | Submission Confirmation |
| 3.1 | TenantUI -> SubmitRentalRequestController | `SubmitRentalRequest(in request: RentalRequestDto, out response: SubmissionResponseDto)` |
| 3.2 | SubmitRentalRequestController -> IRoomListingRepository | `FindByIdAsync(in id: Guid, out listing: RoomListing)` |
| 3.3 | SubmitRentalRequestController -> RentalRequestLogic | `ValidateRequestabilityWithDuplicateCheckAsync(in listing: RoomListing, in tenantId: Guid, out result: ValidationResult)` |
| 3.4 | SubmitRentalRequestController -> IRentalRequestRepository | `SaveAsync(in entity: RentalRequest, out persisted: RentalRequest)` |
| 3.5 | SubmitRentalRequestController -> IEmailGateway | `SendAsync(in message: EmailMessage)` |
| 3.6 | IEmailGateway -> Email Provider | `SendAsync(in message: EmailMessage)` |
| 3.7 | TenantUI -> Tenant | Submission Success |

## Todo

- [ ] Fix `SubmitRentalRequestController.cs` — send email to owner, not tenant
- [ ] Verify `FindByIdAsync` includes `Property` navigation (needed for `OwnerId`)
- [ ] Run `dotnet build` — zero errors
- [ ] Rewrite `step-3.0-design-communication-diagram.md` with corrected participants, layout, messages

## Success Criteria

- Email sent to owner's email address with "New Rental Request Received" subject
- `dotnet build` passes
- Design diagram has 8 participants (no data abstraction objects)
- Msg 3.3 shows `ValidateRequestabilityWithDuplicateCheckAsync` with correct signature
