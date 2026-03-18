# Communication Diagram: UC-11 Publish Room Listing - Analysis Model

## Object Layout

```text
Owner --- OwnerUI --- PublishListingCoordinator --- PublicationRules --- RoomListing
                                                     |
                                                     --- OwnerProfile
```

## Participants

| Position | Object                   | Stereotype             | Justification                                                                                                    |
| -------- | ------------------------ | ---------------------- | ---------------------------------------------------------------------------------------------------------------- |
| 1        | Owner                    | Actor (primary)        | The human user initiating the publication.                                                                       |
| 2        | OwnerUI                  | `<<user interaction>>` | Boundary object receiving inputs and displaying information.                                                      |
| 3        | PublishListingCoordinator | `<<coordinator>>`      | Control object sequencing the overall flow of the use case.                                                      |
| 4        | PublicationRules         | `<<business logic>>`   | Encapsulates the specific business rules for validating owner verification, listing completeness, and image availability. |
| 5        | RoomListing              | `<<entity>>`           | Conceptual data object encapsulating the room listing record.                                                     |
| 6        | OwnerProfile             | `<<entity>>`           | Conceptual data object encapsulating the owner's verification status.                                             |

## Messages (Main Sequence)

| #   | From -> To                                     | Message / Information Passed     | Use Case Step |
| --- | ---------------------------------------------- | -------------------------------- | ------------- |
| 1   | Owner -> OwnerUI                               | Publication Access               | Step 1        |
| 1.1 | OwnerUI -> PublishListingCoordinator           | Listing Detail Request           |               |
| 1.2 | PublishListingCoordinator -> RoomListing       | Listing Detail Query             |               |
| 1.3 | RoomListing -> PublishListingCoordinator       | Listing Data                     |               |
| 1.4 | PublishListingCoordinator -> OwnerUI           | Listing Data and Checklist       | Step 2        |
| 1.5 | OwnerUI -> Owner                               | Listing and Checklist Display     |               |
| 2   | Owner -> OwnerUI                               | Publication Request              | Step 3        |
| 2.1 | OwnerUI -> PublishListingCoordinator           | Publication Evaluation Request   |               |
| 2.2 | PublishListingCoordinator -> PublicationRules  | Eligibility Check (Listing & Owner Data) | Step 4  |
| 2.3 | PublicationRules -> PublishListingCoordinator  | Eligibility Result (Eligible)    |               |
| 2.4 | PublishListingCoordinator -> OwnerUI           | Publication Confirmation Prompt  |               |
| 2.5 | OwnerUI -> Owner                               | Confirmation Prompt Display      |               |
| 3   | Owner -> OwnerUI                               | Publication Confirmation          | Step 5        |
| 3.1 | OwnerUI -> PublishListingCoordinator           | Confirmed Publication             |               |
| 3.2 | PublishListingCoordinator -> RoomListing       | Published Status Update          | Step 6        |
| 3.3 | PublishListingCoordinator -> OwnerUI           | Publication Success              | Step 7        |
| 3.4 | OwnerUI -> Owner                               | Publication Success Message      |               |

## Alternative Sequences

| #    | From -> To                                     | Message / Information Passed                          | Use Case Step       |
| ---- | ---------------------------------------------- | ---------------------------------------------------- | ------------------- |
| 2.3a | PublicationRules -> PublishListingCoordinator  | [Ineligible] Eligibility Result (Unverified/Incomplete) | Alt Step 4.1    |
| 2.4a | PublishListingCoordinator -> OwnerUI           | Ineligibility Error Prompt                            |                     |
| 2.5a | OwnerUI -> Owner                               | Error Display                                         | Returns to Step 2   |

## Architectural Notes

- **Critical Modeling Distinction**: Owner verification, listing completeness, and image availability are **Business Rules** evaluated during the use case (Step 4), NOT Preconditions. Preconditions are only: (1) Owner is signed in, (2) Listing exists in Draft/unpublished state.
- **Analysis vs. Design**: In this analysis model, messages use descriptive noun phrases (e.g., `Published Status Update`) rather than operation signatures (e.g., `publishListing(in, out)`).
- **Combined Business Logic**: `PublicationRules` encapsulates all eligibility checks (owner verification, listing completeness, image availability) in a single `<<business logic>>` object, rather than splitting across multiple logic objects.
- **Entity Access for Validation**: The `PublicationRules` needs access to both `RoomListing` (for completeness and images) and `OwnerProfile` (for verification status) to evaluate eligibility. In the analysis model, this is implied by the `Eligibility Check (Listing & Owner Data)` message.
- **Explicit Returns**: The analysis model shows explicit data flow (e.g., `Listing Data` in Message 1.3, `Eligibility Result (Eligible)` in Message 2.3). In the design phase, these will be embedded into `out` parameters of synchronous calls.

Use `/drawio-communication-diagram` to generate a visual `.drawio` file from this blueprint.
