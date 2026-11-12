---
name: brain-blueprint
description: Collaboratively design and approve the concrete code changes for an established feature before implementation. Use when architecture, interfaces, ownership, call flow, or implementation structure should be reviewed with the user first.
disable-model-invocation: true
---

# Blueprint

**Project brain:** Follow `CLAUDE.local.md` §Project brain loading: read **all** root `.md` files once per session (again after compaction), plus the active branch's pending file when present. Inspect linked detail and verify task-critical facts against current source. Do not send the whole brain to subagents. If no brain exists, proceed and mention `/brain-init` once.

Collaboratively design **how** to implement approved behavior, without implementing it. A blueprint is recommended for substantial features and when the user cares about exact code structure, but unnecessary for a small, well-defined fix. This skill writes **only** the `## Implementation Design` section and its blueprint metadata in the feature's existing `.brain/impl_plans/<feature>.md`; it must not create a competing document. Follow `CLAUDE.local.md` for decision authority.

## 1. Establish the boundary

1. Read the approved spec, tickets if any, the confirmed brainstorm direction, applicable ADRs, and any existing impl plan. Determine which requirements and technical choices are **binding**, which are merely proposed, and which consequential questions remain unresolved.
2. Inspect the actual code: owners, callers, interfaces, persistence, lifecycle, tests, and nearby conventions. Check `git status`, current branch, relevant staged/unstaged edits and untracked code. Treat the brain as orientation, not proof that the code is unchanged.
3. Capture the full `HEAD` SHA as `Design inspected at:` and note material uncommitted or branch-specific assumptions in the design. Never use this SHA as the implementation's `Review base`; `brain-implement` records that immediately before editing code.
4. Ask what code structure the user wants **only where preferences have not already been expressed**. Invite, but do not require, proposed patterns, class boundaries, key signatures, method outlines, pseudocode, and an explicit "keep unchanged" list. Investigate factual questions yourself.
5. If a requested design conflicts with an established requirement or creates a demonstrable correctness problem, explain the evidence and smallest viable adjustment. Do not quietly redesign it. New consequential choices require approval and recording in the governing spec, ADR, or `09_user_decisions.md` through the appropriate workflow **before** they are labeled binding here.

## 2. Propose the smallest viable design

Prepare a blueprint using `${CLAUDE_SKILL_DIR}/references/blueprint-template.md`:

- Identify concrete existing files/components, their current responsibilities and intended changes; explicitly say what **will not change**.
- Describe ownership, key call/data flow, relevant failure paths, compatibility, and any migrations. Prefer extending existing owners rather than introducing speculative abstractions.
- Show important interfaces or method signatures **when they expose a design choice**; use pseudocode or detailed comments when the user requests them or ambiguity warrants it. Do not mechanically specify every private helper.
- Distinguish **Binding** (approved constraint), **Proposed** (awaiting approval), and **Illustrative** (Claude may refine without changing the constraint). Name the source of binding decisions. Approval of the blueprint makes its explicitly identified, non-conflicting design constraints binding for this implementation; illustrative snippets remain illustrative.
- Plan **small end-to-end, independently testable behavioral increments**, not a batch for each architectural layer. Tie each increment to governing Example IDs, ticket criteria, or numbered requirements, and name verification that could demonstrate it works.
- Flag unresolved consequential choices as blockers; do not fill gaps with assumptions or claim a blocker is approved.

## 3. Review the design with the user

1. Present the affected files, ownership and data flow, key signatures, binding vs illustrative choices, unchanged boundaries, increment order, and genuine tradeoffs. Invite edits to class/method outlines and design patterns. **Do not modify production code, tests, or configuration.**
2. Iterate the design with the user. A proposed signature is not automatically binding merely because it appears in a code block; clarify which details the user actually wants fixed.
3. Check the final draft against current code, governing requirements, and the selected design. Run the builder review in `${CLAUDE_SKILL_DIR}/../brain-review-code/references/builder-review.md`, with `blueprint` as `{artifact_kind}` and the governing spec/tickets and source paths as `{sources}`. Resolve factual questions yourself; ask only consequential questions the user must decide. If unavailable, perform the reported weaker self-read.
4. Ask explicitly for approval of the **revised blueprint**. If approval is absent or partial, save it as `draft` or `needs revision` and report precisely what blocks implementation. A feature request or approval of the spec does **not** count as blueprint approval.
5. After explicit approval, set `Blueprint status: approved`, record when/where approval occurred, and state which design constraints are binding. Do not begin implementation; hand off to `/brain-implement` only when separately authorized.

## 4. Persist and hand off

Use **one plan per feature**: with a spec, `.brain/impl_plans/<spec-file-stem>.md`; with tickets only, use their feature slug; otherwise use a stable request slug. Reuse an existing plan and preserve **all** execution history, verification, reviews, and user edits. Create only a minimal shell if none exists. Edit only blueprint metadata and `## Implementation Design`; never reset execution tasks or their status. Keep the blueprint in the same located brain that other skills use.

Record `Design inspected at: <full SHA>` and relevant dirty-worktree assumptions. Statuses: `draft`, `approved`, `needs revision`. If an approved blueprint is revised, mark it `needs revision` until the user approves changed **binding** design. Routine, explicitly illustrative refinements need no new approval; have `brain-implement` record meaningful deviations in its separate `## Design Deviations` execution section instead.

Invoke `brain-update` after creating or materially revising a blueprint, **including a draft**, with a one-line summary so `00_index.md` reflects its current status. Report the path, status, approval or open decisions, affected files, and the next authorized step. Approval to design does not authorize editing code.
