# Class Interface Specification Template

```markdown
# Class Interface Specification: <ClassName>

## Class Summary

- Stereotype: `<<...>>`
- Scope: <target scope or subsystem>
- Hidden Information: <what internal data or representation is hidden>
- Structuring Criterion: <boundary | data abstraction | database wrapper | coordinator | business logic | service | other>

## Assumptions

- <assumption 1>
- <assumption 2>

## Anticipated Changes

- <change 1>
- <change 2>

## Private Attributes

| Attribute | Type | Purpose |
| --- | --- | --- |
| `- <name>` | `<type>` | <why it is stored> |

## Invariants

- <condition that must always hold>

## Collaborators

- `<ClassName>`: <reason>

## Operations Provided

- If this class is purely structural in the current scope, write: `- None in current scope.`

### `+ <operationName>(in <inputParam>, out <outputParam>)`

- Source trace: `<UC id + message numbers + optional statechart transition>`
- Function: <what service this operation provides>
- Parameters:
  - `in <inputParam>: <meaning>`
  - `out <outputParam>: <meaning>`
- Preconditions:
  - <condition>
- Postconditions:
  - <condition>

### `+ <operationName>(in <inputParam>, out <outputParam>)`

- Source trace: `<...>`
- Function: <...>
- Parameters:
  - `in <...>`
  - `out <...>`
- Preconditions:
  - <...>
- Postconditions:
  - <...>
```
