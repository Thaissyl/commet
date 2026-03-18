# Communication Diagram: UC-01 Search Hostel Room - Analysis Model

## Object Layout

```text
Visitor --- VisitorUI --- SearchRoomCoordinator --- SearchRules --- RoomListing
                                     |
                                     --- GoogleMapsProxy --- Google Maps
```

## Participants

| Position | Object                | Stereotype             | Justification                                                             |
| -------- | --------------------- | ---------------------- | ------------------------------------------------------------------------- |
| 1        | Visitor               | Actor (primary)        | The human user initiating the search.                                     |
| 2        | VisitorUI             | `<<user interaction>>` | Boundary object receiving inputs and displaying search forms/results.     |
| 3        | SearchRoomCoordinator | `<<coordinator>>`      | Control object sequencing the overall flow of the search use case.        |
| 4        | SearchRules           | `<<business logic>>`   | Encapsulates conceptual rules for validating the entered search criteria. |
| 5        | GoogleMapsProxy       | `<<proxy>>`            | Boundary object hiding the technical details of the external map API.     |
| 6        | Google Maps           | Actor (secondary)      | The external system providing map data.                                   |
| 7        | RoomListing           | `<<entity>>`           | Conceptual data object encapsulating the published room listing records.  |

## Messages (Main Sequence)

| #    | From -> To                               | Message / Information Passed             | Use Case Step |
| ---- | ---------------------------------------- | ---------------------------------------- | ------------- |
| 1    | Visitor -> VisitorUI                     | Search Function Access                   | Step 1        |
| 1.1  | VisitorUI -> SearchRoomCoordinator       | Initial Search Page Request              |               |
| 1.2  | SearchRoomCoordinator -> RoomListing     | Published Listings Query                 |               |
| 1.3  | RoomListing -> SearchRoomCoordinator     | Published Listings Data                  |               |
| 1.4  | SearchRoomCoordinator -> GoogleMapsProxy | Map Data Request                         |               |
| 1.5  | GoogleMapsProxy -> Google Maps           | Map Request                              |               |
| 1.6  | Google Maps -> GoogleMapsProxy           | Map Data                                 |               |
| 1.7  | GoogleMapsProxy -> SearchRoomCoordinator | Map Data                                 |               |
| 1.8  | SearchRoomCoordinator -> VisitorUI       | Search Form, Published Listings, and Map | Step 2        |
| 1.9  | VisitorUI -> Visitor                     | Initial Search Display                   |               |
| 2    | Visitor -> VisitorUI                     | Search Criteria Submission               | Step 3        |
| 2.1  | VisitorUI -> SearchRoomCoordinator       | Search Criteria Data                     |               |
| 2.2  | SearchRoomCoordinator -> SearchRules     | Criteria Validation Check                | Step 4        |
| 2.3  | SearchRules -> SearchRoomCoordinator     | Validation Result (Valid)                |               |
| 2.4  | SearchRoomCoordinator -> RoomListing     | Matching Listings Query                  | Step 5        |
| 2.5  | RoomListing -> SearchRoomCoordinator     | Matching Listings Data                   |               |
| 2.6  | SearchRoomCoordinator -> GoogleMapsProxy | Map Data Request                         |               |
| 2.7  | GoogleMapsProxy -> Google Maps           | Map Request                              |               |
| 2.8  | Google Maps -> GoogleMapsProxy           | Map Data                                 |               |
| 2.9  | GoogleMapsProxy -> SearchRoomCoordinator | Map Data                                 |               |
| 2.10 | SearchRoomCoordinator -> VisitorUI       | Matching Listings and Map Information    | Step 6        |
| 2.11 | VisitorUI -> Visitor                     | Matching Listings Display                |               |

## Alternative Sequences

| #     | From -> To                               | Message / Information Passed                | Use Case Step     |
| ----- | ---------------------------------------- | ------------------------------------------- | ----------------- |
| 2.3a  | SearchRules -> SearchRoomCoordinator     | [No criteria] Validation Result (Empty)     | Alt Step 3.1      |
| 2.4a  | SearchRoomCoordinator -> RoomListing     | Published Listings Query (default ordering) | Continues to 2.10 |
| 2.5a  | RoomListing -> SearchRoomCoordinator     | [No match] Empty Listings Data              | Alt Step 4.1      |
| 2.6a  | SearchRoomCoordinator -> VisitorUI       | Revision Prompt                             |                   |
| 2.7a  | VisitorUI -> Visitor                     | No Results Display (Returns to Step 3)      |                   |
| 1.7b  | GoogleMapsProxy -> SearchRoomCoordinator | [Maps unavailable] Map Data Failure         | Alt Step 6.1      |
| 2.9b  | GoogleMapsProxy -> SearchRoomCoordinator | [Maps unavailable] Map Data Failure         | Alt Step 6.1      |
| 2.10b | SearchRoomCoordinator -> VisitorUI       | Matching Listings (no map information)      | Continues to 2.11 |

## Architectural Notes

- **External Service Integration**: This use case integrates with Google Maps external actor via `GoogleMapsProxy` (`<<proxy>>`). Map data is fetched twice: (1) initial page load with published listings, (2) filtered search results.
- **Proxy Timeout Pattern**: In design, `GoogleMapsProxy` must implement strict connection timeout limits. If Google Maps is unavailable/unresponsive, the proxy returns a failure result, and the system proceeds without map data rather than blocking the visitor's UI thread.
- **Separation of Concerns**: The `SearchRoomCoordinator` delegates criteria validation to `SearchRules` (`<<business logic>>`), ensuring proper query construction before database access.
- **Analysis vs. Design**: In this analysis model, messages use descriptive noun phrases (e.g., `Published Listings Query`, `Matching Listings Data`) rather than operation signatures (e.g., `searchListings(in, out)`).
- **Empty Criteria Handling**: Alternative sequence 2.3a-2.4a shows the system gracefully handling "no criteria" submission by querying all published listings with default ordering.

Use `/drawio-communication-diagram` to generate a visual `.drawio` file from this blueprint.
