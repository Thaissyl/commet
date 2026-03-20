# Phase 13: Document Fix — Rewrite UC-14 step-3.0-design-communication-diagram.md

**Status:** Ready (no code changes needed)
**File:** `C:\Users\welterial\commet\260310-hmss\phase-3\uc-14-review-rental-request-aspnet-react\step-3.0-design-communication-diagram.md`

## Context Links

- Use case: `C:\Users\welterial\commet\260310-hmss\step-1.3-uc-14-review-rental-request.md`
- Analysis: `C:\Users\welterial\commet\260310-hmss\phase-2\step-2.2-uc-14-review-rental-request-main-seq.md`
- Code: `backend/Hmss.Api/Controllers/ReviewRentalRequestController.cs`

## Errors Being Fixed

| # | Error |
|---|-------|
| 1 | Participant `ReviewRequestController` → `ReviewRentalRequestController` |
| 2 | Object layout `IRentalRequestRepository --- RentalRequest` — remove; add `RentalRequest` directly under controller (controller calls `request.Accept()`, `request.Reject()` directly) |
| 3 | Object layout `IRoomListingRepository --- RoomListing` — remove; add `RoomListing` directly under controller (controller calls `listing.Lock()` directly) |
| 4 | Msg 1.2: `findByRoomId` → `FindByRoomIdAsync`; `out list: RequestList` → `RequestList` is invented collection name, change to `out requests: List<RentalRequest>` |
| 5 | Msg 2.2: `findById` → `FindByIdAsync` |
| 6 | Msg 3.2: `findById` → `FindByIdAsync` |
| 7 | Msg 3.3: `findByRequestId(in requestId: Guid, ...)` — no such method; code calls `FindByIdAsync(request.ListingId)` — fix to `FindByIdAsync(in listingId: Guid, out entity: RoomListing)` |
| 8 | Msg 3.7: `update` → `UpdateAsync` |
| 9 | Msg 3.8: `update` → `UpdateAsync` |

## Corrected Object Layout

```text
Owner --- OwnerUI --- ReviewRentalRequestController
                       |--- IRentalRequestRepository
                       |--- IRoomListingRepository
                       |--- ReviewRequestLogic
                       |--- RentalRequest
                       |--- RoomListing
                       |--- IEmailGateway --- Email Provider
```

## Todo

- [ ] Rename `ReviewRequestController` → `ReviewRentalRequestController` throughout
- [ ] Fix object layout: remove `IRentalRequestRepository --- RentalRequest`; add `RentalRequest` directly under controller
- [ ] Fix object layout: remove `IRoomListingRepository --- RoomListing`; add `RoomListing` directly under controller
- [ ] Fix Msg 1.2: `FindByRoomIdAsync`; remove `RequestList` → `List<RentalRequest>`
- [ ] Fix Msg 2.2: `FindByIdAsync`
- [ ] Fix Msg 3.2: `FindByIdAsync`
- [ ] Fix Msg 3.3: method `FindByIdAsync`; param `in listingId: Guid`
- [ ] Fix Msg 3.7: `UpdateAsync`
- [ ] Fix Msg 3.8: `UpdateAsync`

## Success Criteria

- Controller named `ReviewRentalRequestController`
- `RentalRequest` and `RoomListing` directly under controller in layout
- All repo methods use correct names with Async suffix
- Msg 3.3 uses `FindByIdAsync(in listingId: Guid)` not `findByRequestId`
