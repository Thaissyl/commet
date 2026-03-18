# Input Contract

Use this reference when normalizing source text or deciding whether to stop and ask for clarification.

## Accept Source Forms

- Accept structured markdown with sections such as `Object Layout`, `Participants`, `Messages`, and optional `Notes`.
- Accept loose raw text when it still supplies the same facts in prose or lists.
- Accept an existing `.drawio` file only when the user also provides the revised diagram source or a precise change request.

## Normalize To This Model

Use a model with these fields before drawing:

- `title`: diagram title or basename
- `participants[]`:
  - `name`
  - `kind`: `actor` or `software_object`
  - `actor_role`: optional `primary` or `secondary`
  - `stereotype`: required for every software object
- `associations[]`: undirected links between participant names
- `messages[]`:
  - `number`
  - `from`
  - `to`
  - `text`
- `notes[]`: optional constraints that affect layout or direction

## Participant Rules

- Treat `Actor (primary)` and `Actor (secondary)` as actors.
- Treat `<<...>>` or `&#171;...&#187;` stereotypes as software objects.
- Preserve participant names exactly as written once validated.
- Require a stereotype for every software object.
- Ask when actor vs. software object is unclear.

## Association Rules

- Prefer explicit `Object Layout` over inferred topology.
- If `Object Layout` is missing, derive the minimal undirected graph needed by the message pathways.
- Accept a derived graph only when each pathway is unambiguous and the resulting layout still supports a clear central object and peripheral external actors.
- Ask when two or more graphs would be reasonable.
- Ask when the user names participants that never connect to anything.

## Message Rules

- Require unique message numbers.
- Preserve numbering exactly. Do not renumber unless the user asks.
- Allow numbering gaps if order is still explicit and unique.
- Require every message to have a source, a target, and visible text.
- Require every message endpoint to match a validated participant name exactly.
- In the default grouped style, combine messages into directional groups keyed by exact `from -> to` participant pairs.
- Inside each directional group, preserve every message number and text exactly.
- Keep separate groups for opposite directions such as `A -> B` and `B -> A`.

## Blocking Conditions

Stop and ask focused clarification questions when any of these appear:

- duplicate participant names
- missing participant classification
- missing software-object stereotype
- missing message number, source, target, or text
- duplicate message numbers
- message endpoint not present in the participant list
- explicit layout mentions an unknown participant
- explicit layout contradicts the messages so strongly that no clean pathway exists
- multiple plausible association topologies
- an edit request lacks a clear source of truth for what changed
- the request is not actually for a UML communication diagram

## Output Convention

- Save next to the source file with the same basename and a `.drawio` extension when the source file path is known.
- Save to `output/<slug>.drawio` when the user only provides pasted text.
- Use the normalized title or basename as the draw.io page name.
- Store the diagram as XML text with a `.drawio` extension.

## Clarification Style

- Ask the smallest set of questions that resolves the blockage.
- Prioritize missing participant classification, missing stereotype, ambiguous pathway, and inconsistent names.
- Do not ask for cosmetic preferences unless layout or output path cannot be inferred.
