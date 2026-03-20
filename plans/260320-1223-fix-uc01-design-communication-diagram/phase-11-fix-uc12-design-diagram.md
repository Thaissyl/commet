# Phase 11: Document Fix — Rewrite UC-12 step-3.0-design-communication-diagram.md

**Status:** Ready (no code changes needed)
**File:** `C:\Users\welterial\commet\260310-hmss\phase-3\uc-12-change-listing-visibility-aspnet-react\step-3.0-design-communication-diagram.md`

## Context Links

- Use case: `C:\Users\welterial\commet\260310-hmss\step-1.3-uc-12-change-listing-visibility.md`
- Code: `backend/Hmss.Api/Controllers/RoomListingController.cs`

## Errors Being Fixed

| # | Error |
|---|-------|
| 1 | Participant `ChangeVisibilityController` → `RoomListingController` |
| 2 | Object layout `IRoomListingRepository --- RoomListing` → move `RoomListing` directly under controller |
| 3 | Msg 3.3: `changeVisibility(in action: String, ...)` — no such method; actual code: `listing.Hide()` or `listing.Show()` — fix to `Hide() / Show()` |
| 4 | Msg 1.2, 2.2, 3.2: `findById` → `FindByIdAsync` |
| 5 | Msg 3.4: `update` → `UpdateAsync` |

## Corrected Object Layout

```text
Owner --- OwnerUI --- RoomListingController
                       |--- IRoomListingRepository
                       |--- VisibilityLogic
                       |--- RoomListing
```

## Todo

- [ ] Rename `ChangeVisibilityController` → `RoomListingController` throughout
- [ ] Move `RoomListing` directly under controller in object layout
- [ ] Fix Msg 3.3: `changeVisibility` → `Hide() / Show()` (conditional on action param)
- [ ] Fix Msg 1.2, 2.2, 3.2: `FindByIdAsync`
- [ ] Fix Msg 3.4: `UpdateAsync`

## Success Criteria

- Controller named `RoomListingController`
- `RoomListing` under controller in layout
- Msg 3.3 uses `Hide()` / `Show()`
- All repo methods use correct names with Async suffix
