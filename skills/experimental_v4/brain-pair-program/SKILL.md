---
name: brain-pair-program
description: Pair-program planned or informal coding in adaptive increments. Choose AI-led (recommended), developer-led, or Learning Mode; explain and review each increment.
---

# Pair Program

Use as an **alternative** to `brain-implement` when the user wants to shape the code while building it. All three modes share mandatory increment checkpoints. **AI-led** (recommended): Claude writes code. **Developer-led**: user writes code, Claude designs, teaches and reviews. **Learning Mode**: user designs and codes first, with Claude mentoring and reviewing.

## 1. Establish modes, authority and scope

1. **At the beginning**, ask: "Pair mode: **AI-led (recommended)**, **developer-led**, or **Learning Mode**?" **Wait** if unspecified; don't infer choice from a stale record. Switch only with user consent. **Developer-led and Learning Mode forbid Claude editing production code, tests or migrations.**
2. **Independently**, follow `CLAUDE.local.md` §Execution mode selection: ask `inline` (recommended) or `subagents` when unconfirmed, then wait. Pair mode controls authorship and guidance; execution mode controls delegation. Subagents cannot bypass user authorship/checkpoints.
3. Inspect actual code/tests, Git and existing Brain decisions; read specs, plans, tasks and `execution.md` **when present**. A **spec or implementation plan is not required** for informal coding, review or small settled changes; use the user's goal and edits. **Do not invent plans or task IDs.** Respect approved requirements, original review base and worktree authority. Substantial/design-sensitive implementation still needs approved `brain-design-implementation` first. Discussion or review **does not authorize AI-led code edits**.

## 2. Pair in coherent, verifiable increments

1. For implementation, outline actual files, dependencies, call flow and key design choices; invite correction before code, without a full dump. For review-only questions, start with the user's code, not a mandatory plan.
2. Sequence by **real dependencies**: establish contracts before consumers (e.g. model/exceptions → repository → service → controller), adapting to the codebase. **Never present a completed increment referencing missing classes, methods or migrations.** Include compilation prerequisites in the same slice; no rigid layer order.
3. Choose an **adaptive, logically cohesive** slice (method, class or related methods). Explain purpose, reasoning and meaningful tradeoffs, **not every line** unless asked. Avoid speculative abstractions.
4. **AI-led:** Edit only the current authorized slice, inspect its **actual diff**, perform proportionate focused verification (test-first red/green when feasible), show changes and observed outcomes. **Stop** for review.
5. **Developer-led:** Show focused copyable code and file locations but **do not edit code/tests**. Wait for the user's implementation; then inspect **their real files and diff**, including deviations, and run or inspect authorized checks. Never assume they copied the example. Discuss findings and **stop** for review.
6. **Learning Mode:** Present the next approved or user-chosen increment's objective **without revealing code**. Invite the user's design first; discuss tradeoffs, offer adaptive hints/debugging or code and direct answers **on request**. Review real edits; occasionally check understanding without quizzes. **Read `${CLAUDE_SKILL_DIR}/references/learning-mode.md` whenever selected.**
7. Test throughout, not only at the end. Intentional red tests may exist during work, but **do not approve an incomplete/non-buildable increment as done**. Resolve missing dependencies or report a precise blocker. Never invent test results.

## 3. Mandatory review and revisions

- After **every** implemented slice, show the work, explanation and verification, then explicitly request **user approval** or revisions; ask the user to **approve, revise or challenge** it. **Wait in all three modes.** "Continue" authorizes only the previously reviewed increment; don't silently advance past an unapproved checkpoint.
- Welcome feedback and small reversible corrections. Changes to **approved requirements or binding design** (behavior, API, persistence, concurrency, ownership) require stopping affected work for `brain-write-spec` / `brain-design-implementation` owner approval; preserve unaffected work.
- For tracked feature work, use **the existing** `.brain/features/<feature>/execution.md` for review base, plans/tasks if any, mode, verification and approvals. This skill **shares execution-record ownership with `brain-implement`**. For informal work with no feature record, **no `execution.md` is required**: keep context in conversation; don't invent a progress file. Preserve history and follow template/write rules if recording work. Verified changes remain **awaiting user review** until approved.
- **Review-only:** Inspect and critique current code without writing files or inventing work items. On resume, reconcile any `execution.md` with Git/code and approvals; don't reset review base, skip pending reviews or switch authorship silently. Stage/commit only by explicit user instruction.
- Finish with proportionate final verification/review, `brain-update` when shared knowledge changed, and a concise evidence-based status.

**Read on demand:** `${CLAUDE_SKILL_DIR}/references/pair-program-details.md` for Spring Boot example, mode switches and checkpoint patterns; `${CLAUDE_SKILL_DIR}/../brain-implement/references/todo-template.md` and `implement-details.md` for shared history; `${CLAUDE_SKILL_DIR}/../brain-init/references/feature-document-contract.md` for approvals and ownership.

**Recommended next step:** End the final user-facing reply with one concise, evidence-based next action, naming the appropriate skill or command when useful. If blocked, identify the missing information, prerequisite, or approval instead of advancing; if complete, say no further action is needed. A recommendation is not authorization to execute another step. Keep it outside copy-ready deliverables.
