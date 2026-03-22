# Use Case: Review Owner Verification

## Summary
System Admin reviews a pending owner verification submission, records an approval or rejection, updates the owner's verification status, and notifies the owner of the result.

## Dependency
- None

## Actors
- **Primary Actor:** System Admin
- **Secondary Actor(s):** Cloud Storage, Email Provider

## Preconditions
1. System Admin is signed in.
2. At least one owner verification submission has status Pending Review.

## Description of main sequence
1. System Admin requests to access the owner verification review function.
2. System displays pending verification submissions.
3. System Admin selects a submission to review.
4. System retrieves supporting documents from Cloud Storage and displays the submitted owner information and documents to the System Admin.
5. System Admin reviews the submission and selects Approve.
6. System records the administrative decision as Approved, marks the submission as Verified, sends a notification to the owner via the Email Provider, and displays a success message to the System Admin.

## Description of alternative sequences
- **Step 5: If the System Admin selects Reject**
  - 5.1: System records the decision as Rejected.
  - 5.2: System updates the owner's status to Rejected.
  - Continues to Step 6 to send the notification and display success.
- **Step 6: If the Email Provider is unavailable**
  - 6.1: System records the notification as failed, but still commits the approval or rejection decision and informs the System Admin of the email failure.

## Nonfunctional Requirements
- **Security:** Verification documents must remain confidential and accessible only to System Admin during review.

## Postcondition
The owner verification submission has been reviewed, the status is updated, and the administrative decision has been recorded.

## Outstanding questions
- The final rejection-reason categories presented to the admin will be finalized later.
