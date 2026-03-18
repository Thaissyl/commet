# Example Blueprint

Use this example when you need a concrete source format for a communication-diagram request.

```md
# Communication Diagram: UC-01 Search Hostel Room - Main Sequence

## Object Layout

Visitor --- VisitorUI --- SearchCoordinator --- SearchMatchingLogic --- RoomListing
                                  |
                           GoogleMapsProxy --- Google Maps

## Participants

| Position | Object              | Stereotype             |
| -------- | ------------------- | ---------------------- |
| 1        | Visitor             | Actor (primary)        |
| 2        | VisitorUI           | <<user interaction>>   |
| 3        | SearchCoordinator   | <<coordinator>>        |
| 4        | SearchMatchingLogic | <<business logic>>     |
| 5        | RoomListing         | <<entity>>             |
| 6        | GoogleMapsProxy     | <<proxy>>              |
| 7        | Google Maps         | Actor (secondary)      |

## Messages

| #    | From -> To                               | Message                                           |
| ---- | ---------------------------------------- | ------------------------------------------------- |
| 1    | Visitor -> VisitorUI                     | open search                                       |
| 1.1  | VisitorUI -> SearchCoordinator           | request search page                               |
| 1.2  | SearchCoordinator -> SearchMatchingLogic | request initial published listings                |
| 1.3  | SearchMatchingLogic -> RoomListing       | provide published listings                        |
| 1.4  | SearchMatchingLogic -> SearchCoordinator | listings data                                     |
| 1.5  | SearchCoordinator -> GoogleMapsProxy     | request location data for listings                |
| 1.6  | GoogleMapsProxy -> Google Maps           | location data request                             |
| 1.7  | Google Maps -> GoogleMapsProxy           | location data                                     |
| 1.8  | GoogleMapsProxy -> SearchCoordinator     | location data                                     |
| 1.9  | SearchCoordinator -> VisitorUI           | search form + initial listings with location data |
| 1.10 | VisitorUI -> Visitor                     | display search form with listings                 |

## Notes

- Google Maps is a secondary actor.
- The coordinator calls the proxy, not the business logic, for external map data.
- Default rendering should create separate grouped message blocks for each direction, such as `Visitor -> VisitorUI` and `VisitorUI -> Visitor`.
- In grouped blocks, list only `number: message text` lines under the directional heading.
```
