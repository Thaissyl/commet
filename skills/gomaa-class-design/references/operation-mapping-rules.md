# Operation Mapping Rules

Use this reference when translating analysis artifacts into design operations and contracts.

## Core mapping

| Analysis artifact | Design outcome |
| --- | --- |
| Incoming message to target class | Candidate public operation |
| Forward-carried data in the message | `in` parameters |
| Reply data from target class | `out` parameters |
| Static-model attributes | Private fields |
| Use-case preconditions | Operation preconditions |
| Use-case postconditions | Operation postconditions |
| State transitions and guards | Preconditions, postconditions, invariants |

## Step-3.0 propagation rules

When `step-3.0-design-communication-diagram.md` is available, use it as the design-level propagation source for later artifacts:

- participant in `step-3.0` -> candidate class in `step-3.1` and `step-3.2`
- incoming message to participant in `step-3.0` -> candidate provided operation in `step-3.1`
- outgoing call from one design participant to another in `step-3.0` -> candidate required operation in `step-3.1`
- call path between two non-actor design participants in `step-3.0` -> candidate association in `step-3.2`
- participant stereotype in `step-3.0` -> default stereotype in `step-3.1` and `step-3.2`

Do not silently drop a non-actor participant from `step-3.1` or `step-3.2` when it is still architecturally relevant in `step-3.0`.

## Public operation rules

- Prefer one public operation per distinct incoming service request.
- Merge duplicate operations across use cases when they express the same responsibility.
- Keep operation names verb-led and design-level, such as `submitRentalRequest`, `markAccepted`, or `publishListing`.
- Do not expose internal helper behavior as public unless another class actually invokes it.

## Message interpretation rules

- Treat actor-to-boundary messages as boundary operations.
- Treat actor-to-user-interaction messages as user-interaction operations when the design explicitly includes a UI participant in `step-3.0`.
- Treat coordinator-to-entity or logic-to-entity messages as entity operations only when the entity must provide that service directly.
- Treat coordinator-to-business-logic messages as logic operations when the logic object owns the rule.
- When the user explicitly selects a simple stack-specific backend, allow a controller or boundary object to coordinate repository, service, and proxy collaborators directly instead of forcing a separate facade or business-logic class.
- Treat outgoing calls from the target class as collaboration evidence, not automatic new public operations.

## Entity refinement rules

- In COMET-pure output, analysis `<<entity>>` classes normally refine into `<<data abstraction>>` classes.
- In stack-specific simplified output, an analysis `<<entity>>` may instead map to:
  - a repository or DAO style `<<database wrapper>>`, and
  - a conceptual record or DTO type such as `UserAccountRecord`
- Do not invent a separate `<<data abstraction>>` class when the user explicitly asks for a stack-matched simplified backend and the design can stay clear without it.

## Contract rules

- Preconditions come from:
  - use-case preconditions
  - message guards
  - statechart source states
  - availability or visibility conditions already defined in analysis
- Postconditions come from:
  - use-case success outcomes
  - recorded data changes
  - emitted notifications
  - state transitions
- Invariants are conditions that remain true across the class lifetime, not one-time outcomes.

## Parameter rules

- Keep parameter names domain-oriented.
- Keep parameter types conceptual unless the project already uses concrete types.
- Use `in` parameters for information carried toward the receiver.
- Use `out` parameters for information returned from the receiver.
- Prefer `out` parameters even when there is only one response value.
- Do not use `: ReturnType` unless the user explicitly asks for return-value style.
- For asynchronous or fire-and-forget operations, omit `out` parameters and use an operation name that makes the async intent explicit, such as `sendAsync(in emailMessage)`.

## Structural class rule

- If a class is included only for hierarchy or relationships and has no justified incoming messages in the chosen scope, do not invent operations.
- In that case, write `Operations Provided: none in current scope` in the class specification.

## Multi-output convention

- Represent every reply value as an `out` parameter in the operation signature.
- If one logical result exists, still model it as `out resultName` instead of a return type.
- For multiple reply values, list each one explicitly in the signature, for example `out userAccountDetail, out availableStatusActions`.
- Keep output names stable and domain-oriented, such as `out validationResult`, `out listingSummary`, or `out deliveryStatus`.

## Design communication diagram convention

- Prefer one directional function message per interaction step.
- Put both `in` and `out` parameters in the same message label, for example `changeUserAccountStatus(in accountReference, in statusAction, out statusChangeResult)`.
- Do not draw separate reply arrows for `out` values unless the user explicitly asks for call/return arrows.
- Show a `<<user interaction>>` object between a human actor and a backend controller or boundary object when the design is for a web or UI-driven system.
- For asynchronous operations, use a single one-way message without `out` parameters and without a paired reply arrow.
- When a human actor interacts through `AdminUI` or another `<<user interaction>>` participant in `step-3.0`, carry that same participant into `step-3.1` and `step-3.2` if the user wants cross-step consistency.

## Anti-patterns

- Do not copy analysis message labels unchanged when they are noun phrases and not service names.
- Do not invent CRUD operations that no interaction requires.
- Do not expose private fields through public getters unless the design scope really needs them.
- Do not embed database, framework, or transport details in operations.
