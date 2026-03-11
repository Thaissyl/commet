# Use Case: Update Room Listing

## Summary
Owner updates information on an existing room listing. System records the updated room listing information.

## Dependency
- None

## Actors
- **Primary Actor:** Owner
- **Secondary Actor(s):** Cloud Storage

## Preconditions
1. Owner is signed in.
2. Owner has at least one existing room listing.

## Description of main sequence
1. Owner accesses the room listing management function and selects an existing listing to update.
2. System displays the current room listing information in editable form.
3. Owner modifies the desired fields (title, description, price, capacity, amenities, available-from date) and optionally provides new images.
4. System records any new images and prepares the updated listing information for review.
5. Owner reviews the changes and confirms the update.
6. System records the updated room listing information.
7. System informs the Owner that the listing has been updated successfully.

## Description of alternative sequences
- **Step 4: Required fields are cleared or invalid**
  - 4.1: System informs the Owner which fields must be corrected.
  - Returns to Step 3.
- **Step 4: Image storage unavailable**
  - 4.1: System informs the Owner that image storage failed at this time.
  - Returns to Step 3.

## Nonfunctional Requirements
- **Performance:** Updated listing information must be recorded reliably and reflect promptly.

## Postcondition
Updated room listing information is recorded in the system.

## Outstanding questions
- Whether updating a published listing triggers a re-verification step will be finalized later.
