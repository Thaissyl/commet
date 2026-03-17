# Design Communication Diagram: UC-02 View Room Details - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: `VisitorUI -> Controller`, then `Controller -> Repository` and `Controller -> Gateway`
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label when a response payload is expected
- Separate reply arrows are intentionally omitted because `out` parameters already represent returned data
- Request flow style: synchronous request handling with synchronous external map query (gateway enforces strict timeout to prevent HTTP hang)
- **DTO mapping happens internally within controller operations** — when repository returns `RoomListing`, controller internally extracts fields and builds `RoomDetailResponseDto` before returning to UI

## Object Layout

```text
Visitor --- VisitorUI --- RoomDetailController
                            |--- IRoomListingRepository --- RoomListing
                            |--- IGoogleMapsGateway --- MapData --- Google Maps
```

## Participants

| Position | Object                 | Stereotype             |
| -------- | ---------------------- | ---------------------- |
| 1        | Visitor                | Actor (primary)        |
| 2        | VisitorUI              | `<<user interaction>>` |
| 3        | RoomDetailController   | `<<coordinator>>`      |
| 4        | IRoomListingRepository | `<<database wrapper>>` |
| 5        | RoomListing            | `<<data abstraction>>` |
| 6        | IGoogleMapsGateway     | `<<proxy>>`            |
| 7        | MapData                | `<<data abstraction>>` |
| 8        | Google Maps            | Actor (secondary)      |

> **Note**: `RoomListing` and `MapData` are included as participants because they are data types that flow through this UC via `out` parameters. However, they are **not message targets** — the controller uses them internally to build response DTOs.

## Messages

| #   | From -> To                                     | Message                                                                    |
| --- | ---------------------------------------------- | -------------------------------------------------------------------------- |
| 1   | Visitor -> VisitorUI                           | `selectRoomListing(in listingId: Guid)`                                    |
| 1.1 | VisitorUI -> RoomDetailController              | `getRoomDetail(in listingId: Guid, out response: RoomDetailResponseDto)`   |
| 1.2 | RoomDetailController -> IRoomListingRepository | `findById(in listingId: Guid, out listing: RoomListing)`                   |
| 2   | Visitor -> VisitorUI                           | `requestMapLocation()`                                                     |
| 2.1 | VisitorUI -> RoomDetailController              | `getPropertyMap(in address: String, out response: PropertyMapResponseDto)` |
| 2.2 | RoomDetailController -> IGoogleMapsGateway     | `getLocationData(in address: String, out mapData: MapData)`                |
| 2.3 | IGoogleMapsGateway -> Google Maps              | `getLocationData(in address: String, out mapData: MapData)`                |

## Analysis → Design Message Mapping

| Analysis message                                                           | Design message                                                                                                      | Notes                                                                       |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `1` Visitor → VisitorUI: "select room listing"                             | `1` Visitor -> VisitorUI: `selectRoomListing(in listingId: Guid)`                                                   | Actor trigger; listingId carried explicitly                                 |
| `1.1` VisitorUI → RoomDetailCoordinator: "listing selected (listing id)"   | `1.1` VisitorUI -> RoomDetailController: `getRoomDetail(in listingId: Guid, out response: RoomDetailResponseDto)`   | Coordinator renamed to Controller per ASP.NET mapping                       |
| `1.2` RoomDetailCoordinator → RoomListingLogic: "get listing details"      | —                                                                                                                   | Collapsed into controller; no separate service needed for a read-only fetch |
| `1.3` RoomListingLogic → RoomListing: "fetch listing data"                 | `1.2` RoomDetailController -> IRoomListingRepository: `findById(in listingId: Guid, out listing: RoomListing)`      | Repository loads the data abstraction object                                |
| `1.4–1.6` reply chain                                                       | —                                                                                                                   | Represented by `out response` in message `1.1`; DTO mapping happens internally in controller |
| `2` Visitor → VisitorUI: "request map location"                            | `2` Visitor -> VisitorUI: `requestMapLocation()`                                                                    | Actor trigger; no params needed (address taken from UI state)               |
| `2.1` VisitorUI → RoomDetailCoordinator: "map location requested"          | `2.1` VisitorUI -> RoomDetailController: `getPropertyMap(in address: String, out response: PropertyMapResponseDto)` | UI passes address string from previously loaded room detail                 |
| `2.2` RoomDetailCoordinator → GoogleMapsProxy: "request property location" | `2.2` RoomDetailController -> IGoogleMapsGateway: `getLocationData(in address: String, out mapData: MapData)`       | Proxy renamed to Gateway; synchronous query                                 |
| `2.3–2.5` GoogleMapsProxy ↔ Google Maps exchange                           | `2.3` IGoogleMapsGateway -> Google Maps: `getLocationData(in address: String, out mapData: MapData)`                | External map API call; synchronous because response data is required        |

## Alternative Flow Notes

- At message `1.2`, if no listing is found for the given `listingId`, or if `listing.status` is not publicly visible, the repository returns null and the controller returns an error response; message group `2` is never initiated.
- At message `2.2`, if the Google Maps API is unavailable or times out, `IGoogleMapsGateway` returns an error indicator and `response` reports that map information is temporarily unavailable; room detail previously loaded in group `1` remains unaffected.
- The synchronous call to `IGoogleMapsGateway` requires strict timeout enforcement (e.g., 3-5 seconds) to prevent HTTP response blocking if the external service is degraded.
- If the visitor does not trigger `requestMapLocation()`, message group `2` is skipped entirely.

## Notes

- `VisitorUI` is shown explicitly so the human actor does not interact directly with the backend controller.
- `IRoomListingRepository` loads `RoomListing` (`<<data abstraction>>`) from persistence; the controller then **internally** extracts fields from this object to build `RoomDetailResponseDto` — this is not a separate message but internal coordinator logic.
- `IGoogleMapsGateway` returns `MapData` to the controller; the controller **internally** extracts fields to build `PropertyMapResponseDto` — this is not a separate message but internal coordinator logic.
- `RoomDetailController` acts as the simplified orchestration point: load from repository → internally map to response DTO; and separately, query gateway → internally map to response DTO.
- The synchronous external call is intentional because map data is required for the same HTTP response; timeout handling in `IGoogleMapsGateway` prevents indefinite blocking.
