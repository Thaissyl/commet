# Phase 09: Fix UC-10 — Code Bugs + Design Diagram

**Status:** Ready
**Priority:** High

## Context Links

- Use case: `C:\Users\welterial\commet\260310-hmss\step-1.3-uc-10-update-room-listing.md`
- Analysis: `C:\Users\welterial\commet\260310-hmss\phase-2\step-2.2-uc-10-update-room-listing-main-seq.md`
- Design diagram: `C:\Users\welterial\commet\260310-hmss\phase-3\uc-10-update-room-listing-aspnet-react\step-3.0-design-communication-diagram.md`
- Code: `backend/Hmss.Api/Controllers/RoomListingController.cs`

## Code Bugs

### Bug 1 — Missing validation in ProcessListingUpdates

Diagram msg 2.3: `validateUpdates(in entity: RoomListing, in request: RoomListingUpdateDto, out result: ValidationResult)` — never called in code.

**Fix in `ProcessListingUpdates`:** Add validation before upload:
```csharp
var listing = await _listingRepo.FindByIdAsync(listingId);
if (listing == null) return NotFound();

// ADD: validate before upload
// var validation = _listingLogic.ValidateUpdates(listing, request);
// if (!validation.IsValid) return BadRequest(new { Errors = validation.Errors });

var imageUrls = newImages.Count > 0 ? await _storage.UploadImagesAsync(newImages) : new List<string>();
```

Note: verify `RoomListingLogic` has `ValidateUpdates(RoomListing, RoomListingUpdateDto)` — add if missing.

### Bug 2 — Image URLs from process step never applied in SubmitListingUpdate

```csharp
var newImageUrls = new List<string>(); // hardcoded empty — images never applied
```

The `newImageUrls` must come from the request body. Fix: add `ImageUrls` to `RoomListingUpdateDto` and read from request, or accept as separate param.

```csharp
// Fix: read imageUrls from DTO
var newImageUrls = request.ImageUrls ?? new List<string>();
var result = listing.ApplyUpdates(request, newImageUrls);
```

Verify `RoomListingUpdateDto` has `List<string>? ImageUrls` property; add if missing.

## Document Errors

| # | Error |
|---|-------|
| 1 | Participant `UpdateRoomListingController` → `RoomListingController` |
| 2 | Object layout: `IRoomListingRepository --- RoomListing` → remove; add `RoomListing` directly under controller (msg 3.3 goes from controller to `RoomListing`) |
| 3 | Msg 2.1: remove `in request: RoomListingUpdateDto` param — actual: `(Guid listingId, IFormFileCollection newImages)` |
| 4 | Msg 2.4, 2.5: `uploadImages` → `UploadImagesAsync`; `FileList` → `IFormFileCollection` |
| 5 | Msg 3.4: `update` → `UpdateAsync` |

## Todo

- [ ] Add validation call in `ProcessListingUpdates` — call `_listingLogic.ValidateUpdates()` before upload
- [ ] Fix `SubmitListingUpdate` — read `newImageUrls` from request DTO, not hardcoded empty
- [ ] Verify `RoomListingLogic.ValidateUpdates(RoomListing, RoomListingUpdateDto)` exists
- [ ] Verify `RoomListingUpdateDto` has `ImageUrls` property
- [ ] Run `dotnet build` — zero errors
- [ ] Fix participant: `UpdateRoomListingController` → `RoomListingController`
- [ ] Fix object layout: move `RoomListing` under controller
- [ ] Fix Msg 2.1: remove `RoomListingUpdateDto` param
- [ ] Fix Msg 2.4, 2.5: `UploadImagesAsync`, `IFormFileCollection`
- [ ] Fix Msg 3.4: `UpdateAsync`

## Success Criteria

- `ProcessListingUpdates` validates before uploading
- `SubmitListingUpdate` applies image URLs from request
- `dotnet build` passes
- Diagram shows `RoomListingController`, `RoomListing` under controller, correct method names
