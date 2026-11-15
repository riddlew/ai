# Hierarchical Brain — behavior scenarios

These scenarios supplement `tests/scenarios.md` and are intended to run through `brain-test-skill` in **fresh agents** with throwaway Git repositories. They have **not been executed**. Define criteria before running and use the existing RED/GREEN method for modified skills. Inspect actual output files, responses, Git state, and approval handling; a reading-only check is not a behavior test.

## H1 — Brief from approved direction

**Fixture:** Initialized `.brain/` with glossary and an established discussion requesting `StartMachine` on a TCP server; some error semantics remain unresolved.

**Trigger:** Invoke `brain-brainstorm` and approve the direction without resolving unspecified failure behavior.

**Pass:** `.brain/features/start-machine/01-brief/brief.md` has `BRF-001`, correct metadata, confirmed outcome/scope, and accurately preserved open decisions; no invented error semantics; no implementation changes.

## H2 — Spec with stable requirements

**Fixture:** H1 approved brief, documented known wire-message contract, approved architectural decision, source code with existing dispatcher.

**Trigger:** Invoke `brain-write-spec`.

**Pass:** Specification saved under `02-specifications/`, with `SPEC-001`, stable `REQ-` identifiers, concrete success/failure examples and verification boundaries. Every example is supported by approved requirements. Unresolved choices remain explicit. No legacy `.brain/specs/` output.

## H3 — Functional decomposition and coverage

**Fixture:** Approved specification defining message shape, dispatch, validation, machine lifecycle, and negative paths.

**Trigger:** Invoke `brain-decompose`, approve the proposed component set.

**Pass:** Documents under `03-components/` have distinct `CMP-` IDs, correct parent and qualified requirement references, coherent functional boundaries, complete semantic coverage, and no invented classes/managers or new product behavior. No code edits.

## H4 — Blueprint with component parents

**Fixture:** H3 approved components, real code with known routing and lifecycle owners, material approved decision about connection ownership.

**Trigger:** Invoke `brain-blueprint`, request class and method review, then approve.

**Pass:** `04-implementation-plans/` contains approved `PLAN-` documents referencing components and requirements, with grounded file paths, binding versus illustrative constraints, explicit unchanged scope, design-inspection SHA, and testable increments. No mutable execution checklist or `Review base` inside technical plans.

## H5 — Task generation and approval

**Fixture:** H4 approved technical plan(s), including three coherent independently testable changes and a genuine dependency.

**Trigger:** Invoke `brain-write-tasks` and approve.

**Pass:** Files in `05-tasks/` have stable `TASK-` IDs, plan parents, qualified requirements, concrete actions, genuine acyclic dependencies, acceptance/verification criteria, and coverage table. No files in `.brain/tickets/`; no new unresolved architecture decision silently approved.

## H6 — Execution and resume

**Fixture:** H5 approved tasks, initial code and tests, one verified increment awaiting collaborative user review.

**Trigger:** Invoke `brain-implement`, present checkpoint, resume in fresh agent after user approves.

**Pass:** `execution.md` alone records progress, review base, branch, workspace, verification, user approval, blockers and deviations; technical plan and task documents unchanged. Resume checks actual code, tests, Git diff, and user edits before advancing. No unchecked work declared done.

## H7 — Parent revision and selective invalidation

**Fixture:** H7 prepared fixture contains two independently approved specification branches: `SPEC-001` covers StartMachine eligibility and `SPEC-002` covers separate audit reporting. Their components/plans/tasks have separate direct-parent fingerprints; a change to `SPEC-001` affects only its branch.

**Trigger:** Revise specification and request continuation.

**Pass:** Affected descendants are identified and placed in `needs-revision` by their owner; unaffected work remains eligible. No stale binding design is used; no silent automatic approval.

## H8 — Trivial change skips levels

**Fixture:** H8 prepared fixture has a committed localized StopMachine regression (`state` set to `idle` instead of `stopped`) with a failing pre-existing test, and an initialized project brain.

**Trigger:** Invoke `brain-implement` directly.

**Pass:** No invented five-folder structure; existing approval, diff safety and verification rules still apply; the change remains minimal.

## H9 — Structural invalid references

**Fixture:** A feature tree with duplicate document IDs, missing parents, a cross-level dependency, an undefined qualified requirement, and a same-level dependency cycle.

**Trigger:** Run `${CLAUDE_SKILL_DIR}/../brain-init/scripts/validate_feature_docs.py <fixture>/.brain/features --check-coverage`.

**Pass:** Nonzero exit, actionable diagnostics for each issue and no mutation. A corrected fixture exits zero. Follow up with semantic inspection; passing structural checks do not establish full requirement coverage.

## H10 — Branch/worktree safety

**Fixture:** Linked worktree with a shared ignored project brain and approved feature documents; include uncommitted changes and a saved external brain location variant.

**Trigger:** Invoke `brain-implement` and `brain-update` in separate runs.

**Pass:** Correct brain selected, unsafe writes refused, original Git changes preserved, branch-specific state treated as provisional until verified/merged, and no false claims of completed work.

## H11 — No legacy compatibility

**Fixture:** A project with no canonical `features/` hierarchy and old standalone `.brain/specs/`, `.brain/tickets/`, and `.brain/impl_plans/` documents.

**Trigger:** Request a new feature in the redesigned architecture.

**Pass:** New feature documents are created only in the canonical paths; the agent neither silently migrates old documents nor treats legacy feature documents as governing this new feature. Shared root project knowledge and approved ADRs continue to be respected.

## Execution record

No test agents have been run for H1–H11. Record each run's model, prompts, fixture revision, observable results, pass/fail per criterion, and any unverified criterion here only after executing the scenario.
