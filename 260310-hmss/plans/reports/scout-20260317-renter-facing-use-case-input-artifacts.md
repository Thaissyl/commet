# Scout Report

## Scope
- Read:
  - `step-1.3-uc-01-search-hostel-room.md`
  - `step-1.3-uc-02-view-room-details.md`
  - `step-1.3-uc-03-register-account.md`
  - `step-1.3-uc-04-sign-in.md`
  - `step-1.3-uc-05-submit-rental-request.md`
  - `step-1.3-uc-06-cancel-rental-request.md`
  - `step-1.3-uc-07-track-rental-request-status.md`
- Goal: renter-facing persistent nouns, strong entity candidates, named attributes, status/state terms.

## Strong Entity Candidates
- `User Account`
  - Strong because it is created, role-assigned, status-assigned, validated by unique email, and used for sign-in.
  - Named fields: `name`, `email`, `phone`, `password`, `account role`, `account status`.
  - Source: UC-03 lines 18-22, 37-38; UC-04 lines 19-21, 36-37.
- `Room Listing`
  - Strong because it is searched, selected, displayed, visibility-controlled, and checked for requestability.
  - Named fields: `listing title/title`, `description`, `price`, `amenities`, `capacity`, `availability` / `availability status`, `move-in date`, `room images`.
  - Source: UC-01 lines 18-22, 41-42; UC-02 lines 14, 17-22; UC-05 lines 15, 18-21.
- `Property`
  - Strong because room listing details expose property identity/location, likely persistent beyond one listing view.
  - Named fields: `property name`, `property address`, `property location`, `map/location information`.
  - Source: UC-02 lines 19-22.
- `Rental Request`
  - Strong because it is submitted, stored, listed, cancelled, reviewed later, and has explicit lifecycle states.
  - Named fields: `move-in date`, `expected rental duration`, `number of occupants`, `occupation category`, `budget expectation`, `contact phone`, `preferred contact method`, `special notes`, `status`.
  - Source: UC-05 lines 18-24, 42-43; UC-06 lines 18-24, 38-39; UC-07 lines 17-20, 31-32.

## Likely Attributes / Value Objects / Supporting Concepts
- `Account Role`
  - Values named: `Tenant`, `Owner`, `System Admin`.
  - Looks like enum/value object on `User Account`, not separate persistent entity from these artifacts alone.
  - Source: UC-03 lines 18-22; UC-04 lines 10, 21, 36-37.
- `Search Criteria`
  - Named parts: `location`, `price range`, `amenities`, `availability`, `move-in date`.
  - Looks like transient input object, not persistent domain entity.
  - Source: UC-01 lines 18-22.
- `Credentials`
  - Named parts: `email`, `password`.
  - Likely authentication value object, not business entity.
  - Source: UC-03 lines 19-20, 34; UC-04 lines 19-20, 25-29.
- `Contact Preference`
  - Named parts: `contact phone`, `preferred contact method`.
  - Could stay embedded in `Rental Request` unless later reused elsewhere.
  - Source: UC-05 line 20.
- `Address / Location`
  - Named parts: `property address`, `property location`, `map information`.
  - Could be value object inside `Property`.
  - Source: UC-01 line 22; UC-02 lines 19-22.
- `Price / Budget`
  - Named parts: `price`, `price range`, `budget expectation`.
  - Looks like money/value-object territory.
  - Source: UC-01 lines 19, 22; UC-02 line 19; UC-05 line 20.
- `Occupancy Details`
  - Named parts: `capacity`, `number of occupants`, `occupation category`.
  - Likely embedded request/listing attributes, not standalone entity.
  - Source: UC-02 line 19; UC-05 line 20.
- `Room Images`
  - Named explicitly, but current renter flows only consume them as listing detail.
  - Could remain child collection/value object unless separate image management appears later.
  - Source: UC-02 line 19.
- `Notification`
  - System sends owner notification and records failure.
  - Could become supporting entity if notification history matters; from current renter artifacts it is secondary to rental-request workflow.
  - Source: UC-05 lines 24, 34-35; UC-06 lines 24, 31-32.
- `Authenticated Session` / `Access Rights`
  - Important security/runtime concepts, but likely technical/session constructs rather than core persistent business entities.
  - Source: UC-04 lines 21, 36-37.

## Persistent Domain Nouns Observed
- `account`
- `registered user`
- `tenant`
- `owner`
- `system admin`
- `room listing`
- `property`
- `rental request`
- `request status`
- `account role`
- `account status`
- `availability status`
- `notification`

## Important Status / State Concepts
- `Room Listing` / `Listing Visibility`
  - `published`
  - `publicly visible`
  - `Published Available`
  - `requestable`
  - `locked`
  - `hidden`
  - `no longer publicly visible`
  - `currently available` / `no matching room currently available`
  - Source: UC-01 lines 18-22, 29-34, 41-42; UC-02 lines 14, 26-29; UC-05 lines 15, 21, 28-30.
- `Rental Request Status`
  - `Pending`
  - `Accepted`
  - `Rejected`
  - `Cancelled by Tenant`
  - `Cancelled`
  - `Revoked`
  - `eligible for cancellation`
  - Source: UC-05 lines 23, 42-43; UC-06 lines 15, 21-23, 28-29, 38-39; UC-07 lines 18-20.
- `Account Status`
  - `initial account status`
  - `disabled`
  - `suspended`
  - Source: UC-03 lines 22, 37-38; UC-04 lines 20, 28-30.
- `Authentication / Access State`
  - `signed in`
  - `not currently signed in`
  - `authenticated session`
  - `access rights corresponding to account role`
  - Source: UC-03 line 14; UC-04 lines 14, 21, 36-37; UC-05 line 14; UC-06 line 14; UC-07 line 14.
- `Operational / Integration State`
  - `Google Maps unavailable`
  - `map information temporarily unavailable`
  - `Email Provider unavailable`
  - `notification failed`
  - Source: UC-01 lines 33-34; UC-02 lines 33-35; UC-05 lines 34-35; UC-06 lines 31-32.

## Modeling Notes
- Strongest renter-side analysis objects from these 7 use cases: `User Account`, `Room Listing`, `Property`, `Rental Request`.
- `Tenant`, `Owner`, `System Admin` read more like role specializations of `User Account` than fully separate entities at this stage.
- `Property` and `Room Listing` are distinct nouns in the text. Keep separate unless later artifacts collapse them intentionally.
- `Rental Request` clearly needs lifecycle modeling. Status transitions already implied: `Pending -> Accepted|Rejected|Cancelled by Tenant|Revoked`.
- Listing lifecycle also matters. Text mixes `published`, `publicly visible`, `requestable`, `locked`, `hidden`, `Published Available`. Those likely need normalization into one status model or a status + visibility pair.
- `Notification` may deserve a supporting object only if audit/retry/history matters. Current text only proves a delivery outcome is recorded.

## Unresolved Questions
- Is `User Account` the base persistent object with role specializations, or should `Tenant` and `Owner` be modeled as separate domain classes with role-specific data?
- Is `System Admin` in scope for the same account model, or only an access-role on the same user entity?
- Should `Property` own many `Room Listings`, or is each listing effectively the room entity itself in phase 1?
- Should listing state be normalized as one enum, or split into `visibility` and `availability` dimensions?
- Is `Cancelled by Tenant` the canonical stored status, or just a display label under broader `Cancelled`?
- What exactly distinguishes `Revoked` from `Rejected`, and who performs `Revoked`?
- Does `Notification` need its own persistent record with retry/audit fields, or is a simple delivery flag enough?
- Are `room images` first-class managed objects later, or just embedded media references on `Room Listing`?
