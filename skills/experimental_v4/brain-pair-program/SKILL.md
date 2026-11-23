---
name: brain-pair-program
description: Pair-program approved features in adaptive, dependency-aware increments. Choose AI-led (recommended) or developer-led; explain each increment and wait for user review before continuing.
---

# Pair Program

Use as an **alternative** to `brain-implement` when the user wants to shape the code while building it. Both modes share explanations and mandatory increment checkpoints. **AI-led** (recommended): Claude writes code. **Developer-led**: user writes code, Claude designs, teaches and reviews.

## 1. Establish modes, authority and scope

1. **At the beginning**, ask: "Pair mode: **AI-led (recommended)** or **developer-led**?" **Wait** if unspecified; never silently choose AI-led. A confirmed selection for the same continuing work carries forward, but a stale record alone does not grant permission. Change mode only by explicit user choice. **Developer-led forbids Claude editing production code, tests or migrations.**
2. **Independently**, follow `CLAUDE.local.md` §Execution mode selection. Ask for `inline` (recommended) or `subagents` if not confirmed, and wait. Pair mode controls **who edits code**; execution mode controls delegation. Subagents must not circumvent developer-led authorship or user checkpoints.
3. Read the task's approved specs/examples, components, binding plans, tasks, decisions, `execution.md`, relevant code/tests and current Git changes. Verify the plan's assumptions and original review base. Follow the Brain's approved-document ownership, worktree boundaries and authorization rules. For substantial/design-sensitive work, obtain approval of the binding `brain-design-implementation` first. A request to explain or plan is **not** authorization for AI-led code edits.

## 2. Pair in coherent, verifiable increments

1. Outline actual files/classes, responsibilities, dependencies, and call flow. Explain important proposed design choices **before** starting. Invite correction; don't present a full implementation dump.
2. Sequence work by **real dependencies**: establish existing types and contracts before consumers. E.g. model/exceptions → repository contract → service → controller, adjusted to the codebase. **Never present a completed increment referencing missing classes, methods or migrations.** Include necessary prerequisites in the same increment when required for compilation. Avoid a rigid architecture sequence.
3. Choose an **adaptive, logically cohesive** slice: sometimes one method, sometimes a small class or several related methods. Explain what it does, why the approach fits, and meaningful tradeoffs; **not every line** unless requested. Avoid speculative abstractions.
4. **AI-led:** Edit only the current authorized slice, inspect its **actual diff**, perform proportionate focused verification (test-first red/green when feasible), show changes and observed outcomes. **Stop** for review.
5. **Developer-led:** Show focused copyable code and file locations but **do not edit code/tests**. Wait for the user's implementation; then inspect **their real files and diff**, including deviations, and run or inspect authorized checks. Never assume they copied the example. Discuss findings and **stop** for review.
6. Test throughout, not only at the end. Intentional red tests may exist during work, but **do not approve an incomplete/non-buildable increment as done**. Resolve missing dependencies or report a precise blocker. Never invent test results.

## 3. Mandatory review and revisions

- After **every** slice, show the current work, relevant explanation, verification evidence and ask the user to **approve, revise or challenge** it. **Wait in both modes.** "Continue" authorizes only the previously reviewed increment; don't silently advance past an unapproved checkpoint.
- Welcome feedback. For small reversible illustrative adjustments, update the current proposal. If feedback changes **approved requirements or binding design** (e.g. behavior, APIs, persistence, concurrency, ownership), **stop affected work** and route to `brain-write-spec` / `brain-design-implementation` and affected owners for approval. Preserve unaffected work.
- Track both modes in **the existing** `.brain/features/<feature>/execution.md`: original review base, approved plans/tasks, true code author/pair mode, inline/subagent mode, verification, rulings and checkpoints. This skill **shares execution-record ownership with `brain-implement`**; do not create a parallel progress file or overwrite prior approvals/history. A verified change is **awaiting user review** until approved. Follow `brain-implement`'s execution template and authorized-write rules.
- When resuming or switching workflows, reconcile existing `execution.md` with actual Git/code and user approvals; don't reset review base, skip pending reviews or silently switch who edits. Stage/commit only by explicit user instruction.
- Finish with proportionate final verification/review, `brain-update` when shared knowledge changed, and a concise evidence-based status.

**Read on demand:** `${CLAUDE_SKILL_DIR}/references/pair-program-details.md` for Spring Boot example, mode switches and checkpoint patterns; `${CLAUDE_SKILL_DIR}/../brain-implement/references/todo-template.md` and `implement-details.md` for shared history; `${CLAUDE_SKILL_DIR}/../brain-init/references/feature-document-contract.md` for approvals and ownership.

**Recommended next step:** End the final user-facing reply with one concise, evidence-based next action, naming the appropriate skill or command when useful. If blocked, identify the missing information, prerequisite, or approval instead of advancing; if complete, say no further action is needed. A recommendation is not authorization to execute another step. Keep it outside copy-ready deliverables.
