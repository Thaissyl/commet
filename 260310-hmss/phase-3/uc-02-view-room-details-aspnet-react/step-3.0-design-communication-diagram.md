# Design Communication Diagram: UC-02 View Room Details - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: `VisitorUI -> ViewRoomController`, then `Controller -> Repository` and `Controller -> IGoogleMapsGateway`
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label when a response payload is expected
- Separate reply arrows are intentionally omitted because `out` parameters already represent returned data
- Request flow style: synchronous request handling with read-only query optimization
- Business logic bypass: For performance, controller queries repository directly without logic layer

## Object Layout

```text
Visitor --- VisitorUI --- ViewRoomController
                          |--- IRoomListingRepository --- RoomListing
                          |--- IGoogleMapsGateway --- Google Maps
```

## Participants

| Position | Object                 | Stereotype             |
| -------- | ---------------------- | ---------------------- |
| 1        | Visitor                | Actor (primary)        |
| 2        | VisitorUI              | `<<user interaction>>` |
| 3        | ViewRoomController     | `<<coordinator>>`      |
| 4        | IRoomListingRepository | `<<database wrapper>>` |
| 5        | RoomListing            | `<<data abstraction>>` |
| 6        | IGoogleMapsGateway     | `<<proxy>>`            |
| 7        | Google Maps            | Actor (secondary)      |

## Messages

| #   | From -> To                              | Message                                                            |
| --- | --------------------------------------- | ------------------------------------------------------------------ |
| 1   | Visitor -> VisitorUI                    | Listing Selection                                                  |
| 1.1 | VisitorUI -> ViewRoomController         | `getRoomDetails(in listingId: Guid, out response: RoomDetailDto)`  |
| 1.2 | ViewRoomController -> IRoomListingRepository | `findVisibleListingById(in id: Guid, out entity: RoomListing)` |
| 1.3 | VisitorUI -> Visitor                    | Room Details Display                                               |
| 2   | Visitor -> VisitorUI                    | Map Request                                                        |
| 2.1 | VisitorUI -> ViewRoomController         | `getMapInformation(in locationData: String, out response: MapDto)` |
| 2.2 | ViewRoomController -> IGoogleMapsGateway | `getMapData(in locationData: String, out mapData: MapDto)`     |
| 2.3 | IGoogleMapsGateway -> Google Maps       | `getMapData(in locationData: String, out mapData: MapDto)`        |
| 2.4 | VisitorUI -> Visitor                    | Map Information Display                                            |

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
| ----------------- | -------------- | ----- |
| `1.1-1.3` VisitorUI -> ViewRoomCoordinator -> RoomListing: "Room Detail Request/Query/Data" | `1.1` VisitorUI -> ViewRoomController: `getRoomDetails(in listingId, out response)` then `1.2` findVisibleListingById(...) | bypassed logic layer for performance |
| `2.1-2.5` VisitorUI -> ViewRoomCoordinator -> GoogleMapsProxy -> Google Maps: "Map Info Request/Data Request/Data" | `2.1` VisitorUI -> ViewRoomController: `getMapInformation(in locationData, out response)` then `2.2` getMapData(...) | stateless: UI passes locationData directly |

## Alternative Flow Notes

- **Step 1.2: Listing not visible** - Repository returns null/error (visibility check in query), response contains unavailable error, use case ends
- **Step 1.2: Listing not found** - Repository returns null/error, response contains not found error, use case ends
- **Step 2.2: Google Maps unavailable** - Gateway returns failure/null `mapData`, response contains map unavailable message, continues to step 2.4

## Notes

- `VisitorUI` is shown explicitly so the human actor does not interact directly with the backend controller.
- `IRoomListingRepository` handles read-only queries and returns the listing entity with joined property/owner data.
- `ViewRoomController` acts as the simplified orchestration point.
- `IGoogleMapsGateway` handles synchronous map data retrieval. Returns `MapDto` in `out` parameter for UI display.
- **Bypassing Business Logic for Queries (Message 1.2)**: Because the system merely needs to retrieve data and verify a simple string/boolean status (Is Visible), passing through a `<<business logic>>` class creates an unnecessary layer. To meet the 3-second nonfunctional performance requirement, the `ViewRoomController` relies on the `IRoomListingRepository` to execute an optimized SQL query (e.g., `SELECT ... WHERE Status = 'Visible'`), directly returning the result.
- **Relational Database JOIN Abstraction**: Although the use case explicitly asks for property name, property address, and basic owner information, Property and Owner entities are not depicted here. In standard COMET relational database design, the `IRoomListingRepository` handles SQL JOINs internally using foreign keys to fetch the requested parent data, mapping it directly into a comprehensive `RoomDetailDto` for the UI.
- **Stateless Coordinator (Message 2.1)**: The `ViewRoomController` remains completely stateless. When the user requests the map in Sequence 2, the UI passes the required `locationData` directly into the `getMapInformation` operation signature. The controller does not preserve the `RoomListing` object in RAM between Sequence 1 and Sequence 2.
- **Proxy Timeout Handling (Alternative 6.1)**: Message 2.2 crosses a network boundary. The `IGoogleMapsGateway` (`<<proxy>>`) object implements a strict connection timeout. If Google Maps fails to respond, the proxy suppresses the exception and returns a predefined failure/null `MapDto`, fulfilling Alternative 6.1 and preventing the UI thread from hanging.
- **Repository Query Pattern**:
  - `findVisibleListingById(in id: Guid, out entity)` - Fetches single listing by ID with visibility check (WHERE clause filters by visible status)
- **Optional Map Request (Sequence 2)**: Sequence 2 is optional—the visitor may or may not request map information. If not requested, the use case proceeds directly to Step 7 (review details) in the original use case description.
- **Implicit DTO mapping**: The controller implicitly maps response data from entities to DTOs (`RoomDetailDto`, `MapDto`). This mapping is not shown as a separate message.
- Actor-to-UI messages (1, 1.3, 2, 2.4) use noun phrases because they represent physical user interactions, not code method calls.
