# Phase 17: Document Fix — Rewrite UC-18 step-3.0-design-communication-diagram.md

**Status:** Ready (no code changes needed)
**File:** `C:\Users\welterial\commet\260310-hmss\phase-3\uc-18-control-listing-visibility-aspnet-react\step-3.0-design-communication-diagram.md`

## Context Links

- Use case: `C:\Users\welterial\commet\260310-hmss\step-1.3-uc-18-control-listing-visibility.md`
- Analysis: `C:\Users\welterial\commet\260310-hmss\phase-2\step-2.2-uc-18-control-listing-visibility-main-seq.md`
- Code: `backend/Hmss.Api/Controllers/ControlListingController.cs`

## Errors Being Fixed

| # | Error |
|---|-------|
| 1 | Object layout `IRoomListingRepository --- RoomListing` — remove; add `RoomListing` directly under controller (`listing.Archive()` called directly by controller) |
| 2 | Missing `IUserAccountRepository <<database wrapper>>` from participants and layout — used in `GetVisibleListings` and `GetListingDetails` for owner name/email lookup |
| 3 | Msg 1.2: `findByStatus` → `FindByStatusAsync`; `out list: ListingList` — `ListingList` invented; change to `out listings: List<RoomListing>` |
| 4 | Msg 2.2: `findById` → `FindByIdAsync` |
| 5 | Msg 3.2: `findById` → `FindByIdAsync` |
| 6 | Msg 3.4: `disableByAdmin(out result: StatusChangeResult)` → `Archive(out result: StatusChangeResult)` — actual entity method in code is `Archive()`, not `disableByAdmin()` |
| 7 | Msg 3.5: `update` → `UpdateAsync` |

## Corrected Object Layout

```text
System Admin --- AdminUI --- ControlListingController
                              |--- IRoomListingRepository
                              |--- IUserAccountRepository
                              |--- ListingControlLogic
                              |--- NotificationService
                              |--- IEmailGateway --- Email Provider
                              |--- RoomListing
```

## Todo

- [ ] Fix object layout: remove `IRoomListingRepository --- RoomListing`; add `RoomListing` directly under controller
- [ ] Add `IUserAccountRepository <<database wrapper>>` to participants table
- [ ] Add `IUserAccountRepository` under controller in layout
- [ ] Fix Msg 1.2: `FindByStatusAsync`; `List<RoomListing>`
- [ ] Fix Msg 2.2: `FindByIdAsync`
- [ ] Fix Msg 3.2: `FindByIdAsync`
- [ ] Fix Msg 3.4: `disableByAdmin` → `Archive`
- [ ] Fix Msg 3.5: `UpdateAsync`

## Success Criteria

- `RoomListing` directly under controller in layout (not under repository)
- `IUserAccountRepository` present in participants and layout
- Msg 3.4 uses `Archive()` not `disableByAdmin()`
- All repo methods with Async suffix
- No invented collection names
