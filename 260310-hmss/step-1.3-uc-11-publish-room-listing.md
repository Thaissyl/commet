# Use Case: Publish Room Listing

## Summary
A verified owner publishes a prepared room listing so it becomes publicly visible and searchable to visitors and tenants.

## Dependency
- None

## Actors
- **Primary Actor:** Owner
- **Secondary Actor(s):** None

## Preconditions
1. Owner is signed in.
2. Selected room listing exists in Draft or unpublished state.

## Description of main sequence
1. Owner accesses the publication function for a prepared listing.
2. System displays the listing information and publication requirements checklist.
3. Owner reviews the listing and requests publication.
4. System evaluates publication eligibility, including owner verification, listing completeness, and image availability.
5. Owner confirms the publication request.
6. System records the room listing as Published Available.
7. System informs the Owner that the listing is now publicly searchable.

## Description of alternative sequences
- **Step 4: Owner not yet verified**
  - 4.1: System informs the Owner that unverified owners cannot publish listings.
  - Use case ends unsuccessfully.
- **Step 4: Required listing fields are incomplete**
  - 4.1: System informs the Owner which fields are missing.
  - Returns to Step 3.
- **Step 4: No images exist for the listing**
  - 4.1: System informs the Owner that at least one image is required before publication.
  - Returns to Step 3.

## Nonfunctional Requirements
- **Performance:** Publication status must be reflected promptly in public search.
- **Security:** Publication rules must be enforced consistently; unverified owners must never bypass this check.

## Postcondition
Selected room listing is in Published Available status and appears in public search results.

## Outstanding questions
- The exact minimum completeness rule for release 1 publication will be finalized later.
