# Phase 08: Document Fix — Rewrite UC-09 step-3.0-design-communication-diagram.md

**Status:** Ready (no code changes needed)
**Priority:** High
**File:** `C:\Users\welterial\commet\260310-hmss\phase-3\uc-09-create-room-listing-aspnet-react\step-3.0-design-communication-diagram.md`

## Context Links

- Use case: `C:\Users\welterial\commet\260310-hmss\step-1.3-uc-09-create-room-listing.md`
- Analysis: `C:\Users\welterial\commet\260310-hmss\phase-2\step-2.2-uc-09-create-room-listing-main-seq.md`
- Code: `backend/Hmss.Api/Controllers/RoomListingController.cs`

## Errors Being Fixed

| # | Error |
|---|-------|
| 1 | Participant `CreateRoomListingController` → `RoomListingController` |
| 2 | `RoomListing <<data abstraction>>` participant — remove (no message sent to it; entity is instantiated implicitly in code) |
| 3 | Object layout `IRoomListingRepository --- RoomListing` line — remove |
| 4 | Msg 2.3, 2.4: `uploadImages` → `UploadImagesAsync`; param type `FileList` → `IFormFileCollection` |
| 5 | Msg 3.1: `in imageUrls: List<String>` is not a separate param — imageUrls is inside `RoomListingDraftDto` (`request.ImageUrls`); remove as separate param |
| 6 | Msg 3.2: `save` → `SaveAsync` |

## Todo

- [ ] Rename `CreateRoomListingController` → `RoomListingController` throughout
- [ ] Remove `RoomListing <<data abstraction>>` from participants table
- [ ] Remove `IRoomListingRepository --- RoomListing` from object layout
- [ ] Fix Msg 2.3, 2.4: `uploadImages` → `UploadImagesAsync`, `FileList` → `do`
- [ ] Fix Msg 3.1: remove `in imageUrls: List<String>` param
- [ ] Fix Msg 3.2: `save` → `SaveAsync`

## Success Criteria

- Controller named `RoomListingController`
- No `RoomListing` participant
- Msg 2.3, 2.4 use `UploadImagesAsync` with `IFormFileCollection`
- Msg 3.1 has no separate `imageUrls` param
- Msg 3.2 uses `SaveAsync`
