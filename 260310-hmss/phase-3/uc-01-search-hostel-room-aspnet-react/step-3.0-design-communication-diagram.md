# Design Communication Diagram: UC-01 Search Hostel Room - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: `VisitorUI -> Controller`, then `Controller -> Repository` and `Controller -> infrastructure collaborators`
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label when a response payload is expected
- Separate reply arrows are intentionally omitted because `out` parameters already represent returned data
- Request flow style: synchronous request handling with synchronous external map data fetch

## Object Layout

```text
Visitor --- VisitorUI --- RoomSearchController
                            |--- IRoomListingRepository --- RoomListing
                            |--- SearchMatchingService
                            |--- IGoogleMapsGateway --- Google Maps
```

## Participants

| Position | Object | Stereotype |
| --- | --- | --- |
| 1 | Visitor | Actor (primary) |
| 2 | VisitorUI | `<<user interaction>>` |
| 3 | RoomSearchController | `<<coordinator>>` |
| 4 | IRoomListingRepository | `<<database wrapper>>` |
| 5 | RoomListing | `<<data abstraction>>` |
| 6 | SearchMatchingService | `<<service>>` |
| 7 | IGoogleMapsGateway | `<<proxy>>` |
| 8 | Google Maps | Actor (secondary) |

## Messages

| # | From -> To | Message |
| --- | --- | --- |
| 1 | Visitor -> VisitorUI | `openSearch()` |
| 1.1 | VisitorUI -> RoomSearchController | `getSearchPage(out response: SearchPageResponseDto)` |
| 1.2 | RoomSearchController -> IRoomListingRepository | `findPublishedListings(out listings: RoomListingList)` |
| 1.3 | RoomSearchController -> SearchMatchingService | `buildListingSummaries(in listings: RoomListingList, out summaries: ListingSummaryList)` |
| 1.4 | RoomSearchController -> IGoogleMapsGateway | `getLocationData(in listings: RoomListingList, out locationData: LocationDataList)` |
| 1.5 | IGoogleMapsGateway -> Google Maps | `getLocationData(in listings: RoomListingList, out locationData: LocationDataList)` |
| 2 | Visitor -> VisitorUI | `submitSearch(in criteria: SearchCriteriaDto)` |
| 2.1 | VisitorUI -> RoomSearchController | `searchRooms(in criteria: SearchCriteriaDto, out response: SearchResponseDto)` |
| 2.2 | RoomSearchController -> IRoomListingRepository | `findListingsByCriteria(in criteria: SearchCriteriaDto, out matchedListings: RoomListingList)` |
| 2.3 | RoomSearchController -> SearchMatchingService | `buildListingSummaries(in listings: RoomListingList, out summaries: ListingSummaryList)` |
| 2.4 | RoomSearchController -> IGoogleMapsGateway | `getLocationData(in listings: RoomListingList, out locationData: LocationDataList)` |
| 2.5 | IGoogleMapsGateway -> Google Maps | `getLocationData(in listings: RoomListingList, out locationData: LocationDataList)` |
| 3 | Visitor -> VisitorUI | `selectListing(in listingId: Guid)` |
| 3.1 | VisitorUI -> RoomSearchController | `getListingEntryPoint(in listingId: Guid, out response: ListingEntryPointResponseDto)` |
| 3.2 | RoomSearchController -> IRoomListingRepository | `findById(in listingId: Guid, out listing: RoomListing)` |

## Alternative Flow Notes

- At message `1.4` / `2.4`, if Google Maps is unavailable, `IGoogleMapsGateway` returns an empty or partial `locationData` and the controller includes listings in the response without map information.
- At message `2.2`, if no listing matches the submitted criteria, `matchedListings` is empty; the response at `2.1` carries a zero-result payload and the UI informs the visitor that no matching room is available.
- At message `2`, if the visitor submits with no criteria, `criteria` is treated as empty-filter by `findListingsByCriteria` and all published listings are returned using the default ordering.
- At message `3.2`, if the requested `listingId` does not exist or is unpublished, `IRoomListingRepository` returns an empty result and `RoomSearchController` responds with a not-found error.

## Notes

- `VisitorUI` is shown explicitly so the human actor does not interact directly with the backend controller.
- `IRoomListingRepository` handles persistence — `findListingsByCriteria` pushes filtering to the SQL engine so the full listing table is never loaded into memory; `findById` retrieves a single listing for Sequence 3.
- `RoomListing` (`<<data abstraction>>`) is the in-memory representation of listing data returned by the repository; it implements information hiding so the controller and service work with structured domain objects rather than raw database rows.
- `SearchMatchingService` owns listing summary construction only; criteria filtering was moved to the repository layer for performance.
- `IGoogleMapsGateway` encapsulates the Google Maps API call; the controller uses its response directly without delegating this to `SearchMatchingService` (COMET rule: business logic / service never calls proxy).
- UC-01 is a read-only use case — no write or mutate operations are performed and no `applyXxxChange` pattern is needed.
- Map data fetch is synchronous because the search response depends on it; the gateway must enforce a strict timeout so a Google Maps outage does not block the HTTP response.
