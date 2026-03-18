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
1. System Admin accesses the owner verification review function.
2. System displays pending verification submissions.
3. System Admin selects a submission to review.
4. System retrieves supporting documents from Cloud Storage and displays the submitted owner information and documents to the System Admin.
5. System Admin reviews the submission and selects Approve.
6. System records the administrative decision as Approved.
7. System updates the owner's overall status to Verified.
8. System sends notification to the Owner of the verification result.
9. System informs the System Admin that the review has been completed successfully.

## Description of alternative sequences
- **Step 5: System Admin selects Reject**
  - 5.1: System records the administrative decision as Rejected.
  - 5.2: System updates the owner's overall status to Rejected.
  - Continues to Step 8.
- **Step 8: Email Provider unavailable**
  - 8.1: System records the notification as failed but the decision still succeeds.
  - Continues to Step 9.

## Nonfunctional Requirements
- **Security:** Verification documents must remain confidential and accessible only to System Admin during review.

## Postcondition
Selected owner verification status is Verified or Rejected.

## Outstanding questions
- The final rejection-reason categories presented to the admin will be finalized later.
