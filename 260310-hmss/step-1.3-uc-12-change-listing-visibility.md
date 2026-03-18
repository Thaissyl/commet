# Use Case: Change Listing Visibility

## Summary
Owner hides or archives a published room listing, removing it from public search without deleting it.

## Dependency
- None

## Actors
- **Primary Actor:** Owner
- **Secondary Actor(s):** None

## Preconditions
1. Owner is signed in.
2. Owner has at least one published room listing.

## Description of main sequence
1. Owner accesses the listing management function and selects a published listing.
2. System displays the current listing status and a standard menu of visibility actions.
3. Owner selects the desired visibility action.
4. System evaluates whether the selected action is valid for the listing's current status.
5. Owner confirms the visibility change.
6. System records the listing status as Hidden or Archived.
7. System informs the Owner that the listing visibility has been changed successfully.

## Description of alternative sequences
- **Step 4: Selected action is not valid for the listing's current status**
  - 4.1: System informs the Owner that the action cannot be applied.
  - Use case ends unsuccessfully.

## Nonfunctional Requirements
- **Performance:** Visibility change must be reflected immediately so the listing no longer appears in public search.

## Postcondition
Selected listing is no longer visible in public search and is in Hidden or Archived status.

## Outstanding questions
- The archive retention policy and whether archived listings can be restored will be finalized later.
