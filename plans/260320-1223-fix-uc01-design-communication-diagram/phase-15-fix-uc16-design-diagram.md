# Phase 15: Document Fix — Rewrite UC-16 step-3.0-design-communication-diagram.md

**Status:** Ready (no code changes needed)
**File:** `C:\Users\welterial\commet\260310-hmss\phase-3\uc-16-review-owner-verification-aspnet-react\step-3.0-design-communication-diagram.md`

## Context Links

- Use case: `C:\Users\welterial\commet\260310-hmss\step-1.3-uc-16-review-owner-verification.md`
- Analysis: `C:\Users\welterial\commet\260310-hmss\phase-2\step-2.2-uc-16-review-owner-verification-main-seq.md`
- Code: `backend/Hmss.Api/Controllers/ReviewVerificationController.cs`

## Errors Being Fixed

| # | Error |
|---|-------|
| 1 | Participant `IOwnerProfileRepository` — remove entirely; code uses `IUserAccountRepository` instead |
| 2 | Participant `OwnerProfile <<data abstraction>>` — remove entirely; no such entity in code; no `Verify()` method called |
| 3 | Add participant `IUserAccountRepository <<database wrapper>>` (used in seq 2 and seq 3 for owner lookup) |
| 4 | Object layout: `IOwnerVerificationRepository --- OwnerVerification` — remove; add `OwnerVerification` directly under controller (`verification.Approve()` called directly by controller) |
| 5 | Object layout: `IOwnerProfileRepository --- OwnerProfile` — remove entirely |
| 6 | Add `IUserAccountRepository` under controller in layout |
| 7 | Msg 1.2: `findPending` → `FindPendingAsync`; `out list: VerificationList` — `VerificationList` is invented; change to `out list: List<OwnerVerification>` |
| 8 | Msg 2.2: `findById` → `FindByIdAsync` |
| 9 | Msg 2.3: `retrieveDocuments` → `RetrieveDocumentsAsync`; `out documents: FileList` → `out documentUrls: List<String>` |
| 10 | Msg 3.2: `findById` → `FindByIdAsync` |
| 11 | Msg 3.3: `IOwnerProfileRepository.findByVerificationId(...)` → replace with `IUserAccountRepository.FindByIdAsync(in ownerId: Guid, out owner: UserAccount)` (code fetches owner for email) |
| 12 | Msg 3.6: `OwnerProfile.verify()` — remove (no such entity/method in code) |
| 13 | Msg 3.7: `update` → `UpdateAsync` |
| 14 | Msg 3.8: `IOwnerProfileRepository.update(OwnerProfile)` — remove (no such call in code) |

## Corrected Object Layout

```text
System Admin --- AdminUI --- ReviewVerificationController
                              |--- IOwnerVerificationRepository
                              |--- IUserAccountRepository
                              |--- VerificationLogic
                              |--- ICloudStorageGateway --- Cloud Storage
                              |--- IEmailGateway --- Email Provider
                              |--- OwnerVerification
```

## Corrected Seq 3 Flow

- 3.1: `approveVerification(in verificationId: Guid, in reviewNote: String, out response: DecisionResponseDto)`
- 3.2: `FindByIdAsync(in verificationId: Guid, out entity: OwnerVerification)` → IOwnerVerificationRepository
- 3.3: `FindByIdAsync(in ownerId: Guid, out owner: UserAccount)` → IUserAccountRepository
- 3.4: `ValidateDecision(in verification: OwnerVerification, out result: ValidationResult)` → VerificationLogic
- 3.5: `Approve(in reviewNote: String, out result: StatusChangeResult)` → OwnerVerification
- 3.6: `UpdateAsync(in entity: OwnerVerification)` → IOwnerVerificationRepository  *(was 3.7)*
- 3.7: `SendAsync(in message: EmailMessage)` → IEmailGateway  *(was 3.9)*
- 3.8: IEmailGateway → Email Provider  *(was 3.10)*

## Todo

- [ ] Remove `IOwnerProfileRepository` from participants table
- [ ] Remove `OwnerProfile` from participants table
- [ ] Add `IUserAccountRepository <<database wrapper>>` to participants table
- [ ] Fix object layout: remove `IOwnerVerificationRepository --- OwnerVerification`; add `OwnerVerification` directly under controller
- [ ] Fix object layout: remove `IOwnerProfileRepository --- OwnerProfile`
- [ ] Add `IUserAccountRepository` under controller in layout
- [ ] Fix Msg 1.2: `FindPendingAsync`; `List<OwnerVerification>`
- [ ] Fix Msg 2.2: `FindByIdAsync`
- [ ] Fix Msg 2.3: `RetrieveDocumentsAsync`; `out documentUrls: List<String>`
- [ ] Fix Msg 3.2: `FindByIdAsync`
- [ ] Fix Msg 3.3: replace with `IUserAccountRepository.FindByIdAsync(in ownerId: Guid, out owner: UserAccount)`
- [ ] Remove Msg 3.6 `OwnerProfile.verify()`
- [ ] Fix Msg 3.7: `UpdateAsync`
- [ ] Remove Msg 3.8 `IOwnerProfileRepository.update(OwnerProfile)`
- [ ] Renumber remaining messages accordingly

## Success Criteria

- No `IOwnerProfileRepository` or `OwnerProfile` in diagram
- `IUserAccountRepository` present in layout and participants
- `OwnerVerification` directly under controller in layout
- `RetrieveDocumentsAsync` returning `List<String>` not `FileList`
- Seq 3 shows only `OwnerVerification.Approve()` mutation (no `OwnerProfile.verify()`)
- All repo methods with Async suffix
