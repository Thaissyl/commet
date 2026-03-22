# Design Communication Diagram: UC-09 Create Room Listing - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: OwnerUI -> RoomListingController, then Controller -> Repository, Controller -> RoomListingLogic, and Controller -> ICloudStorageGateway
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label
- Separate reply arrows intentionally omitted — `out` parameters represent returned data
- Request flow style: synchronous request handling

## Object Layout

```text
Owner --- OwnerUI --- RoomListingController
                       |--- RoomListingLogic
                       |--- ICloudStorageGateway --- Cloud Storage
                       |--- IRoomListingRepository
```

## Participants

| Position | Object                  | Stereotype             |
| -------- | ----------------------- | ---------------------- |
| 1        | Owner                   | Actor (primary)        |
| 2        | OwnerUI                 | `<<user interaction>>` |
| 3        | RoomListingController   | `<<coordinator>>`      |
| 4        | RoomListingLogic        | `<<business logic>>`   |
| 5        | ICloudStorageGateway    | `<<proxy>>`            |
| 6        | Cloud Storage           | Actor (secondary)      |
| 7        | IRoomListingRepository  | `<<database wrapper>>` |

> `RoomListing` removed — return type only, no messages sent to it in this use case.

## Messages

| #   | From -> To                                  | Message                                                            |
| --- | ------------------------------------------- | ------------------------------------------------------------------ |
| 1   | Owner -> OwnerUI                            | Room Creation Access                                               |
| 1.1 | OwnerUI -> RoomListingController            | `GetRoomListingForm(in propertyId: Guid, out response: RoomListingFormResponseDto)` |
| 1.2 | OwnerUI -> Owner                            | Room Listing Form Display                                          |
| 2   | Owner -> OwnerUI                            | Room Information and Images Input                                  |
| 2.1 | OwnerUI -> RoomListingController            | `ProcessListingDetails(in request: RoomListingDraftDto, in images: IFormFileCollection, out response: ProcessListingResponseDto)` |
| 2.2 | RoomListingController -> RoomListingLogic   | `ValidateRequiredFields(in request: RoomListingDraftDto, out result: ValidationResult)` |
| 2.3 | RoomListingController -> ICloudStorageGateway | `UploadImagesAsync(in images: IFormFileCollection, out imageUrls: List<string>)` |
| 2.4 | ICloudStorageGateway -> Cloud Storage       | `uploadImages(in images: IFormFileCollection, out imageUrls: List<string>)` |
| 2.5 | OwnerUI -> Owner                            | Room Review Display                                                |
| 3   | Owner -> OwnerUI                            | Saving Confirmation                                                |
| 3.1 | OwnerUI -> RoomListingController            | `SaveDraftListing(in request: RoomListingDraftDto, out response: ListingResponseDto)` |
| 3.2 | RoomListingController -> IRoomListingRepository | `SaveAsync(in entity: RoomListing, out persisted: RoomListing)` |
| 3.3 | OwnerUI -> Owner                            | Draft Saved Message                                                |

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
|---|---|---|
| `1.1` OwnerUI -> CreateRoomListingCoordinator: "Room Creation Form Request" | `1.1` OwnerUI -> RoomListingController: `GetRoomListingForm(...)` | renamed |
| `2.1` OwnerUI -> CreateRoomListingCoordinator: "Validation and Upload Request" | `2.1` OwnerUI -> RoomListingController: `ProcessListingDetails(...)` | validation + upload |
| `2.2` CreateRoomListingCoordinator -> RoomListingRules: "Validation Check" | `2.2` RoomListingController -> RoomListingLogic: `ValidateRequiredFields(...)` | business logic |
| `2.3-2.4` CreateRoomListingCoordinator -> CloudStorageProxy -> Cloud Storage | `2.3-2.4` RoomListingController -> ICloudStorageGateway -> Cloud Storage: `UploadImagesAsync(...)` | image upload |
| `3.1-3.2` OwnerUI -> CreateRoomListingCoordinator -> RoomListing: "Save Draft" | `3.1-3.2` OwnerUI -> RoomListingController -> IRoomListingRepository: `SaveDraftListing(...) -> SaveAsync(...)` | persist |

## Alternative Flow Notes

- **Step 2.2: Validation fails** — `ValidationResult.IsValid = false`, response includes errors, no upload executed
- **Step 2.3: Upload fails** — `ICloudStorageGateway.UploadImagesAsync()` catches exception, returns partial or empty list
- **Step 3.2: Save fails** — Repository exception handled, response contains error

## Notes

- `OwnerUI` shown explicitly — human actor does not interact directly with backend controller.
- `RoomListingController` acts as stateless orchestration point.
- `RoomListingLogic` encapsulates `ValidateRequiredFields` validation.
- `ICloudStorageGateway` handles image upload to cloud storage with exception handling.
- `IRoomListingRepository` persists `RoomListing` draft entity.
- **Implicit DTO mapping**: Controller implicitly maps entity to response DTO. Not shown as separate message.
- **Two-step process**: Process (validate + upload) returns image URLs; Save uses those URLs in entity.
- Actor-to-UI messages (1, 1.2, 2, 2.5, 3, 3.3) use noun phrases — physical user interactions, not code method calls.
