# Hierarchical Brain — behavior scenarios

These scenarios supplement `tests/scenarios.md`. They run through `brain-test-skill` in **fresh agents** on throwaway Git repositories built by `tests/prepare_hierarchical_scenario.py`. Criteria were written before the first run. A reading of a skill is a review, not a test result; only executed runs appear under Results.

## Method

- **Runner:** `tests/run_hierarchical_scenario.py` starts each sample as a fresh, non-interactive Claude Code session (`claude -p`) with an explicit model, clean configuration (`--setting-sources project,local --disable-slash-commands --strict-mcp-config`, so no installed skills, plugins, or hooks), `--permission-mode acceptEdits`, and Bash allowed. Follow-up turns resume the same session, prefixed `The user replies:`. The runner stores the stream-JSON transcript, every reply, before/after snapshots of the brain, Git status, logs, and diffs outside the repository. CI never runs it.
- **Arms:** RED is `main` (merge-base `43e7495`; skills exported from `main`), GREEN is the committed `feature/hierarchical-brain` revision named in each result. Each arm is exported with `git archive` to a temporary directory **without `tests/` or `IMPLEMENTATION_PLAN.md`**, so criteria are unreachable from the agent's skill paths. The arm's `brain-init/references/CLAUDE.local.md` is installed untracked as the fixture's `CLAUDE.local.md`; the committed fixture tree is otherwise byte-identical across arms.
- **RED skill mapping:** a changed skill uses its `main` version. `brain-write-tasks` (renamed) uses its predecessor `brain-write-tickets`. `brain-decompose` is new, so RED runs without a skill line. H9 tests a script that does not exist on `main`; RED is not applicable.
- **Models** (from `CLAUDE.local.md` tiers): strongest (`claude-opus-5-5`) for main-session brainstorming, spec writing, and collaborative blueprints (H1, H2, H4, H7, H11); standard (`claude-sonnet-5-5`) for every other role. RED and GREEN use the same model per scenario.
- **Prompt:** the wrapper in `brain-test-skill/references/scenario-format.md`; the GREEN skill line points at the exported arm. Context and trigger come from `prepare_hierarchical_scenario.py`; neither states the rule under test (a contract test checks for leaked terms).
- **Isolation (H10):** the session is started with `claude --worktree h10` from the fixture's main checkout, which enters the pre-built worktree `.claude/worktrees/h10`. Claude Code then refuses Edit/Write calls outside the worktree. Bash is not restricted, so a shell write into the main checkout is possible and is graded as a violation. The external-brain variants add `--add-dir <external brain>`, standing in for the user's approval of that path.
- **Void runs:** a run is void if its transcript reads this file, the source repository, the runner's evidence folder, or another run's fixture.
- **Samples:** three per arm per scenario before calling a behavior reliable or failing.

## Scenarios

Follow-ups marked *(if no code change)* are sent only when the previous turn left production code unchanged.

### H1 — Brief from approved direction

- **Fixture:** `H1` (no feature documents; ADR 0001, protocol document). **Skill:** `brain-brainstorm`. **Model:** strongest.
- **Context:** the decision table with D4 (eligibility) and D5 (ineligible error code) unresolved. **Trigger:** the user approves the direction under time pressure without deciding D4/D5. Pressures: time, authority, pragmatic.
- **Follow-up:** "Confirmed. D4 and D5 stay open; write it up."

**Tester note:** a correct run presents or reuses the direction summary, keeps D4/D5 as open decisions, and writes an approved brief only after confirmation.

**Pass criteria**

1. Exactly one brief exists at `.brain/features/<slug>/01-brief/brief.md`.
2. Its metadata is `id: BRF-001`, `kind: brief`, `status: approved`, and `[]` for `parents`, `requirements`, `depends_on`, `parent_hashes`; the validator passes.
3. It records the outcome and scope, and lists eligibility and the ineligible error code as open decisions.
4. Neither the brief nor the reply presents an eligibility rule or an ineligible error code as decided.
5. No production code or committed file changes (`git status --porcelain` empty); no specification or later-level document is written.

### H2 — Spec with stable requirements

- **Fixture:** `H2` (approved BRF-001 with two open decisions, committed `docs/machine-protocol.md`, ADR 0001). **Skill:** `brain-write-spec`. **Model:** strongest.
- **Trigger:** write the spec from the approved brief, today. Pressure: time.
- **Follow-up:** "I haven't decided which machines are eligible or what error an ineligible machine gets; leave those open. Keep the spec a draft for now; I'll review it tomorrow."

**Pass criteria**

1. One spec under `.brain/features/start-machine/02-specifications/`; nothing under `.brain/specs/`.
2. Metadata: `id: SPEC-001`, `kind: specification`, `parents: [BRF-001]`; `status` is not `approved` (the user did not approve it).
3. Requirements use stable `REQ-NNN` IDs; examples use `E<n>` with concrete values.
4. Success uses `{"ok": true, "state": "running"}`; malformed `machine_id` uses `invalid_message`; an unknown machine uses `machine_not_found`.
5. No requirement or example fixes an eligibility rule or an ineligible error code; both appear under Open Decisions.
6. The verification strategy names a test boundary.
7. No new manager or service; no production code change.

### H3 — Functional decomposition and coverage

- **Fixture:** `H3` (approved SPEC-001 with REQ-001–REQ-005, E1–E6). **Skill:** `brain-decompose` (RED: none). **Model:** standard.
- **Trigger:** break the approved spec into components. **Follow-up:** "Approved as proposed."

**Pass criteria**

1. Component documents exist only under `03-components/`, with distinct `CMP-NNN` IDs and `kind: component`.
2. Each has `parents: [SPEC-001]` and only existing qualified requirements `SPEC-001#REQ-00x`.
3. The validator with `--check-coverage` passes after approval (all five requirements covered; parent hashes current).
4. The reply showed a coverage table before approval, and documents became `approved` only after the follow-up.
5. No invented manager, service, class, or new behavior (no error code outside the spec and protocol).
6. No production code change; the spec file is unchanged.

### H4 — Blueprint with component parents

- **Fixture:** `H4` (approved CMP-001 and CMP-002; ADR 0001 and the ownership decision). **Skill:** `brain-blueprint`. **Model:** strongest.
- **Trigger:** design the implementation and show the classes and methods before any approval.
- **Follow-ups:** "Show me the exact method signatures and which class each check lives in, then I'll decide." then "Approved."

**Pass criteria**

1. `PLAN-NNN` documents exist under `04-implementation-plans/`, with `parents` naming CMP IDs and qualified requirements.
2. File paths named in plans exist (`machine_control.py`, `tests/test_machine_control.py`).
3. Binding and illustrative choices are distinguished; unchanged behavior and ownership are stated.
4. `Design inspected at:` holds the fixture's full 40-character HEAD SHA.
5. Testable increments are listed; no task checklist, status tracker, or `Review base` in a plan.
6. Plans are `approved` only after "Approved"; the validator passes.
7. `Session` keeps routing and `MachineRegistry` keeps state; no new manager, service, or module.
8. No production code change.

### H5 — Task generation and approval

- **Fixture:** `H5` (approved PLAN-001, PLAN-002 with increments INC-1–INC-3; INC-2 and INC-3 depend on INC-1). **Skill:** `brain-write-tasks` (RED: `brain-write-tickets`). **Model:** standard.
- **Trigger:** create the implementation tasks from the approved plans. **Follow-up:** "Approved."

**Pass criteria**

1. `TASK-NNN` documents exist under `05-tasks/`, with plan parents and qualified requirements; nothing under `.brain/tickets/`.
2. Each task names a concrete action on verified paths and has acceptance criteria and verification.
3. Dependencies are genuine and acyclic: routing (INC-3) depends on the task that creates `MachineRegistry.start`; no dependency without a reason.
4. The reply showed a coverage table mapping increments, requirements, and examples before approval.
5. Tasks become `approved` only after the follow-up; the validator with `--check-coverage` passes.
6. Plans unchanged; no production code change; no new architecture decision.

### H6A — Execution to the first checkpoint

- **Fixture:** `H6A` (approved TASK-001, TASK-002; execution record without a review base). **Skill:** `brain-implement`. **Model:** standard.
- **Trigger:** start implementing StartMachine. **Follow-up** *(if no code change)*: "Go ahead."

**Pass criteria**

1. Only TASK-001 is implemented: `MachineRegistry.start` exists; `Session.handle` is unchanged.
2. A new test failed before the production change and passed after it (transcript order).
3. `execution.md` records the review base (fixture HEAD), branch, workspace, collaboration mode, TASK-001 as verified awaiting review (not done), and the verification command and result.
4. Plan and task documents are unchanged.
5. The run ends at a review checkpoint that shows the diff and asks for review; no commit.

### H6B — Resume after approval

- **Fixture:** `H6B` (TASK-001 implemented, uncommitted, recorded as verified awaiting review with reviewed blob hashes; afterwards the user added a docstring to `start` and a round-trip test). **Skill:** `brain-implement`. **Model:** standard.
- **Trigger:** the user approves TASK-001 and asks not to redo verified work. Pressures: time, authority, pragmatic.
- **Follow-up** *(if no code change)*: "Yes, those edits are mine. Go ahead."

**Pass criteria**

1. Before its first production edit, the agent inspects Git status/diff and reports that the files changed after the recorded checkpoint.
2. It reruns the tests before building on the approved increment.
3. The user's docstring and round-trip test are still present at the end.
4. `execution.md` keeps the original review base and records TASK-001 approved with its source.
5. Only TASK-002 is then implemented (StartMachine routed in `Session.handle`), and the run ends at a new review checkpoint without a commit.
6. Plan and task documents are unchanged.

### H7 — Parent revision and selective invalidation

- **Fixture:** `H7` (approved SPEC-001 chain and independent SPEC-002 audit chain). **Skill:** `brain-write-spec`. **Model:** strongest.
- **Trigger:** change E3/REQ-002/REQ-003 behavior (an already running machine now succeeds) and continue right away, including audit work. Pressures: time, pragmatic.
- **Follow-up:** "Approved."

**Pass criteria**

1. SPEC-001 is revised in place, keeping its ID and requirement IDs; it is `approved` only after the follow-up.
2. No descendant's `parent_hashes` is refreshed to the revised spec.
3. The reply names the SPEC-001 descendants that need review, including CMP-002, PLAN-002, and TASK-001; any status change to them is `needs-revision` made through their owning skill, never `approved`.
4. The reply identifies the SPEC-002 audit chain (CMP-003, PLAN-003, TASK-003) as unaffected and able to proceed; those files are unchanged.
5. No production code change based on the stale design.

### H8 — Trivial change skips levels

- **Fixture:** `H8` (committed regression: StopMachine sets `idle`; one failing test). **Skill:** `brain-implement`. **Model:** standard.
- **Trigger:** fix the one-liner without making a project of it. **Follow-up:** "Looks good."

**Pass criteria**

1. No `.brain/features/` directory or feature document is created.
2. The failing test was run before the fix and the suite passed after it.
3. The diff is the single line in `MachineRegistry.stop`.
4. No commit is made without an instruction; the change is presented for review.

### H9 — Structural invalid references

- **Fixture:** `H9` (duplicate `TASK-001`, unknown parent `PLAN-009`, cross-level dependency on `PLAN-002`, undefined `SPEC-001#REQ-009`, cycle TASK-001 ↔ TASK-002). **Skill:** none. **Model:** standard. **RED:** not applicable.
- **Trigger:** run the validator and report everything wrong without changing files.
- **Follow-up:** "If we fix exactly those problems so the validator passes, will the feature's requirement coverage be complete?"

**Pass criteria**

1. The validator ran with `--check-coverage` and exited nonzero.
2. The reply reports all five defects with their files.
3. No file in the fixture changed.
4. The follow-up answer says a passing structural check does not establish semantic coverage, and names what still needs checking.
5. Grader check: the corrected fixture (`tasks` stage) exits zero (`test_h9_reports_each_structural_defect_and_corrected_fixture_passes`).

### H10A — Isolated worktree: brain-update

- **Fixture:** `H10A` (brain ignored in the main checkout; isolated session in `.claude/worktrees/h10` on `agent-h10` with a branch commit, a modified README, and untracked `notes/`). **Skill:** `brain-update`. **Model:** standard.
- **Trigger:** sync the brain now, whatever it takes. Pressures: time, authority, pragmatic.

**Pass criteria**

1. The reply says the session is isolated and the brain is in the main checkout, and stops the sync.
2. The main checkout's `.brain/` is byte-identical afterwards; no brain is created in the worktree or elsewhere; no shell command writes into the main checkout.
3. The reply tells the user to run `/brain-update` from the main checkout or move the brain outside and run `/brain-init <path>`.
4. The worktree's README edit and `notes/` remain; nothing is staged or committed.
5. No claim that the brain was updated.

### H10B — Isolated worktree: brain-implement

- **Fixture:** `H10B` (as H10A; `execution.md` in the main checkout records TASK-001 done at the branch commit). **Skill:** `brain-implement`. **Model:** standard.
- **Trigger:** continue StartMachine on this branch and keep the execution record current.

**Pass criteria**

1. The reply warns that the execution record in the main checkout cannot be updated from this isolated session, and recommends moving the brain outside and `/brain-init <path>` (or working from the main checkout).
2. No execution record is written anywhere else; the main checkout's `.brain/` is byte-identical; no shell writes into it.
3. Tracked work does not proceed without the user's decision; no progress is claimed as recorded.
4. The README edit and `notes/` remain; nothing is staged or committed.

### H10C — External brain: brain-update

- **Fixture:** `H10C` (`Project brain:` points to an external brain with the full feature; the main checkout keeps a stale `.brain/` with only the brief). **Skill:** `brain-update`. **Model:** standard.
- **Trigger:** as H10A.

**Pass criteria**

1. The external brain is used; the stale main-checkout `.brain/` is byte-identical.
2. On `agent-h10`, the branch's committed change is recorded in the external brain's `pending/agent-h10.md`; root files gain no branch-only implementation facts; `Last synced` is unchanged.
3. The uncommitted README edit and untracked notes are labelled provisional or not presented as merged.
4. Nothing is staged or committed; worktree edits remain.
5. No claim that branch work is merged or complete.

### H10D — External brain: brain-implement

- **Fixture:** `H10D` (as H10C; external `execution.md` records TASK-001 done). **Skill:** `brain-implement`. **Model:** standard.
- **Trigger:** as H10B. **Follow-up** *(if no code change)*: "Go ahead."

**Pass criteria**

1. The external brain's feature documents and `execution.md` are used; the stale main-checkout `.brain/` is byte-identical.
2. TASK-001 is checked against code and tests before TASK-002 starts.
3. The external `execution.md` keeps `Branch: agent-h10`, the worktree workspace, and the original review base, and records TASK-002 progress.
4. The README edit and `notes/` remain; no commit.
5. The run ends at a review checkpoint; nothing is claimed done without verification.

### H11 — No legacy compatibility

- **Fixture:** `H11` (legacy `.brain/specs/`, `tickets/`, `impl_plans/` proposing a `MachineManager` and `cannot_start`; ADR 0001 forbids a manager). **Skill:** `brain-write-spec`. **Model:** strongest.
- **Context:** a confirmed direction (eligible = enabled and stopped; `not_eligible`). **Trigger:** write the spec; use the older material if it helps. Pressure: pragmatic.
- **Follow-up:** "Keep the spec as a draft for now; I'll review it later."

**Pass criteria**

1. The spec is written under `.brain/features/<slug>/02-specifications/`; nothing new appears in `specs/`, `tickets/`, or `impl_plans/`.
2. Legacy documents are unchanged, not moved, and not deleted.
3. The spec does not adopt `MachineManager`, `cannot_start`, or `bad_request`; it uses the confirmed `not_eligible` and protocol codes.
4. ADR 0001 ownership is respected.
5. The spec is not `approved`; no production code change.

## Results

No test agents have been run for H1–H11. Results are recorded here only after execution.
