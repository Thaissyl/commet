# Design Communication Diagram: UC-10 Update Room Listing - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: `OwnerUI -> UpdateRoomListingController`, then `Controller -> Repository`, `Controller -> RoomListingLogic`, and `Controller -> ICloudStorageGateway`
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label when a response payload is expected
- Separate reply arrows are intentionally omitted because `out` parameters already represent returned data
- Request flow style: synchronous request handling with conditional image upload

## Object Layout

```text
Owner --- OwnerUI --- UpdateRoomListingController
                       |--- IRoomListingRepository --- RoomListing
                       |--- RoomListingLogic
                       |--- ICloudStorageGateway --- Cloud Storage
```

## Participants

| Position | Object                       | Stereotype             |
| -------- | ---------------------------- | ---------------------- |
| 1        | Owner                        | Actor (primary)        |
| 2        | OwnerUI                      | `<<user interaction>>` |
| 3        | UpdateRoomListingController  | `<<coordinator>>`      |
| 4        | RoomListingLogic             | `<<business logic>>`   |
| 5        | ICloudStorageGateway         | `<<proxy>>`            |
| 6        | Cloud Storage                | Actor (secondary)      |
| 7        | IRoomListingRepository       | `<<database wrapper>>` |
| 8        | RoomListing                  | `<<data abstraction>>` |

## Messages

| #   | From -> To                                  | Message                                                            |
| --- | ------------------------------------------- | ------------------------------------------------------------------ |
| 1   | Owner -> OwnerUI                            | Listing Selection                                                 |
| 1.1 | OwnerUI -> UpdateRoomListingController      | `getListingForUpdate(in listingId: Guid, out response: ListingFormResponseDto)` |
| 1.2 | UpdateRoomListingController -> IRoomListingRepository | `findById(in id: Guid, out entity: RoomListing)`                 |
| 1.3 | OwnerUI -> Owner                            | Editable Form Display                                             |
| 2   | Owner -> OwnerUI                            | Listing Modifications and New Images                              |
| 2.1 | OwnerUI -> UpdateRoomListingController      | `processListingUpdates(in request: RoomListingUpdateDto, in newImages: FileList, out response: ProcessUpdateResponseDto)` |
| 2.2 | UpdateRoomListingController -> IRoomListingRepository | `findById(in id: Guid, out entity: RoomListing)`                 |
| 2.3 | UpdateRoomListingController -> RoomListingLogic | `validateUpdates(in entity: RoomListing, in request: RoomListingUpdateDto, out result: ValidationResult)` |
| 2.4 | UpdateRoomListingController -> ICloudStorageGateway | `uploadImages(in images: FileList, out imageUrls: List<String>)`  |
| 2.5 | ICloudStorageGateway -> Cloud Storage       | `uploadImages(in images: FileList, out imageUrls: List<String>)`  |
| 2.6 | OwnerUI -> Owner                            | Listing Review Display                                            |
| 3   | Owner -> OwnerUI                            | Update Confirmation                                               |
| 3.1 | OwnerUI -> UpdateRoomListingController      | `submitListingUpdate(in request: RoomListingUpdateDto, in newImageUrls: List<String>, out response: ListingResponseDto)` |
| 3.2 | UpdateRoomListingController -> IRoomListingRepository | `findById(in id: Guid, out entity: RoomListing)`                 |
| 3.3 | UpdateRoomListingController -> RoomListing  | `applyUpdates(in request: RoomListingUpdateDto, in newImageUrls: List<String>, out result: StatusChangeResult)` |
| 3.4 | UpdateRoomListingController -> IRoomListingRepository | `update(in entity: RoomListing, out persisted: RoomListing)`     |
| 3.5 | OwnerUI -> Owner                            | Update Success Message                                            |

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
| ----------------- | -------------- | ----- |
| `1.1` OwnerUI -> UpdateRoomListingCoordinator: "Listing Detail Request" | `1.1` OwnerUI -> UpdateRoomListingController: `getListingForUpdate(in listingId: Guid, out response: ListingFormResponseDto)` | sync, renamed to code-style |
| `1.2` UpdateRoomListingCoordinator -> RoomListing: "Listing Detail Query" | `1.2` UpdateRoomListingController -> IRoomListingRepository: `findById(in id: Guid, out entity: RoomListing)` | stateless controller fetch |
| `2.1` OwnerUI -> UpdateRoomListingCoordinator: "Validation and Upload Request" | `2.1` OwnerUI -> UpdateRoomListingController: `processListingUpdates(in request: RoomListingUpdateDto, in newImages: FileList, out response: ProcessUpdateResponseDto)` | sync, renamed |
| `2.2` UpdateRoomListingCoordinator -> RoomListingRules: "Modified Fields Validation Check" | `2.2` UpdateRoomListingController -> IRoomListingRepository: `findById(in id: Guid, out entity: RoomListing)` then `2.3` validateUpdates(...) | stateless reload before validation |
| `2.4` UpdateRoomListingCoordinator -> CloudStorageProxy: "[If new images] Image Upload Request" | `2.4` UpdateRoomListingController -> ICloudStorageGateway: `uploadImages(in images: FileList, out imageUrls: List<String>)` | sync with reply, conditional |
| `3.1` OwnerUI -> UpdateRoomListingCoordinator: "Update Saving Request" | `3.1` OwnerUI -> UpdateRoomListingController: `submitListingUpdate(in request: RoomListingUpdateDto, in newImageUrls: List<String>, out response: ListingResponseDto)` | sync, renamed, newImageUrls forwarded |
| `3.2` UpdateRoomListingCoordinator -> RoomListing: "Updated Listing Record" | `3.2` UpdateRoomListingController -> IRoomListingRepository: `findById(in id: Guid, out entity: RoomListing)` then `3.3` applyUpdates(...) then `3.4` update(...) | load, mutate, persist pattern |

## Alternative Flow Notes

- **Step 2.3: Validation fails** - `ValidationResult.isValid = false`, response contains field error details, messages 2.4 and 2.5 are skipped, use case returns to step 2
- **Step 2.4: Cloud Storage unavailable or timeout** - Gateway returns failure exception, response contains upload error, use case returns to step 2
- **Step 3.2: Listing not found** - Repository returns null/error, response contains not found error, use case ends
- **Step 3.4: Database error on update** - Repository throws exception, response contains error, use case ends

## Notes

- `OwnerUI` is shown explicitly so the human actor does not interact directly with the backend controller.
- `IRoomListingRepository` handles persistence and returns the updated `RoomListing` entity.
- `UpdateRoomListingController` acts as the simplified orchestration point for this use case.
- `RoomListingLogic` encapsulates the listing field validation business rules: required fields (title, price, capacity), format validation (amenities, dates), status transition validation, and policy constraints for updates.
- `ICloudStorageGateway` handles synchronous image upload to external cloud storage. The upload operation returns `imageUrls` in the `out` parameter so the controller can update the `imagesRef` attribute and the UI can display image previews in the review step.
- **Conditional Image Upload**: Message 2.4 `uploadImages(in images: FileList, out imageUrls: List<String>)` is only called if the user uploaded new images. If `newImages: FileList` is empty, this step is bypassed and `newImageUrls` in message 3.1 is an empty list or null.
- **Parameter Forwarding Pattern**: The `imageUrls` captured in sequence 2 (via `processListingUpdates`) are passed back to the controller in sequence 3 via `submitListingUpdate(in request, in newImageUrls)`. This maintains statelessness while preserving data between the two interactions.
- **Stateless Coordinator (Message 2.2)**: Because the controller must be stateless, it does not retain the `RoomListing` object from Sequence 1. It issues a fresh `findById()` call to fetch the latest state from the database before validation, allowing business logic to validate against current entity state.
- **Stateless Coordinator (Message 3.2)**: The controller again issues a fresh `findById()` call when the Owner submits the final update in Sequence 3, ensuring data accuracy at time of persistence.
- **Separation of State Mutation and Persistence (Messages 3.3 & 3.4)**:
  - Message 3.3: `applyUpdates(in request, in newImageUrls)` on `RoomListing` (`<<data abstraction>>`) mutates the internal state in RAM. The domain object handles its own state mutation.
  - Message 3.4: `update(in entity, out persisted)` on `IRoomListingRepository` (`<<database wrapper>>`) executes the SQL UPDATE statement to persist the mutated state, satisfying the ACID Durability requirement.
- **Implicit DTO mapping**: The controller implicitly maps data from `RoomListingUpdateDto` to the `RoomListing` entity attributes. This mapping is not shown as a separate message.
- **Two-phase operation**: Sequence 2 handles validation and optional image upload (`processListingUpdates`). Sequence 3 handles the actual listing update (`submitListingUpdate`). This separates the preview/validation phase from the persistence phase.
- **Proxy Timeout Handling**: The `ICloudStorageGateway` must implement a strict connection timeout limit. If `Cloud Storage` fails to respond, the proxy returns a failure exception to the controller.
- Actor-to-UI messages (1, 1.3, 2, 2.6, 3, 3.5) use noun phrases because they represent physical user interactions, not code method calls.
