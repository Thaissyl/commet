# Communication Diagram: UC-10 Update Room Listing - Main Sequence

## Object Layout

```text
Owner --- RoomListingManagementUI --- ListingManagementCoordinator --- RoomListingRules --- RoomListing
                                                 |
                                                 --- CloudStorageProxy --- Cloud Storage
```

## Participants

| Position | Object | Stereotype |
|---|---|---|
| 1 | Owner | Actor (primary) |
| 2 | RoomListingManagementUI | `<<user interaction>>` |
| 3 | ListingManagementCoordinator | `<<coordinator>>` |
| 4 | RoomListingRules | `<<business logic>>` |
| 5 | RoomListing | `<<entity>>` |
| 6 | CloudStorageProxy | `<<proxy>>` |
| 7 | Cloud Storage | Actor (secondary) |

## Messages

| # | From -> To | Message |
|---|---|---|
| 1 | Owner -> RoomListingManagementUI | Room Listing Management Access |
| 1.1 | RoomListingManagementUI -> ListingManagementCoordinator | Room Listing Selection |
| 1.2 | ListingManagementCoordinator -> RoomListingRules | Room Listing Detail Request |
| 1.3 | RoomListingRules -> RoomListing | Room Listing Detail Request |
| 1.4 | RoomListing -> RoomListingRules | Room Listing Detail |
| 1.5 | RoomListingRules -> ListingManagementCoordinator | Room Listing Detail |
| 1.6 | ListingManagementCoordinator -> RoomListingManagementUI | Room Listing Update Form |
| 1.7 | RoomListingManagementUI -> Owner | Room Listing Update Form |
| 2 | Owner -> RoomListingManagementUI | Updated Listing Information and Images |
| 2.1 | RoomListingManagementUI -> ListingManagementCoordinator | Updated Listing Information and Images |
| 2.2 | ListingManagementCoordinator -> CloudStorageProxy | New Listing Images |
| 2.3 | CloudStorageProxy -> Cloud Storage | New Listing Images |
| 2.4 | Cloud Storage -> CloudStorageProxy | Image References |
| 2.5 | CloudStorageProxy -> ListingManagementCoordinator | Image References |
| 2.6 | ListingManagementCoordinator -> RoomListingManagementUI | Listing Update Review |
| 2.7 | RoomListingManagementUI -> Owner | Listing Update Review |
| 3 | Owner -> RoomListingManagementUI | Listing Update Confirmation |
| 3.1 | RoomListingManagementUI -> ListingManagementCoordinator | Listing Update Request |
| 3.2 | ListingManagementCoordinator -> RoomListingRules | Updated Listing Information |
| 3.3 | RoomListingRules -> RoomListing | Updated Room Listing Record |
| 3.4 | RoomListing -> RoomListingRules | Updated Room Listing Record |
| 3.5 | RoomListingRules -> ListingManagementCoordinator | Listing Update Result |
| 3.6 | ListingManagementCoordinator -> RoomListingManagementUI | Listing Update Outcome |
| 3.7 | RoomListingManagementUI -> Owner | Listing Update Confirmation |

## Notes

- `ListingManagementCoordinator` handles external image storage through `CloudStorageProxy`.
- `RoomListingRules` encapsulates room-listing update rules separately from the entity data.
- Messages are kept at analysis level and avoid method-style naming.

Use `/drawio` to generate a visual `.drawio` file from this blueprint.
