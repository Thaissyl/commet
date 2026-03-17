# Class Interface Specification: UserAccountDB

## Class Summary

- Stereotype: `<<database wrapper>>`
- Scope: `UC-17 Manage User Account Status`
- Hidden Information: persistence schema, query details, and update statements used to load and save user-account data
- Structuring Criterion: database wrapper

## Assumptions

- User accounts are long-lived records and are stored in a physical database.
- SQL and persistence mechanics are intentionally hidden behind this wrapper rather than exposed to `UserManagementLogic`.

## Anticipated Changes

- Query optimization or indexing changes may alter the retrieval strategy without changing the public contract.
- Future audit-trace persistence may be added in the same persistence layer or a separate wrapper.

## Private Attributes

- None in current scope.

## Invariants

- Every retrieval operation must return data consistent with the currently stored user-account records.
- Save operations must persist the latest account status produced by `UserAccount`.

## Collaborators

- `UserManagementLogic`: requests user-account retrieval and persistence services
- `UserAccount`: is reconstituted from or flattened into persisted account data

## Operations Provided

### `+ findUserAccountSummaries(out userAccountList: UserAccountSummaryList)`

- Source trace: `UC-17 main sequence step 2; design communication message 1.3`
- Function: Loads the account summaries needed for the administration list.
- Parameters:
  - `out userAccountList`: manageable user-account summaries with current statuses
- Preconditions:
  - None in current scope.
- Postconditions:
  - `userAccountList` reflects the currently persisted account data.

### `+ findUserAccountByReference(in userAccountReference: UserAccountReference, out userAccount: UserAccount)`

- Source trace: `UC-17 main sequence steps 4 and 6; design communication messages 2.3 and 3.3`
- Function: Loads the selected account as a design-level `UserAccount` abstraction.
- Parameters:
  - `in userAccountReference`: identifies the target account
  - `out userAccount`: reconstituted in-memory account abstraction
- Preconditions:
  - `userAccountReference` identifies an existing stored account.
- Postconditions:
  - `userAccount` contains the current persisted account state.

### `+ saveUserAccountStatus(in userAccount: UserAccount, out accountStatusRecord: AccountStatusRecord)`

- Source trace: `UC-17 main sequence step 6; design communication message 3.5`
- Function: Persists the updated account status produced by the in-memory `UserAccount` abstraction.
- Parameters:
  - `in userAccount`: updated in-memory account abstraction
  - `out accountStatusRecord`: persisted status record after saving
- Preconditions:
  - `userAccount` contains a valid post-transition account state.
- Postconditions:
  - The latest account status is persisted.
  - `accountStatusRecord` reflects the saved account status.
