---
name: brain-next
description: Recommend the next actionable Brain skill or work increment from actual feature approvals, dependencies, execution evidence and Git state. Read-only by default; optionally coordinate explicitly requested document reconciliation.
disable-model-invocation: true
argument-hint: "[feature-or-increment] [--reconcile <confirmed change>]"
---

# Next — Evidence-Based Workflow Navigator

Use `/brain-next` to determine what to do next after brainstorming, documentation, implementation or review. `$ARGUMENTS` may identify a feature, an existing task/increment, or an explicit `--reconcile` request. **Default mode is read-only: recommend a next action, do not perform it.** This skill owns no project artifacts and creates no global progress file.

## Default path and optional complexity

Prefer `brain-brainstorm` (if unresolved) → `brain-write-spec` → `brain-design-implementation` → `brain-implement`. A spec can contain simple functional boundaries; a binding plan can contain ordered verifiable increments. Trivial settled work may implement directly.

Recommend `brain-decompose-feature` **(optional)** if distinct functional owners need separate requirement coverage or approvals. Recommend `brain-write-tasks` **(optional)** if dependencies, delegation or multi-session handoffs justify separate work items. Give a concrete feature-specific reason for either, not a ritual checklist. **Existing affected/stale component or task documents are not optional**: their owners must reconcile them before dependent work proceeds.

## Workflow

1. **Resolve scope.** Follow `CLAUDE.local.md` for Brain discovery, authorized worktree/branch context, and the private `.brain/.notes/` boundary. Prefer an explicitly named feature or existing task/increment; otherwise examine project-wide `.brain/state.md`, current branch/pending records and the conversation to locate an active feature. `state.md` is a **discovery index**, not authoritative progress or a global "current step." If several features remain plausible, ask which one; never guess. If no Brain exists, follow the active no-brain policy and mention `/brain-init` if useful.
2. **Read state.** For that feature, inspect applicable `01-brief/`, `02-specifications/`, `03-components/`, `04-implementation-plans/`, `05-tasks/` and `execution.md`, plus governing ADRs/decisions and relevant `planning/` records. Check document approval (`draft`, `approved`, `needs-revision`), `parents`, `parent_hashes`, scope and requirement coverage; don't require optional levels. For planned work inspect task `depends_on` and verified execution status, review checkpoints, blockers and test evidence. Inspect current Git status, code and affected tests before recommending a particular implementation increment: `execution.md` is **evidence to verify**, not proof.
3. **Find the earliest real blocker or ready action.** Unresolved direction → `brain-brainstorm`; changed behavior → `brain-write-spec`; stale/missing binding design → `brain-design-implementation`; approved ready work → `brain-implement`. Recommend `brain-decompose-feature` or `brain-write-tasks` as required only for affected existing documents or an actual approval blocker; otherwise make them optional, with reasons. A pending review or failing verification for the current increment takes precedence over starting the next. When governing documents are current and approved, dependencies satisfied and execution evidence reconciled, recommend `brain-implement` with the **actual recorded** next unblocked task/increment ID. Do not invent `INC-*` identifiers or assume numeric order defines dependencies.
4. **Consider other steps.** Unresolved failure diagnosis → `brain-diagnose`; substantive completed work needing review → `brain-review-code`; stale shared knowledge → `brain-update`; nothing actionable → explicitly say no further action is needed. Don't recommend reproducing completed, approved stages. If evidence conflicts or a prerequisite is ambiguous, report the blocker rather than guessing.
5. **Return one next action.** Format `Next: /skill-name <actual-existing-feature-or-work-id>` with evidence and blockers. If useful, also state `Optional: /brain-decompose-feature <feature> — <reason>` or `Optional: /brain-write-tasks <feature> — <reason>`. The optional step is never silently a prerequisite; an affected existing document requiring reapproval becomes the main next action. Recommending a step is **not permission** to run it, edit the Brain or implement code. `brain-implement` requires an explicit user request, regardless of the recommendation.

## Explicit documentation reconciliation

Only on an **explicit request to update feature documentation** (for example, `/brain-next yaml-cli --reconcile unknown fields now warn`), apply `references/next-routing.md` to select the *minimum* affected document-producing skills. Show the route and, where the Claude Code Skill tool supports invocation, coordinate those skills **sequentially** in dependency order, waiting for each required user approval. Owners write/reapprove their own documents; **brain-next does not write or approve producer-owned files**, silently refresh hashes or change `execution.md`. If invocation is unavailable, stop and give a targeted copyable `/skill-name` handoff; never claim it ran. Do not invoke `brain-implement`, edit production code or commit. Re-read the actual approvals and status before returning a next-step recommendation.

**Read on demand:** `${CLAUDE_SKILL_DIR}/references/next-routing.md` for the decision order, increment examples and revision safety; `${CLAUDE_SKILL_DIR}/../brain-init/references/feature-document-contract.md` for governing metadata and approval rules.

**Recommended next step:** End the final user-facing reply with one concise, evidence-based next action, naming the appropriate skill or command when useful. If blocked, identify the missing information, prerequisite, or approval instead of advancing; if complete, say no further action is needed. A recommendation is not authorization to execute another step. Keep it outside copy-ready deliverables.
