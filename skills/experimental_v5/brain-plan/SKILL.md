---
name: brain-plan
description: Manage complex, multi-session planning efforts using durable, dependency-aware tickets under `.brain/planning/`. Use when an effort involves interdependent decisions, research, prototypes, or prerequisites that require multiple sessions. Not for single-session planning or implementation.
---

# Plan Feature

Use for substantial uncertainty requiring **multi-session decision/investigation coordination**, not for ordinary one-session brainstorming or implementation. This owns `.brain/planning/<effort>/INDEX.md` and numbered decision tickets; feature designs/tasks remain with their producing skills.

## Workflow

1. Read current decisions, active project architecture and source facts. Establish the objective, prerequisites and consequential unknowns. If all can be resolved in one session, do not create planning documents.
2. Survey the full decision space breadth-first, including dependencies, evidence to investigate and possible bounded prototypes. Define only real tickets: `decision`, `research`, `prototype`, or prerequisite `task`—never implementation of the objective.
3. Scaffold a concise index and numbered tickets via `brain-tool doc new --kind planning-index|planning-ticket` when justified. Each ticket has one actionable question, dependencies, evidence, status and final rationale. Never treat assumptions as approved decisions.
4. Resolve **unblocked** tickets in prerequisite order. Research facts independently; consult user for consequential choices. Default to one non-research ticket per session unless the user requests more. Persist evidence and update the index; stop on blocked decisions.
5. Preserve the existing planning record on resumption, reconcile source changes, and send settled feature intent to `brain-brainstorm`/`brain-write-spec`. Design belongs to `brain-design-implementation`, implementation tasks to `brain-write-tasks`. Invoke `brain-update` after Brain changes.

**Read on demand:** `${CLAUDE_SKILL_DIR}/references/plan-details.md` for ticket schema, status transitions, explicit dependency grammar, planning-index format, scope exclusions and continuation/replan rules; `../brain-init/references/deterministic-tooling.md` for CLI safeguards.

**Plan, do not implement.** Planning or a prototype does not authorize product code changes or consequential architecture decisions.


**Writing:** Follow `${CLAUDE_SKILL_DIR}/../brain-init/references/compact-writing.md` when recording Brain facts: concise, evidence-complete entries without duplicated narrative. Do not reformat unrelated existing files solely for style.

**Recommended next step:** End the final user-facing reply with one concise, evidence-based next action, naming the appropriate skill or command when useful. If blocked, identify the missing information, prerequisite, or approval instead of advancing; if complete, say no further action is needed. A recommendation is not authorization to execute another step. Keep it outside copy-ready deliverables.
