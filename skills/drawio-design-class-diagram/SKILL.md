---
name: drawio-design-class-diagram
description: Create or update editable draw.io UML design class diagrams from markdown design class diagram blueprints and optional class interface specification files. Use when Codex must parse class names, stereotypes, private attributes, public operations, associations, aggregation or composition, generalization, multiplicity, and render a design class diagram as draw.io XML. Support both COMET-pure class models and stack-specific simplified class models such as ASP.NET simple layered backend. When `step-3.0-design-communication-diagram.md` exists in the same scope, use it to keep class presence, stereotypes, and left-to-right flow aligned with the finalized design interaction model. Use only for design class diagrams, not communication diagrams.
---

# Drawio Design Class Diagram

Use this skill to turn design class diagram source text into editable draw.io XML and save it as a `.drawio` file.

## Quick Start

1. Normalize the input with [references/input-contract.md](references/input-contract.md).
2. Stop and ask focused clarification questions when any blocking issue appears. Do not guess.
3. Build or update the diagram in XML with [references/xml-patterns.md](references/xml-patterns.md).
4. Save the XML as a `.drawio` file.
5. Open the XML with `mcp__drawio__open_drawio_xml` for a visual check when that tool is available.

## Supported Inputs

- Use for structured markdown blueprints with sections such as `Scope`, `Class Boxes`, `Relationships`, `Generalizations`, and `Notes`.
- Use for a Phase 3 folder that contains `step-3.2-design-class-diagram-blueprint.md` and optional `step-3.1-class-interface-*.md` files.
- When available, also read `step-3.0-design-communication-diagram.md` to keep the class diagram aligned with the finalized design interaction model.
- Use for update requests that include an existing `.drawio` file plus revised blueprint text.

If `step-3.0-design-communication-diagram.md` exists in the same scope folder, load it before drawing.

Load [references/example-blueprint.md](references/example-blueprint.md) only when you need a concrete example of the normalized source format.

## Normalize Before Drawing

Require a normalized model with:
- a diagram title or output basename
- unique classes with names and stereotypes
- attributes per class
- operations per class
- relationships with known endpoints and relationship type
- association names and reading direction when the user wants polished report-grade relationship lines
- navigability metadata when the relationship is meant to be directional
- whole-part direction for every aggregation or composition
- multiplicity labels when the source gives them
- generalizations with known superclass and subclass

Normalize stereotype text to the inner content only.
Example: source `<<data abstraction>>` becomes normalized stereotype `data abstraction`, then render it back as `&#171;data abstraction&#187;` in the class header.
Respect user-chosen simplifications from the blueprint. If the blueprint intentionally omits a separate `<<data abstraction>>` or business-logic class for an ASP.NET-style simple layered backend, do not add it back during drawing.

Per-class interface spec files are optional enrichment.
When a class box in the blueprint already defines attributes or operations, treat that blueprint as the source of truth unless the user explicitly asks for merge behavior.

## Create Workflow

- Parse the blueprint into the normalized model.
- Validate class names, stereotypes, relationship endpoints, multiplicities, and generalization pairs before drawing.
- When `step-3.0-design-communication-diagram.md` is available, cross-check that non-actor design participants from `step-3.0` are represented consistently in the blueprint before drawing.
- If the blueprint conflicts with `step-3.0`, stop and reconcile the difference instead of drawing from stale class-level inputs.
- Normalize infix relationship shorthand `ClassA mult -- mult ClassB : label` to `association` before drawing.
- Render each class as a simple single-cell UML class box, not a nested container assembly.
- Keep private attributes in the middle section and public operations in the bottom section of that single class box.
- Render stereotypes in the class header.
- Apply layer-based color styling from stereotype so boundary, coordination, logic, data, service, and proxy classes are visually distinct.
- Render associations, aggregation or composition, and generalization using UML-style edges.
- When relationship semantics are available, render association name, reading direction marker, navigability arrowheads, and multiplicities together.
- When the blueprint expresses a simple layered backend, preserve that compact class set instead of expanding it into COMET-pure layers.
- Place boundary and user interaction classes to the left, coordinators and business logic near the center, data abstractions toward the right or lower-right, and proxies or services toward the right when that improves readability.
- Save the final XML as a `.drawio` file next to the source file when a source file exists.
- Save to `output/<slug>.drawio` when the user gives only pasted text and no source path.

## Update Workflow

- Read the existing `.drawio` XML and the revised blueprint text.
- Preserve current class positions and edge routing when the structure is still compatible.
- Patch labels, compartments, multiplicities, and changed relationships when the topology is unchanged.
- Regenerate the full diagram instead of patching piecemeal when the class set, hierarchy, or layout logic changed substantially.
- Tell the user when you switch from minimal patching to full regeneration.

## Non-Negotiable Rules

- Do not guess missing class names, stereotypes, relationship endpoints, multiplicities, or inheritance direction.
- Do not silently rename classes.
- Do not use Mermaid or CSV for final rendering. Use draw.io XML.
- Render each class as a simple UML class box with three visible sections inside one draw.io cell.
- Use stereotype-driven colors consistently across the full diagram.
- When `step-3.0` is available, do not silently omit a still-relevant non-actor participant that appears there but is also intended to exist in the class-level design.
- When `step-3.0` is available, do not draw a class-level participant order that contradicts its finalized left-to-right interaction flow unless the user explicitly asks for a different layout.
- Keep multiplicities visible when the source provides them.
- Prefer short association names on the line; do not dump long prose onto the edge.
- Show navigability only when it is explicit or unambiguous from the normalized model.
- Use the relationship type from the blueprint: association, aggregation, or composition.
- Treat generalization as a separate inheritance list, not as a normal association-style relationship entry.
- Do not invent methods or attributes that are absent from the supplied blueprint or interface specs.
- Do not add extra COMET classes that are absent from the supplied blueprint just because they would exist in a more detailed or purist design.

## References

- Use [references/input-contract.md](references/input-contract.md) for parsing rules, blocking conditions, and output naming.
- Use [references/xml-patterns.md](references/xml-patterns.md) for draw.io XML structure, class-box construction, edge styles, multiplicity labels, and layout heuristics.
- Use [references/example-blueprint.md](references/example-blueprint.md) only when you need a full example blueprint.
