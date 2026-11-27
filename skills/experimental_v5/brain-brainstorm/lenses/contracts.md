# Lens: Contracts

Use when a decision affects an interface that other code or systems depend on: public APIs, protocols, events, CLI flags and output, configuration formats, library exports, or error responses.

## Decisions that typically arise

- Change type: additive (new optional field or endpoint) vs. breaking (removed or renamed fields, changed semantics, new required inputs, stricter validation).
- Handling a breaking change: new version, new field or endpoint alongside the old, feature flag, or coordinated release.
- Error contract: which failures callers can distinguish, their codes or types, which are retryable, and what detail is exposed.
- Defaults and absence: behavior when an optional input is omitted; whether null, missing, and empty differ.
- Compatibility window: how long the old form is supported and who must migrate.
- Contract ownership: who may change it and who must be told.

## Evidence to gather

- All known consumers: internal callers, other services, clients, scripts, and documentation examples, plus schemas (OpenAPI, protobuf, GraphQL).
- Existing versioning conventions and deprecation history.
- How errors are represented today and how consumers branch on them (status codes, error types, parsed messages).
- Serialization behavior: unknown-field handling, enum handling, number and date formats.
- Whether consumers deploy independently of this change.

## Questions that surface decisions

- Who calls this today, and can they all change in the same release?
- What should an old client see after this change?
- Which failures must a caller tell apart, and what should it do for each?
- Is this field or behavior part of the contract, or an incidental detail consumers happen to rely on?
- What happens when a new enum value or field reaches an old consumer?

## False dichotomies

- "Breaking change" vs. "no change": an additive change plus deprecation often meets the need.
- "Version the whole API" vs. "change in place": versioning one field or endpoint is often enough.
- "Expose all error detail" vs. "generic error": stable error codes with safe messages separate caller logic from diagnostics.
