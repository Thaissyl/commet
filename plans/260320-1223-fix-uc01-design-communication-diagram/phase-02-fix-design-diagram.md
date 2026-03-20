# Phase 02: Document Fix — Rewrite step-3.0-design-communication-diagram.md

**Status:** Blocked by Phase 01
**Priority:** High
**File:** `C:\Users\welterial\commet\260310-hmss\phase-3\uc-01-search-hostel-room-aspnet-react\step-3.0-design-communication-diagram.md`

## Context Links

- Plan Phase 01: `phase-01-code-fix.md`
- Analysis model: `C:\Users\welterial\commet\260310-hmss\phase-2\step-2.2-uc-01-search-hostel-room-main-seq.md`
- Code (post-fix): `RoomSearchController.cs`, `SearchMatchingService.cs`, `IRoomListingRepository.cs`, `IGoogleMapsGateway.cs`

## Errors Being Fixed

| # | Error |
|---|-------|
| 1 | `SearchMatchingService` missing as participant — analysis `SearchRules` maps to this |
| 2 | `RoomListingList` must be removed — return type, not a message-passing object |
| 3 | Controller named `SearchRoomController` → must be `RoomSearchController` |
| 4 | `findByCriteria` on repository missing → now `FindByCriteriaAsync` after Phase 01 |
| 5 | Wrong DTO names: `SearchPageDto` → `SearchPageResponseDto`, `SearchResultDto` → `SearchResponseDto` |
| 6 | `getMapData(MapDto)` → `GetLocationDataAsync(List<LocationDataDto>)` |
| 7 | Design decision note claims "bypasses logic layer" → false; `SearchMatchingService` is used |

## Corrected Document Content

### Design Communication Decision (header block)

```
- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: VisitorUI -> RoomSearchController, then Controller -> IRoomListingRepository,
  Controller -> SearchMatchingService, Controller -> IGoogleMapsGateway
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label
- Separate reply arrows intentionally omitted — `out` parameters represent returned data
- Request flow style: synchronous request handling
- Business logic: SearchMatchingService handles criteria filtering (sequence 2) and DTO projection (sequences 1 & 2)
```

### Object Layout

```text
Visitor --- VisitorUI --- RoomSearchController
                          |--- SearchMatchingService
                          |--- IRoomListingRepository
                          |--- IGoogleMapsGateway --- Google Maps
```

### Participants Table

| Position | Object | Stereotype |
|---|---|---|
| 1 | Visitor | Actor (primary) |
| 2 | VisitorUI | `<<user interaction>>` |
| 3 | RoomSearchController | `<<coordinator>>` |
| 4 | SearchMatchingService | `<<business logic>>` |
| 5 | IRoomListingRepository | `<<database wrapper>>` |
| 6 | IGoogleMapsGateway | `<<proxy>>` |
| 7 | Google Maps | Actor (secondary) |

> `RoomListingList` removed — `List<RoomListing>` is a CLR return type, not a message-passing object. Communication diagrams only show objects that send or receive messages.

### Messages Table

> Only messages traceable to the analysis model are shown. `BuildListingSummaries` (implicit DTO mapping) has no analysis model counterpart — not shown.

| # | From -> To | Message |
|---|---|---|
| 1 | Visitor -> VisitorUI | Search Function Access |
| 1.1 | VisitorUI -> RoomSearchController | `GetSearchPage(out response: SearchPageResponseDto)` |
| 1.2 | RoomSearchController -> IRoomListingRepository | `FindPublishedListingsAsync(out list: List<RoomListing>)` |
| 1.3 | RoomSearchController -> IGoogleMapsGateway | `GetLocationDataAsync(in listings: List<RoomListing>, out locationData: List<LocationDataDto>)` |
| 1.4 | IGoogleMapsGateway -> Google Maps | `geocode(in address: string, out coordinates: Coordinates)` |
| 1.5 | VisitorUI -> Visitor | Search Form and Initial Listings Display |
| 2 | Visitor -> VisitorUI | Search Criteria Submission |
| 2.1 | VisitorUI -> RoomSearchController | `SearchRooms(in criteria: SearchCriteriaDto, out response: SearchResponseDto)` |
| 2.2 | RoomSearchController -> SearchMatchingService | `ValidateCriteria(in criteria: SearchCriteriaDto, out isValid: bool)` |
| 2.3 | RoomSearchController -> IRoomListingRepository | `FindByCriteriaAsync(in criteria: SearchCriteriaDto, out filtered: List<RoomListing>)` |
| 2.4 | RoomSearchController -> IGoogleMapsGateway | `GetLocationDataAsync(in listings: List<RoomListing>, out locationData: List<LocationDataDto>)` |
| 2.5 | IGoogleMapsGateway -> Google Maps | `geocode(in address: string, out coordinates: Coordinates)` |
| 2.6 | VisitorUI -> Visitor | Matching Listings and Map Display |
### Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
|---|---|---|
| `1.1` VisitorUI -> SearchRoomCoordinator: "Initial Search Page Request" | `1.1` VisitorUI -> RoomSearchController: `GetSearchPage(...)` | renamed |
| `1.2-1.3` SearchRoomCoordinator -> RoomListing: "Published Listings Query/Data" | `1.2` RoomSearchController -> IRoomListingRepository: `FindPublishedListingsAsync(...)` | direct DB read |
| `1.4-1.7` SearchRoomCoordinator -> GoogleMapsProxy -> Google Maps | `1.3` RoomSearchController -> IGoogleMapsGateway: `GetLocationDataAsync(...)` | per-listing coords, not single MapDto |
| `2.1` VisitorUI -> SearchRoomCoordinator: "Search Criteria Submission" | `2.1` VisitorUI -> RoomSearchController: `SearchRooms(...)` | renamed |
| `2.2` SearchRoomCoordinator -> SearchRules: "Criteria Validation Check" | `2.2` RoomSearchController -> SearchMatchingService: `ValidateCriteria(...)` | SearchRules → SearchMatchingService |
| `2.4-2.5` SearchRoomCoordinator -> RoomListing: "Matching Listings Query/Data" | `2.3` RoomSearchController -> IRoomListingRepository: `FindByCriteriaAsync(...)` | DB-level filter + in-memory amenities |
| `2.6-2.9` SearchRoomCoordinator -> GoogleMapsProxy -> Google Maps | `2.4` RoomSearchController -> IGoogleMapsGateway: `GetLocationDataAsync(...)` | same as 1.3 |

### Alternative Flow Notes

- **Step 2.2: Invalid criteria** — `ValidateCriteria` returns `isValid=false` (e.g. MinPrice > MaxPrice); controller returns `400 BadRequest`; no DB query executed
- **Step 2.2: Empty criteria** — all fields null; `ValidateCriteria` returns valid; `FindByCriteriaAsync` applies no filters, returns all published
- **Step 2.3: No matches** — `FindByCriteriaAsync` returns empty list; `SearchResponseDto.HasResults = false`; UI shows revision prompt; returns to step 2
- **Step 1.3 / 2.4: Google Maps unavailable** — `GetLocationDataAsync` catches per-listing exceptions; returns partial or empty `List<LocationDataDto>`; listings still returned without map pins

### Notes

- `VisitorUI` shown explicitly — human actor does not interact directly with backend controller.
- `RoomSearchController` is the stateless coordinator. Does not retain state between sequences 1 and 2.
- **SearchMatchingService role**: `<<business logic>>` participant. Corresponds to `SearchRules` in analysis model. Provides `ValidateCriteria` (shown in diagram) and `BuildListingSummaries` (implicit DTO mapping — not shown).
- **FindByCriteriaAsync filtering strategy**: Most criteria (location, price, dates, furnishing, WC) filtered at DB level via EF Core LINQ. Amenities filtered in-memory within the repository after `ToListAsync()` — EF Core cannot translate JSON array containment to SQL.
- **Stateless coordinator**: `RoomSearchController` always executes fresh queries; no state held between sequences.
- **Proxy timeout handling**: `GoogleMapsGateway` uses `HttpClient.Timeout = 5s`. Per-listing exceptions caught and logged; partial results returned gracefully.
- **No RoomListingList participant**: `List<RoomListing>` is a CLR return type — not a message-passing object. Only objects that send or receive messages appear in a communication diagram.
- Actor-to-UI messages (1, 1.5, 2, 2.6, 3) use noun phrases — physical user interactions, not code method calls.

## Todo

- [ ] Verify Phase 01 code fix is complete before starting
- [ ] Rewrite `step-3.0-design-communication-diagram.md` with corrected content above
- [ ] Verify all method names match final code exactly

## Success Criteria

- 7 participants listed (no RoomListingList; SearchMatchingService present)
- Controller named `RoomSearchController` throughout
- Message 2.2 is `ValidateCriteria` on `SearchMatchingService`
- Message 2.3 is `FindByCriteriaAsync` on `IRoomListingRepository`
- `BuildListingSummaries` NOT shown (implicit DTO mapping, no analysis counterpart)
- `GetLocationDataAsync` used (not `getMapData`)
- `SearchResponseDto` / `SearchPageResponseDto` used throughout
- Analysis → Design mapping correctly traces `SearchRules` → `SearchMatchingService.ValidateCriteria`
