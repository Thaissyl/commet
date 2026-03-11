# Communication Diagram: UC-12 Change Listing Visibility - Main Sequence

## Object Layout

```text
Owner --- RoomListingManagementUI --- ListingManagementCoordinator --- RoomListingRules --- RoomListing
```

## Participants

| Position | Object | Stereotype |
|---|---|---|
| 1 | Owner | Actor (primary) |
| 2 | RoomListingManagementUI | `<<user interaction>>` |
| 3 | ListingManagementCoordinator | `<<coordinator>>` |
| 4 | RoomListingRules | `<<business logic>>` |
| 5 | RoomListing | `<<entity>>` |

## Messages

| # | From -> To | Message |
|---|---|---|
| 1 | Owner -> RoomListingManagementUI | Listing Management Access |
| 1.1 | RoomListingManagementUI -> ListingManagementCoordinator | Published Listing Selection |
| 1.2 | ListingManagementCoordinator -> RoomListingRules | Visibility Options Request |
| 1.3 | RoomListingRules -> RoomListing | Visibility Options Request |
| 1.4 | RoomListing -> RoomListingRules | Listing Visibility Context |
| 1.5 | RoomListingRules -> ListingManagementCoordinator | Listing Visibility Context |
| 1.6 | ListingManagementCoordinator -> RoomListingManagementUI | Listing Visibility Options |
| 1.7 | RoomListingManagementUI -> Owner | Listing Visibility Options |
| 2 | Owner -> RoomListingManagementUI | Visibility Action Selection |
| 2.1 | RoomListingManagementUI -> ListingManagementCoordinator | Visibility Action Selection |
| 2.2 | ListingManagementCoordinator -> RoomListingRules | Visibility Change Assessment |
| 2.3 | RoomListingRules -> RoomListing | Visibility Change Assessment |
| 2.4 | RoomListing -> RoomListingRules | Visibility Change Result |
| 2.5 | RoomListingRules -> ListingManagementCoordinator | Visibility Change Review |
| 2.6 | ListingManagementCoordinator -> RoomListingManagementUI | Visibility Change Review |
| 2.7 | RoomListingManagementUI -> Owner | Visibility Change Review |
| 3 | Owner -> RoomListingManagementUI | Visibility Change Confirmation |
| 3.1 | RoomListingManagementUI -> ListingManagementCoordinator | Visibility Change Request |
| 3.2 | ListingManagementCoordinator -> RoomListingRules | Visibility Change Decision |
| 3.3 | RoomListingRules -> RoomListing | Listing Visibility Record |
| 3.4 | RoomListing -> RoomListingRules | Listing Visibility Record |
| 3.5 | RoomListingRules -> ListingManagementCoordinator | Visibility Change Result |
| 3.6 | ListingManagementCoordinator -> RoomListingManagementUI | Visibility Change Outcome |
| 3.7 | RoomListingManagementUI -> Owner | Visibility Change Confirmation |

## Notes

- `ListingManagementCoordinator` separates the visibility review step from the confirmed visibility change step.
- `RoomListingRules` evaluates action validity and applies the resulting visibility state change to `RoomListing`.
- Messages are kept at analysis level and avoid method-style naming.

Use `/drawio` to generate a visual `.drawio` file from this blueprint.
