# Design Communication Diagram: UC-09 Create Room Listing - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: `OwnerUI -> CreateRoomListingController`, then `Controller -> Repository`, `Controller -> RoomListingLogic`, and `Controller -> ICloudStorageGateway`
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label when a response payload is expected
- Separate reply arrows are intentionally omitted because `out` parameters already represent returned data
- Request flow style: synchronous request handling

## Object Layout

```text
Owner --- OwnerUI --- CreateRoomListingController
                       |--- IRoomListingRepository --- RoomListing
                       |--- RoomListingLogic
                       |--- ICloudStorageGateway --- Cloud Storage
```

## Participants

| Position | Object                       | Stereotype             |
| -------- | ---------------------------- | ---------------------- |
| 1        | Owner                        | Actor (primary)        |
| 2        | OwnerUI                      | `<<user interaction>>` |
| 3        | CreateRoomListingController  | `<<coordinator>>`      |
| 4        | RoomListingLogic             | `<<business logic>>`   |
| 5        | ICloudStorageGateway         | `<<proxy>>`            |
| 6        | Cloud Storage                | Actor (secondary)      |
| 7        | IRoomListingRepository       | `<<database wrapper>>` |
| 8        | RoomListing                  | `<<data abstraction>>` |

## Messages

| #   | From -> To                                  | Message                                                            |
| --- | ------------------------------------------- | ------------------------------------------------------------------ |
| 1   | Owner -> OwnerUI                            | Room Creation Access                                               |
| 1.1 | OwnerUI -> CreateRoomListingController      | `getRoomListingForm(in propertyId: Guid, out response: RoomListingFormResponseDto)` |
| 1.2 | OwnerUI -> Owner                            | Room Listing Form Display                                          |
| 2   | Owner -> OwnerUI                            | Room Information and Images Input                                  |
| 2.1 | OwnerUI -> CreateRoomListingController      | `processListingDetails(in request: RoomListingDraftDto, in images: FileList, out response: ProcessListingResponseDto)` |
| 2.2 | CreateRoomListingController -> RoomListingLogic | `validateRequiredFields(in request: RoomListingDraftDto, out result: ValidationResult)` |
| 2.3 | CreateRoomListingController -> ICloudStorageGateway | `uploadImages(in images: FileList, out imageUrls: List<String>)`  |
| 2.4 | ICloudStorageGateway -> Cloud Storage       | `uploadImages(in images: FileList, out imageUrls: List<String>)`  |
| 2.5 | OwnerUI -> Owner                            | Room Review Display                                                |
| 3   | Owner -> OwnerUI                            | Saving Confirmation                                                |
| 3.1 | OwnerUI -> CreateRoomListingController      | `saveDraftListing(in request: RoomListingDraftDto, in imageUrls: List<String>, out response: ListingResponseDto)` |
| 3.2 | CreateRoomListingController -> IRoomListingRepository | `save(in entity: RoomListing, out persisted: RoomListing)`       |
| 3.3 | OwnerUI -> Owner                            | Draft Saved Message                                               |

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
| ----------------- | -------------- | ----- |
| `1.1` OwnerUI -> CreateRoomListingCoordinator: "Room Creation Form Request" | `1.1` OwnerUI -> CreateRoomListingController: `getRoomListingForm(in propertyId: Guid, out response: RoomListingFormResponseDto)` | sync, renamed to code-style |
| `1.2` CreateRoomListingCoordinator -> OwnerUI: "Room Creation Form" | implicit in `1.1` response | form data returned |
| `2.1` OwnerUI -> CreateRoomListingCoordinator: "Validation and Upload Request" | `2.1` OwnerUI -> CreateRoomListingController: `processListingDetails(in request: RoomListingDraftDto, in images: FileList, out response: ProcessListingResponseDto)` | sync, generic method name |
| `2.2` CreateRoomListingCoordinator -> RoomListingRules: "Required Fields Validation Check" | `2.2` CreateRoomListingController -> RoomListingLogic: `validateRequiredFields(in request: RoomListingDraftDto, out result: ValidationResult)` | sync, business logic handles validation |
| `2.4` CreateRoomListingCoordinator -> CloudStorageProxy: "Image Upload Request" | `2.3` CreateRoomListingController -> ICloudStorageGateway: `uploadImages(in images: FileList, out imageUrls: List<String>)` | sync with reply, URLs returned |
| `2.5` CloudStorageProxy -> Cloud Storage: "Image Upload" | `2.4` ICloudStorageGateway -> Cloud Storage: `uploadImages(in images: FileList, out imageUrls: List<String>)` | sync propagation |
| `2.6` Cloud Storage -> CloudStorageProxy: "Image Upload Confirmation" | embedded in `2.3`/`2.4` out parameter | reply via `out imageUrls` |
| `2.7` CloudStorageProxy -> CreateRoomListingCoordinator: "Upload Result (Success)" | embedded in `2.1` response | imageUrls included in response |
| `2.8` CreateRoomListingCoordinator -> OwnerUI: "Review Prompt" | `2.5` OwnerUI -> Owner | room review with image previews |
| `3.1` OwnerUI -> CreateRoomListingCoordinator: "Draft Saving Request" | `3.1` OwnerUI -> CreateRoomListingController: `saveDraftListing(in request: RoomListingDraftDto, in imageUrls: List<String>, out response: ListingResponseDto)` | sync, renamed, imageUrls forwarded |
| `3.2` CreateRoomListingCoordinator -> RoomListing: "New Draft Record" | `3.2` CreateRoomListingController -> IRoomListingRepository: `save(in entity: RoomListing, out persisted: RoomListing)` | sync, DTO mapping implicit |
| `3.3` CreateRoomListingCoordinator -> OwnerUI: "Saving Success" | `3.3` OwnerUI -> Owner | success confirmation |

## Alternative Flow Notes

- **Step 2.2: Validation fails** - `ValidationResult.isValid = false`, response contains field error details, messages 2.3 and 2.4 are skipped, use case returns to step 2
- **Step 2.3: Cloud Storage unavailable or timeout** - Gateway returns failure exception or invalid result, response contains upload error, use case returns to step 2
- **Step 3.2: Database error on save** - Repository throws exception, response contains error, use case ends

## Notes

- `OwnerUI` is shown explicitly so the human actor does not interact directly with the backend controller.
- `IRoomListingRepository` handles persistence and returns the created `RoomListing` entity with database-generated values.
- `CreateRoomListingController` acts as the simplified orchestration point for this use case.
- `RoomListingLogic` encapsulates the listing field validation business rules: required fields (title, price, capacity), format validation (amenities, dates), and policy constraints.
- `ICloudStorageGateway` handles synchronous image upload to external cloud storage. The upload operation returns `imageUrls` in the `out` parameter so the controller can embed them in the `RoomListing` entity and the UI can display image previews in the review step.
- **Synchronous Image Upload with Reply**: Messages 2.3 and 2.4 use `uploadImages(in images: FileList, out imageUrls: List<String>)`. The URLs are returned to the controller for embedding in the entity and to the UI for preview display.
- **Parameter Forwarding Pattern**: The `imageUrls` captured in sequence 2 (via `processListingDetails`) are passed back to the controller in sequence 3 via `saveDraftListing(in request, in imageUrls)`. This maintains statelessness while preserving data between the two interactions.
- **Two-phase operation**: Sequence 2 handles validation and image upload (`processListingDetails`). Sequence 3 handles the actual listing persistence (`saveDraftListing`). This separates the preview/validation phase from the persistence phase.
- **Implicit Instantiation**: Between messages 3.1 and 3.2, the controller implicitly instantiates the `RoomListing <<data abstraction>>` object in RAM using data mapped from `RoomListingDraftDto`, the `imageUrls`, and the `propertyId` foreign key. The `status = Draft` is set during this instantiation. This mapping is not shown as a separate message to keep the diagram clean.
- **Proxy Timeout Handling**: The `ICloudStorageGateway` must implement a strict connection timeout limit. If `Cloud Storage` fails to respond, the proxy returns a failure exception to the controller, preventing indefinite blocking.
- **Initial listing state**: Newly created listings have `status = Draft` and are ready for subsequent publishing workflow (UC-11).
- **Stateless coordinator**: The controller operates across two distinct interactions (processing in Sequence 2 and saving in Sequence 3). The UI passes the `RoomListingDraftDto` and `imageUrls` back to the controller in Sequence 3, so the controller does not preserve user state in memory between requests.
- Actor-to-UI messages (1, 1.2, 2, 2.5, 3, 3.3) use noun phrases because they represent physical user interactions, not code method calls.
- **Property entity omission**: The `Property` entity is not a participant in this UC because its state is not queried or modified. The `propertyId` is passed as a foreign key parameter during listing creation. This follows the COMET principle of "only participating objects are depicted" and optimizes memory usage by avoiding loading the entire parent entity when only the ID is needed for the database relationship.
