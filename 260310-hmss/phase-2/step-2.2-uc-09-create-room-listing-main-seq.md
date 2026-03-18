# Communication Diagram: UC-09 Create Room Listing - Analysis Model

## Object Layout

```text
Owner --- OwnerUI --- CreateRoomListingCoordinator --- RoomListingRules
                                      |                         |
                                      |                         --- RoomListing
                                      |
                                      --- CloudStorageProxy --- Cloud Storage
```

## Participants

| Position | Object                      | Stereotype             | Justification                                                                                               |
| -------- | --------------------------- | ---------------------- | ----------------------------------------------------------------------------------------------------------- |
| 1        | Owner                       | Actor (primary)        | The human user initiating the room listing use case.                                                        |
| 2        | OwnerUI                     | `<<user interaction>>` | Boundary object communicating directly with the human user by receiving physical inputs and providing outputs. |
| 3        | CreateRoomListingCoordinator | `<<coordinator>>`      | Control object that makes overall decisions and determines the sequencing for the use case without holding state. |
| 4        | RoomListingRules            | `<<business logic>>`   | Encapsulates the business-specific application rules, such as verifying required fields.                      |
| 5        | CloudStorageProxy           | `<<proxy>>`            | Boundary object serving as the local representative of the external system, hiding the technical details of communication. |
| 6        | Cloud Storage               | Actor (secondary)      | The external system actor receiving the uploaded images.                                                      |
| 7        | RoomListing                 | `<<entity>>`           | Conceptual data-intensive object representing the new draft room listing.                                     |

## Messages (Main Sequence)

| #   | From -> To                                        | Message / Information Passed     | Use Case Step |
| --- | ------------------------------------------------- | -------------------------------- | ------------- |
| 1   | Owner -> OwnerUI                                  | Room Creation Access             | Step 1        |
| 1.1 | OwnerUI -> CreateRoomListingCoordinator           | Room Creation Form Request       |               |
| 1.2 | CreateRoomListingCoordinator -> OwnerUI           | Room Creation Form               |               |
| 1.3 | OwnerUI -> Owner                                  | Form Display                     | Step 2        |
| 2   | Owner -> OwnerUI                                  | Room Information and Images Input | Step 3        |
| 2.1 | OwnerUI -> CreateRoomListingCoordinator           | Validation and Upload Request    |               |
| 2.2 | CreateRoomListingCoordinator -> RoomListingRules  | Required Fields Validation Check | Step 4        |
| 2.3 | RoomListingRules -> CreateRoomListingCoordinator  | Validation Result (Valid)        |               |
| 2.4 | CreateRoomListingCoordinator -> CloudStorageProxy  | Image Upload Request             | Step 4        |
| 2.5 | CloudStorageProxy -> Cloud Storage                | Image Upload                     |               |
| 2.6 | Cloud Storage -> CloudStorageProxy                | Image Upload Confirmation        |               |
| 2.7 | CloudStorageProxy -> CreateRoomListingCoordinator  | Upload Result (Success)          |               |
| 2.8 | CreateRoomListingCoordinator -> OwnerUI           | Review Prompt                    |               |
| 2.9 | OwnerUI -> Owner                                  | Room Review Display              | Step 5        |
| 3   | Owner -> OwnerUI                                  | Saving Confirmation              | Step 5        |
| 3.1 | OwnerUI -> CreateRoomListingCoordinator           | Draft Saving Request             |               |
| 3.2 | CreateRoomListingCoordinator -> RoomListing       | New Draft Record                 | Step 6        |
| 3.3 | CreateRoomListingCoordinator -> OwnerUI           | Saving Success                   | Step 7        |
| 3.4 | OwnerUI -> Owner                                  | Draft Saved Message              |               |

## Alternative Sequences

| #    | From -> To                                        | Message / Information Passed                  | Use Case Step    |
| ---- | ------------------------------------------------- | -------------------------------------------- | ---------------- |
| 2.3a | RoomListingRules -> CreateRoomListingCoordinator  | [Incomplete fields] Validation Result (Invalid) | Alt Step 4.1     |
| 2.4a | CreateRoomListingCoordinator -> OwnerUI           | Correction Prompt                            |                  |
| 2.5a | OwnerUI -> Owner                                  | Correction Display                           | Returns to 2     |
| 2.7b | CloudStorageProxy -> CreateRoomListingCoordinator  | [Storage unavailable] Upload Result (Failure) | Alt Step 4.1     |
| 2.8b | CreateRoomListingCoordinator -> OwnerUI           | Upload Error Prompt                          |                  |
| 2.9b | OwnerUI -> Owner                                  | Upload Error Display                         | Returns to 2     |

## Architectural Notes

- **Analysis vs. Design**: In this analysis model, messages use descriptive noun phrases (e.g., `New Draft Record`) rather than operation signatures (e.g., `createDraftListing(in, out)`). The focus is on what the system does, not how it's programmed.
- **Only Participating Objects**: The `Property` entity is intentionally omitted because its state is not being updated or queried in this use case. The UI already knows the `propertyId` from the precondition and passes it as an input parameter.
- **Foreign Key Mapping**: In the design phase, the parent Property's primary key will be embedded as a foreign key in the `RoomListing` entity. Only the ID is needed to establish the database link, not the entire Property object loaded into RAM.
- **External Service Integration**: This use case demonstrates integration with an external secondary actor (`Cloud Storage`). The `CloudStorageProxy` (`<<proxy>>`) hides the technical complexity (API endpoints, authentication, network protocols) from the rest of the application.
- **Separation of Concerns**: The `CreateRoomListingCoordinator` delegates: (1) validation to `RoomListingRules` (`<<business logic>>`), (2) image upload to `CloudStorageProxy` (`<<proxy>>`), and (3) persistence to `RoomListing` (`<<entity>>`).
- **Explicit Returns**: The analysis model shows explicit data flow (e.g., `Image Upload Confirmation` in Message 2.6, `Upload Result (Success)` in Message 2.7). In the design phase, these will be embedded into `out` parameters of synchronous calls.
- **Stateless Coordinator**: The controller operates across two distinct interactions (validation/upload in Sequence 2 and saving in Sequence 3). The UI passes the data back to the controller in Sequence 3 so the controller does not have to preserve user state in memory between requests.

Use `/drawio-communication-diagram` to generate a visual `.drawio` file from this blueprint.
