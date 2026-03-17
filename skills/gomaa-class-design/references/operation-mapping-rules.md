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

## Public operation rules

- Prefer one public operation per distinct incoming service request.
- Merge duplicate operations across use cases when they express the same responsibility.
- Keep operation names verb-led and design-level, such as `submitRentalRequest`, `markAccepted`, or `publishListing`.
- Do not expose internal helper behavior as public unless another class actually invokes it.

## Message interpretation rules

- Treat actor-to-boundary messages as boundary operations.
- Treat coordinator-to-entity or logic-to-entity messages as entity operations only when the entity must provide that service directly.
- Treat coordinator-to-business-logic messages as logic operations when the logic object owns the rule.
- Treat outgoing calls from the target class as collaboration evidence, not automatic new public operations.

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

## Anti-patterns

- Do not copy analysis message labels unchanged when they are noun phrases and not service names.
- Do not invent CRUD operations that no interaction requires.
- Do not expose private fields through public getters unless the design scope really needs them.
- Do not embed database, framework, or transport details in operations.
