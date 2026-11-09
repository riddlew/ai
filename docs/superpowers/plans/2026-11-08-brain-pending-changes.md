# Pending brain changes for branches: implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** The brain's code descriptions describe the main branch. Other branches' changes wait in `.brain/pending/<branch>.md` until the user says the branch merged. Every `brain-update` run starts with a reminder list of pending files.

**Architecture:**
- `brain-update` gains a main-branch check, a reminder, and a new §2 "Branches": recording pending changes, applying merges, abandoned branches, legacy brains.
- `brain-init` records `Main branch:` and runs its first run only on the main branch.
- `templates.md` gains the header line and the pending-file template.
- The shared preamble changes only if a baseline shows it's needed.
- Behavior is tested with writing-skills scenarios on new branch fixtures.

**Tech Stack:** Markdown skills, POSIX shell + git, `tests/fixture/` (Python `crate` app).

**Spec:** `docs/superpowers/specs/2026-11-08-brain-pending-changes-design.md`

## Global Constraints

- **Scope:** all edits under `skills/experimental_v4/` and `docs/superpowers/`. Branch `worktree-brain-pending`.
- **Commits:** no attribution trailer.
- **Model names:** only in root `CLAUDE.md`'s Model tiers table.
- **Git:** no skill text runs `git commit`, `git push`, or `git merge`.
- **Portability:** commands are portable across Linux, macOS, and Windows (Git Bash or WSL).
- **Fixed names:**
  - the header line `Main branch: <name>` in `00_index.md`, after `Git:`;
  - the folder `.brain/pending/`, with one file per branch: `<branch>.md`, where a `/` in the branch name becomes `--`;
  - the pending-file header lines: `Branch: <name>`, `Base: <merge-base sha>`, `Updated: <branch HEAD sha> (<YYYY-MM-DD>)`;
  - entry verbs: `Add`, `Change`, `Remove`.
- **Size:** `brain-update/SKILL.md` additions stay under about 400 words (now 1,275). `brain-init/SKILL.md` additions stay under about 80 (now 1,164).
- **Test agents:** standard tier. RED runs use a skills copy taken before Task 3. Every fixture is built in its own `mktemp -d` folder, outside this repository.

## Review Focus

1. **A user says a branch merged while on that branch, not on main.** `brain-update` should say merges are applied from the main branch, and apply nothing (S57).
2. **A branch name with `/`.** It must map to `--` in the file name (S51 uses `feature/cue-points`).
3. **A branch that keeps going after its merge.** The user says `cue-points` merged, but the branch has a commit that isn't on main. Only the entries the main branch's code confirms are applied. The rest are reported, and the user is asked whether to keep them pending or drop them. S53's planted entry, which the code contradicts, exercises this path.
4. **A detached `HEAD`.** `brain-update` should ask which branch the work belongs to. No scenario; the reviewer checks the text.
5. **Intent recorded as pending by mistake.** A decision made on a branch must go straight to `09`, not into the pending file (S51 criterion 3).

---

### Task 1: Branch fixtures and scenarios

**Files:**
- Create: `skills/experimental_v4/tests/fixture/pending/feature--cue-points.md`
- Create: `skills/experimental_v4/tests/fixture/pending/old-idea.md`
- Modify: `skills/experimental_v4/tests/scenarios.md`

**Interfaces:**
- Produces fixture recipes **branched**, **branched+pending** and **merged**, and scenarios S51–S57 plus revised S1, S4, S11 and S12. Tasks 2 and 7 use them.

- [ ] **Step 1: Write `fixture/pending/feature--cue-points.md`.** Use the Global Constraints header, with `Base` set to the literal `__A_SHA__`, and these entries:
  - `02_features.md`: Add `cue add <track> <seconds>`.
  - `04_data_model.md`: Add the `cue_points` table, with `track_id` and `seconds` as a float.
  - `04_data_model.md`: Add `cue_points.position_ms`, an integer of milliseconds. This entry is planted; the code contradicts it.
- [ ] **Step 2: Write `fixture/pending/old-idea.md`.** It holds one `Add` entry for `05_settings.md`. Its branch `old-idea` never exists.
- [ ] **Step 3: Add the fixture recipes to `scenarios.md`,** after **synced**:
  - **branched:** commit A on `main`, the brain synced to A, then `git checkout -q -b feature/cue-points` and commit B there. No WIP file. `<FIXTURE>` is on `feature/cue-points`.
  - **branched+pending:** branched, plus the pending fixture copied to `.brain/pending/feature--cue-points.md`, with `__A_SHA__` replaced.
  - **merged:** branched+pending, then `git checkout -q main && git merge --squash feature/cue-points && git commit -qm "Add cue points (#12)"`. It is a squash merge, so there is no ancestry.
- [ ] **Step 4: Add the scenarios.** All run on the standard tier.
  - **S51** (branched, `brain-update`, context: S2's session summary, trigger `/brain-update`):
    1. `pending/feature--cue-points.md` exists and covers `cue add` and the `cue_points` table.
    2. `02_features.md` and `04_data_model.md` don't mention cue points, and `Last synced` is still `<A>`.
    3. `09` records seconds-as-floats.
    4. `state.md` lists cue points as in progress on `feature/cue-points` and links the pending file.
    5. `00_index.md` has `Main branch: main` and lists the pending file.
  - **S52** (branched+pending, then `git checkout -q main` and S4's `--version` commit on `main`; trigger `/brain-update`):
    1. The reply begins with the pending list, naming `feature/cue-points`.
    2. The pending file is byte-identical, and no root file describes cue points.
    3. `02_features.md` mentions `--version`, and `Last synced` is `main`'s `HEAD`.
  - **S53** (merged, trigger `/brain-update feature/cue-points merged`; follow-up, if it asks about unconfirmed entries: `The user replies: "Drop them."`):
    1. `02` describes `cue add`, and `04` has the `cue_points` table in seconds.
    2. The milliseconds entry is reported as not matching the code, it asks whether to keep or drop it, and `04` doesn't mention `position_ms`.
    3. After the follow-up, the pending file is deleted, `state.md` marks cue points done, and `00_index.md` no longer lists the file.
    4. `Last synced` is `HEAD`.
  - **S54** (synced, plus `fixture/pending/old-idea.md` copied into `.brain/pending/`; trigger `/brain-update`):
    1. The reply begins with the list, marking `old-idea` "branch not found".
    2. `pending/old-idea.md` still exists.
  - **S55** (commit A only, then `git checkout -q -b feature/x`; `brain-init`; trigger `/brain-init`):
    1. It says the brain describes the main branch, and to run `/brain-init` from a checkout of `main`.
    2. It stops, and no `.brain/` exists.
  - **S56** (branched+pending, header H1 on the impl plan; `brain-implement`; trigger as S9):
    1. It reads `pending/feature--cue-points.md`.
  - **S57** (branched+pending, still on `feature/cue-points`; trigger `/brain-update feature/cue-points merged`):
    1. It says merges are applied from the main branch.
    2. The pending file and the root files' code descriptions are unchanged.
- [ ] **Step 5: Revise the existing scenarios.**
  - **S1:** add the criterion "`00_index.md` has `Main branch: main`".
  - **S4:** the run is now on branch `wt`, so the criteria become: `--version` goes into `<RUN>/.brain/pending/wt.md`, and not into `02_features.md`.
  - **S11:** the worktree is on `wt`, so the criteria become: it says to run from a checkout of `main`, and creates no `.brain/`.
  - **S12:**
    1. The reply says the brain was last synced from a commit not on the main branch.
    2. `--version` moves out of `02_features.md` into `pending/wt.md`.
    3. `Last synced` is `main`'s `HEAD`, and `00_index.md` lists `pending/wt.md`.
- [ ] **Step 6: Commit:** `test: add branch fixtures and S51-S57; revise S1, S4, S11, S12`.

### Task 2: RED runs

- [ ] **Step 1:** Copy the skills, without `tests/`, to the run root as the RED copy.
- [ ] **Step 2:** Run S51, S52, S53 and S57 three times each. Run S54, S55, S56, S4, S11 and S12 once each. Follow-ups as in the scenarios.
- [ ] **Step 3:** Record the results in a new `### Pending brain changes, RED` results section.
  - Expected: S51–S55 and S57 fail. S4, S11 and S12 fail their revised criteria.
  - **S56 decides Task 5:** if RED passes, Task 5 is skipped, and that decision is recorded.
- [ ] **Step 4: Commit:** `test: record pending-changes RED results`.

### Task 3: `brain-update` and templates

**Files:**
- Modify: `skills/experimental_v4/brain-update/SKILL.md`
- Modify: `skills/experimental_v4/brain-update/references/templates.md`

**Interfaces:**
- Consumes: the fixed names in Global Constraints.
- Produces: `brain-update` §2 "Branches". Its old §2–§4 become §3–§5. Every cross-reference is updated, including `brain-init`'s pointers to `brain-update` §3 and §4, which become §4 and §5.

- [ ] **Step 1: §1.**
  - After finding the brain, read `Main branch:`. If the line is missing, detect the branch (spec goal 2), add the line, and say so.
  - **Reminder:** before anything else in the reply, list each pending file with its branch, entry count and `Updated:` date. Mark "branch not found" when `git rev-parse --verify --quiet refs/heads/<branch>` fails.
- [ ] **Step 2: Write the new §2, "Branches".** It has four short parts, matching spec goals 3–5 and 7–9:
  - **On another branch:** pending entries, from the diff between the merge base and `HEAD`; intent goes to the root files directly; `state.md` and `00_index.md` items. On a detached `HEAD`, ask which branch the work belongs to.
  - **The user says a branch merged:** this happens only on the main branch. Verify each entry and apply the confirmed ones. Report the rest, and ask whether to keep them pending or drop them. Delete the file once no entry is left, and mark the `state.md` items done.
  - **Abandoned:** delete only on the user's word.
  - **Legacy:** spec goal 9.
- [ ] **Step 3: Update the old §2.** It is now §3, "Update", and runs only on the main branch.
  - Step 2's "not an ancestor" paragraph now points to §2 Legacy.
  - Step 6 sets `Last synced` only on the main branch.
  - The update steps' references change: ADRs "(§4)" becomes "(§5)", and spikes and size "(§3)" becomes "(§4)".
- [ ] **Step 4: Update `templates.md`.** Add `Main branch: main` to the `00_index.md` header block, and add a `## pending/<branch>.md` template with the three header lines and one example entry per verb.
- [ ] **Step 5:** Run `wc -w brain-update/SKILL.md`. Expected: about 1,675 or fewer.
- [ ] **Step 6: Commit:** `feat(brain-update): record pending changes for branches and apply them on merge`.

### Task 4: `brain-init`

**Files:**
- Modify: `skills/experimental_v4/brain-init/SKILL.md`

- [ ] **Step 1: The "No path" branch, before the first run.** If the current branch isn't the main branch (detected as in spec goal 2), say the brain describes the main branch, tell the user to run `/brain-init` from a checkout of it, and stop. A detached `HEAD` counts as not the main branch.
- [ ] **Step 2: §2 step 5.** Write `Main branch: <name>` in `00_index.md`, and report it.
- [ ] **Step 3: Update the cross-references** to `brain-update` §4 (root files) and §5 (ADRs).
- [ ] **Step 4: Commit:** `feat(brain-init): record the main branch and run the first run only on it`.

### Task 5 (only if S56 RED failed): the shared preamble

**Files:**
- Modify: the shared preamble in the 11 skills that carry it.

- [ ] **Step 1:** After "read every root `.md` file in that brain now", add: "On a branch other than the brain's `Main branch:`, also read `pending/<branch>.md` when it exists."
- [ ] **Step 2: Commit:** `feat: read the current branch's pending brain changes`.

### Task 6: README

**Files:**
- Modify: `skills/experimental_v4/README.md`

- [ ] **Step 1:** Replace the **Known limit** paragraph with **Branches**, in three sentences:
  - the code descriptions describe the main branch;
  - other branches' changes wait in `.brain/pending/`;
  - run `/brain-update <branch> merged` on the main branch after a merge, and every run starts by listing pending files.
- [ ] **Step 2:** Add `pending/` to the `.brain/` tree.
- [ ] **Step 3: Commit:** `docs: describe pending brain changes`.

### Task 7: GREEN and regression

- [ ] **Step 1:** Copy the skills as the GREEN copy.
- [ ] **Step 2: Run S51–S57 three times each, or once each for S54–S56.** Expected: all pass.
- [ ] **Step 3: Regression, one run each:**
  - S1, S4, S11 and S12, against their revised criteria;
  - S2, S5, S46 and S47, unchanged.
- [ ] **Step 4:** Record the results.
- [ ] **Step 5: Commit:** `test: record pending-changes GREEN and regression results`.

### Task 8: Final review

- [ ] **Step 1:** Dispatch a strongest-tier reviewer on `git diff <base>..HEAD`, with the spec, this plan's Review Focus, and the results.
- [ ] **Step 2:** Fix Critical and Important findings test-first, and record deferred minors.
- [ ] **Step 3:** Rerun the affected scenarios once, record the results, and commit.
