# Input Contract

Use this reference to decide whether the source set is complete enough for markdown class design output.

## Required source set

- `step-2.1-static-model.md`
- at least one `step-1.3-uc-*.md`
- at least one `step-2.2-*.md`

## Optional source set

- matching `step-2.3-statechart-*.md` files for classes with lifecycle behavior
- `step-3.0-design-communication-diagram.md` when the user wants class interfaces and the design class diagram to align with a finalized design interaction view

## Step-3.0 precedence

If `step-3.0-design-communication-diagram.md` exists in the same design scope folder, treat it as the authoritative source for:

- design participant names
- design participant stereotypes
- interaction ordering
- synchronous versus asynchronous call style
- message signatures that should propagate into `step-3.1` and `step-3.2`

## Normalize to this model

- `target_scope`
  - class names, or
  - use-case cluster, or
  - subsystem name
- `design_style`
  - `comet-pure`, or
  - `stack-specific-simplified`
- `stack_hint`
  - optional framework or technology target such as `asp.net simple layered backend`
- `classes[]`
  - `name`
  - `stereotype`
  - `attributes[]`
  - `relationships[]`
- `use_cases[]`
  - `id`
  - `name`
  - `preconditions[]`
  - `main_flow[]`
  - `alternative_flows[]`
  - `postconditions[]`
- `interactions[]`
  - `diagram`
  - `messages[]`
    - `number`
    - `from`
    - `to`
    - `text`
- `design_interaction`
  - `participants[]`
    - `name`
    - `stereotype`
    - `kind`
  - `messages[]`
    - `number`
    - `from`
    - `to`
    - `signature`
- `state_models[]`
  - `class_name`
  - `states[]`
  - `transitions[]`

## Minimum completeness rules

- Require the target class to exist in the static model.
- Require at least one incoming message to the target class, unless the class is purely structural in the chosen scope.
- Require use-case coverage for every operation that will be exposed publicly.
- Require statechart coverage when the class contract depends on status or state transitions.
- If the user explicitly selects a simplified stack-specific design, allow analysis `<<entity>>` responsibilities to be represented by a repository-managed record type instead of a separate `<<data abstraction>>` class.
- If the user explicitly selects a simplified stack-specific design, allow a controller or boundary object to orchestrate repository and infrastructure collaborators directly.
- If `step-3.0` exists, require participant names and stereotypes in `step-3.1` and `step-3.2` to stay aligned unless the user explicitly requests a redesign between steps.

Purely structural classes are allowed only when they are kept in scope for relationships, composition, aggregation, or generalization. For those classes:

- do not invent public operations
- allow a class interface specification with `Operations Provided: none in current scope`
- always include them in the design class diagram blueprint when they affect structure

## Blocking conditions

Stop and ask, or clearly downgrade the output, when any of these appear:

- no `step-2.1-static-model.md`
- target class missing from the static model
- communication diagram names do not match static-model classes closely enough to reconcile safely
- no communication diagram covers the chosen target class, unless the class is explicitly structural in the chosen scope
- class appears stateful but no lifecycle source exists and the operation contracts would depend on state
- user asks for a final design class diagram blueprint while relationships are missing

## Allowed downgrade

If the user insists on proceeding with incomplete inputs:

- produce a provisional class specification using the available static model, use cases, and communication diagrams
- do not invent private attributes or relationships that are not supported by the static model
- do not finalize lifecycle-sensitive preconditions, postconditions, or invariants without a supporting statechart
- mark all unsupported lifecycle-sensitive statements as assumptions
- preserve any user-requested simplification that intentionally removes intermediate layers or separate in-memory design objects
- when `step-3.0` exists, prefer its participant list and message signatures over older analysis naming when deriving `step-3.1` and `step-3.2`

## Output Naming

When the session folder is known, use:

- `phase-3/<scope-folder>/step-3.1-class-interface-<class>.md`
- `phase-3/<scope-folder>/step-3.2-design-class-diagram-blueprint.md`
- optional `phase-3/<scope-folder>/step-3.0-design-communication-diagram.md`

When the session folder is not known, use:

- `output/<scope-folder>/step-3.1-class-interface-<class>.md`
- `output/<scope-folder>/step-3.2-design-class-diagram-blueprint.md`
- optional `output/<scope-folder>/step-3.0-design-communication-diagram.md`

Naming normalization:

- normalize `<class>` to lowercase kebab-case from the design class name, for example `RentalRequest` -> `rental-request`
- when the scope is a single use case, normalize `<scope-folder>` as `uc-<id>-<use-case-slug>`
- otherwise normalize `<scope-folder>` from the subsystem name, use-case cluster name, or `system`
