# Lens: Architecture

Use when a decision affects who owns a responsibility, state, or resource; component lifecycle; dependency direction; or how hard a choice is to reverse.

## Decisions that typically arise

- Which existing component owns new state or behavior, and whether ownership moves.
- Lifecycle coupling: whether something new lives and dies with an existing owner or independently.
- Dependency direction: which module may know about which; whether a change creates a cycle or makes a lower layer depend on a higher one.
- Sharing: whether a resource is per owner or shared across owners, and who arbitrates access.
- Placement: inside an existing module, at its edge as an adapter, or in a new module.
- Reversibility: what becomes expensive to change later (public types, persisted shapes, cross-team contracts).

## Evidence to gather

- The current owner of the relevant state or resource: where it is created, mutated, and released.
- Lifecycle: construction, shutdown order, and who holds references.
- Callers and imports around the affected modules; dependency rules in lint configuration, layering docs, `.brain/03_architecture.md`, or ADRs in `.brain/adrs/`.
- Change coupling: files that repeatedly change together (`git log --name-only` over relevant history).
- Tests: which boundary they exercise today and how much unrelated setup they need.

## Questions that surface decisions

- What must be true about the lifetime of X relative to Y?
- Who else needs this state or resource **now**, not hypothetically?
- If the alternative is needed later, is migrating a local refactor or a contract or persistence change?
- Does the proposed component own anything, or does it only forward calls?
- Which modules must change if this requirement changes?

## False dichotomies

- "Keep it in the existing class" vs. "extract a new service": a private helper or module-internal collaborator often satisfies the requirement without moving ownership.
- "Generic and reusable" vs. "hard-coded": a narrow interface for current callers can widen when a second real caller appears.
- "Restructure now" vs. "never touch it": a staged change (introduce, migrate callers, remove) is often available.
- Module or service count vs. domain boundaries: several packages do not imply several owners of meaning.
