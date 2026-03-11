# Communication Diagram: UC-11 Publish Room Listing - Main Sequence

## Object Layout

```text
Owner --- RoomListingManagementUI --- ListingManagementCoordinator --- RoomListingRules --- RoomListing
                                                 |
                                                 --- VerificationLogic --- OwnerVerification
```

## Participants

| Position | Object | Stereotype |
|---|---|---|
| 1 | Owner | Actor (primary) |
| 2 | RoomListingManagementUI | `<<user interaction>>` |
| 3 | ListingManagementCoordinator | `<<coordinator>>` |
| 4 | RoomListingRules | `<<business logic>>` |
| 5 | RoomListing | `<<entity>>` |
| 6 | VerificationLogic | `<<business logic>>` |
| 7 | OwnerVerification | `<<entity>>` |

## Messages

| # | From -> To | Message |
|---|---|---|
| 1 | Owner -> RoomListingManagementUI | Room Listing Publication Access |
| 1.1 | RoomListingManagementUI -> ListingManagementCoordinator | Room Listing Publication Request |
| 1.2 | ListingManagementCoordinator -> RoomListingRules | Room Listing Publication Review Request |
| 1.3 | RoomListingRules -> RoomListing | Room Listing Publication Review Request |
| 1.4 | RoomListing -> RoomListingRules | Room Listing Publication Context |
| 1.5 | RoomListingRules -> ListingManagementCoordinator | Room Listing Publication Context |
| 1.6 | ListingManagementCoordinator -> VerificationLogic | Owner Verification Status Request |
| 1.7 | VerificationLogic -> OwnerVerification | Owner Verification Status Request |
| 1.8 | OwnerVerification -> VerificationLogic | Owner Verification Status |
| 1.9 | VerificationLogic -> ListingManagementCoordinator | Owner Verification Status |
| 1.10 | ListingManagementCoordinator -> RoomListingManagementUI | Publication Review |
| 1.11 | RoomListingManagementUI -> Owner | Publication Review |
| 2 | Owner -> RoomListingManagementUI | Publication Confirmation |
| 2.1 | RoomListingManagementUI -> ListingManagementCoordinator | Publication Request |
| 2.2 | ListingManagementCoordinator -> RoomListingRules | Publication Decision Context |
| 2.3 | RoomListingRules -> RoomListing | Published Room Listing Record |
| 2.4 | RoomListing -> RoomListingRules | Published Room Listing Record |
| 2.5 | RoomListingRules -> ListingManagementCoordinator | Publication Result |
| 2.6 | ListingManagementCoordinator -> RoomListingManagementUI | Publication Outcome |
| 2.7 | RoomListingManagementUI -> Owner | Publication Confirmation |

## Notes

- `ListingManagementCoordinator` coordinates publication review and confirmation across listing and verification logic.
- `RoomListingRules` evaluates listing readiness and applies the publication state change to `RoomListing`.
- `VerificationLogic` provides owner publishing eligibility through `OwnerVerification`.
- Messages are kept at analysis level and avoid method-style naming.

Use `/drawio` to generate a visual `.drawio` file from this blueprint.
