# Class Interface Specification: RoomListing

## Class Summary

- Stereotype: `<<data abstraction>>`
- Scope: `UC-01 Search Hostel Room - ASP.NET simple layered backend`
- Hidden Information: Internal attribute structure of a published room listing; encapsulates the domain representation returned from the repository
- Structuring Criterion: data abstraction

## Assumptions

- `RoomListing` is a domain model class populated by `IRoomListingRepository` from EF Core entities.
- In UC-01 this class is read-only; no state-change methods are invoked.
- `SearchMatchingService` receives `RoomListing` objects and reads their attributes to apply criteria filtering and build summaries.

## Anticipated Changes

- Additional attributes (e.g. rating, review count) may be added to the domain class without breaking the search interface.

## Private Attributes

| Attribute | Type | Purpose |
| --- | --- | --- |
| `- listingId` | `Guid` | Unique identifier for the listing |
| `- propertyId` | `Guid` | Reference to the owning property |
| `- title` | `string` | Display title of the listing |
| `- description` | `string` | Detailed listing description |
| `- price` | `decimal` | Monthly rental price |
| `- capacity` | `int` | Maximum number of occupants |
| `- amenities` | `AmenityList` | List of amenities offered |
| `- availableFrom` | `DateOnly` | Date from which the room is available |
| `- furnishedStatus` | `FurnishedStatus` | Furnished, semi-furnished, or unfurnished |
| `- privateWCStatus` | `bool` | Whether a private bathroom is included |
| `- imagesRef` | `string` | Reference to stored listing images |
| `- status` | `ListingStatus` | Current listing status (must be `Published Available` in this scope) |
| `- publishedAt` | `DateTime` | Timestamp when the listing was published |

## Invariants

- In this use-case scope `status` is always `Published Available`; listings with other statuses are not returned by `IRoomListingRepository.findPublishedListings`.

## Collaborators

- `IRoomListingRepository`: loads and hydrates `RoomListing` objects
- `SearchMatchingService`: reads attributes to filter and summarise listings

## Operations Provided

- None in current scope. `RoomListing` acts as a data carrier in UC-01; no behaviour methods are invoked.

## Operations Required

- None in current scope.
