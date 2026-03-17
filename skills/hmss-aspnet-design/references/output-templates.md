# Output Templates

Exact file templates for all three Phase 3 outputs.
Copy structure, fill placeholders, remove placeholder comments.

---

## step-3.0 — Design Communication Diagram

```markdown
# Design Communication Diagram: <UC-ID> <UC Name> - ASP.NET Simple Layered Backend

## Design Communication Decision

- Diagram level: design phase
- Backend style: simple layered backend
- Main flow: `<UI> -> Controller`, then `Controller -> Repository` and `Controller -> infrastructure collaborators`
- Message style: single directional function messages
- Synchronous request messages carry `in` and `out` parameters in the same label when a response payload is expected
- Separate reply arrows are intentionally omitted because `out` parameters already represent returned data
- Request flow style: <e.g. "synchronous request handling" or "synchronous request handling with asynchronous email dispatch">

## Object Layout

\`\`\`text
<Actor> --- <UI> --- <Controller>
                       |--- <IRepository>
                       |--- <Service> (if any)
                       |--- <IGateway> --- <External Actor> (if any)
\`\`\`

## Participants

| Position | Object | Stereotype |
| --- | --- | --- |
| 1 | <Actor name> | Actor (primary) |
| 2 | <UI class> | `<<user interaction>>` |
| 3 | <Controller class> | `<<coordinator>>` |
| 4 | <IRepository class> | `<<database wrapper>>` |
| 5 | <Entity domain class> | `<<data abstraction>>` |
| 6 | <Service class> | `<<service>>` |
| 7 | <IGateway class> | `<<proxy>>` |
| 8 | <External system> | Actor (secondary) |

<!-- Remove rows that do not apply to this UC.
     <<data abstraction>> = the domain Model class (MVC Model). Owns business rules and state-change methods.
     <<database wrapper>> = the Repository interface. Loads/saves <<data abstraction>> objects; hides EF Core/SQL. -->

## Messages

| # | From -> To | Message |
| --- | --- | --- |
| ... | ... | ... |

<!-- Derive message groups from the use-case main sequence steps.
     Number top-level groups by sequence step (1, 2, 3...), sub-messages as X.1, X.2...
     Convert analysis noun-phrase messages to verb-led method names per aspnet-stack-mapping.md.

     Write pattern for any action that mutates a domain object:
       X.N   Controller -> IRepository    findById(in id: Guid, out entity: DomainClass)
       X.N+1 Controller -> DomainClass    applyXxxChange(in action: ActionDto, out result: ChangeResult)
       X.N+2 Controller -> IRepository    save(in entity: DomainClass, out persisted: DomainClass)

     Async pattern (fire-and-forget, no out):
       X.N   Controller -> IGateway       sendAsync(in msg: EmailMessage)
       X.N+1 IGateway   -> External       sendAsync(in msg: EmailMessage)

     See aspnet-stack-mapping.md for full message-type decision rules and naming conventions. -->

## Analysis → Design Message Mapping

| Analysis message | Design message | Notes |
| --- | --- | --- |
| `#` From → To: "noun phrase" | `#.n` From -> To: `methodName(in ..., out ...)` | e.g. sync/async, renamed |

<!-- One row per analysis message. Shows traceability from step-2.2 simple messages to step-3.0 function-style messages.
     Leave blank / omit if a design message has no direct analysis counterpart (e.g. added for infrastructure reasons). -->

## Alternative Flow Notes

- <Describe what is skipped or changed when an alternative or error path applies>

## Notes

- `<UI>` is shown explicitly so the human actor does not interact directly with the backend controller.
- `<IRepository>` handles persistence and returns data abstractions (e.g., `RoomListing`) via `out` parameters.
- `<Controller>` acts as the simplified orchestration point. **DTO mapping happens internally within the controller's operations** — when repository returns a data abstraction, controller extracts fields and builds the response DTO. This is internal logic, not a separate message.
- <Any async justification, e.g. "Email dispatch is intentionally asynchronous to avoid blocking the HTTP request.">
```

---

## step-3.1 — Class Interface Specification

One file per design participant (excluding actors). Filename: `step-3.1-class-interface-<class-kebab>.md`.

```markdown
# Class Interface Specification: <ClassName>

## Class Summary

- Stereotype: `<<stereotype>>`
- Scope: `<UC-ID> <UC Name> - ASP.NET simple layered backend`
- Hidden Information: <what this class hides — e.g. "HTTP route binding, ASP.NET model binding, API response translation">
- Structuring Criterion: <boundary | database wrapper | service | proxy | user interaction>

## Assumptions

- <assumption 1>
- <assumption 2>

## Anticipated Changes

- <anticipated change 1>

## Private Attributes

- None in current scope.

<!-- OR list attributes:
| Attribute | Type | Purpose |
| --- | --- | --- |
| `- <name>` | `<Type>` | <why stored> |
-->

## Invariants

- <condition that always holds, e.g. "Must not embed SQL directly.">

## Collaborators

- `<ClassName>`: <role, e.g. "frontend caller", "loads and persists records">

## Operations Provided

<!-- Derive from incoming messages in step-3.0 where this class is the receiver -->

### `+ <operationName>(in <param>: <Type>, out <param>: <Type>)`

- Source communication messages: `<1.1>`, `<1.2>`
- Function: <what this operation does>
- Parameters:
  - `in <param>`: <meaning>
  - `out <param>`: <meaning>
- Preconditions:
  - <condition>
- Postconditions:
  - <condition>

## Operations Required

<!-- List outgoing calls this class makes in step-3.0 -->

- `<CollaboratorClass>.<method>(in <param>: <Type>, out <param>: <Type>)` from message `<#>`
```

---

## step-3.2 — Design Class Diagram Blueprint

```markdown
# Design Class Diagram Blueprint: <UC-ID> <UC Name> - ASP.NET Simple Layered Backend

## Scope

- Included classes: `<UI>`, `<Controller>`, `<IRepository>`, `<Service>` (if any), `<IGateway>` (if any)
- Synchronization source:
  - participant set and call structure from `step-3.0-design-communication-diagram.md`
  - class operations and responsibilities from `step-3.1-class-interface-*.md`

## Class Boxes

### `<ClassName>`

- Stereotype: `<<stereotype>>`
- Attributes:
  - none in current scope
  <!-- OR: - `- <name>: <Type>` -->
- Operations:
  - `+ <methodName>(in <param>: <Type>, out <param>: <Type>)`
  - `+ <asyncMethod>(in <param>: <Type>)` <!-- no out for async -->

<!-- Repeat for every non-actor design participant -->

## Relationships

<!-- One block per directed association derived from step-3.0 call paths -->

- association:
  - from: `<SourceClass>`
  - to: `<TargetClass>`
  - source multiplicity: `1`
  - target multiplicity: `1`
  - association name: `<short verb phrase>`
  - reading direction: `source-to-target`
  - source navigability: `none`
  - target navigability: `navigable`

## Generalizations

- none in current scope

## Notes

- This version uses a simplified orchestration style where the controller coordinates repository and infrastructure collaborators directly.
- `<UI>` is included to keep the class diagram aligned with the design communication diagram.
- **Data abstractions** (`<<data abstraction>>`) that flow through the UC as `out` parameters should be included as class boxes to show their structure (attributes). However, mark Operations as "none in current scope" when the controller only accesses their fields internally to build response DTOs — this is not a separate method call but internal coordinator logic.
- <Any note about async separation, interface hiding, or simplification rationale>
```
