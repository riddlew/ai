---
name: brain-brainstorm
description: Resolve consequential product and architecture decisions with the user through dependency-ordered questions and evidence-based recommendations, investigating discoverable facts independently. Use when a requested feature or change has unclear behavior, scope, or design direction that should be settled before writing a specification or code.
---

# Brainstorm

Settle genuinely consequential behavior and design decisions **before** writing a spec or implementing. Investigate discoverable facts; do not ask the user for them or reinterpret prior approvals.

## Workflow

1. Read applicable project decisions, architecture, source and tests under `CLAUDE.local.md`. Note the objective, confirmed scope, binding design preferences and affected behavior.
2. Maintain a small decision table: `Established`, `Investigate`, `User decision`, `Deferred`. Resolve factual questions yourself. For user decisions, compare the smallest viable approach against materially different alternatives, including preservation of existing ownership.
3. Ask the smallest set of prerequisite-resolved questions (usually 1–3); state evidence, tradeoffs and a recommendation. Wait for answers. Do not invent extra requirements, decisions or speculative architecture.
4. Verify observable success/failure/boundary behavior and the user's intentional design choices. Mark unresolved consequential decisions explicitly; don't silently settle them as implementation details.
5. Show the final behavior/scope, intended changes, preserved behavior, assumptions, decisions and relevant source facts. Confirm the direction with the user. Only then optionally scaffold a nontrivial approved `.brain/features/<feature-slug>/01-brief/brief.md` via `brain-tool doc new --kind brief`; keep stable IDs and record approval evidence. Invoke `brain-update` when Brain content changes.

See `${CLAUDE_SKILL_DIR}/../brain-init/references/feature-document-contract.md` for document rules and `${CLAUDE_SKILL_DIR}/../brain-init/references/deterministic-tooling.md` for safe CLI invocation.

**Read on demand:** `${CLAUDE_SKILL_DIR}/references/brainstorm-details.md` for dependency-order tables, complete output shape, architecture/data/API/failure decision lenses, complex behavioral coverage or the optional visual companion. Brainstorming never authorizes production code changes.
