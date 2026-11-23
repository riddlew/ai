# Next-step routing and documentation reconciliation

`brain-next` recommends from **verified project state**; its default invocation is read-only. `CLAUDE.local.md` and the feature-document contract prevail over examples. No additional global progress file is needed.

## Sources and ownership

| Evidence | Use | Limitation |
|---|---|---|
| `.brain/state.md` and `00_index.md` | Discover features, links, high-level project status | Owned by `brain-update`; potentially stale; never a global active-increment pointer |
| `01-brief/`, `02-specifications/` | Scope, approved requirements and acceptance examples | Check explicit approval and governing decisions |
| `03-components/`, `04-implementation-plans/`, `05-tasks/` | Optional coverage, binding design, executable tasks and `depends_on` | Check statuses, requirement IDs, `parents` and `parent_hashes`; optional stages are not gates |
| `features/<feature>/execution.md` | Per-feature increments, review base, verification, approvals, blockers and current focus | `brain-implement` owns it; must verify against actual Git/code/tests |
| Git, code, diffs, tests | What is present and verified in the current branch/worktree | Facts about implementation, not authority to rewrite requirements |
| `pending/<branch>.md` / `planning/` | Current branch facts and longer-running investigation | Do not promote other branches' pending work into this feature |

**Feature selection:** explicit feature or existing task/increment wins. Resolve an increment identifier (e.g. `INC-4`) to actual work and its parent feature; do not create or infer missing IDs. Otherwise consult current conversation/branch/`state.md`. If two features are plausible, ask which rather than assume a global working state. Never traverse `.brain/.notes/` without explicit request.

## Default workflow and optional depth

Prefer `brain-brainstorm` (only for unresolved decisions) → `brain-write-spec` → `brain-design-implementation` → `brain-implement`. Tiny settled fixes can be implemented directly. Specifications can record simple responsibility boundaries; implementation plans can contain an ordered, verifiable increment checklist without separate components or task files.

Optional examples:
- `Next: /brain-design-implementation messaging`; `Optional: /brain-decompose-feature messaging — separate client/server owners need explicit independent requirement coverage and approval`. If chosen, decompose **before** design.
- `Next: /brain-implement messaging`; `Optional: /brain-write-tasks messaging — dependent increments will be delegated to multiple agents across sessions`. If chosen, write tasks **before** implementation.

Neither optional skill is a routine gate. But an **existing** component or task with a stale approved parent or changed responsibility is a **required** owning-skill reconciliation, not optional. Distinguish existing affected artifacts from unneeded new documents.

## Recommend one next step

1. **Unresolved consequential behavior/design decision:** `brain-brainstorm` or a focused user question. A prior-session decision must be recorded or provided, not reconstructed.
2. **Changed/missing requirements or stale spec:** `brain-write-spec`. When a changed spec affects an existing component, the owning `brain-decompose-feature` skill revalidates it before dependent plans.
3. **Changed/missing component coverage:** require `brain-decompose-feature` for **existing affected components**; otherwise suggest it only as optional when separate ownership/traceability has real value.
4. **Binding design not approved/current:** `brain-design-implementation`. Even if design text stays the same, direct-parent hash changes need documented review and renewed approval where required.
5. **Tasks used and affected/unapproved:** require `brain-write-tasks` when existing governing tasks need reconciliation; for new complex dependencies or delegation recommend it only as optional. Small settled work can use plan-level increments.
6. **Current increment in progress, tests failing or review pending:** recommend resuming/reviewing **that increment**, or `brain-diagnose` for an unresolved failure. Do not advance past a pending collaborative approval.
7. **Ready work:** after verifying approved and current governing documents, actual Git/test state and `depends_on`, recommend `/brain-implement <real-unblocked-id>`. If `INC-4.5` is recorded, unblocked and prioritized, it can come before `INC-5`. Never invent either ID or order solely by numbers. If several independent increments are ready and no priority is established, disclose the tie and ask.
8. **After verified completion:** recommend risk-proportionate `brain-review-code`, `brain-update` for stale shared knowledge, or no further action. If repeated failed fixes, redundant investigation or confusing instructions are evidenced, optionally suggest `/brain-retro <feature>` with a concrete reason, **never invoke it**. Ordinary review findings alone are insufficient.

**Conflict handling:** an outdated `execution.md`, stale `state.md`, mismatched direct parent hash, unrecorded approval or surprising uncommitted code is a verification blocker, not a reason to guess completion. Check source and authoritative documents and choose the earliest genuinely actionable stage.

## INC-4 → INC-4.5 → INC-5 example (illustrative identifiers)

| Actual evidence | Next recommendation |
|---|---|
| A confirmed change after INC-4 modifies behavior; spec needs revision | `/brain-write-spec <feature>` |
| Revised spec approved but component coverage is affected | `/brain-decompose-feature <feature>` |
| Components current, binding implementation plan stale | `/brain-design-implementation <feature>` |
| Plan approved but task definitions/dependencies have changed | `/brain-write-tasks <feature>` |
| An **existing recorded** INC-4.5 is unblocked, governing documents approved/current, user has not yet requested implementation | `/brain-implement INC-4.5` (recommendation only) |
| INC-4.5 has verified code but still awaits review | Recommend review/approval of INC-4.5, **not** INC-5 |
| INC-4.5 approved, INC-5 recorded and is next unblocked item | `/brain-implement INC-5` |
| INC-4.5 is **not actually defined** | Don't invent it; refer to real tasks or recommend the relevant plan/task-owning skill |

## Optional document reconciliation mode

Only a request explicitly asking to **update/reconcile** documents enables this mode. Default `/brain-next` stays read-only.

| Change | First owning skill | Revalidate descendants only where affected |
|---|---|---|
| Observable requirements, error semantics, compatibility, acceptance examples | `brain-write-spec` | `brain-decompose-feature` → `brain-design-implementation` → `brain-write-tasks` |
| Functional component boundaries and coverage, unchanged behavior | `brain-decompose-feature` | `brain-design-implementation` → `brain-write-tasks` |
| Binding architecture/API/threading/lifecycle, unchanged behavior | `brain-design-implementation` | `brain-write-tasks` |
| Task dependencies or acceptance evidence under unchanged design | `brain-write-tasks` | No obligatory earlier stage |
| Local illustrative helper or execution progress | No producer-document revision | Separately authorized `brain-implement` |
| Shared root knowledge, ADR or index | `brain-update` | Route any affected normative feature documents to their owner first |

A confirmed conversation or `brain-brainstorm` result is input, not approval of the later written revision. Owners preserve stable IDs and handle material `needs-revision` status, explicit document approval, `parents`/`parent_hashes` and requirement coverage. A plan's unchanged body does not justify auto-refreshing its parent hashes. Preserve `execution.md` and verified increments. Don't use `brain-update` to rewrite owner documents.

Where the Skill tool is not available, provide the exact copyable next command with feature/IDs/decision, **stop** and report the incomplete stage; never emulate invocation by writing files directly or shelling out to `claude`.

Example: `/brain-next yaml-cli --reconcile unknown keys should warn rather than error`. Resolve any undecided semantics first, then update only affected docs via their owners and recommend the next **separately authorized** action.
