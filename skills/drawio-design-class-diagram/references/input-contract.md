# Input Contract

Use this reference when normalizing design class diagram source text or deciding whether to stop and ask for clarification.

## Accept Source Forms

- Accept structured markdown with sections such as `Scope`, `Class Boxes`, `Relationships`, `Generalizations`, and optional `Notes`.
- Accept a Phase 3 use-case or subsystem folder when it contains a design class diagram blueprint and optional per-class interface specs.
- Accept an existing `.drawio` file only when the user also provides the revised blueprint source or a precise change request.
- Ignore supplemental sections that help traceability but do not define geometry, such as `Source artifacts` and `Traceability Summary`, unless the user explicitly asks to visualize them.
- Accept infix association shorthand in `Relationships`, such as ``ClassA 1 -- 1 ClassB : label``.

## Normalize To This Model

Use a model with these fields before drawing:

- `title`
- `classes[]`
  - `name`
  - `stereotype`
  - `attributes[]`
  - `operations[]`
- `relationships[]`
  - `from`
  - `to`
  - `type`
  - `source_multiplicity`
  - `target_multiplicity`
  - `association_name`
  - `reading_direction`
  - `source_navigability`
  - `target_navigability`
  - `label`
- `generalizations[]`
  - `superclass`
  - `subclass`
- `notes[]`

## Class Rules

- Require a unique name for every class.
- Require a stereotype for every class.
- Normalize stereotype text to the inner content only.
- Example: source `<<coordinator>>` becomes normalized value `coordinator`.
- Preserve class names exactly as written once validated.
- Treat `- attr: Type` and `+ op(...)` lines in the blueprint as the authoritative visible members for drawing.
- If the blueprint omits attributes or operations for a class, use matching `step-3.1-class-interface-*.md` files only when they are explicitly in scope and clearly match that class.
- Keep blueprint ordering when it is already reasonable because it often reflects the intended reading order in the report.

## Relationship Rules

- Require every relationship endpoint to match a validated class name exactly.
- Accept these relationship types only: `association`, `aggregation`, `composition`.
- For `aggregation` and `composition`, normalize `from` as the whole and `to` as the part so the diamond can be rendered on the correct side.
- Normalize plain infix `--` relationship syntax as `association`.
- Preserve multiplicities exactly when supplied.
- Treat `association_name` as the preferred short label for report-grade diagrams.
- Accept `reading_direction` values such as `source-to-target`, `target-to-source`, `left-to-right`, `right-to-left`, `top-to-bottom`, or `bottom-to-top`.
- Accept `source_navigability` and `target_navigability` values `none` or `navigable`.
- Keep `label` as optional source prose for backward compatibility with older blueprints.
- If a shorthand relationship provides only long prose after `:`, keep that prose as `label`; derive a shorter displayed association name only when the phrase already contains an obvious concise verb phrase.
- Ask when a relationship type is ambiguous or when the source uses prose that could mean more than one UML relationship.
- Parse inheritance in `generalizations[]`, not in `relationships[]`.

## Note Rules

- Accept plain notes from a `Notes` section as optional visual annotations.
- If a note explicitly starts with a validated class name followed by `:`, treat it as class-local and place it near that class.
- Otherwise place the note in a small note area below or to the side of the main class layout.
- Do not infer hidden relationships from notes alone.

## Blocking Conditions

Stop and ask focused clarification questions when any of these appear:

- duplicate class names
- missing class name
- relationship endpoint not present in the class list
- ambiguous relationship type
- mixed inheritance encoding where one source expresses the same link as both a relationship and a generalization
- generalization without clear superclass and subclass
- the request is not actually for a UML design class diagram
- two different source files disagree on a class signature and the user did not define precedence

## Output Convention

- Save next to the source blueprint with the same basename and a `.drawio` extension when the blueprint path is known.
- Save to `output/<slug>.drawio` when the user only provides pasted text.
- Use the normalized title or basename as the draw.io page name.
- Store the diagram as XML text with a `.drawio` extension.

## Clarification Style

- Ask the smallest set of questions that resolves the blockage.
- Prioritize missing class identity, unknown relationship type, inconsistent multiplicity, and conflicting class signatures.
- Do not ask for cosmetic preferences unless layout or output path cannot be inferred.
