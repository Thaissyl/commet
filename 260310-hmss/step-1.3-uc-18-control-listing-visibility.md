# Use Case: Control Listing Visibility

## Summary
System Admin applies the Disable action to a suspicious or policy-violating publicly visible listing so that it is removed from public search and the Owner is notified.

## Dependency
- None

## Actors
- **Primary Actor:** System Admin
- **Secondary Actor(s):** Email Provider

## Preconditions
1. System Admin is signed in.

## Description of main sequence
1. System Admin accesses the listing administration function.
2. System displays publicly visible listings with their associated information.
3. System Admin selects a listing to review.
4. System displays the listing details and the Disable control action.
5. System Admin selects the Disable action for the listing.
6. System validates that the selected listing is still publicly visible.
7. System removes the listing from public search.
8. System sends notification to the Owner that the listing has been disabled by admin action.
9. System informs the System Admin that the listing-control action has been applied successfully.

## Description of alternative sequences
- **Step 6: Listing is no longer publicly visible**
  - 6.1: System informs the System Admin that the action cannot be completed.
  - Use case ends unsuccessfully.
- **Step 8: Email Provider unavailable**
  - 8.1: System records the notification as failed but the listing-control action still succeeds.
  - Continues to Step 9.

## Nonfunctional Requirements
- **Security:** Admin listing-control actions must be traceable and applied immediately to protect platform users.

## Postcondition
The listing is removed from public search and is no longer visible to visitors or tenants.

## Outstanding questions
- None at this stage.
