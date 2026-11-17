---
name: brain-write-tasks
description: Decompose approved technical implementation plans into small, verifiable executable tasks with grounded dependencies, requirement coverage, and user-approved task boundaries.
---

# Write Tasks

Translate approved requirements and binding implementation plans into the **smallest independently verifiable behavioral increments**. Do not invent a new architecture or require tasks for trivial direct changes.

## Workflow

1. Read approved specs/examples, applicable components/plans, explicit exclusions and dependencies. Stop affected tasks if a governing design is `draft` or `needs-revision`.
2. Divide work by observable behavior and real prerequisites, not arbitrary code layers or one-line edits. Each task cites relevant `SPEC-...#REQ-...` requirements, examples and approved plan parents.
3. Write clear actions, acceptance evidence, expected tests and negative constraints. Use `brain-tool doc new --kind task` for new drafts in `.brain/features/<feature-slug>/05-tasks/`; preserve stable task IDs on revision.
4. Validate dependency ordering, cycles, parent fingerprints and requirement coverage; check semantic completeness too. Get explicit approval where required and leave unresolved design choices blocked.
5. Report the executable task order, skipped levels and handoff to `brain-implement`. Invoke `brain-update` when records change.

Use `${CLAUDE_SKILL_DIR}/../brain-init/references/feature-document-contract.md`. **Read on demand:** `${CLAUDE_SKILL_DIR}/references/task-details.md` for nuanced decomposition/approval and full task examples, or `../brain-init/references/deterministic-tooling.md` for CLI.
