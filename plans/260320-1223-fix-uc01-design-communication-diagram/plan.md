# Plan: Fix UC-01 & UC-02 — Code + Design Communication Diagram Sync

**Status:** Ready
**Scope:** Code fixes (UC-01, UC-05, UC-06) + document fixes (UC-01, UC-02, UC-05, UC-06)
**Goal:** Align backend code and design diagrams for UC-01, UC-02, UC-05, UC-06.

## Context

**UC-01:** Design diagram missing `SearchMatchingService`, wrong signatures, invalid `RoomListingList` participant. Code missing `FindByCriteriaAsync` and `ValidateCriteria`.

**UC-02:** Design diagram has wrong `GetMapInformation` signature and missing second DB query in sequence 2. Code is correct — document-only fix.

**UC-05:** Code sends email to tenant instead of owner. Design diagram has wrong method signatures and data abstraction participants.

**UC-06:** Code sends cancellation email to tenant instead of owner. Design diagram has wrong controller name and method names.

## Phases

| Phase | Scope | Status |
|-------|-------|--------|
| [Phase 01](phase-01-code-fix.md) | Code: `FindByCriteriaAsync`, `ValidateCriteria`, update controller | Ready |
| [Phase 02](phase-02-fix-design-diagram.md) | Doc: rewrite UC-01 `step-3.0-design-communication-diagram.md` | Blocked by Phase 01 |
| [Phase 03](phase-03-fix-uc02-design-diagram.md) | Doc: rewrite UC-02 `step-3.0-design-communication-diagram.md` | Ready (code already correct) |
| [Phase 04](phase-04-fix-uc05-code-and-diagram.md) | Code + Doc: UC-05 email bug fix + diagram corrections | Ready |
| [Phase 05](phase-05-fix-uc06-code-and-diagram.md) | Code + Doc: UC-06 email bug fix + diagram naming fixes | Ready |
| [Phase 06](phase-06-fix-uc07-design-diagram.md) | Doc: rewrite UC-07 `step-3.0-design-communication-diagram.md` | Ready (no code changes) |
| [Phase 07](phase-07-fix-uc08-design-diagrams.md) | Doc: rewrite UC-08a & UC-08b `step-3.0-design-communication-diagram.md` | Ready (no code changes) |
| [Phase 08](phase-08-fix-uc09-design-diagram.md) | Doc: rewrite UC-09 `step-3.0-design-communication-diagram.md` | Ready (no code changes) |
| [Phase 09](phase-09-fix-uc10-code-and-diagram.md) | Code + Doc: UC-10 missing validation + image URL bug + diagram fixes | Ready |
| [Phase 10](phase-10-fix-uc11-design-diagram.md) | Doc: rewrite UC-11 `step-3.0-design-communication-diagram.md` | Ready (no code changes) |
| [Phase 11](phase-11-fix-uc12-design-diagram.md) | Doc: rewrite UC-12 `step-3.0-design-communication-diagram.md` | Ready (no code changes) |
| [Phase 12](phase-12-fix-uc13-design-diagram.md) | Doc: rewrite UC-13 `step-3.0-design-communication-diagram.md` | Ready (no code changes) |
| [Phase 13](phase-13-fix-uc14-design-diagram.md) | Doc: rewrite UC-14 `step-3.0-design-communication-diagram.md` | Ready (no code changes) |
| [Phase 14](phase-14-fix-uc15-code-and-diagram.md) | Code + Doc: UC-15 email bug fix + diagram corrections | Ready |
| [Phase 15](phase-15-fix-uc16-design-diagram.md) | Doc: rewrite UC-16 `step-3.0-design-communication-diagram.md` | Ready (no code changes) |
| [Phase 16](phase-16-fix-uc17-design-diagram.md) | Doc: rewrite UC-17 `step-3.0-design-communication-diagram.md` | Ready (no code changes) |
| [Phase 17](phase-17-fix-uc18-design-diagram.md) | Doc: rewrite UC-18 `step-3.0-design-communication-diagram.md` | Ready (no code changes) |

## Files Affected

**Code (backend/Hmss.Api/):**
- `Repositories/Interfaces/IRoomListingRepository.cs`
- `Repositories/Implementations/RoomListingRepository.cs`
- `Services/SearchMatchingService.cs`
- `Controllers/RoomSearchController.cs`
- `Controllers/SubmitRentalRequestController.cs`
- `Controllers/TenantRentalRequestController.cs`

**Documents:**
- `C:\Users\welterial\commet\260310-hmss\phase-3\uc-01-search-hostel-room-aspnet-react\step-3.0-design-communication-diagram.md`
- `C:\Users\welterial\commet\260310-hmss\phase-3\uc-02-view-room-details-aspnet-react\step-3.0-design-communication-diagram.md`
- `C:\Users\welterial\commet\260310-hmss\phase-3\uc-05-submit-rental-request-aspnet-react\step-3.0-design-communication-diagram.md`
- `C:\Users\welterial\commet\260310-hmss\phase-3\uc-06-cancel-rental-request-aspnet-react\step-3.0-design-communication-diagram.md`
- `C:\Users\welterial\commet\260310-hmss\phase-3\uc-07-track-rental-request-status-aspnet-react\step-3.0-design-communication-diagram.md`
- `C:\Users\welterial\commet\260310-hmss\phase-3\uc-08a-create-property-aspnet-react\step-3.0-design-communication-diagram.md`
- `C:\Users\welterial\commet\260310-hmss\phase-3\uc-08b-update-property-aspnet-react\step-3.0-design-communication-diagram.md`
- `C:\Users\welterial\commet\260310-hmss\phase-3\uc-09-create-room-listing-aspnet-react\step-3.0-design-communication-diagram.md`
