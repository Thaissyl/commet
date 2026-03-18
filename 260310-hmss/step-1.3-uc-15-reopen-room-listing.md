# Use Case: Reopen Room Listing

## Summary
Owner revokes a previously accepted rental request after the offline arrangement fails and reopens the locked room to receive new requests.

## Dependency
- None

## Actors
- **Primary Actor:** Owner
- **Secondary Actor(s):** Email Provider

## Preconditions
1. Owner is signed in.
2. At least one of the Owner's rooms has a rental request in Accepted status and is currently Locked / Not Requestable.

## Description of main sequence
1. Owner accesses the accepted arrangement management function.
2. System displays the accepted request and the corresponding locked room information.
3. Owner selects the accepted arrangement to handle.
4. System validates that the selected request is still in Accepted status.
5. System displays the reopen action and the business consequence (request will be Revoked, room will become requestable again).
6. Owner confirms that the offline arrangement has failed and requests reopening.
7. System records the accepted request as Revoked by Owner.
8. System records the room as Published Available.
9. System sends notification to the Tenant that the accepted request has been revoked.
10. System informs the Owner that the room listing has been reopened successfully.

## Description of alternative sequences
- **Step 3: Selected request is no longer in Accepted status**
  - 3.1: System informs the Owner that the room cannot be reopened from this request.
  - Use case ends unsuccessfully.
- **Step 8: Email Provider unavailable**
  - 8.1: System records the notification as failed but the reopen action still succeeds.
  - Continues to Step 9.

## Nonfunctional Requirements
- **Performance:** Room status must be updated promptly so new requests can be submitted without delay.

## Postcondition
Selected request status is Revoked by Owner. Room status is Published Available and accepts new rental requests.

## Outstanding questions
- The business note shown to the tenant after revocation will be finalized later.
