# Use Case: Review Rental Request

## Summary
Owner reviews submitted rental requests for a room and decides to accept, reject, or keep each pending. Accepting locks the room from further requests and triggers notification to the tenant.

## Dependency
- None

## Actors
- **Primary Actor:** Owner
- **Secondary Actor(s):** Email Provider

## Preconditions
1. Owner is signed in.
2. At least one rental request exists for a room managed by the Owner.

## Description of main sequence
1. Owner accesses the rental request review function for a selected room.
2. System displays all submitted requests for that room with their visible request information.
3. Owner selects a request to handle.
4. System displays the request details and available decision options (Accept / Reject / Keep Pending).
5. Owner selects the desired decision.
6. System records the decision for the selected request.
7. System records the resulting request status and, if accepted, records the room as Locked / Not Requestable.
8. System sends the decision notification to the tenant.
9. System informs the Owner that the decision has been recorded successfully.

## Description of alternative sequences
- **Step 5: Owner keeps request pending**
  - 5.1: System preserves Pending status.
  - Returns to Step 2.
- **Step 5: Owner rejects the request**
  - 5.1: System updates status to Rejected.
  - 5.2: Room remains requestable if no other request was accepted.
  - Continues to Step 8.
- **Step 8: Email Provider unavailable**
  - 8.1: System records the notification as failed but the decision still succeeds.
  - Continues to Step 9.

## Nonfunctional Requirements
- **Performance:** Decision must be reflected promptly in both request and room status.
- **Security:** Request information must be accessible only to the relevant Owner and System Admin.

## Postcondition
Selected request is updated to Accepted, Rejected, or Pending. If Accepted, the room status is Locked / Not Requestable.

## Outstanding questions
- The exact comparison view for reviewing multiple requests side by side may be refined later.
