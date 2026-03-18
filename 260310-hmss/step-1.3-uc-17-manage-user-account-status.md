# Use Case: Manage User Account Status

## Summary
System Admin changes a user account status by applying a status transition permitted for the account's current state and notifies the user of the change.

## Dependency
- None

## Actors
- **Primary Actor:** System Admin
- **Secondary Actor(s):** Email Provider

## Preconditions
1. System Admin is signed in.
2. The target user account exists in the system.

## Description of main sequence
1. System Admin accesses the user account administration function.
2. System displays user accounts and their current statuses.
3. System Admin selects a user account to manage.
4. System displays the current account information and the status-management actions permitted for the selected account's current status.
5. System Admin selects the Suspend action (for an Active account).
6. System validates the status transition and updates the user account status to Suspended.
7. System sends notification to the user about the status change.
8. System informs the System Admin that the account-management action has been applied successfully.

## Description of alternative sequences
- **Step 4: No status-management action is available for the selected account**
  - 4.1: System informs the System Admin that no further status change is available for the selected account.
  - Use case ends unsuccessfully.
- **Step 6: Selected action is no longer permitted under the current account status**
  - 6.1: System informs the System Admin that the action cannot be completed.
  - Use case ends unsuccessfully.
- **Step 7: Email Provider unavailable**
  - 7.1: System records the notification as failed but the account status update still succeeds.
  - Continues to Step 8.

## Nonfunctional Requirements
- **Security:** Account-management actions must be traceable and applied consistently. Suspended or disabled accounts must not retain unauthorized access.

## Postcondition
User account status is updated according to the permitted transition. A suspended or disabled account cannot access protected system functions.

## Outstanding questions
- None at this stage.
