# Design Communication Diagram: UC-18 Control Listing Visibility - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend aligned to the implemented ASP.NET controller
- Main flow: `AdminUI -> ControlListingController`, then controller -> repositories, validation logic, and email gateway
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label
- Separate reply arrows intentionally omitted; returned data is represented by `out` parameters in the request label
- Request flow style: stateless controller orchestration with list/detail enrichment and archive-based disable action
- View simplification: internal notification payload composition is omitted from this communication view so the interaction stays focused on the main collaborators

## Object Layout

```text
System Admin --- AdminUI --- ControlListingController
                              |--- IRoomListingRepository
                              |--- IUserAccountRepository
                              |--- ListingControlLogic
                              |--- IEmailGateway --- Email Provider
```

## Participants

| Position | Object                   | Stereotype             |
| -------- | ------------------------ | ---------------------- |
| 1        | System Admin             | Actor (primary)        |
| 2        | AdminUI                  | `<<user interaction>>` |
| 3        | ControlListingController | `<<coordinator>>`      |
| 4        | IRoomListingRepository   | `<<database wrapper>>` |
| 5        | IUserAccountRepository   | `<<database wrapper>>` |
| 6        | ListingControlLogic      | `<<business logic>>`   |
| 7        | IEmailGateway            | `<<proxy>>`            |
| 8        | Email Provider           | Actor (secondary)      |

## Messages

| #   | From -> To                                     | Message |
| --- | ---------------------------------------------- | ------- |
| 1   | System Admin -> AdminUI                        | Listing Administration Access |
| 1.1 | AdminUI -> ControlListingController            | `GetVisibleListings(out response: List<AdminListingSummaryDto>)` |
| 1.2 | ControlListingController -> IRoomListingRepository | `FindByStatusAsync(in status: string, out listings: List<RoomListing>)` |
| 1.3 | ControlListingController -> IUserAccountRepository | `FindByIdAsync(in id: Guid, out owner: UserAccount)` |
| 1.4 | AdminUI -> System Admin                        | Visible Listings Display |
| 2   | System Admin -> AdminUI                        | Listing Selection |
| 2.1 | AdminUI -> ControlListingController            | `GetListingDetails(in listingId: Guid, out response: AdminListingDetailDto)` |
| 2.2 | ControlListingController -> IRoomListingRepository | `FindByIdAsync(in id: Guid, out listing: RoomListing)` |
| 2.3 | ControlListingController -> IUserAccountRepository | `FindByIdAsync(in id: Guid, out owner: UserAccount)` |
| 2.4 | AdminUI -> System Admin                        | Listing Details and Disable Action Display |
| 3   | System Admin -> AdminUI                        | Disable Action Decision |
| 3.1 | AdminUI -> ControlListingController            | `DisableListing(in listingId: Guid, out response: ControlActionDto)` |
| 3.2 | ControlListingController -> IRoomListingRepository | `FindByIdAsync(in id: Guid, out listing: RoomListing)` |
| 3.3 | ControlListingController -> ListingControlLogic | `ValidateDisableAction(in listing: RoomListing, out result: ValidationResult)` |
| 3.4 | ControlListingController -> IRoomListingRepository | `UpdateAsync(in entity: RoomListing, out persisted: RoomListing)` |
| 3.5 | ControlListingController -> IEmailGateway      | `SendAsync(in notification: EmailMessage)` |
| 3.6 | IEmailGateway -> Email Provider                | Send Email Notification |
| 3.7 | AdminUI -> System Admin                        | Action Success Message |

## Alternative Flow Notes

- **Step 2.2: Listing not found** - controller returns `NotFound()`
- **Step 3.3: Validation fails** - `ListingControlLogic.ValidateDisableAction(...)` returns invalid when the listing cannot be disabled in the current state
- **Step 3.4: Status mutation fails** - `listing.Archive()` returns failure and the controller responds with `BadRequest`
- **Step 3.5: Notification composition** - `NotificationService.CreateDisableNotification(...)` still exists in the code and runs before `SendAsync(...)`, but it is intentionally omitted from this communication view
- **Step 3.6: Email delivery** - `_email.SendAsync(...)` is invoked without awaiting a delivery result; notification failure is outside the synchronous success path of the request

## Notes

- `AdminUI` is shown explicitly; the human actor never calls backend endpoints directly.
- `ControlListingController` is the real orchestration point in the implemented system.
- `GetVisibleListings(...)` filters by `PublishedAvailable` and enriches each summary with owner information from `IUserAccountRepository`.
- `GetListingDetails(...)` enriches the selected listing with owner name and email plus parsed image references.
- The business action name remains `Disable`, but the implemented mutation is `RoomListing.Archive()`.
- `NotificationService` still exists in the codebase as a helper that builds the email payload, but it is intentionally omitted from this communication view.
- `IEmailGateway` is the design-level boundary to the external email system, and `Email Provider` is shown explicitly as the secondary actor behind that boundary.
- Actor-to-UI messages remain noun phrases because they represent physical interaction, not function calls.
