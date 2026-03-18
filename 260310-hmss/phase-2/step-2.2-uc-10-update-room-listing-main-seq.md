# Communication Diagram: UC-10 Update Room Listing - Analysis Model

## Object Layout

```text
Owner --- OwnerUI --- UpdateRoomListingCoordinator --- RoomListingRules --- RoomListing
                                      |
                                      --- CloudStorageProxy --- Cloud Storage
```

## Participants

| Position | Object                      | Stereotype             | Justification                                                                                               |
| -------- | --------------------------- | ---------------------- | ----------------------------------------------------------------------------------------------------------- |
| 1        | Owner                       | Actor (primary)        | The human user initiating the update.                                                                       |
| 2        | OwnerUI                     | `<<user interaction>>` | Boundary object receiving physical inputs and displaying information.                                        |
| 3        | UpdateRoomListingCoordinator | `<<coordinator>>`      | Control object sequencing the overall flow of the use case.                                                  |
| 4        | RoomListingRules            | `<<business logic>>`   | Encapsulates business rules for validating the modified fields.                                              |
| 5        | CloudStorageProxy           | `<<proxy>>`            | Boundary object hiding the details of the external storage API.                                              |
| 6        | Cloud Storage               | Actor (secondary)      | The external system receiving the new image uploads.                                                         |
| 7        | RoomListing                 | `<<entity>>`           | Conceptual data object encapsulating the room listing record.                                                |

## Messages (Main Sequence)

| #   | From -> To                                        | Message / Information Passed     | Use Case Step |
| --- | ------------------------------------------------- | -------------------------------- | ------------- |
| 1   | Owner -> OwnerUI                                  | Listing Selection                | Step 1        |
| 1.1 | OwnerUI -> UpdateRoomListingCoordinator           | Listing Detail Request           |               |
| 1.2 | UpdateRoomListingCoordinator -> RoomListing       | Listing Detail Query             |               |
| 1.3 | RoomListing -> UpdateRoomListingCoordinator       | Listing Detail Data              |               |
| 1.4 | UpdateRoomListingCoordinator -> OwnerUI           | Editable Listing Form            | Step 2        |
| 1.5 | OwnerUI -> Owner                                  | Editable Form Display            |               |
| 2   | Owner -> OwnerUI                                  | Listing Modifications and New Images | Step 3     |
| 2.1 | OwnerUI -> UpdateRoomListingCoordinator           | Validation and Upload Request    |               |
| 2.2 | UpdateRoomListingCoordinator -> RoomListingRules  | Modified Fields Validation Check | Step 4        |
| 2.3 | RoomListingRules -> UpdateRoomListingCoordinator  | Validation Result (Valid)        |               |
| 2.4 | UpdateRoomListingCoordinator -> CloudStorageProxy  | [If new images] Image Upload Request | Step 4     |
| 2.5 | CloudStorageProxy -> Cloud Storage                | Image Upload                     |               |
| 2.6 | Cloud Storage -> CloudStorageProxy                | Image Upload Confirmation        |               |
| 2.7 | CloudStorageProxy -> UpdateRoomListingCoordinator  | Upload Result (Success)          |               |
| 2.8 | UpdateRoomListingCoordinator -> OwnerUI           | Updated Listing Review Prompt    |               |
| 2.9 | OwnerUI -> Owner                                  | Listing Review Display           |               |
| 3   | Owner -> OwnerUI                                  | Update Confirmation              | Step 5        |
| 3.1 | OwnerUI -> UpdateRoomListingCoordinator           | Update Saving Request            |               |
| 3.2 | UpdateRoomListingCoordinator -> RoomListing       | Updated Listing Record           | Step 6        |
| 3.3 | UpdateRoomListingCoordinator -> OwnerUI           | Update Success                   | Step 7        |
| 3.4 | OwnerUI -> Owner                                  | Update Success Message           |               |

## Alternative Sequences

| #    | From -> To                                        | Message / Information Passed                  | Use Case Step       |
| ---- | ------------------------------------------------- | -------------------------------------------- | ------------------- |
| 2.3a | RoomListingRules -> UpdateRoomListingCoordinator  | [Invalid fields] Validation Result (Invalid) | Alt Step 4.1        |
| 2.4a | UpdateRoomListingCoordinator -> OwnerUI           | Correction/Error Prompt                      |                     |
| 2.5a | OwnerUI -> Owner                                  | Error Display                                | Returns to Step 3   |
| 2.7b | CloudStorageProxy -> UpdateRoomListingCoordinator  | [Storage unavailable] Upload Result (Failure) | Alt Step 4.1     |
| 2.8b | UpdateRoomListingCoordinator -> OwnerUI           | Upload Error Prompt                          |                     |
| 2.9b | OwnerUI -> Owner                                  | Upload Error Display                         | Returns to Step 3   |

## Architectural Notes

- **Analysis vs. Design**: In this analysis model, messages use descriptive noun phrases (e.g., `Updated Listing Record`) rather than operation signatures (e.g., `updateListing(in, out)`). The focus is on what the system does, not how it's programmed.
- **Conditional Image Upload**: Message 2.4 includes `[If new images]` to indicate that image upload only occurs if the user actually uploaded new images. If no new images, this step is bypassed.
- **External Service Integration**: This use case demonstrates integration with an external secondary actor (`Cloud Storage`). The `CloudStorageProxy` (`<<proxy>>`) hides the technical complexity from the rest of the application.
- **Separation of Concerns**: The `UpdateRoomListingCoordinator` delegates: (1) validation to `RoomListingRules` (`<<business logic>>`), (2) image upload to `CloudStorageProxy` (`<<proxy>>`), and (3) persistence to `RoomListing` (`<<entity>>`).
- **Explicit Returns**: The analysis model shows explicit data flow (e.g., `Listing Detail Data` in Message 1.3, `Upload Result (Success)` in Message 2.7). In the design phase, these will be embedded into `out` parameters of synchronous calls.

Use `/drawio-communication-diagram` to generate a visual `.drawio` file from this blueprint.
