# Scout Report

## Scope

Source files reviewed:
- `step-1.3-uc-08a-create-property.md`
- `step-1.3-uc-08b-update-property.md`
- `step-1.3-uc-09-create-room-listing.md`
- `step-1.3-uc-10-update-room-listing.md`
- `step-1.3-uc-11-publish-room-listing.md`
- `step-1.3-uc-12-change-listing-visibility.md`
- `step-1.3-uc-13-submit-owner-verification.md`
- `step-1.3-uc-14-review-rental-request.md`
- `step-1.3-uc-15-reopen-room-listing.md`
- `step-1.3-uc-16-review-owner-verification.md`
- `step-1.3-uc-17-manage-user-account-status.md`
- `step-1.3-uc-18-control-listing-visibility.md`

Goal: extract persistent domain nouns, strong entity candidates, candidate attributes explicitly named, status/state concepts, and inheritance or association-class hints from owner/admin-facing HMSS requirement artifacts.

## Persistent Domain Nouns Seen Repeatedly

- property
- owner
- room listing
- listing
- room
- room image
- user account
- user
- tenant
- rental request
- owner verification submission
- owner verification status
- supporting document
- identification document
- notification
- status-management action
- visibility action
- listing-control action

## Strong Entity Candidates

These have direct persistence language or clear lifecycle/state changes in the use cases.

### 1. User Account

Why strong:
- explicitly exists as a managed object
- has current status, permitted status transitions, and protected-access consequences

Evidence:
- UC-17: target user account exists, current statuses displayed, status updated, suspended/disabled access blocked

Likely attributes named explicitly:
- current status
- account information

Notes:
- `Owner`, `System Admin`, and likely `Tenant` look more like roles or subtypes than separate root entities.

### 2. Property

Why strong:
- explicitly created, updated, listed under owner account, and persists as a record

Evidence:
- UC-08a: new property record created under owner account
- UC-08b: existing properties listed and updated

Explicit attributes named:
- name
- address
- map location
- description
- general policies

### 3. Room Listing

Why strong:
- explicitly created, updated, published, hidden, archived, reopened, disabled, and shown in public search

Evidence:
- UC-09 through UC-12, UC-15, UC-18

Explicit attributes named:
- title
- description
- price
- capacity
- amenities
- available-from date
- furnished status
- private WC status

Direct child/related records strongly implied:
- stored image(s)
- visibility/publication status

### 4. Rental Request

Why strong:
- explicitly exists for a room/listing, is reviewed, decided, and carries its own status lifecycle

Evidence:
- UC-14 and UC-15

Explicit attributes named:
- request information
- request details
- resulting request status

Notes:
- strong candidate for an association class between `Tenant` and `Room Listing` or `Room`.

### 5. Owner Verification Submission

Why strong:
- explicitly submitted, stored, reviewed, approved/rejected, and has its own status

Evidence:
- UC-13 and UC-16

Explicit attributes named:
- personal information
- supporting identification documents
- administrative decision

Related state:
- Pending Review

### 6. Verification Document

Why strong:
- documents are uploaded, stored securely, displayed during admin review, and access-controlled

Evidence:
- UC-13 and UC-16

Explicit attributes named:
- no explicit document metadata fields are named in these use cases

Notes:
- could also be modeled as a child entity under `Owner Verification Submission` rather than a root entity.

### 7. Listing Image

Why strong:
- images are uploaded, stored, required for publication, and checked for availability

Evidence:
- UC-09, UC-10, UC-11

Explicit attributes named:
- no explicit image metadata fields are named in these use cases

Notes:
- likely child entity of `Room Listing`, not a root business entity.

## Likely Attributes or Value Objects

These appear more like fields, structured values, or small owned objects than standalone root entities.

### Property-side

- property name
- address
- map location
- description
- general policies

### Room-listing-side

- title
- description
- price
- capacity
- amenities
- available-from date
- furnished status
- private WC status

### Verification-side

- personal information
- verification information fields
- document requirements
- rejection-reason category

### Decision/UI/support terms that look weaker than entities

- publication requirements checklist
- visibility action
- status-management action
- listing-control action
- business note
- comparison view

### Value-object candidates

- `Address`
- `MapLocation`
- `Money/Price`
- `Amenity` or amenity collection
- `Policy` or policy collection
- `VerificationDecision`
- `RejectionReason`

## Status and State Concepts

### Room Listing / Room

Explicit status/state terms:
- Draft
- unpublished state
- Published Available
- Hidden
- Archived
- publicly visible
- removed from public search
- disabled by admin action
- Locked / Not Requestable
- requestable again

Observation:
- The artifacts suggest listing publication, discoverability, moderation, and requestability may all be mixed into one state vocabulary. This may be one overloaded status field, or several separate state dimensions.

### Rental Request

Explicit status/state terms:
- Pending
- Accepted
- Rejected
- Revoked by Owner

Behavioral link:
- accepting a request locks the room/listing from further requests
- revoking an accepted request reopens the room/listing

### Owner Verification Submission / Owner Verification

Explicit terms:
- Pending Review
- Verified
- Rejected
- not yet verified
- unverified

Observation:
- Submission status and owner verification status may be separate but coupled concepts.

### User Account

Explicit terms:
- current state
- current status
- permitted transition
- suspended
- disabled

Observation:
- the full user-account state set is not enumerated in these files.

## Inheritance Hints

### User-role hierarchy

Strong hint:
- `Owner`, `System Admin`, and likely `Tenant` are specializations or roles of a broader `User` / `User Account`.

Reason:
- admin manages user accounts
- owner and tenant receive notifications and participate in account-governed actions
- verification seems to apply to the owner role, not to a completely separate identity object

### Possible role-vs-profile split

Medium hint:
- `Owner` may be a verified-capable role/profile attached to a user account rather than a separate entity from `User Account`.

## Association and Composition Hints

### Owner -> Property

Strong association:
- one owner account has many properties
- property belongs under owner account

### Property -> Room Listing

Strong composition:
- room listing is created under a selected property

### Room Listing -> Listing Image

Strong composition:
- listing owns uploaded images
- publication requires at least one stored image

### Owner -> Owner Verification Submission

Strong association:
- owner submits verification material
- admin reviews the submission

### Owner Verification Submission -> Verification Document

Strong composition:
- submission contains supporting identification documents

### Tenant <-> Room Listing/Room via Rental Request

Strong association-class hint:
- rental request links a tenant to a room/listing
- the request carries business data and a full status lifecycle
- owner decisions operate on that request object

### System Admin -> User Account via Account Status Change

Medium association-class / audit-event hint:
- requirement text stresses permitted transitions and traceability
- may imply a persistent status-change record or audit log

### System Admin -> Listing via Disable Action

Medium association-class / moderation-event hint:
- admin disable action is traceable and user-facing
- may imply persistent moderation action history

### Notification

Medium entity/event hint:
- notification failures are explicitly recorded while business decisions still succeed
- this implies some persistent outbound notification record or delivery log

## Normalized Candidate Model Split

### Strong entity candidates

- User Account
- Property
- Room Listing
- Rental Request
- Owner Verification Submission
- Verification Document
- Listing Image

### Role/subtype candidates

- Owner
- System Admin
- Tenant

### Likely attributes or value objects

- Address
- Map Location
- Property Description
- General Policies / Policy set
- Listing Title
- Listing Description
- Price
- Capacity
- Amenity / amenity set
- Available-from Date
- Furnished Status
- Private WC Status
- Personal Information
- Verification Decision
- Rejection Reason

## Main Modeling Risks

- `room` and `room listing` are used interchangeably in some flows; this can produce a wrong object structure if not resolved early.
- listing visibility and availability may currently collapse multiple concerns into one status field
- owner verification may need two linked states: submission status and owner verification status
- actions that must be traceable may need persistent event/history objects even if they are not named as standalone entities yet

## Unresolved Questions

- Is `Room Listing` the same persistent object as `Room`, or is there a separate `Room` entity plus a publishable `Listing` wrapper?
- Should `Hidden`, `Archived`, `Disabled`, `Draft`, `Published Available`, and `Locked / Not Requestable` belong to one listing state machine, or to separate dimensions such as publication status, moderation status, and requestability?
- Is `Owner Verification Submission` a reusable history of submissions, with `Owner Verification Status` stored separately on the owner account?
- Are `general policies` and `amenities` plain text fields, enum sets, or repeatable child records?
- Do images and verification documents need standalone metadata beyond storage reference and availability?
- What are the full allowed values and transitions for `User Account` status?
