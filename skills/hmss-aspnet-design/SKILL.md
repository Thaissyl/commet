---
name: hmss-aspnet-design
description: Generate ASP.NET + React COMET Phase 3 design artifacts for one HMSS use case: design communication diagram (step-3.0), per-class interface specs (step-3.1), and design class diagram blueprint (step-3.2), then invoke drawio-design-class-diagram to render the .drawio file. Use when working on 260310-hmss Phase 3 for a specific use case with the simple ASP.NET Web API + React stack. Trigger on phrases like "do phase 3 for UC-XX", "design communication diagram for UC", "class interface spec for UC", "step-3.0 for UC-XX", "generate design artifacts for use case".
---

# HMSS ASP.NET Design — Phase 3 Artifact Generator

Generate all Phase 3 design artifacts for one HMSS use case targeting the ASP.NET Web API + React simple layered backend.

## Required Inputs

Read these files before producing anything:

1. `260310-hmss/step-1.3-uc-<id>-<slug>.md` — use case description (pre/postconditions, main and alt flows)
2. `260310-hmss/phase-2/step-2.1-static-model.md` — analysis class stereotypes and attributes
3. `260310-hmss/phase-2/step-2.2-uc-<id>-<slug>-main-seq.md` — analysis communication diagram (participants, simple messages)

## Output — save all to `260310-hmss/phase-3/uc-<id>-<slug>-aspnet-react/`

| File | What it is |
|------|-----------|
| `step-3.0-design-communication-diagram.md` | Design comm diagram with design participants, ASP.NET stereotypes, and function-style message signatures |
| `step-3.0-design-communication-diagram.drawio` | Rendered by `drawio-communication-diagram` skill after step-3.0 is saved |
| `step-3.1-class-interface-<class-kebab>.md` | One file per design participant (excluding actors) |
| `step-3.2-design-class-diagram-blueprint.md` | Design class diagram with all classes, attributes, operations, and relationships |
| `step-3.2-design-class-diagram-blueprint.drawio` | Rendered by `drawio-design-class-diagram` skill after step-3.2 is saved |

## Workflow

**Step 1 — Read inputs.** Read the three required files listed above.

**Step 2 — Map analysis objects to design objects.** Apply rules from `references/aspnet-stack-mapping.md`.

**Step 3 — Write `step-3.0`.** Follow the format in `references/output-templates.md` → section "step-3.0". Decide sync vs async per message using the message-type rules in `references/aspnet-stack-mapping.md`. Output the file immediately.

**Step 3.5 — Render `step-3.0.drawio`.** Invoke the `drawio-communication-diagram` skill with the saved `step-3.0` file as input. Follow layout and style rules from `references/drawio-mapping-guide.md` → section "Step-3.0 → Communication Diagram". Save next to the `.md` file as `step-3.0-design-communication-diagram.drawio`.

**Step 4 — Write `step-3.1` files.** One file per non-actor design participant, derived directly from step-3.0 message signatures. Use the template in `references/output-templates.md` → section "step-3.1". For each class: incoming messages → `Operations Provided`, outgoing calls → `Operations Required`. Output each file immediately.

**Step 5 — Write `step-3.2`.** Derived from step-3.0 (participants + stereotypes) and step-3.1 (attributes + operations). Use template in `references/output-templates.md` → section "step-3.2". Output the file immediately.

**Step 6 — Render `step-3.2.drawio`.** Invoke the `drawio-design-class-diagram` skill with the saved `step-3.2` file as input. Also pass the `step-3.0` path so the class diagram layout aligns with the communication diagram participant flow. Follow style rules from `references/drawio-mapping-guide.md` → section "Step-3.2 → Design Class Diagram". Save as `step-3.2-design-class-diagram-blueprint.drawio`.

## Rules

- Do not narrate reasoning. Output artifacts directly.
- step-3.0 is the authoritative source for participant names and stereotypes. step-3.1 and step-3.2 must align with it.
- Never separate reply arrows — encode `out` params in the same message label as `in` params.
- Email and other external dispatch: always `sendAsync(in message)` — no `out` param.
- Do not invent operations that have no incoming messages in step-3.0.
- **Data abstraction participant rule**: A `<<data abstraction>>` that flows through the UC as an `out` parameter (e.g., `out listing: RoomListing`, `out mapData: MapData`) **MUST** be included in the step-3.0 Participants table and Object Layout. However, it is **NOT a message target** — do not add separate messages to it in the Messages table. The controller uses these data abstractions internally via field extraction/DTO mapping, not via method calls.
- In step-3.2 class diagrams, show `<<data abstraction>>` classes with their attributes, but mark Operations as "none in current scope" when the controller only accesses fields internally to build response DTOs.
- **DB-level filtering rule**: When a UC passes user search criteria to the repository, push filtering into `<<database wrapper>>` (e.g. `findListingsByCriteria(in criteria: ..., out matchedListings: ...)`). Do NOT load the full table then filter in a `<<service>>` — that causes memory exhaustion at scale.
- **Complete every coordinator sequence**: Every sequence where a `<<coordinator>>` returns a response must show all repository/service calls it needs to build that response. A controller that returns data without querying anything is a "hanging" coordinator — add the missing `findById` or equivalent call.
- **Synchronous external calls**: When a UC response depends on external gateway data, the call is synchronous (with `out` param). Note in the design that the `<<proxy>>` must enforce a strict timeout so external outages do not block the HTTP response.
- Also read `skills/gomaa-class-design/references/operation-mapping-rules.md` for parameter naming, precondition/postcondition derivation, and anti-pattern rules. Those rules apply here too.

## References

- `references/aspnet-stack-mapping.md` — object mapping + message-type decision rules
- `references/output-templates.md` — exact file templates for all three outputs
- `references/drawio-mapping-guide.md` — drawio component styles, color palette, layout rules, and invocation sequence for step-3.0 and step-3.2
- `skills/gomaa-class-design/references/operation-mapping-rules.md` — parameter and contract rules (reuse, do not duplicate)
- `skills/gomaa-class-design/references/input-contract.md` — blocking conditions and downgrade rules
- `skills/drawio-communication-diagram/references/xml-patterns.md` — drawio XML patterns for communication diagrams
- `skills/drawio-design-class-diagram/references/xml-patterns.md` — drawio XML patterns for design class diagrams
