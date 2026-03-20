# Phase 10: Document Fix — Rewrite UC-11 step-3.0-design-communication-diagram.md

**Status:** Ready (no code changes needed)
**Priority:** High
**File:** `C:\Users\welterial\commet\260310-hmss\phase-3\uc-11-publish-room-listing-aspnet-react\step-3.0-design-communication-diagram.md`

## Context Links

- Use case: `C:\Users\welterial\commet\260310-hmss\step-1.3-uc-11-publish-room-listing.md`
- Analysis: `C:\Users\welterial\commet\260310-hmss\phase-2\step-2.2-uc-11-publish-room-listing-main-seq.md`
- Code: `backend/Hmss.Api/Controllers/RoomListingController.cs`

## Errors Being Fixed

| # | Error |
|---|-------|
| 1 | Participant `PublishListingController` → `RoomListingController` |
| 2 | `OwnerProfile <<data abstraction>>` participant — remove (code returns `bool` from `IsOwnerVerifiedAsync`, no entity loaded) |
| 3 | Object layout `IOwnerRepository --- OwnerProfile` line — remove |
| 4 | Object layout `IRoomListingRepository --- RoomListing` — move `RoomListing` directly under controller (msg 3.3 goes controller → `RoomListing`) |
| 5 | Msg 2.1: remove `in ownerId: Guid` param (comes from JWT) |
| 6 | Msg 2.3: `IOwnerRepository.findById(out entity: OwnerProfile)` → `IOwnerRepository.IsOwnerVerifiedAsync(in ownerId: Guid, out isVerified: bool)` |
| 7 | Msg 2.4: `validateEligibility(in listing: RoomListing, in owner: OwnerProfile, ...)` → `ValidateEligibility(in listing: RoomListing, in isVerified: bool, out result: ValidationResult)` |
| 8 | Msg 1.2, 2.2, 3.2: `findById` → `FindByIdAsync` |
| 9 | Msg 3.4: `update` → `UpdateAsync` |

## Corrected Object Layout

```text
Owner --- OwnerUI --- RoomListingController
                       |--- IRoomListingRepository
                       |--- IOwnerRepository
                       |--- PublishListingLogic
                       |--- RoomListing
```

## Todo

- [ ] Rename participant `PublishListingController` → `RoomListingController`
- [ ] Remove `OwnerProfile <<data abstraction>>` from participants table
- [ ] Remove `IOwnerRepository --- OwnerProfile` from object layout
- [ ] Move `RoomListing` directly under controller in object layout
- [ ] Fix Msg 2.1: remove `in ownerId: Guid`
- [ ] Fix Msg 2.3: `IsOwnerVerifiedAsync(in ownerId: Guid, out isVerified: bool)`
- [ ] Fix Msg 2.4: remove `OwnerProfile` param, add `in isVerified: bool`
- [ ] Fix Msg 1.2, 2.2, 3.2: `FindByIdAsync`
- [ ] Fix Msg 3.4: `UpdateAsync`

## Success Criteria

- Controller named `RoomListingController`
- No `OwnerProfile` participant
- `IOwnerRepository` shows `IsOwnerVerifiedAsync` returning `bool`
- `ValidateEligibility` takes `isVerified: bool` not `OwnerProfile`
- `RoomListing` under controller in layout
- All repo/entity methods use correct names
