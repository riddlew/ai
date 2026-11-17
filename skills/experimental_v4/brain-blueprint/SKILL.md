---
name: brain-blueprint
description: Collaboratively design and approve concrete code-level implementation plans for approved feature components before implementation.
---

# Blueprint — Implementation Plans

Turn approved behavior into a **user-approved, code-specific binding design**, when the task is substantial or design-sensitive. A small settled change need not have a blueprint.

## Workflow

1. Read approved specs, components when used, binding user decisions, relevant code owners/callers/tests and ADRs. Inspect actual implementation and record the inspected Git SHA.
2. Present the smallest viable design: ownership, data/control flow, significant signatures/patterns, failure handling, important negative constraints and verification approach. Clearly distinguish **binding** decisions from illustrative pseudocode/private helpers.
3. Consult before consequential new ownership, API/protocol/persistence/security changes or departures from approved decisions. Invite the user to review binding structure before code is edited.
4. Save approved design under `.brain/features/<feature-slug>/04-implementation-plans/` using `brain-tool doc new --kind plan` for new drafts, stable IDs, real governing parents and fingerprints. Mark approved only after explicit user approval.
5. Report design approval, decisions, open issues and handoff to tasks or `brain-implement`.

Use `${CLAUDE_SKILL_DIR}/../brain-init/references/feature-document-contract.md`. **Read on demand:** `${CLAUDE_SKILL_DIR}/references/blueprint-details.md` and `${CLAUDE_SKILL_DIR}/references/blueprint-template.md` for collaborative design iterations and full document shape; CLI details live in `../brain-init/references/deterministic-tooling.md`.

**Recommended next step:** End the final user-facing reply with one concise, evidence-based next action, naming the appropriate skill or command when useful. If blocked, identify the missing information, prerequisite, or approval instead of advancing; if complete, say no further action is needed. A recommendation is not authorization to execute another step. Keep it outside copy-ready deliverables.
