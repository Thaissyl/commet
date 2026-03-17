---
title: "Draw.io Design Class Diagram Skill"
description: "Plan a Codex skill that turns Phase 3 markdown class blueprints into editable draw.io class diagrams."
status: pending
priority: P2
effort: 3h
branch: main
tags: [skills, drawio, uml, class-diagram]
created: 2026-03-17
---

# Overview

Goal: add a new skill `skills/drawio-design-class-diagram` that reads `step-3.2-design-class-diagram-blueprint.md` and optional `step-3.1-class-interface-*.md`, then emits editable draw.io XML for design class diagrams only.

Inputs:
- required: Phase 3 class diagram blueprint markdown
- optional: class interface specs for fuller attributes and operations

Outputs:
- `.drawio` file generated from draw.io XML
- skill docs and references for repeatable create/update workflow

# Phases

## Phase 1: Reuse existing patterns
- Inspect `skills/drawio-communication-diagram` for XML structure, save/update workflow, and draw.io tool usage.
- Inspect `skills/gomaa-class-design` for Phase 3 artifact naming and blueprint assumptions.
- Keep only shared mechanics; do not inherit communication-diagram message rules.

## Phase 2: Define skill contract
- Write `SKILL.md` with supported inputs, blocking conditions, naming, output location, and create vs update workflow.
- Require explicit class names, stereotypes, attributes, operations, and relationship types from blueprint/specs.
- Stop on ambiguous multiplicity, inheritance, or composition semantics instead of guessing.

## Phase 3: Define class-diagram XML rules
- Add references for three-compartment class boxes, stereotype rendering, private attributes `-`, public operations `+`.
- Define edge styles for association, aggregation, composition, and generalization, including multiplicity/navigability labels.
- Include layout heuristics for readable subsystem or use-case-scope diagrams.

## Phase 4: Validate with repo artifacts
- Dry-run against one existing Phase 3 blueprint in `260310-hmss/phase-3/`.
- Confirm the result opens cleanly in draw.io and remains editable.
- Tighten rules only where the dry-run exposes ambiguity.

# Deliverables

- `skills/drawio-design-class-diagram/SKILL.md`
- `skills/drawio-design-class-diagram/references/input-contract.md`
- `skills/drawio-design-class-diagram/references/xml-patterns.md`
- optional example blueprint if validation shows it is needed

# Risks

- Blueprint markdown may omit multiplicity or relationship semantics.
- Long operation lists can make class boxes unreadable without layout rules.
- Update-in-place for existing `.drawio` may be less reliable than regeneration.

# Done

- Skill handles create and update flows for design class diagrams only.
- Output is draw.io XML, not Mermaid or image export.
- One repo blueprint renders successfully without manual XML surgery.

# Unresolved questions

- None.
