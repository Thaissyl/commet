# Phase 03: Document Fix — Rewrite UC-02 step-3.0-design-communication-diagram.md

**Status:** Ready (no code changes needed — code is correct)
**Priority:** High
**File:** `C:\Users\welterial\commet\260310-hmss\phase-3\uc-02-view-room-details-aspnet-react\step-3.0-design-communication-diagram.md`

## Context Links

- Use case spec: `C:\Users\welterial\commet\260310-hmss\step-1.3-uc-02-view-room-details.md`
- Analysis model: `C:\Users\welterial\commet\260310-hmss\phase-2\step-2.2-uc-02-view-room-details-main-seq.md`
- Code: `backend/Hmss.Api/Controllers/ViewRoomController.cs`
- Code: `backend/Hmss.Api/Repositories/Interfaces/IRoomListingRepository.cs`
- Code: `backend/Hmss.Api/Gateways/Interfaces/IGoogleMapsGateway.cs`

## Errors Being Fixed

| # | Error |
|---|-------|
| 1 | `RoomListing <<data abstraction>>` is a participant — it's a return type, not a message-passing object; must be removed |
| 2 | Object layout shows `IRoomListingRepository --- RoomListing` link — must be removed |
| 3 | Msg 2.1 wrong signature: `getMapInformation(in locationData: String)` — actual code takes `Guid listingId`, not a location string |
| 4 | Missing msg 2.2: `GetMapInformation` re-fetches listing via `FindVisibleListingByIdAsync` before calling gateway — undocumented in diagram |
| 5 | Design note claims "UI passes locationData directly (stateless)" — false; server re-fetches by ID for security |
| 6 | Method casing: `getMapData` → `GetMapDataAsync`, `getRoomDetails` → `GetRoomDetails`, `findVisibleListingById` → `FindVisibleListingByIdAsync` |

## Why Code is Correct (No Code Change)

The original spec said the UI passes `locationData` string directly to sequence 2. The actual implementation instead accepts `listingId` (Guid) and re-fetches the listing server-side to get the location. This is **more secure** — the server controls what location string is sent to Google Maps, preventing client-supplied location spoofing. Document should reflect this intentional design decision.

## Corrected Document Content

### Design Communication Decision (header block)

```
- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: VisitorUI -> ViewRoomController, then Controller -> IRoomListingRepository and Controller -> IGoogleMapsGateway
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label
- Separate reply arrows intentionally omitted — `out` parameters represent returned data
- Request flow style: synchronous request handling with read-only query optimization
- Business logic bypass: controller queries repository directly — simple visibility check, no logic layer needed
```

### Object Layout

```text
Visitor --- VisitorUI --- ViewRoomController
                          |--- IRoomListingRepository
                          |--- IGoogleMapsGateway --- Google Maps
```

### Participants Table

| Position | Object | Stereotype |
|---|---|---|
| 1 | Visitor | Actor (primary) |
| 2 | VisitorUI | `<<user interaction>>` |
| 3 | ViewRoomController | `<<coordinator>>` |
| 4 | IRoomListingRepository | `<<database wrapper>>` |
| 5 | IGoogleMapsGateway | `<<proxy>>` |
| 6 | Google Maps | Actor (secondary) |

> `RoomListing` removed — it is an entity return type, not a message-passing object. Communication diagrams only show objects that send or receive messages.

### Messages Table

> Only messages traceable to the analysis model are shown. Implicit DTO mapping is not shown.

| # | From -> To | Message |
|---|---|---|
| 1 | Visitor -> VisitorUI | Listing Selection |
| 1.1 | VisitorUI -> ViewRoomController | `GetRoomDetails(in listingId: Guid, out response: RoomDetailDto)` |
| 1.2 | ViewRoomController -> IRoomListingRepository | `FindVisibleListingByIdAsync(in id: Guid, out listing: RoomListing)` |
| 1.3 | VisitorUI -> Visitor | Room Details Display |
| 2 | Visitor -> VisitorUI | [Optional] Map Request |
| 2.1 | VisitorUI -> ViewRoomController | `GetMapInformation(in listingId: Guid, out response: MapDto)` |
| 2.2 | ViewRoomController -> IRoomListingRepository | `FindVisibleListingByIdAsync(in id: Guid, out listing: RoomListing)` |
| 2.3 | ViewRoomController -> IGoogleMapsGateway | `GetMapDataAsync(in location: string, out mapData: MapDto)` |
| 2.4 | IGoogleMapsGateway -> Google Maps | `geocode(in address: string, out coordinates: Coordinates)` |
| 2.5 | VisitorUI -> Visitor | Map Information Display |

### Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
|---|---|---|
| `1.1` VisitorUI -> ViewRoomCoordinator: "Room Detail Request" | `1.1` VisitorUI -> ViewRoomController: `GetRoomDetails(...)` | renamed |
| `1.2` ViewRoomCoordinator -> RoomListing: "Room Detail Query (with Visibility Check)" | `1.2` ViewRoomController -> IRoomListingRepository: `FindVisibleListingByIdAsync(...)` | visibility check inside query |
| `2.1` VisitorUI -> ViewRoomCoordinator: "Map Info Request" | `2.1` VisitorUI -> ViewRoomController: `GetMapInformation(in listingId: Guid, ...)` | takes ID, not locationData string |
| `2.2` ViewRoomCoordinator -> GoogleMapsProxy: "Map Data Request" | `2.2` ViewRoomController -> IRoomListingRepository: `FindVisibleListingByIdAsync(...)` + `2.3` ViewRoomController -> IGoogleMapsGateway: `GetMapDataAsync(...)` | controller re-fetches listing to resolve location server-side before calling gateway |
| `2.3-2.4` GoogleMapsProxy -> Google Maps: "Map Request/Data" | `2.4` IGoogleMapsGateway -> Google Maps: `geocode(...)` | same |

### Alternative Flow Notes

- **Step 1.2: Listing not visible / not found** — `FindVisibleListingByIdAsync` returns null; controller returns `404 NotFound`; use case ends
- **Step 2.2: Listing not found during map request** — `FindVisibleListingByIdAsync` returns null; controller returns `404 NotFound`
- **Step 2.3: Google Maps unavailable** — `GetMapDataAsync` catches exception; returns empty `MapDto`; response contains no map data; continues to 2.5

### Notes

- `VisitorUI` shown explicitly — human actor does not interact directly with backend controller.
- `ViewRoomController` is stateless. Sequence 2 re-queries the repository independently; no state held from sequence 1.
- **Server-side location resolution (Messages 2.2–2.3)**: `GetMapInformation` accepts `listingId` (not a location string). Controller re-fetches the listing to resolve `Property.MapLocation ?? Property.Address` server-side before passing to `IGoogleMapsGateway`. This prevents client-supplied location spoofing. The original spec note "UI passes locationData directly" was a design error — corrected here.
- **Visibility check in query**: `FindVisibleListingByIdAsync` filters `Status IN ('PublishedAvailable', 'Hidden')`. Handles the concurrency edge case where listing status changes between UC-01 (search) and UC-02 (view details).
- **Relational JOIN abstraction**: `IRoomListingRepository` performs SQL JOINs internally to fetch `Property.Name`, `Property.Address`, `Property.GeneralPolicies`. These joins are not shown as separate messages.
- **Proxy timeout handling**: `GoogleMapsGateway` uses `HttpClient.Timeout = 5s`. Exception caught; returns empty `MapDto` gracefully.
- **No RoomListing participant**: `RoomListing` is a CLR entity returned as `out` data — not an object with behaviour. Only objects that send or receive messages appear in a communication diagram.
- Actor-to-UI messages (1, 1.3, 2, 2.5) use noun phrases — physical user interactions, not code method calls.

## Todo

- [ ] Read current `step-3.0-design-communication-diagram.md`
- [ ] Replace Object Layout (remove `IRoomListingRepository --- RoomListing` link)
- [ ] Replace Participants table (remove `RoomListing`, 6 participants total)
- [ ] Replace Messages table (fix 2.1 signature, add 2.2 repo call, fix casing)
- [ ] Replace Analysis → Design Mapping table
- [ ] Replace Alternative Flow Notes
- [ ] Replace Notes section (fix stateless note, add server-side location resolution explanation)

## Success Criteria

- 6 participants (no `RoomListing`)
- Msg 2.1 takes `Guid listingId` (not `String locationData`)
- Msg 2.2 shows `FindVisibleListingByIdAsync` in sequence 2
- Msg 2.3 is `GetMapDataAsync` on `IGoogleMapsGateway`
- Notes explain server-side location resolution as intentional security decision
- All method names match actual C# code (PascalCase, `Async` suffix)
