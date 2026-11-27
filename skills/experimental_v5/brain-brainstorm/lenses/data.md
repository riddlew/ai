# Lens: Data

Use when a decision affects the shape of stored or transmitted data, migrations, consistency between copies, or repeated operations.

## Decisions that typically arise

- Representation: new field vs. new entity; embedded copy vs. reference; nullable vs. required with a default.
- Source of truth: which store or component is authoritative when copies exist (caches, read models, search indexes, client state).
- Migration: expand/contract vs. in-place change; backfill method; whether old and new code run against the same data concurrently.
- Consistency: what readers may observe during and after a write; transaction boundaries; acceptable staleness.
- Idempotency and uniqueness: what identifies a duplicate request or record, and where uniqueness is enforced.
- Retention and deletion: soft vs. hard delete, cascades, audit requirements.

## Evidence to gather

- Current schema, migration history, models, and serialization code; constraints and indexes actually defined in the store.
- Data volume, when it affects migration feasibility.
- Deployment model: whether old and new versions run side by side (rolling deploys, independently deployed clients).
- All readers and writers of the data, including jobs, reports, and other services.
- Where integrity is enforced today: store constraint, application check, or neither.

## Questions that surface decisions

- During a deploy, will old code read data written by new code, or the reverse? What must it do?
- If the same request arrives twice, what should happen?
- When two writers race, which result wins, or should one fail?
- When copies disagree, which is authoritative, and how stale may the others be?
- Can existing data violate the new rule? What happens to it?
- Must deleted data be recoverable or auditable?

## False dichotomies

- "Migrate everything now" vs. "never migrate": expand/contract with a backfill keeps both versions valid.
- "Strong consistency everywhere" vs. "eventual consistency": consistency can be chosen per read path.
- "Store constraint" vs. "application validation": often both; the constraint guarantees integrity and the validation gives a useful error.
- "New table" vs. "serialized blob": decide by whether the data is queried, constrained, or migrated independently.
