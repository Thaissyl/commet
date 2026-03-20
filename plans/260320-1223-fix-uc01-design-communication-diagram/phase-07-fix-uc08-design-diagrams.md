# Phase 07: Document Fix — Rewrite UC-08a & UC-08b step-3.0-design-communication-diagram.md

**Status:** Ready (no code changes needed)
**Priority:** High

## Context Links

- Use case 08a: `C:\Users\welterial\commet\260310-hmss\step-1.3-uc-08a-create-property.md`
- Use case 08b: `C:\Users\welterial\commet\260310-hmss\step-1.3-uc-08b-update-property.md`
- Analysis 08a: `C:\Users\welterial\commet\260310-hmss\phase-2\step-2.2-uc-08a-create-property-main-seq.md`
- Analysis 08b: `C:\Users\welterial\commet\260310-hmss\phase-2\step-2.2-uc-08b-update-property-main-seq.md`
- Design 08a: `C:\Users\welterial\commet\260310-hmss\phase-3\uc-08a-create-property-aspnet-react\step-3.0-design-communication-diagram.md`
- Design 08b: `C:\Users\welterial\commet\260310-hmss\phase-3\uc-08b-update-property-aspnet-react\step-3.0-design-communication-diagram.md`
- Code: `backend/Hmss.Api/Controllers/PropertyController.cs`

## UC-08a Errors

| # | Error |
|---|-------|
| 1 | Participant `CreatePropertyController` → `PropertyController` |
| 2 | `Property <<data abstraction>>` participant + `IPropertyRepository --- Property` layout line — remove (no method called on `Property` in UC-08a) |
| 3 | `PropertyService` stereotype `<<service>>` → `<<business logic>>` |
| 4 | Msg 3.3: `save` → `SaveAsync` |

## UC-08b Errors

| # | Error |
|---|-------|
| 1 | Participant `UpdatePropertyController` → `PropertyController` |
| 2 | Participant name `Property / PropertyList` → `Property` only (no method called on `PropertyList`) |
| 3 | Object layout `IPropertyRepository --- Property / PropertyList` → remove entirely; add `Property` directly under controller (controller calls `applyUpdates`, not the repo) |
| 4 | Msg 1.1: remove `in ownerId: Guid` param (comes from JWT, not request param) |
| 5 | Msg 1.2: `findByOwnerId` → `FindByOwnerIdAsync`; return type `PropertyList` → `List<Property>` |
| 6 | Msg 2.2, 4.2: `findById` → `FindByIdAsync` |
| 7 | Msg 4.5: `update` → `UpdateAsync` |

## Todo

**UC-08a:**
- [ ] Rename participant `CreatePropertyController` → `PropertyController`
- [ ] Remove `Property <<data abstraction>>` from participants table
- [ ] Remove `IPropertyRepository --- Property` from object layout
- [ ] Fix `PropertyService` stereotype: `<<service>>` → `<<business logic>>`
- [ ] Fix Msg 3.3: `save` → `SaveAsync`

**UC-08b:**
- [ ] Rename participant `UpdatePropertyController` → `PropertyController`
- [ ] Rename participant `Property / PropertyList` → `Property`
- [ ] Fix object layout: remove `IPropertyRepository --- Property / PropertyList`; add `|--- Property` directly under `PropertyController`
- [ ] Fix Msg 1.1: remove `in ownerId: Guid`
- [ ] Fix Msg 1.2: `findByOwnerId` → `FindByOwnerIdAsync`, `PropertyList` → `List<Property>`
- [ ] Fix Msg 2.2, 4.2: `findById` → `FindByIdAsync`
- [ ] Fix Msg 4.5: `update` → `UpdateAsync`

## Success Criteria

- Both diagrams show `PropertyController` as coordinator
- UC-08a: no `Property` participant; `PropertyService` is `<<business logic>>`; `SaveAsync` used
- UC-08b: participant is `Property` only; `FindByOwnerIdAsync`, `FindByIdAsync`, `UpdateAsync` used; no `in ownerId` param in msg 1.1
