# Design Communication Diagram: UC-10 Update Room Listing - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: OwnerUI -> RoomListingController, then Controller -> Repository, Controller -> RoomListingLogic, and Controller -> ICloudStorageGateway
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label
- Separate reply arrows intentionally omitted — `out` parameters represent returned data
- Request flow style: synchronous request handling with conditional image upload

## Object Layout

```text
Owner --- OwnerUI --- RoomListingController
                       |--- IRoomListingRepository
                       |--- RoomListingLogic
                       |--- ICloudStorageGateway --- Cloud Storage
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
| 1   | Owner -> OwnerUI                            | Listing Selection                                                 |
| 1.1 | OwnerUI -> RoomListingController            | `GetListingForUpdate(in listingId: Guid, out response: ListingFormResponseDto)` |
| 1.2 | RoomListingController -> IRoomListingRepository | `FindByIdAsync(in id: Guid, out entity: RoomListing)` |
| 1.3 | OwnerUI -> Owner                            | Editable Form Display                                             |
| 2   | Owner -> OwnerUI                            | Listing Modifications and New Images                              |
| 2.1 | OwnerUI -> RoomListingController            | `ProcessListingUpdates(in request: RoomListingUpdateDto, in newImages: IFormFileCollection, out response: ProcessUpdateResponseDto)` |
| 2.2 | RoomListingController -> RoomListingLogic   | `ValidateUpdates(in entity: RoomListing, in request: RoomListingUpdateDto, out result: ValidationResult)` |
| 2.3 | RoomListingController -> ICloudStorageGateway | `UploadImagesAsync(in images: IFormFileCollection, out imageUrls: List<string>)` |
| 2.4 | ICloudStorageGateway -> Cloud Storage       | `uploadImages(in images: IFormFileCollection, out imageUrls: List<string>)` |
| 2.5 | OwnerUI -> Owner                            | Listing Review Display                                            |
| 3   | Owner -> OwnerUI                            | Update Confirmation                                               |
| 3.1 | OwnerUI -> RoomListingController            | `SubmitListingUpdate(in listingId: Guid, in request: RoomListingUpdateDto, out response: ListingResponseDto)` |
| 3.2 | RoomListingController -> IRoomListingRepository | `FindByIdAsync(in id: Guid, out entity: RoomListing)` |
| 3.3 | RoomListingController -> RoomListingLogic   | `ValidateUpdates(in entity: RoomListing, in request: RoomListingUpdateDto, out result: ValidationResult)` |
| 3.4 | RoomListingController -> IRoomListingRepository | `UpdateAsync(in entity: RoomListing, out persisted: RoomListing)` |
| 3.5 | OwnerUI -> Owner                            | Update Success Message                                            |

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
|---|---|---|
| `1.1` OwnerUI -> UpdateRoomListingCoordinator: "Listing Update Form Request" | `1.1` OwnerUI -> RoomListingController: `GetListingForUpdate(...)` | renamed |
| `1.2` UpdateRoomListingCoordinator -> RoomListing: "Listing Detail Query" | `1.2` RoomListingController -> IRoomListingRepository: `FindByIdAsync(...)` | direct DB query |
| `2.1` OwnerUI -> UpdateRoomListingCoordinator: "Update and Upload Request" | `2.1` OwnerUI -> RoomListingController: `ProcessListingUpdates(...)` | validation + upload |
| `2.2` UpdateRoomListingCoordinator -> RoomListingRules: "Validation Check" | `2.2` RoomListingController -> RoomListingLogic: `ValidateUpdates(...)` | business logic |
| `2.3-2.4` UpdateRoomListingCoordinator -> CloudStorageProxy -> Cloud Storage | `2.3-2.4` RoomListingController -> ICloudStorageGateway -> Cloud Storage: `UploadImagesAsync(...)` | conditional upload |
| `3.1-3.3` OwnerUI -> UpdateRoomListingCoordinator -> RoomListing: "Apply and Save" | `3.1-3.4` OwnerUI -> RoomListingController -> RoomListingLogic -> IRoomListingRepository | validation then persist |

## Alternative Flow Notes

- **Step 2.2: Validation fails** — `ValidationResult.IsValid = false`, response includes errors, no upload executed
- **Step 2.3: No new images** — `IFormFileCollection` empty, skip upload, return empty URLs
- **Step 2.3: Upload fails** — Gateway catches exception, returns partial or empty list
- **Step 3.3: Validation fails** — Response contains errors, entity not persisted
- **Step 3.4: Update fails** — Repository exception handled, response contains error

## Notes

- `OwnerUI` shown explicitly — human actor does not interact directly with backend controller.
- `RoomListingController` acts as stateless orchestration point. Sequence 3 re-queries listing by ID independently.
- `RoomListingLogic` encapsulates `ValidateUpdates` validation rules.
- `ICloudStorageGateway` handles conditional image upload with exception handling.
- `IRoomListingRepository` queries and persists `RoomListing` entity.
- **Two-step process**: Process (validate + upload) returns image URLs; Submit uses those URLs in DTO.
- **Implicit DTO mapping**: Controller implicitly maps entity to response DTO. Not shown as separate message.
- Actor-to-UI messages (1, 1.3, 2, 2.5, 3, 3.5) use noun phrases — physical user interactions, not code method calls.
