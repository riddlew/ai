---
name: brain-write-spec
description: Synthesize established decisions and repository evidence into a feature specification with concrete examples, without inventing or reopening requirements.
---

# Write Spec

Specify **what observable behavior and invariants must hold**, grounded in the user-confirmed direction and authoritative sources. Do not invent requirements or approve your own draft.

## Workflow

1. Inspect approved decisions, relevant source, existing code/tests, and active feature documents. Resolve consequential behavior questions with the user before treating them as settled.
2. Declare uniquely numbered requirements (`REQ-001`, etc.) and concrete examples (`E1`, etc.): normal, edge, failure, compatibility and unchanged behavior. Make observable expected results and exclusions testable, independent of the implementation.
3. Specify verification at stable boundaries, including required tests/evidence, known limitations and links to authoritative technical contracts. Preserve confirmed user-directed code constraints as binding requirements where applicable.
4. Write or revise a document in `.brain/features/<feature-slug>/02-specifications/` via `brain-tool doc new --kind specification` for new drafts only. Use `${CLAUDE_SKILL_DIR}/../brain-init/references/feature-document-contract.md`, its templates, and the deterministic validator for metadata, parent IDs, traceability and coverage. Existing IDs survive revisions.
5. Ask for explicit approval when required; record only observed approval. Report open decisions, exclusions, coverage and the next applicable stage; invoke `brain-update` after recording a change.

**Revising an approved spec.** On material behavior changes, set `status: needs-revision` in the same edit; never renumber stable IDs and a request to revise is not approval of the written revision. The producing skills `brain-decompose`, `brain-blueprint`, `brain-write-tasks` must review affected descendants; do not change their status or `parent_hashes` yourself. **Unaffected:** leave independent descendants and approvals intact. Editorial changes without material meaning need no blanket invalidation.

**Read on demand:** `${CLAUDE_SKILL_DIR}/references/spec-details.md` for full example template, technical decisions, verification strategy and nuanced revision handling. For safe CLI invocation see `${CLAUDE_SKILL_DIR}/../brain-init/references/deterministic-tooling.md`.
