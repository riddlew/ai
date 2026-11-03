# brain-update / experimental_v4 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create `skills/experimental_v4/`: v3's skills renamed with a `brain-` prefix, a new `brain-update` skill that maintains a `.brain/` project store, and every other skill reworked to read from and write to `.brain/`.

**Architecture:** The skills are Markdown. "Tests" follow superpowers:writing-skills. Each scenario runs a fresh subagent in a throwaway fixture git repo. The baseline run gets only the user's original brief; the skill run gets the skill. The scenario passes when the pass criteria (fixture file state plus the agent's reply) hold. Static `grep` checks catch leftover v3 names and paths.

**Tech Stack:** Markdown skills (Claude Code `SKILL.md` format), bash, git, Python 3 (fixture app only, never executed by tests).

**Spec:** `docs/superpowers/specs/2026-11-03-brain-update-design.md`

## Global Constraints

- All edits happen in `skills/experimental_v4/`. `skills/experimental_v3/` is never modified.
- Skill directory name == `name:` frontmatter == `brain-<v3 name>`, per the design's naming table. `domain-modeling` and `handoff` do not exist in v4.
- `disable-model-invocation: true` stays exactly where v3 has it (`implement`, `write-spec`, `review-merge-request`, `distill-content`, `handoff`). `brain-update` is model-invocable.
- `brain-update`'s instructions never dispatch subagents. Existing subagent use in `brain-review-code` stays unchanged.
- `brain-update` never runs `git commit`. `.brain` defaults to untracked.
- A brain exists iff `.brain/00_index.md` exists.
- Size limits: 4,000 words per root file; 25,000 words across all root files.
- `00_index.md` header lines are exactly `Last synced: <40-char sha> (<YYYY-MM-DD>)` and `Git: tracked` or `Git: ignored`.
- Reading preamble, inserted verbatim as the first paragraph after each skill's H1 (every v4 skill except `brain-distill-content` and `brain-update`):
  `**Project brain:** If `.brain/00_index.md` exists (at this worktree's root, or in the main checkout when working in a linked git worktree) and you have not read its root files in this session (or they were lost to context compaction), read every root `.md` file in that `.brain/` now. Read subfolders only when a root file links to them or the task needs them. Do not load `.brain` into subagents wholesale; pass only what their task needs. If no brain exists, proceed without one and mention once that `/brain-update` can create it.`
- Invocation sentence, verbatim, where a skill must call brain-update: `Then invoke `brain-update` with a one-line summary of what changed.`
- Commits go to this worktree's branch `worktree-update-brain` only, with `git add skills/experimental_v4 docs/superpowers` (never `git add -A`; `skills/experimental_v3/` is an untracked copy that must stay uncommitted). No `Co-Authored-By` or other attribution trailer in commit messages.

## Review Focus

1. A linked git worktree with an untracked brain must use the main checkout's `.brain/` and must not create one in the worktree. Test: S4, in Task 5.
2. When the `Last synced` commit is gone (rebased), the skill re-verifies every root file instead of diffing an empty range. Test: S5, in Task 5.
3. A root file over 4,000 words gets split into `.brain/NN_<topic>/` without losing content. Test: S6, in Task 5.
4. A `.brain/` with only `specs/` (no `00_index.md`) triggers a first run that keeps the spec. Test: S7, in Task 5.
5. Root files that don't apply get omitted and marked not applicable, and are never left as placeholder files. Test: S1 criterion 6, in Tasks 3 and 4.

---

### Task 1: Scaffold experimental_v4 with renamed skills

**Files:**
- Create: `skills/experimental_v4/` (copy of `skills/experimental_v3/`)
- Delete: `skills/experimental_v4/handoff/`
- Rename: each remaining skill directory to `brain-<name>` (keep `domain-modeling/` unrenamed for now; Task 4 deletes it)
- Modify: every `SKILL.md` and reference file under `skills/experimental_v4/` except `README.md` (Task 8 rewrites it)

**Interfaces:**
- Produces: the renamed tree that all later tasks edit. Paths are `skills/experimental_v4/brain-<name>/SKILL.md`.

- [ ] **Step 1: Copy and rename**

```bash
cd /Users/wmbp/repos/ai/collection/.claude/worktrees/update-brain
diff -rq /Users/wmbp/repos/ai/collection/skills/experimental_v3 skills/experimental_v3   # must print nothing
cp -R skills/experimental_v3 skills/experimental_v4
cd skills/experimental_v4 && rm -rf handoff
for d in brainstorm diagnose distill-content implement plan-feature refine-backlog review-architecture review-code review-merge-request review-security write-spec write-tickets; do mv "$d" "brain-$d"; done
```

If the first `diff` prints anything, re-copy v3 from the main checkout before continuing.

- [ ] **Step 2: Rewrite skill references.** In every `.md` under `skills/experimental_v4/` except `README.md`, apply these replacements for each of the 12 renamed names `<n>`:
  - `name: <n>` → `name: brain-<n>`;
  - a backticked `` `<n>` `` → `` `brain-<n>` ``;
  - a backticked `` `/<n>` `` → `` `/brain-<n>` ``;
  - the path segment `../<n>/` → `../brain-<n>/`.

  Do not touch unbackticked words: "implement", "brainstorm" and "diagnose" also appear as plain English verbs. Leave H1 titles unchanged. In `brain-review-architecture/SKILL.md` line 61, replace `` `domain-modeling` `` with `` `brain-update` ``.

- [ ] **Step 3: Verify**

```bash
cd skills/experimental_v4
grep -rnE '`/?(brainstorm|diagnose|distill-content|implement|plan-feature|refine-backlog|review-architecture|review-code|review-merge-request|review-security|write-spec|write-tickets|handoff)`' --include='*.md' . | grep -v '^./README.md'
grep -rnE '\.\./(review-code)/' .
for f in brain-*/SKILL.md; do d=${f%%/*}; grep -q "^name: $d$" "$f" || echo "MISMATCH $f"; done
grep -rn 'handoff' --include='*.md' . | grep -v '^./README.md'
```

Expected: the four commands print nothing.

- [ ] **Step 4: Commit**

```bash
cd /Users/wmbp/repos/ai/collection/.claude/worktrees/update-brain
git add skills/experimental_v4 docs/superpowers
git commit -m "Scaffold experimental_v4 with brain- prefixed skills"
```

---

### Task 2: Test harness: fixture builder and scenarios

**Files:**
- Create: `skills/experimental_v4/tests/make-fixture.sh`
- Create: `skills/experimental_v4/tests/brief.md`
- Create: `skills/experimental_v4/tests/scenarios.md`
- Create: `skills/experimental_v4/tests/.gitignore` containing `.runs/`

**Interfaces:**
- Produces: `bash skills/experimental_v4/tests/make-fixture.sh <fresh|synced|partial> <dest>`. `<dest>` must not exist. Creates a git repo (identity `fixture <fixture@example.com>`, branch `main`) and prints `A=<sha>` and `HEAD=<sha>`.
- Produces: the run directory convention `skills/experimental_v4/tests/.runs/<scenario>-<baseline|skill>/`.
- Produces: the prompt wrapper (below), used verbatim by Tasks 3–7.

**Fixture facts:** tests depend on these, so they must hold exactly.
- **Commit A** (all variants):
  - `README.md` ("crate — a command-line tool for DJs to organize tracks into crates").
  - `crate/models.py`: `Track(title: str, artist: str, bpm: float)` and `Crate(name: str, tracks: list[Track])`.
  - `crate/store.py`: SQLite through `sqlite3`. Crates are stored in table `playlists`. The DB path comes from env var `CRATE_DB` (default `~/.crate.db`).
  - `crate/cli.py`: `argparse` commands `add-track`, `list-crate`, and `filter --bpm-min --bpm-max`. Filter bounds are inclusive (`min <= bpm <= max`).
  - `tests/test_store.py`: one test.
- **`fresh` and `partial` only:** commit A also tracks the following. (`synced` has none of these in git, because its brain already absorbed them.)
  - `CONTEXT.md`: terms Crate ("a named, ordered collection of tracks; stored as `playlists`"), Track, and BPM.
  - `docs/adr/0001-use-sqlite.md`.
  - `docs/specs/01-bpm-filter.md`: inclusive bounds. **E1:** tracks at 120/128/140 BPM, filter 125–135 → `[128]`. **E2:** filter 120–128 → `[120, 128]`.
- **`fresh`:** commit A only. No `.brain/`.
- **`partial`:** commit A plus untracked `.brain/specs/01-bpm-filter.md`, a copy of the spec. No `00_index.md`.
- **`synced`:** commit A, with `.brain/` listed in `.git/info/exclude` and filled in to match commit A:
  - `00_index.md`: `Last synced: <A sha> (2026-10-01)`, `Git: ignored`, every file listed, and `06_ux_interface.md` marked "not applicable: CLI with no visual interface".
  - `01_about.md`.
  - `02_features.md`: the three commands.
  - `03_architecture.md`: Python 3.11, `sqlite3`, the module list.
  - `04_data_model.md`: Track, and Crate → table `playlists`.
  - `05_settings.md`: `CRATE_DB`.
  - `07_integrations.md`: SQLite file only.
  - `08_error_logging.md`: errors go to stderr with exit code 1.
  - `09_user_decisions.md`: "2026-10-01 — Use SQLite for storage — `adrs/0001-use-sqlite.md`".
  - `glossary.md`: Crate (UI) ↔ `playlists` (DB), Track, BPM.
  - `open_questions.md`: "Should crates support nesting?"
  - `spikes.md`: "Rekordbox XML export format — unverified".
  - `state.md`: add-track and list-crate done. BPM filter in progress, linking spec 01 and impl plan 01.
  - `adrs/0001-use-sqlite.md`.
  - `specs/01-bpm-filter.md`.
  - `impl_plans/01-bpm-filter.md`, using the todo template: `Review base: <A sha>`, `[x] Inclusive lower bound (E1)`, `[ ] Inclusive upper bound (E2)`.
  - `reviews/architecture/01-store-layering.md`, linked only from `00_index.md`.

  It then makes **commit B**:
  - adds `cue_points: list[float]` (seconds) to `Track`;
  - adds a `cue add <track> <seconds>` command;
  - changes the filter upper bound to exclusive (`bpm < max`), which contradicts E2.

  Finally it leaves the untracked file `crate/stats.py` (`# WIP: average BPM per crate`).

**`brief.md`:** a verbatim copy of the user's original request for this feature: the "What this skill does" text through "The goal is to have all files and folders go to `.brain` as a central source." Copy it from the conversation, unedited.

**Prompt wrapper** (in `scenarios.md`, used verbatim):

```
You are an AI coding assistant working in the project at <FIXTURE>. Run every command from that directory.
<GUIDANCE>
<CONTEXT>
<TRIGGER>
Behave exactly as you would in a real session. When you need the user's input or approval, stop and end your reply with your question; the answer arrives in a follow-up message.
End every reply with a section "Files read and commands run:" listing each one.
```

- `<GUIDANCE>`, baseline: `The user previously described how they want project knowledge kept; read <ABS>/tests/brief.md.`
- `<GUIDANCE>`, skill: `You have the skill <name>. Read <ABS>/<name>/SKILL.md and follow it. ${CLAUDE_SKILL_DIR} means <ABS>/<name>. Skills it mentions live in <ABS>/.`
- `<TRIGGER>`: either `The user says: "<request>"` or `Another skill invokes you: "<message>"`.

**Scenarios** (`scenarios.md` records each one's setup, context, trigger, simulated answers, pass criteria, and results). Pass criteria are checked by reading the reply and the fixture.

- **S1: First run.** Fixture: `fresh`. Trigger: user says `/brain-update`. Each turn's answer below is the user's next message. After the answer sheet runs out, answer `I don't know yet; record it as open.`
  - **Turn 1** has created no files and moved none. It cites at least one fact from the code (SQLite, `playlists`, or a command name) and asks whether `.brain` should be tracked in git, saying the default is no. *Answer: `No, don't track it.`*
  - **Turn 2** proposes destinations for `CONTEXT.md`, `docs/adr/0001-use-sqlite.md` and `docs/specs/01-bpm-filter.md`. It says moving them takes them out of git, offers to leave them in place, and waits. *Answer: `Move them.`*
  - **Every later turn** asks exactly one question, and nothing the repo answers (language, database, commands, env vars). Answer sheet, in order:
    - purpose: "Personal tool for gigging DJs to prep sets offline."
    - users: "Me and a few DJ friends."
    - non-goals: "No streaming-service integration."
    - planned features: "Cue points next, Rekordbox export later."
  - **Final state:**
    - `00_index.md` has `Last synced: <HEAD sha>` and `Git: ignored`, and `.brain/` is in `.git/info/exclude`.
    - `glossary.md` maps Crate ↔ `playlists`.
    - The ADR is at `.brain/adrs/0001-use-sqlite.md`, the spec at `.brain/specs/01-bpm-filter.md`, and `CONTEXT.md` is gone.
    - **Criterion 6:** every omitted root file is marked not applicable in the index, and no root file is only placeholder text.
    - `open_questions.md` is non-empty, and `spikes.md` lists Rekordbox export as unverified.
    - HEAD is unchanged (no commit).
    - The final reply lists the open questions and assumptions.
- **S2: Update after work.** Fixture: `synced`. Context: "Session summary: the user decided cue points are stored in seconds as floats. The assistant had recommended integer milliseconds; the user did not approve that." Trigger: user says `/brain-update`. Pass criteria:
  - `02_features.md` describes `cue add`.
  - `04_data_model.md` has `cue_points`.
  - `glossary.md` has "Cue point".
  - `09_user_decisions.md` records seconds-as-floats, and contains no milliseconds decision.
  - `open_questions.md` flags the filter upper bound contradicting spec E2, and `.brain/specs/01-bpm-filter.md` is byte-identical to before.
  - `state.md` doesn't mark statistics done.
  - `Last synced` = commit B.
  - HEAD is unchanged, and `git status` shows only `crate/stats.py`.
- **S3: Invoked by another skill, no brain.** Fixture: `partial`. Trigger: another skill invokes you: `brain-write-spec saved .brain/specs/01-bpm-filter.md.` Pass criteria:
  - no root `.md` file is created;
  - the reply says no brain exists and `/brain-update` sets one up;
  - the spec is unchanged.
- **S4–S7** (Task 5) and **S8–S9** (Tasks 6–7) are specified in those tasks.

- [ ] **Step 1: Write `make-fixture.sh`, `brief.md`, `.gitignore`, and `scenarios.md`** with S1–S3 filled in, and placeholders headed S4–S9 for later tasks.
- [ ] **Step 2: Verify the fixtures**

```bash
cd skills/experimental_v4/tests
for v in fresh synced partial; do bash make-fixture.sh $v .runs/check-$v; done
git -C .runs/check-fresh log --oneline | wc -l          # 1
ls .runs/check-fresh/.brain 2>&1 | head -1               # No such file
git -C .runs/check-synced log --oneline | wc -l          # 2
git -C .runs/check-synced status --short                 # ?? crate/stats.py   (only)
grep -c 'Last synced' .runs/check-synced/.brain/00_index.md   # 1
ls .runs/check-partial/.brain                            # specs
rm -rf .runs/check-*
```

Expected: the values in the comments.

- [ ] **Step 3: Commit:** `git add skills/experimental_v4 docs/superpowers && git commit -m "Add brain skill test harness"`

---

### Task 3: RED: baseline runs for S1–S3

**Files:**
- Modify: `skills/experimental_v4/tests/scenarios.md` (Results → Baseline)

- [ ] **Step 1:** For each of S1–S3, build a fresh fixture at `.runs/S<n>-baseline` and dispatch a general-purpose subagent with the baseline wrapper. For S1, continue the same subagent with SendMessage for each answer.
- [ ] **Step 2:** Check every pass criterion. Record each failure verbatim in Results → Baseline, with the agent's own wording for its rationalizations.
- [ ] **Step 3:** Expected: S1 and S2 each fail at least one criterion. If a scenario passes everything, note it; the skill text for that behavior can stay minimal.
- [ ] **Step 4: Commit:** `git add skills/experimental_v4 docs/superpowers && git commit -m "Record brain-update baseline results"`

---

### Task 4: GREEN: write brain-update and remove domain-modeling

**Files:**
- Create: `skills/experimental_v4/brain-update/SKILL.md`
- Create: `skills/experimental_v4/brain-update/references/templates.md`
- Delete: `skills/experimental_v4/domain-modeling/`

**Interfaces:**
- Consumes: the baseline failures from Task 3. Each one must be addressed by a specific line in SKILL.md.
- Produces: the skill name `brain-update`, invoked by later tasks' skills through the invocation sentence.

- [ ] **Step 1: Write the SKILL.md frontmatter, exactly:**

```yaml
---
name: brain-update
description: Use when a project has no .brain/ folder and the user wants one set up, when another skill finishes work that changed project knowledge, or when the user asks to sync, update, or rebuild the project brain.
---
```

- [ ] **Step 2: Write the SKILL.md body.** Use these sections, in order. Each one implements the design section named.
  1. Purpose. Ownership: `brain-update` owns the root files and `adrs/`. ("Who writes what")
  2. Locating the brain and choosing a mode. ("Reading the brain" locating rules; "Mode selection")
  3. First run, steps 1–6. ("First run")
  4. Update, steps 1–8. ("Update")
  5. Authority rules. ("Authority rules")
  6. Root files: a one-line purpose per file and the size limits, linking to `references/templates.md`. ("Layout", "Root files", "Size limits")
  7. ADRs: the three criteria, numbering, and supersession, carried over from v3 `domain-modeling` §5. Glossary rules come from `domain-modeling` §2–3, with the `CONTEXT.md` mechanics dropped.
  8. Report.

  It must state:
  - Never dispatch subagents unless the user asks.
  - Never commit.
  - Ask one question at a time.

  Target: 1,600 words or fewer (`wc -w`).
- [ ] **Step 3: Write `references/templates.md`:**
  - **Templates** for `00_index.md` (with the exact header lines), `09_user_decisions.md` entries, `glossary.md` entries, `open_questions.md` entries, `spikes.md` entries, `state.md`, and an ADR. The ADR template comes from v3 `domain-modeling` §5.
  - **Placement rule** for an optional `NN_<topic>.md` root file.
- [ ] **Step 4: Delete `domain-modeling/`.** Verify: `grep -rn 'domain-modeling\|CONTEXT-MAP\|CONTEXT\.md' skills/experimental_v4/brain-update`. Expected: matches only in the first-run migration list.
- [ ] **Step 5: Run S1–S3 with the skill** in `.runs/S<n>-skill`, then check every criterion. Expected: all pass.
- [ ] **Step 6:** If any criterion fails, add an explicit counter in SKILL.md quoting the agent's rationalization, and rerun that scenario until it passes. Record the results in `scenarios.md`.
- [ ] **Step 7: Commit:** `git add skills/experimental_v4 docs/superpowers && git commit -m "Add brain-update skill"`

---

### Task 5: REFACTOR: Review Focus scenarios S4–S7

**Files:**
- Modify: `skills/experimental_v4/tests/scenarios.md` (S4–S7)
- Modify: `skills/experimental_v4/brain-update/SKILL.md` (only to fix failures)

Each scenario uses the skill wrapper.

- [ ] **Step 1: Add S4–S7 to `scenarios.md`:**
  - **S4: Worktree.** Fixture: `synced`. Run `git -C <fixture> worktree add <fixture>-wt -b wt`, then in `-wt` commit a `--version` flag in `crate/cli.py`. Run from `<fixture>-wt`. Trigger: user says `/brain-update`. Pass criteria:
    - there's no `.brain/` in `-wt`;
    - the main fixture's `.brain/02_features.md` mentions `--version`.
  - **S5: Missing sync commit.** Fixture: `synced`, with `Last synced` replaced by `deadbeefdeadbeefdeadbeefdeadbeefdeadbeef`. Trigger: user says `/brain-update`. Pass criteria:
    - the reply says the recorded commit is missing and that it re-verified the root files;
    - S2's `cue_points` and `cue add` criteria pass;
    - `Last synced` = HEAD.
  - **S6: Oversized root file.** Fixture: `synced`. Append to `.brain/02_features.md` until `wc -w` > 4,500, including the unique line `SENTINEL-FEATURE-DETAIL`. Trigger: user says `/brain-update`. Pass criteria:
    - `02_features.md` is ≤ 4,000 words and links into `.brain/02_features/`;
    - `grep -r SENTINEL-FEATURE-DETAIL .brain/02_features/` matches.
  - **S7: Partial folder.** Fixture: `partial`. Trigger: user says `/brain-update`. Turn 1 pass criteria:
    - it asks the git-tracking question;
    - `.brain/specs/01-bpm-filter.md` is unchanged;
    - no root files exist yet.
- [ ] **Step 2: Run S4–S7.** Expected: all pass. Fix any failure in SKILL.md with an explicit counter, rerun the failing scenario, then rerun S1–S3 to confirm nothing regressed.
- [ ] **Step 3: Commit:** `git add skills/experimental_v4 docs/superpowers && git commit -m "Cover brain-update edge cases"`

---

### Task 6: Producer skills write to .brain

**Files** (all under `skills/experimental_v4/`):
- Modify: `brain-write-spec/SKILL.md`, `brain-write-tickets/SKILL.md`, `brain-plan-feature/SKILL.md`, `brain-implement/SKILL.md`, `brain-implement/references/todo-template.md`, `brain-diagnose/SKILL.md`
- Delete: `brain-implement/references/guidance-template.md`

**Interfaces:**
- Consumes: `brain-update` (Task 4), the preamble, and the invocation sentence (Global Constraints).
- Produces: paths that Task 7's readers rely on. Specs are `.brain/specs/NN-<slug>.md`. Impl plans are `.brain/impl_plans/<spec-stem or feature-slug>.md`, with a `Review base:` line.

- [ ] **Step 1: Apply the edits**

| File | Edit |
|---|---|
| all six SKILL.md | Insert the preamble after the H1. Replace `CONTEXT-MAP.md` / `CONTEXT.md` reads with `.brain/glossary.md` and `.brain/03_architecture.md`. Replace `docs/adr/` with `.brain/adrs/`. |
| `brain-write-spec` | §4: `docs/specs/<NN>-<short-slug>.md` → `.brain/specs/<NN>-<short-slug>.md`. Use glossary terms. Add the invocation sentence after the file is written. The Boundaries section mentions `brain-implement`'s impl plan. |
| `brain-write-tickets` | §6: `docs/tickets/<feature-slug>/issues/<NN>-<slug>.md` → `.brain/tickets/<feature-slug>/<NN>-<slug>.md`. The template's spec path becomes `.brain/specs/<NN>-<slug>.md`. Add the invocation sentence after the tickets are written. |
| `brain-plan-feature` | `docs/planning/<feature-stub>/` → `.brain/planning/<feature-stub>/`, including the description. "Do not create `docs/implementation/`" → "Do not create `.brain/impl_plans/` entries". Add the invocation sentence after "After resolving a ticket" step 4. |
| `brain-implement` | §2: the workspace becomes one file, `.brain/impl_plans/<spec-file-stem>.md` (or `<ticket-feature-slug>.md` / `<task-stub>.md`), replacing the `docs/implementation/<…>/` folder. Remove every `guidance.md` mention. Discoveries go to the root files through `brain-update`. Rename `todo.md` mentions to "the impl plan". Add the invocation sentence at the end of §6 (session end) and at the end of §7 (completion). |
| `brain-implement/references/todo-template.md` | Retitle it "Impl plan template". Use paths `.brain/specs/014-external-communication.md` and `.brain/tickets/external-communication/`. |
| `brain-diagnose` | §5: `docs/diagnoses/` → `.brain/diagnoses/`. Add the invocation sentence at the end of §4 (after a verified fix). Replace `CONTEXT.md` in §1 with `.brain` root files. |

- [ ] **Step 2: Static check**

```bash
cd skills/experimental_v4
grep -rnE 'docs/|CONTEXT(-MAP)?\.md|guidance\.md|todo\.md' brain-write-spec brain-write-tickets brain-plan-feature brain-implement brain-diagnose
for f in brain-write-spec brain-write-tickets brain-plan-feature brain-implement brain-diagnose; do grep -q 'Project brain:' $f/SKILL.md || echo "NO PREAMBLE $f"; grep -q 'invoke `brain-update`' $f/SKILL.md || echo "NO INVOKE $f"; done
```

Expected: no output.

- [ ] **Step 3: Add and run S8.**
  - **S8: brain-write-spec.** Fixture: `synced`. Skill: `brain-write-spec`, which mentions `brain-update` at `<ABS>/brain-update/`. Context: an approved direction summary for cue points, in the `brain-brainstorm` §7 format. Decisions: seconds as floats; `cue add <track> <seconds>`; at most 8 cues per track, where a 9th cue is rejected with a non-zero exit. Trigger: user says `/brain-write-spec`.
  - **Pass criteria:**
    - `.brain/specs/02-cue-points.md` exists, with an Examples section that includes the 9th-cue rejection;
    - no `docs/` directory is created;
    - `00_index.md` lists `specs/02-cue-points.md`;
    - `state.md` lists cue points as planned.

  Expected: pass.
- [ ] **Step 4: Commit:** `git add skills/experimental_v4 docs/superpowers && git commit -m "Point producer skills at .brain"`

---

### Task 7: Reader skills use .brain

**Files** (under `skills/experimental_v4/`):
- Modify: `brain-brainstorm/SKILL.md`, `brain-brainstorm/lenses/architecture.md`, `brain-review-code/SKILL.md`, `brain-review-architecture/SKILL.md`, `brain-review-security/SKILL.md`, `brain-review-merge-request/SKILL.md`, `brain-refine-backlog/SKILL.md`

- [ ] **Step 1: Apply the edits**

| File | Edit |
|---|---|
| every SKILL.md listed | Insert the preamble after the H1. In `brain-refine-backlog`, it goes after the H1 and before `Invocation arguments`. |
| `brain-brainstorm` | §1: `` `CONTEXT.md`, and ADRs `` → `` `.brain` root files and `.brain/adrs/` ``. §7: after "Ask the user to confirm the direction…", add the invocation sentence, to run once the direction is confirmed. |
| `brain-brainstorm/lenses/architecture.md` | `ADRs` → `ADRs in .brain/adrs/`. |
| `brain-review-code` | §1 item 2: `` `Review base` in a `todo.md` `` → `` `Review base` in the impl plan (`.brain/impl_plans/`) ``. §2 item 3: `` under `docs/` or `specs/` `` → `` under `.brain/specs/` ``. Line 44: `` `CONTEXT-MAP.md` / `CONTEXT.md`, and relevant ADRs `` → `` `.brain/glossary.md`, `.brain/03_architecture.md`, and relevant ADRs in `.brain/adrs/` ``. |
| `brain-review-architecture` | Line 19: use the same replacement as review-code line 44. Output: `docs/reviews/architecture/<NN>-<short-slug>-review.md` → `.brain/reviews/architecture/<NN>-<short-slug>.md`. After the saved-record sentence, add the invocation sentence, applying only when a record was saved. |
| `brain-review-security` | Output: `docs/security/<NN>-<short-slug>-review.md` → `.brain/reviews/security/<NN>-<short-slug>.md`. Add the invocation sentence the same way as review-architecture. "domain records" → "`.brain` root files". |
| `brain-review-merge-request` | Requirement source 3: "domain records" → "`.brain` root files". |

- [ ] **Step 2: Static check (whole tree except README)**

```bash
cd skills/experimental_v4
grep -rnE 'docs/|CONTEXT(-MAP)?\.md|todo\.md|guidance\.md' --include='*.md' . | grep -vE '^\./(README\.md|tests/|brain-update/)'
for d in brain-*/; do d=${d%/}; [ "$d" = brain-distill-content ] || [ "$d" = brain-update ] || grep -q 'Project brain:' $d/SKILL.md || echo "NO PREAMBLE $d"; done
```

Expected: no output.

- [ ] **Step 3: Add and run S9.**
  - **S9: brain-implement resume.** Fixture: `synced`. Skill: `brain-implement`. Trigger: user says `/brain-implement resume the BPM filter work. Stop after you report the next work item and the files you read.`
  - **Pass criteria:**
    - every root `.md` is read once;
    - `.brain/impl_plans/01-bpm-filter.md` and `.brain/specs/01-bpm-filter.md` are read;
    - nothing under `.brain/reviews/` is read;
    - the review base reported equals commit A;
    - the next item is the E2 upper bound;
    - no `CONTEXT.md` or `docs/` reads are attempted.

  Expected: pass.
- [ ] **Step 4: Commit:** `git add skills/experimental_v4 docs/superpowers && git commit -m "Point reader skills at .brain"`

---

### Task 8: CLAUDE.md and README.md

**Files:**
- Modify: `skills/experimental_v4/CLAUDE.md`
- Modify: `skills/experimental_v4/README.md`

- [ ] **Step 1: `CLAUDE.md`.**
  - **Line 3:** replace "repository-specific guidance, specifications, and ADRs" with "repository-specific guidance and the project brain (`.brain/`: specifications, ADRs, and project knowledge)".
  - **Line 49:** replace the durable-docs bullet with two bullets:
    1. `.brain/` is the project's single document store. `brain-update` owns its root files and `adrs/`; other skills write only their own documents into its subfolders, then invoke `brain-update`.
    2. Reviews and diagnoses are delivered in the conversation unless the user requests a saved record.
  - **Line 51:** replace the `todo.md` bullet. It should say impl plans in `.brain/impl_plans/` and the `.brain` root files are continuity aids that summarize other sources, never authorities over specs, ADRs, or user decisions. Verify them against the code.
- [ ] **Step 2: `README.md`.** Rewrite these parts:
  - **Title paragraph:** 13 skills plus `.brain`.
  - **Install tree:** v4 names and the `tests/` note. Remove the `review-code` findings note's old name.
  - **New `.brain` section:** the design's layout block, plus three sentences on reading once per session, `brain-update` ownership, and default-untracked.
  - **Skills table:** v4 names; drop `domain-modeling` and `handoff`; add the `brain-update` row with the output "`.brain/` root files and ADRs".
  - **Every workflow and slash command:** v4 names.
  - **"Resuming implementation across sessions":** the `.brain` tree, with `impl_plans/<feature>.md`.
  - **"Changes from experimental_v2" → "Changes from experimental_v3":** bullets for the rename, `.brain`, `brain-update`, the removed skills, and the path moves.
- [ ] **Step 3: Static check**

```bash
cd skills/experimental_v4
grep -nE 'docs/|CONTEXT(-MAP)?\.md|todo\.md|guidance\.md|domain-modeling|handoff|experimental_v2' CLAUDE.md README.md
grep -nE '`/?(brainstorm|diagnose|distill-content|implement|plan-feature|refine-backlog|review-architecture|review-code|review-merge-request|review-security|write-spec|write-tickets)`' CLAUDE.md README.md
```

Expected:
- First command: matches only in the "Changes from experimental_v3" section, which names the removed skills and old paths.
- Second command: no output.

- [ ] **Step 4: Commit:** `git add skills/experimental_v4 docs/superpowers && git commit -m "Document .brain in v4 CLAUDE.md and README"`

---

### Task 9: Final sweep and copy back

- [ ] **Step 1:** Rerun all of S1–S9 with the final skills. Expected: all pass. Record the results in `scenarios.md`.
- [ ] **Step 2: Verify v3 is untouched.** Run `diff -rq /Users/wmbp/repos/ai/collection/skills/experimental_v3 skills/experimental_v3`. Expected: no output.
- [ ] **Step 3: Clean up and commit.** Delete `skills/experimental_v4/tests/.runs/`, then commit: `git add skills/experimental_v4 docs/superpowers && git commit -m "Final brain-update verification"`.
- [ ] **Step 4: Copy back to the main checkout.** Copy `skills/experimental_v4/`, `docs/superpowers/specs/2026-11-03-brain-update-design.md`, and `docs/superpowers/plans/2026-11-03-brain-update.md` into `/Users/wmbp/repos/ai/collection/` at the same relative paths. Do this only after confirming none of those paths already exist there.
