---
name: gomaa-class-design
description: Generate markdown-only Gomaa/COMET Phase Design artifacts from Phase 1.3 use case descriptions, Phase 2.1 static model, Phase 2.2 communication diagrams, optional Phase 2.3 statecharts, and design-level communication diagrams at step 3.0. Use when Codex must derive class interface specifications, operation contracts, private attributes, design communication diagrams, and a design class diagram blueprint for detailed design. Support both COMET-pure outputs and stack-specific simplifications such as ASP.NET simple layered backend. When `step-3.0-design-communication-diagram.md` exists, propagate its participants, stereotypes, and call flow into `step-3.1` and `step-3.2`. Do not use for analysis-level communication diagrams or draw.io rendering.
---

# Gomaa Class Design

Use this skill to turn COMET analysis artifacts into markdown design artifacts for class-level detailed design.

## Required Inputs

- `step-2.1-static-model.md` for classes, stereotypes, attributes, and relationships
- one or more `step-1.3-uc-*.md` files for business intent, preconditions, postconditions, and alternative flows
- one or more `step-2.2-*.md` communication diagrams for message-to-operation mapping
- optional `step-2.3-statechart-*.md` files for stateful classes
- optional `step-3.0-design-communication-diagram.md` when the user wants `step-3.1` and `step-3.2` to stay tightly aligned with a finalized design interaction model

Load [references/input-contract.md](references/input-contract.md) before deriving outputs.

## Output Set

Generate markdown only.

- `phase-3/<scope-folder>/step-3.0-design-communication-diagram.md` when the user asks for design interaction output or when later outputs must be aligned to an existing design interaction model
- `phase-3/<scope-folder>/step-3.1-class-interface-<class>.md`
- `phase-3/<scope-folder>/step-3.2-design-class-diagram-blueprint.md`

Filename rules:
- normalize `<class>` to lowercase kebab-case derived from the design class name
- use a dedicated folder per scope under `phase-3/`
- when the scope is a single use case, prefer `uc-<id>-<use-case-slug>` as the folder name
- when the scope is a subsystem or use-case cluster, normalize that scope to lowercase kebab-case for the folder name

Use:
- [references/class-interface-spec-template.md](references/class-interface-spec-template.md)
- [references/design-class-diagram-blueprint-template.md](references/design-class-diagram-blueprint-template.md)

## Workflow

1. Define scope by target class, subsystem, or use-case cluster.
2. Read the static model and confirm the target class exists there.
3. Collect every use case and communication diagram where that class participates.
4. Load the statechart when the class has lifecycle states, status fields, or state-dependent behavior. If it is missing and the contract depends on lifecycle rules, downgrade that class to a provisional specification instead of emitting a final lifecycle-sensitive contract.
5. Refine analysis stereotypes into design stereotypes where needed. In COMET-pure output, analysis `<<entity>>` classes normally become `<<data abstraction>>` classes. In stack-specific simplified output, an analysis `<<entity>>` may instead map to a repository-managed record type plus a `<<database wrapper>>` when the user explicitly wants an ASP.NET-style controller or repository flow and does not want a separate in-memory design object.
6. Apply information hiding: keep attributes private unless there is a strong design reason otherwise.
7. Map incoming messages to candidate public operations. Do not turn every outgoing message into a public operation. If a class is in scope only for relationships or hierarchy and has no justified incoming messages, record `no public operations in current scope` instead of inventing services.
8. Derive `in` parameters, `out` parameters, preconditions, postconditions, and invariants.
9. When the user asks for a design communication diagram, convert analysis messages into function-style messages. Prefer one directional message per function call and place both `in` and `out` parameters in that single message signature. Show a `<<user interaction>>` object between a human actor and any backend controller or boundary object. Use asynchronous messages without `out` parameters when the user explicitly wants background or fire-and-forget behavior such as outbound email dispatch.
10. If `step-3.0-design-communication-diagram.md` exists or is being generated in the same request, load it before writing `step-3.1` or `step-3.2` and treat it as the authoritative design interaction model for participant names, stereotypes, orchestration order, synchronous versus asynchronous calls, and message signatures.
11. Merge duplicate operations across use cases when they represent the same service.
12. Write the class interface specification.
13. Add the class to the design class diagram blueprint and update relationships if the analysis model already defines them.
14. When `step-3.0` is in scope, ensure every non-actor design participant that remains architecturally relevant in `step-3.1` and `step-3.2` is carried forward with the same name and stereotype unless the user explicitly asks to drop it.
15. Add traceability notes back to source artifacts.
16. Preserve the user's chosen architecture simplification. If the user explicitly asks for a simple layered backend, do not re-expand the design into extra COMET layers such as a separate business-logic facade or `<<data abstraction>>` class unless the user asks for that additional detail.

Load [references/operation-mapping-rules.md](references/operation-mapping-rules.md) when deriving operations.

## Non-Negotiable Rules

- Stay at design level, not implementation level.
- Produce markdown only. Do not generate draw.io, Mermaid, or images.
- Treat `step-2.1-static-model.md` as required for final design output. If it is missing, do not invent attributes or relationships.
- Treat statecharts as required for final lifecycle-sensitive contracts of stateful classes. If absent, downgrade that class to a provisional specification and mark lifecycle-sensitive statements as assumptions.
- Refine analysis `<<entity>>` classes to `<<data abstraction>>` by default in design output, unless the user explicitly requests a stack-specific simplified backend that intentionally omits a separate data-abstraction class.
- Map public operations primarily from incoming communication-diagram messages to the target class.
- If a class has no justified incoming messages in the chosen scope, do not invent public operations. Emit `no public operations in current scope` when the class is kept only for structural reasons.
- Keep entity data private by default.
- Keep naming consistent and service-oriented. Prefer verb-led operation names.
- Prefer operation signatures that use `in` and `out` parameters. Do not use `: ReturnType` unless the user explicitly asks for return-value notation.
- For design communication diagrams, use function-style messages. Prefer a single directional message with both `in` and `out` parameters in the signature, because `out` already implies returned data.
- For stack-specific simplified backends, allow a controller or boundary object to orchestrate repository, notification, and proxy collaborators directly when the user explicitly wants that simpler shape.
- When `step-3.0` exists, keep `step-3.1` and `step-3.2` consistent with it:
  - incoming messages to a participant in `step-3.0` become candidate operations of that participant in `step-3.1`
  - non-actor participants in `step-3.0` become candidate class boxes in `step-3.2`
  - call links in `step-3.0` become candidate associations in `step-3.2`
  - participant stereotypes from `step-3.0` should be preserved across `step-3.1` and `step-3.2` unless the user explicitly wants a refinement
- Do not finalize `step-3.1` or `step-3.2` while ignoring an existing `step-3.0` in the same scope folder.
- Trace every operation to at least one communication message and one use-case responsibility.

## Default Behavior for Gaps

- If `step-2.1` is missing: stop and ask for it, or explicitly limit output to a provisional operation list.
- If `step-2.3` is missing for a stateful class and the contract depends on lifecycle rules: do not emit a final lifecycle-sensitive contract. Produce a provisional specification and mark lifecycle-sensitive statements as assumptions.
- If messages and static model disagree on class names or responsibilities: surface the mismatch instead of silently reconciling it.

## References

- [references/input-contract.md](references/input-contract.md)
- [references/operation-mapping-rules.md](references/operation-mapping-rules.md)
- [references/class-interface-spec-template.md](references/class-interface-spec-template.md)
- [references/design-class-diagram-blueprint-template.md](references/design-class-diagram-blueprint-template.md)
