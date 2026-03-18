# Communication Diagram: UC-02 View Room Details - Analysis Model

## Object Layout

```text
Visitor --- VisitorUI --- ViewRoomCoordinator --- RoomListing
                                  |
                                  --- GoogleMapsProxy --- Google Maps
```

## Participants

| Position | Object               | Stereotype             | Justification                                                                                      |
| -------- | -------------------- | ---------------------- | ---------------------------------------------------------------------------------------------------- |
| 1        | Visitor              | Actor (primary)        | The human user initiating the room detail view.                                                     |
| 2        | VisitorUI            | `<<user interaction>>` | Boundary object receiving physical inputs and displaying information.                        |
| 3        | ViewRoomCoordinator  | `<<coordinator>>`      | Control object sequencing the overall flow without holding state.                             |
| 4        | RoomListing          | `<<entity>>`           | Conceptual data object encapsulating the room, property, and owner data.                          |
| 5        | GoogleMapsProxy      | `<<proxy>>`            | Boundary object hiding the technical details of the external map API.                           |
| 6        | Google Maps          | Actor (secondary)      | The external system providing geographic map data.                                                |

## Messages (Main Sequence)

| #   | From -> To                                   | Message / Information Passed   | Use Case Step |
| --- | -------------------------------------------- | ----------------------------- | ------------- |
| 1   | Visitor -> VisitorUI                         | Listing Selection              | Step 1        |
| 1.1 | VisitorUI -> ViewRoomCoordinator            | Room Detail Request             |               |
| 1.2 | ViewRoomCoordinator -> RoomListing        | Room Detail Query (with Visibility Check) | Step 2       |
| 1.3 | RoomListing -> ViewRoomCoordinator        | Room Detail Data                |               |
| 1.4 | ViewRoomCoordinator -> VisitorUI           | Room Details                    | Step 3        |
| 1.5 | VisitorUI -> Visitor                         | Room Details Display            | Step 4        |
| 2   | Visitor -> VisitorUI                         | [Optional] Map Request          | Step 5        |
| 2.1 | VisitorUI -> ViewRoomCoordinator            | Map Info Request                |               |
| 2.2 | ViewRoomCoordinator -> GoogleMapsProxy    | Map Data Request                |               |
| 2.3 | GoogleMapsProxy -> Google Maps            | Map Request                     |               |
| 2.4 | Google Maps -> GoogleMapsProxy            | Map Data                        |               |
| 2.5 | GoogleMapsProxy -> ViewRoomCoordinator   | Map Data                        |               |
| 2.6 | ViewRoomCoordinator -> VisitorUI           | Map Information                 | Step 6        |
| 2.7 | VisitorUI -> Visitor                         | Map Information Display         | Step 7        |

## Alternative Sequences

| #    | From -> To                                   | Message / Information Passed           | Use Case Step          |
| ---- | -------------------------------------------- | ---------------------------------------- | ----------------------- |
| 1.3a | RoomListing -> ViewRoomCoordinator         | [Not visible] Invalid Status Data        | Alt Step 2.1            |
| 1.4a | ViewRoomCoordinator -> VisitorUI           | Unavailable Error Prompt                |                         |
| 1.5a | VisitorUI -> Visitor                         | Error Display & Redirect                | Alt Step 2.2 (Ends)    |
| 2.5b | GoogleMapsProxy -> ViewRoomCoordinator   | [Maps unavailable] Map Data Failure      | Alt Step 6.1            |
| 2.6b | ViewRoomCoordinator -> VisitorUI           | Room Details (no map information)       | Continues to 2.7         |

## Architectural Notes

- **Precondition vs. Business Logic**: Removed "The selected room listing is publicly visible" from Preconditions. The system must actively check visibility during the transaction (because Owner could have hidden it between search and selection), making this business rule validation, not a precondition. Only valid precondition: "Visitor has access to the system."
- **Explicit Visibility Check**: Step 2 (Room Detail Query with Visibility Check) validates that the listing is still publicly visible before returning details. This handles the concurrency edge case where the listing status changes between UC-01 (Search) and UC-02 (View Details).
- **Bypassed Logic Layer**: For simple read operations like fetching room details, the `ViewRoomCoordinator` queries `RoomListing` directly without a business logic intermediate. This optimizes performance by eliminating unnecessary pass-through layers.
- **Optional Map Request**: Sequence 2 is marked as [Optional] because the visitor may or may not request map information. If not requested, the use case proceeds directly to Step 7 (review details).
- **External Service Timeout**: In design, `GoogleMapsProxy` must implement timeout mechanisms. If Google Maps is unavailable, the system gracefully degrades by displaying room details without map information.

Use `/drawio-communication-diagram` to generate a visual `.drawio` file from this blueprint.
