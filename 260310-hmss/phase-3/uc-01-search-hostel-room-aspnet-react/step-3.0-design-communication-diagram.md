# Design Communication Diagram: UC-01 Search Hostel Room - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: `VisitorUI -> SearchRoomController`, then `Controller -> Repository` and `Controller -> IGoogleMapsGateway`
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label when a response payload is expected
- Separate reply arrows are intentionally omitted because `out` parameters already represent returned data
- Request flow style: synchronous request handling with read-only query optimization
- Business logic bypass: For performance, controller queries repository directly without logic layer

## Object Layout

```text
Visitor --- VisitorUI --- SearchRoomController
                          |--- IRoomListingRepository --- RoomListingList
                          |--- IGoogleMapsGateway --- Google Maps
```

## Participants

| Position | Object                 | Stereotype             |
| -------- | ---------------------- | ---------------------- |
| 1        | Visitor                | Actor (primary)        |
| 2        | VisitorUI              | `<<user interaction>>` |
| 3        | SearchRoomController   | `<<coordinator>>`      |
| 4        | IRoomListingRepository | `<<database wrapper>>` |
| 5        | RoomListingList        | `<<data abstraction>>` |
| 6        | IGoogleMapsGateway     | `<<proxy>>`            |
| 7        | Google Maps            | Actor (secondary)      |

## Messages

| #   | From -> To                              | Message                                                            |
| --- | --------------------------------------- | ------------------------------------------------------------------ |
| 1   | Visitor -> VisitorUI                    | Search Function Access                                             |
| 1.1 | VisitorUI -> SearchRoomController       | `getInitialSearchPage(out response: SearchPageDto)`                |
| 1.2 | SearchRoomController -> IRoomListingRepository | `findPublishedListings(out list: RoomListingList)`             |
| 1.3 | SearchRoomController -> IGoogleMapsGateway | `getMapData(in locations: LocationList, out mapData: MapDto)`  |
| 1.4 | IGoogleMapsGateway -> Google Maps       | `getMapData(in locations: LocationList, out mapData: MapDto)`      |
| 1.5 | VisitorUI -> Visitor                    | Search Form and Initial Listings Display                           |
| 2   | Visitor -> VisitorUI                    | Search Criteria Submission                                         |
| 2.1 | VisitorUI -> SearchRoomController       | `searchRooms(in criteria: SearchCriteriaDto, out response: SearchResultDto)` |
| 2.2 | SearchRoomController -> IRoomListingRepository | `findByCriteria(in criteria: SearchCriteriaDto, out list: RoomListingList)` |
| 2.3 | SearchRoomController -> IGoogleMapsGateway | `getMapData(in locations: LocationList, out mapData: MapDto)`  |
| 2.4 | IGoogleMapsGateway -> Google Maps       | `getMapData(in locations: LocationList, out mapData: MapDto)`      |
| 2.5 | VisitorUI -> Visitor                    | Matching Listings and Map Display                                  |
| 3   | Visitor -> VisitorUI                    | Listings Review                                                    |

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
| ----------------- | -------------- | ----- |
| `1.1` VisitorUI -> SearchRoomCoordinator: "Initial Search Page Request" | `1.1` VisitorUI -> SearchRoomController: `getInitialSearchPage(out response: SearchPageDto)` | sync, renamed |
| `1.2-1.3` SearchRoomCoordinator -> RoomListing: "Published Listings Query/Data" | `1.2` SearchRoomController -> IRoomListingRepository: `findPublishedListings(out list: RoomListingList)` | direct DB read, bypasses logic layer |
| `1.4-1.7` SearchRoomCoordinator -> GoogleMapsProxy -> Google Maps: "Map Data Request/Data" | `1.3` SearchRoomController -> IGoogleMapsGateway: `getMapData(in locations, out mapData)` | sync with reply |
| `2.1-2.3` VisitorUI -> SearchRoomCoordinator -> SearchRules: "Search Criteria Data/Validation Check" | `2.1` VisitorUI -> SearchRoomController: `searchRooms(in criteria, out response)` then `2.2` findByCriteria(...) | bypassed logic layer for performance |
| `2.4-2.5` SearchRoomCoordinator -> RoomListing: "Matching Listings Query/Data" | `2.2` SearchRoomController -> IRoomListingRepository: `findByCriteria(in criteria, out list)` | optimized SQL query |
| `2.6-2.9` SearchRoomCoordinator -> GoogleMapsProxy -> Google Maps: "Map Data Request/Data" | `2.3` SearchRoomController -> IGoogleMapsGateway: `getMapData(in locations, out mapData)` | sync with reply |

## Alternative Flow Notes

- **Step 2.2: Empty criteria** - `criteria` is empty/null, repository returns all published listings with default ordering, continues to step 2.5
- **Step 2.2: No matches found** - `list` is empty, response contains no results message, UI displays revision prompt, returns to step 2
- **Step 1.3: Google Maps unavailable** - Gateway returns failure/null `mapData`, response contains listings without map, continues to step 1.5
- **Step 2.3: Google Maps unavailable** - Gateway returns failure/null `mapData`, response contains listings without map, continues to step 2.5

## Notes

- `VisitorUI` is shown explicitly so the human actor does not interact directly with the backend controller.
- `IRoomListingRepository` handles read-only queries and returns listing collections.
- `SearchRoomController` acts as the simplified orchestration point.
- `IGoogleMapsGateway` handles synchronous map data retrieval. Returns `MapDto` in `out` parameter for UI display.
- **Bypassing Business Logic for Queries (Message 2.2)**: Because the search step strictly involves querying the database based on filters (location, price, dates), routing through a `<<business logic>>` class creates an unnecessary pass-through layer. To satisfy the 3-second nonfunctional performance requirement, the `SearchRoomController` bypasses logic and passes the `SearchCriteriaDto` directly into the `IRoomListingRepository` (`<<database wrapper>>`) to execute optimized SQL queries.
- **Stateless Coordinator (Messages 1.2, 2.2)**: Web controllers must remain perfectly stateless to scale. The `SearchRoomController` does not remember the default listings fetched in Sequence 1. When the visitor submits a search in Sequence 2, it executes a completely fresh `findByCriteria` database query.
- **Proxy Timeout Handling (Alternative 6.1)**: Messages 1.3 and 2.3 invoke the `IGoogleMapsGateway`. Because external API calls carry network latency risks, the `<<proxy>>` object is configured with a strict timeout limit. If Google Maps fails to respond within the allowed threshold, the proxy suppresses the exception, returns a null `MapDto`, and allows the controller to safely return the text listings to the UI without maps, fulfilling Alternative Sequence 6.1 and preserving the 3-second performance requirement.
- **Repository Query Patterns**:
  - `findPublishedListings(out list)` - Fetches all published listings for initial page load (sequence 1)
  - `findByCriteria(in criteria, out list)` - Fetches listings matching search filters (sequence 2)
- **Empty Criteria Handling (Alternative 3.1)**: When visitor submits with no criteria, the `SearchCriteriaDto` is empty/null. The repository interprets this as "return all published listings" and applies default ordering (newest first, relevance, etc.).
- **No Results Handling (Alternative 4.1)**: When `findByCriteria` returns an empty list, the response contains a "no results found" message, and the UI displays a revision prompt inviting the visitor to adjust search criteria.
- **Implicit DTO mapping**: The controller implicitly maps response data from entities to DTOs (`SearchPageDto`, `SearchResultDto`). This mapping is not shown as a separate message.
- Actor-to-UI messages (1, 1.5, 2, 2.5, 3) use noun phrases because they represent physical user interactions, not code method calls.
