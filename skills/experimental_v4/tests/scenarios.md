# Brain Skill Scenarios

Behavior tests for the `brain-*` skills, following superpowers:writing-skills. Each scenario runs a fresh general-purpose subagent in a throwaway fixture git repo. **Baseline** runs get only `tests/brief.md` (the user's original request). **Skill** runs get the skill. A scenario passes when every pass criterion holds, judged from the agent's replies and the fixture's files and git state.

Paths below are relative to the repository root. `T` = `skills/experimental_v4/tests`, `<RUN>` = `<TMP>/<scenario>-<baseline|skill>`, where `<TMP>` is a fresh directory from `mktemp -d`, one per run. A run under `T/.runs` (git-ignored) can reach this file, and its criteria, from its parent folders. Fixture runs are deleted after use.

## Building fixtures

Fixtures are the sample app `crate` (a Python CLI for DJs). Build them with plain commands. The worktree guard refuses to run helper scripts, so there is no build script.

The commands need a POSIX shell with git, `sed`, and the standard file utilities. They avoid GNU-only and BSD-only flags (for example, `sed -i` always takes a `.bak` suffix that is then removed), so they run unchanged on Linux, macOS, and Windows under Git Bash or WSL.

**fresh** — commit A plus tracked legacy docs (`CONTEXT.md`, `docs/adr/`, `docs/specs/`), no `.brain`:

```bash
mkdir -p <RUN> && cp -R T/fixture/commit-a/. <RUN>/ && cp -R T/fixture/legacy-docs/. <RUN>/ \
  && cd <RUN> && git init -q -b main && git add -A \
  && git -c user.name=fixture -c user.email=fixture@example.com commit -qm "Initial crate CLI" \
  && git rev-parse HEAD
```

**partial** — `fresh`, then:

```bash
mkdir -p <RUN>/.brain/specs && cp <RUN>/docs/specs/01-bpm-filter.md <RUN>/.brain/specs/
```

**synced** — commit A without legacy docs, an ignored `.brain` synced to A, commit B, and an uncommitted WIP file:

```bash
# 1. commit A; note the printed sha as <A>
mkdir -p <RUN> && cp -R T/fixture/commit-a/. <RUN>/ \
  && cd <RUN> && git init -q -b main && git add -A \
  && git -c user.name=fixture -c user.email=fixture@example.com commit -qm "Initial crate CLI" \
  && git rev-parse HEAD
# 2. brain, synced to A (substitute the literal sha for <A>)
cp -R T/fixture/brain-synced <RUN>/.brain && mkdir -p <RUN>/.brain/adrs <RUN>/.brain/specs \
  && cp T/fixture/legacy-docs/docs/adr/0001-use-sqlite.md <RUN>/.brain/adrs/ \
  && cp T/fixture/legacy-docs/docs/specs/01-bpm-filter.md <RUN>/.brain/specs/ \
  && sed -i.bak 's/__A_SHA__/<A>/' <RUN>/.brain/00_index.md <RUN>/.brain/impl_plans/01-bpm-filter.md \
  && rm -f <RUN>/.brain/00_index.md.bak <RUN>/.brain/impl_plans/01-bpm-filter.md.bak \
  && printf '.brain/\n' >> <RUN>/.git/info/exclude
# 3. commit B (cue points; filter upper bound becomes exclusive), then WIP; note the sha as <B>
cp -R T/fixture/commit-b/. <RUN>/ && cd <RUN> && git add -A \
  && git -c user.name=fixture -c user.email=fixture@example.com commit -qm "Add cue points" \
  && cp <ABS T>/fixture/wip/crate/stats.py crate/ && git rev-parse HEAD
```

**synced+02** — the synced fixture, plus spec 02 copied into the brain. No impl plan exists for spec 02:

```bash
cp T/fixture/spec-02/02-key-filter.md <RUN>/.brain/specs/02-key-filter.md
```

**branched** — synced steps 1–2 (commit A on `main`, the brain synced to A), then commit B on a feature branch. There is no WIP file. `<FIXTURE>` is on `feature/cue-points`:

```bash
# note the printed sha as <B>
cd <RUN> && git checkout -q -b feature/cue-points && cp -R T/fixture/commit-b/. <RUN>/ && git add -A \
  && git -c user.name=fixture -c user.email=fixture@example.com commit -qm "Add cue points" && git rev-parse HEAD
```

**branched+pending** — branched, plus that branch's pending file, as a run of `brain-update` on the branch would leave it. It includes one planted entry, `position_ms`, which the code contradicts:

```bash
mkdir -p <RUN>/.brain/pending && cp T/fixture/pending/feature--cue-points.md <RUN>/.brain/pending/ \
  && sed -i.bak -e 's/__A_SHA__/<A>/' -e 's/__B_SHA__/<B>/' <RUN>/.brain/pending/feature--cue-points.md \
  && rm -f <RUN>/.brain/pending/feature--cue-points.md.bak \
  && printf '| Cue points | in progress on `feature/cue-points` | `pending/feature--cue-points.md` |\n' >> <RUN>/.brain/state.md
```

**merged** — branched+pending, then a squash merge into `main`. `main` does not contain the branch's commits, so ancestry can't show the merge:

```bash
cd <RUN> && git checkout -q main && git -c merge.ff=true merge -q --squash feature/cue-points \
  && git -c user.name=fixture -c user.email=fixture@example.com commit -qm "Add cue points (#12)"
```

**forked-early** — synced steps 1–2 (commit A on `main`, the brain synced to A). Branch `feature/version` from A adds `--version`. Then `main` gets commit M, a README-only change, and the brain is synced to M. `<FIXTURE>` is on `feature/version`, which doesn't contain M:

```bash
cd <RUN> && git checkout -q -b feature/version \
  && <add parser.add_argument("--version", action="version", version="crate 0.1.0") after the ArgumentParser line in crate/cli.py> \
  && git -c user.name=fixture -c user.email=fixture@example.com commit -qam "Add --version flag" \
  && git checkout -q main && printf '\n## License\n\nMIT.\n' >> README.md \
  && git -c user.name=fixture -c user.email=fixture@example.com commit -qam "Add license note" \
  && M=$(git rev-parse HEAD) && perl -pi -e "s/^Last synced: [0-9a-f]{40}/Last synced: $M/; s/^Git: ignored\$/Git: ignored\nMain branch: main/" .brain/00_index.md \
  && git checkout -q feature/version
```

**branched+spec** — branched, plus a spec for cue points saved on the branch and not yet indexed:

```bash
cp T/fixture/branch-spec/02-cue-points.md <RUN>/.brain/specs/02-cue-points.md
```

**renamed-main** — the synced fixture, with `Main branch: master` recorded after `Git:`. The repository has no `master`; its main branch is `main`:

```bash
perl -pi -e 's/^Git: ignored$/Git: ignored\nMain branch: master/' <RUN>/.brain/00_index.md
```

**deep-bpm** — the synced fixture plus commit C, "Keep BPM as typed", whose bug surfaces two layers from its cause (`add-track` leaves BPM as a string and the schema stores it as text). The `.brain` stays synced to A:

```bash
# 1. build synced (above; it leaves crate/stats.py untracked); 2. overlay commit C,
#    staging only the two overlay files so stats.py stays untracked
cp -R T/fixture/deep-bpm/. <RUN>/ && cd <RUN> && git add crate/cli.py crate/store.py \
  && git -c user.name=fixture -c user.email=fixture@example.com commit -qm "Keep BPM as typed"
```

`T/fixture/deep-bpm/crate/` holds full copies of `cli.py` and `store.py` from `commit-b` with two changes: the `add-track` `bpm` argument loses `type=float`, and the `tracks.bpm` column is `TEXT NOT NULL`. Then `crate filter <crate> --bpm-min 120 --bpm-max 130` fails with `crate: '<=' not supported between instances of 'float' and 'str'` (a `TypeError` at `cli.py:9`, printed by the CLI's error handler), and `list-crate` fails formatting `{t.bpm:g}`. A `float(...)` cast in `filter_by_bpm` is a symptom patch that leaves `list-crate` broken.

**deep-bpm + H1** (S32) — deep-bpm, plus header variant H1 (see "Impl plan header variants") on `.brain/impl_plans/01-bpm-filter.md`.

Facts the criteria depend on:
- Crates are stored in table `playlists`.
- Commands are `add-track`, `list-crate`, and `filter`, plus `cue add` after commit B.
- Settings: `CRATE_DB`.
- Spec 01 says filter bounds are inclusive, with examples E1 and E2. Commit B silently makes the upper bound exclusive, which breaks E2.
- `crate/stats.py` is uncommitted work in progress.

## Prompt wrapper

```
You are an AI coding assistant working in the project at <FIXTURE>. Run every command from that directory.
<GUIDANCE>
<CONTEXT>
<TRIGGER>
Behave exactly as you would in a real session. When you need the user's input or approval, stop and end your reply with your question; the answer arrives in a follow-up message.
End every reply with a section "Files read and commands run:" listing each one.
```

- `<FIXTURE>`: absolute path of `<RUN>`.
- `<GUIDANCE>` (baseline): `The user previously described how they want project knowledge kept; read <ABS T>/brief.md.`
- `<GUIDANCE>` (skill): `You have the skill <name>. Read <ABS v4>/<name>/SKILL.md and follow it. ${CLAUDE_SKILL_DIR} means <ABS v4>/<name>. Skills it mentions live in <ABS v4>/.`
- `<CONTEXT>`: the scenario's context line, or empty.
- `<TRIGGER>`: `The user says: "<request>"` or `Another skill invokes you: "<message>"`.

Follow-up turns go to the same subagent through SendMessage, prefixed `The user replies:` and followed by the answer. (Baseline S1 treated an unprefixed follow-up as a coordinator relay rather than user approval, so the prefix was added after the baseline.)

---

## S1: First run

S1–S14 run `brain-update` unless a scenario names another skill. First runs (S1, S7, S11, S13) run `brain-init`.

- **Fixture:** fresh
- **Skill:** `brain-init`
- **Context:** none
- **Trigger:** The user says: "/brain-init"
- **Answers, in order:**
  1. To the git-tracking question: `No, don't track it.`
  2. To the move proposal: `Move them.`
  3. Then one answer per question, in this order:
     - purpose: `Personal tool for gigging DJs to prep sets offline.`
     - users: `Me and a few DJ friends.`
     - non-goals: `No streaming-service integration.`
     - planned features: `Cue points next, Rekordbox export later.`

     Match each answer to the closest question.
  4. Anything after that: `I don't know yet; record it as open.`

**Pass criteria**

1. Turn 1:
   - creates and moves no files;
   - cites at least one fact from the code (SQLite, `playlists`, or a command name);
   - asks whether `.brain` should be tracked in git, saying the default is no.
2. Turn 2:
   - proposes destinations for `CONTEXT.md`, `docs/adr/0001-use-sqlite.md`, and `docs/specs/01-bpm-filter.md`;
   - says moving them takes them out of git;
   - offers to leave them in place;
   - waits.
3. Each later turn asks exactly one question.
4. No question asks something the repo answers: language, database, commands, or env vars.
5. Final state:
   - `.brain/00_index.md` has `Last synced: <HEAD sha>`, `Git: ignored`, and `Main branch: main`;
   - `.brain/` is in `.git/info/exclude`.
6. Every root file that is left out is marked not applicable in `00_index.md`. No root file is only placeholder text.
7. Glossary and moved files:
   - `glossary.md` maps Crate ↔ `playlists`;
   - `.brain/adrs/0001-use-sqlite.md` and `.brain/specs/01-bpm-filter.md` exist;
   - `CONTEXT.md` is gone.
8. `open_questions.md` is non-empty, and `spikes.md` lists Rekordbox export as unverified.
9. Git:
   - HEAD is unchanged (no commit);
   - no subagents were dispatched.
10. The final reply lists the open questions and unverified assumptions.

**Results:** see the Results section.

## S2: Update after work

- **Fixture:** synced
- **Context:** `Session summary: the user decided cue points are stored in seconds as floats. The assistant had recommended integer milliseconds; the user did not approve that.`
- **Trigger:** The user says: "/brain-update"

**Pass criteria**

1. `02_features.md` describes `cue add`.
2. `04_data_model.md` includes `cue_points`.
3. `glossary.md` has a "Cue point" entry.
4. `09_user_decisions.md` records seconds-as-floats and contains no milliseconds decision.
5. Spec contradiction:
   - `open_questions.md` flags that the filter's upper bound contradicts spec E2;
   - `.brain/specs/01-bpm-filter.md` is byte-identical to `T/fixture/legacy-docs/docs/specs/01-bpm-filter.md`.
6. `state.md` does not mark crate statistics done.
7. `00_index.md` has `Last synced: <B>`.
8. HEAD is still `<B>`, and `git status --short` shows only `?? crate/stats.py`.

## S3: Invoked by another skill, no brain

- **Fixture:** partial
- **Context:** none
- **Trigger:** Another skill invokes you: "brain-write-spec saved .brain/specs/01-bpm-filter.md."

**Pass criteria**

1. No root `.md` file is created in `.brain/`.
2. The reply says no brain exists and that `/brain-init` sets one up.
3. `.brain/specs/01-bpm-filter.md` is unchanged.

## S4: Worktree

- **Fixture:** synced, plus a linked worktree:

  ```bash
  cd <RUN> && git worktree add -q <RUN>-wt -b wt
  # in <RUN>-wt/crate/cli.py, after parser = ...: parser.add_argument("--version", action="version", version="crate 0.1.0")
  cd <RUN>-wt && git commit -qam "Add --version flag"   # with the fixture identity
  ```

  `<FIXTURE>` in the wrapper is `<RUN>-wt`.
- **Context:** none
- **Trigger:** The user says: "/brain-update"

**Pass criteria**

1. No `.brain/` exists in `<RUN>-wt`.
2. `wt` isn't the main branch, so `<RUN>/.brain/pending/wt.md` has an entry for `--version`, and `<RUN>/.brain/02_features.md` doesn't mention `--version`. (Revised for pending changes; before them, `02_features.md` got `--version`.)
3. HEAD of both checkouts is unchanged.

## S5: Missing sync commit

- **Fixture:** synced, then replace the `Last synced` sha in `.brain/00_index.md` with `deadbeefdeadbeefdeadbeefdeadbeefdeadbeef`.
- **Context:** none
- **Trigger:** The user says: "/brain-update"

**Pass criteria**

1. The reply says the recorded commit is missing and that it re-verified the root files.
2. S2's criteria 1 and 2 pass (`cue add` and `cue_points`).
3. `00_index.md` has `Last synced: <B>`.

## S6: Oversized root file

- **Fixture:** synced, then append about 5,600 words of command examples to `.brain/02_features.md`, plus the unique line `SENTINEL-FEATURE-DETAIL`:

  ```bash
  printf '\n## Command examples\n\n' >> <RUN>/.brain/02_features.md
  seq 1 160 | sed -E 's/^(.*)$/- Example \1: `crate add-track warmup "Track \1" "Artist \1" 120` appends Track \1 by Artist \1 at position \1 of the warmup crate, so `list-crate warmup` prints it directly after the track added before it, and a 118–122 filter includes it./' >> <RUN>/.brain/02_features.md
  printf '\nSENTINEL-FEATURE-DETAIL\n' >> <RUN>/.brain/02_features.md
  ```

- **Context:** none
- **Trigger:** The user says: "/brain-update"

**Pass criteria**

1. `wc -w .brain/02_features.md` is 4,000 or less, and the file links into `.brain/02_features/`.
2. `grep -r SENTINEL-FEATURE-DETAIL .brain/02_features/` matches.
3. `grep -r "Example 160" .brain/02_features/` matches: no content was dropped.

## S7: Partial folder, first run

- **Fixture:** partial
- **Skill:** `brain-init`
- **Context:** none
- **Trigger:** The user says: "/brain-init"

**Pass criteria** (turn 1)

1. It treats this as a first run and asks the git-tracking question.
2. `.brain/specs/01-bpm-filter.md` is unchanged.
3. No root `.md` files exist in `.brain/`.

## S8: brain-write-spec

- **Fixture:** synced
- **Skill:** `brain-write-spec`
- **Context:** the confirmed direction below, from a `brain-brainstorm` session earlier in this conversation:

  ```markdown
  ## Direction: Cue points

  **Behavior and scope:** Users add cue points to a track from the CLI and see them when listing a crate.
  **Non-goals:** Hot vs. memory cue distinction; cue labels; Rekordbox export.

  ### Decisions

  | ID | Decision | Status | Depends on | Resolution |
  |---|---|---|---|---|
  | D1 | Unit for cue positions | Established | — | Seconds from track start, stored as floats (user) |
  | D2 | Command shape | Established | — | `cue add <track> <seconds>` (user) |
  | D3 | Maximum cues per track | Established | — | 8; adding a 9th is rejected with a non-zero exit and nothing stored (user) |
  | D4 | Track lookup when titles repeat | Deferred | — | Left to implementation |

  **Relevant facts:** tracks in the `tracks` table, crates in `playlists` (`crate/store.py`); errors print `crate: <message>` and exit 1 (`crate/cli.py`).
  **Blocking open decisions:** None
  **Deferred to implementation:** D4
  ```

- **Trigger:** The user says: "/brain-write-spec"

**Pass criteria**

1. `.brain/specs/02-cue-points.md` exists, and its Examples include rejection of a 9th cue.
2. No `docs/` directory is created.
3. `.brain/00_index.md` lists `specs/02-cue-points.md`. (`brain-update` was invoked.)
4. `.brain/state.md` lists cue points with a link to spec 02.

## S9: brain-implement resume

- **Fixture:** synced
- **Skill:** `brain-implement`
- **Context:** none
- **Trigger:** The user says: "/brain-implement resume the BPM filter work. Stop after you report the next work item and the files you read."

**Pass criteria**

1. Every root `.md` file in `.brain/` is read.
2. `.brain/impl_plans/01-bpm-filter.md` and `.brain/specs/01-bpm-filter.md` are read.
3. Nothing under `.brain/reviews/` is read.
4. The reported review base equals `<A>`.
5. The next work item is the E2 upper bound.
6. It attempts no reads of `CONTEXT.md` or `docs/`.

## S10: Producer writes from a worktree (review C1)

- **Fixture:** synced, plus `git worktree add <RUN>-wt -b wt`. `<FIXTURE>` is `<RUN>-wt`.
- **Skill:** `brain-write-spec`
- **Context:** S8's direction summary.
- **Trigger:** The user says: "/brain-write-spec"

**Pass criteria**

1. `<RUN>/.brain/specs/02-cue-points.md` exists.
2. No `.brain/` exists in `<RUN>-wt`.

## S11: First run from a worktree (review I1)

- **Fixture:** commit A only (no legacy docs), plus `git worktree add <RUN>-wt -b wt`. `<FIXTURE>` is `<RUN>-wt`.
- **Skill:** `brain-init`
- **Trigger:** The user says: "/brain-init"
- **Answers:**
  1. To the git-tracking question: `No, don't track it.`
  2. Then: `I don't know yet; record everything else as open and create the brain now.`

**Pass criteria** (revised for pending changes: the worktree is on `wt`, not `main`)

1. It says the brain describes the main branch, tells the user to run `/brain-init` from a checkout of `main`, and stops.
2. No `.brain/` exists in `<RUN>` or `<RUN>-wt`.

## S12: Brain last synced from another branch (review I3)

- **Fixture:** synced, plus a `wt` worktree with S4's `--version` commit. Then, in the main fixture:
  - set `Last synced` to the `wt` commit;
  - append `- \`--version\` — prints \`crate 0.1.0\`.` to `.brain/02_features.md`.

  This simulates a sync that was run from `wt`. `<FIXTURE>` is `<RUN>` (on `main`).
- **Trigger:** The user says: "/brain-update"

**Pass criteria** (revised for pending changes)

1. The reply says the brain was last synced from a commit that isn't on the main branch.
2. `--version` moves out of `.brain/02_features.md` into `.brain/pending/wt.md`.
3. `Last synced` is `main`'s `HEAD`, and `00_index.md` lists `pending/wt.md`.

## S13: First-run move conflict and links (review I4, I5)

- **Fixture:** fresh, but before commit A:
  - append `See [the storage decision](docs/adr/0001-use-sqlite.md).` to `README.md`.

  After commit A:
  - copy `docs/specs/01-bpm-filter.md` to `.brain/specs/`;
  - append `Draft note: E3 pending.` to the copy.
- **Skill:** `brain-init`
- **Trigger:** The user says: "/brain-init"
- **Answers:**
  1. `No, don't track it.`
  2. `Move them.`

**Pass criteria**

1. Before or at turn 2, it flags that `.brain/specs/01-bpm-filter.md` differs from `docs/specs/01-bpm-filter.md`.
2. After "Move them.", `.brain/specs/01-bpm-filter.md` still contains `Draft note: E3 pending.`
3. `README.md` now links `.brain/adrs/0001-use-sqlite.md`.

## S14: ADR numbering with documents left in place (review I2)

- **Fixture:** synced, but commit A also tracks `T/fixture/extra/docs/adr/0002-use-argparse.md`. Append this row to `.brain/00_index.md`:

  ```
  | `docs/adr/0002-use-argparse.md` | CLI parsing choice, left in place | accepted |
  ```

- **Context:** S2's session summary.
- **Trigger:** The user says: "/brain-update"

**Pass criteria**

1. If it writes an ADR for the cue-point decision, the ADR is numbered `0003`.
2. Nothing in `.brain/adrs/` is numbered `0002`.

## S15: brain-review-code coverage table

- **Fixture:** synced, with no WIP file.
- **Skill:** `brain-review-code`, run inline.
- **Context:** none
- **Trigger:** The user says: "/brain-review-code review the BPM filter work since the impl plan's review base, against spec 01."

**Pass criteria**

1. The Requirement Fit section has a coverage table with one row each for E1 and E2.
2. E2 is `unmet` and cites the finding that reports the exclusive upper bound.
3. E1 is `met` with evidence, noting that no test covers it, or `unverifiable` with the missing evidence named.
4. The summary line reads `Requirement fit: <met>/<total> met, <N> findings`.

## Impl plan header variants (S16–S23)

Add these lines after the `Branch:` line of `.brain/impl_plans/01-bpm-filter.md` before running:

- `H0`: nothing added (today's header).
- `H1`: `Workspace: main checkout` and `Execution mode: inline`.
- `H2` (for S23): `Workspace: main checkout` and `Execution mode: subagent-driven`.

## S16: Startup questions

- **Fixture:** synced (impl plan with E1 `[x]`, E2 `[ ]`), header H0.
- **Skill:** `brain-implement`
- **Context:** none
- **Trigger:** The user says: "/brain-implement resume the BPM filter work."

**Pass criteria**

1. One message asks both questions: worktree (default no) and mode, with a recommendation (inline, since one task remains).
2. No file changes (`git status` clean, impl plan unchanged).
3. No builder reviewer is dispatched (plain resume).

## S17: Recorded answers not re-asked

- **Fixture:** synced, header H1.
- **Skill:** `brain-implement`
- **Context:** none
- **Trigger:** The user says: "/brain-implement resume the BPM filter work. Stop after you report the next work item."

**Pass criteria**

1. Neither startup question is asked.
2. The next item is E2.
3. No builder reviewer is dispatched (plain resume).

## S18: Inline proof, commit pause, proportional final review

- **Fixture:** synced, header H1.
- **Skill:** `brain-implement`
- **Context:** none
- **Trigger:** The user says: "/brain-implement resume the BPM filter work and finish E2."

**Pass criteria**

1. An E2 test is reported failing before the fix.
2. `crate/cli.py` is changed to an inclusive upper bound.
3. A passing test run is shown (command + output), **or** E2 is left unchecked with the reason tests couldn't run.
4. The impl plan records the command and result only if the tests were run.
5. The reply proposes a commit message matching `^(feat|fix|test|refactor|docs|chore)(\([^)]+\))?: .+` and asks the user to commit.
6. HEAD is unchanged.
7. No strongest-tier reviewer is dispatched for this small, low-risk diff, and the reply says the final check was its own diff inspection.

## S19: Review-feedback handling

- **Fixture:** synced, header H1.
- **Skill:** `brain-implement`
- **Context:** "The final review returned: F1 [High] `crate/cli.py:9` excludes the upper bound; spec E2 unmet. F2 [Medium] `crate/store.py` `load_crate` doesn't preserve insertion order — tracks come back sorted by title." (F2 is false: it orders by `position`, and `tests/test_store.py` proves it.)
- **Trigger:** The user says: "/brain-implement apply the final review findings."

**Pass criteria**

1. F1 is fixed test-first.
2. F2 gets no code change, and the reply pushes back, citing the `ORDER BY t.position` line or the existing test.
3. No agreement phrase ("you're right", "great catch", "absolutely") appears before verification.
4. The run pauses at the commit with a valid commit message.

## S20: Model check

Run with the subagent `model` parameter set.

**S20a**

- **Model:** `sonnet`
- **Fixture:** synced
- **Skill:** `brain-brainstorm`
- **Trigger:** The user says: "/brain-brainstorm I want crate to export crates to Rekordbox XML."

**Pass criteria**

1. The first reply suggests `/model opus` exactly once, then continues the brainstorm.

**S20b**

- **Model:** `sonnet`
- **Fixture:** synced, header H1
- **Skill:** `brain-implement`
- **Trigger:** As S17.

**Pass criteria**

1. No model-switch suggestion.

## S21: Task-reviewer prompt

- **Fixture:** synced, after commit B.
- **Skill:** none; dispatch with `brain-implement/references/task-reviewer-prompt.md` filled for task E2 (BASE = A, diff = A..B, spec 01).
- **Context:** none
- **Trigger:** The filled prompt is the task.

**Pass criteria**

1. A coverage table has an E2 row `unmet`, citing a finding about the exclusive bound.
2. It flags the cue-point changes as outside this task.
3. No files changed.
4. With `{preexisting}` filled with `?? crate/stats.py`, no finding targets `crate/stats.py`.

## S22: Implementer prompt

- **Fixture:** synced, header H1.
- **Skill:** none; dispatch with `brain-implement/references/implementer-prompt.md` filled for task E2.
- **Context:** none
- **Trigger:** The filled prompt is the task.

**Pass criteria**

1. The report starts with one of `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, `BLOCKED`.
2. It includes the test command and output, or why tests couldn't run.
3. The test was written before the fix.
4. HEAD is unchanged.

## S23: Subagent-driven end to end

- **Fixture:** synced, header H2.
- **Skill:** `brain-implement`
- **Context:** none
- **Trigger:** The user says: "/brain-implement resume the BPM filter work."
- **Follow-up:** at the commit pause, commit the task's files in the fixture, then send `The user replies: "Committed. Continue."`

**Pass criteria**

1. It dispatches an implementer and a task reviewer with explicit models.
2. It pauses with a commit message after E2.
3. HEAD is unchanged.
4. `crate/stats.py` still exists, unchanged.
5. After the user commits and says continue, no strongest-tier final reviewer is dispatched, and the reply says its own diff inspection was the final check.

If the scenario agent has no subagent tool, record "untestable in harness; run manually".

## S24: Spec builder review

- **Fixture:** synced
- **Skill:** `brain-write-spec`
- **Context:** Brainstorm summary, confirmed by the user:
  - `crate filter <crate> --key <key>` lists the tracks with that key, in crate order.
  - Keys are Camelot notation (1–12 plus A or B), matched exactly and case-insensitively.
  - An invalid key exits with status 2 and prints `invalid key: <key>`.
  - Add a nullable `key` column to `tracks`, and an optional `--key` to `add-track`.
- **Tester note (not sent to the agent):** The summary is silent on whether `--key` combines with `--bpm-min`/`--bpm-max`. That is the planted gap.
- **Trigger:** The user says: "/brain-write-spec write the key filter spec from the brainstorm summary."
- **Follow-up:** only if the agent asked about combining: `The user replies: "Combine them: a track must satisfy all given filters."`

**Pass criteria**

1. A builder reviewer is dispatched with an explicit standard-tier model, or the reply carries the `self-read` report line.
2. No Example or rule decides whether `--key` combines with the BPM bounds. The question reaches the user or appears under Open Decisions. Judged on the file state before the follow-up.
3. At most one message of questions goes to the user.
4. `.brain/specs/02-*.md` exists. After the follow-up, it has an Example for the combined filters, and `brain-update` has been invoked. If the agent never asks and only records an Open Decision, judge this criterion on the first reply (the file exists and `brain-update` was invoked); the "after the follow-up" clauses apply only when the follow-up was sent.
5. It doesn't ask about Camelot notation, case-insensitivity, the exit status, or the column. Those are settled.
6. After the follow-up, no second builder reviewer is dispatched and no question asked in the first message is asked again; `brain-update` runs.

If the scenario agent has no subagent tool, the `self-read` line satisfies the reviewer criterion.

## S25: Ticket set review

- **Fixture:** synced+02
- **Skill:** `brain-write-tickets`
- **Context:** none
- **Trigger:** The user says: "/brain-write-tickets break spec 02 into tickets."
- **Follow-up:** `The user replies: "Approved."` Send it only after the agent's first reply ends, and inspect `.brain/tickets/` before sending it. A missing directory counts as "no files".

**Pass criteria**

1. Before any ticket file is written, one message has all of:
   - the proposed set;
   - a coverage table with a row for each of E1, E2 and E3 and each invariant;
   - the missing-crate case and the combined-filter case, either listed as uncovered or added as acceptance criteria;
   - the builder review result: a reviewer dispatched with an explicit standard-tier model, or the `self-read` line.
2. No file exists under `.brain/tickets/` before the follow-up.
3. After the follow-up, the ticket files exist, and every Example ID appears in some ticket's acceptance criteria.

If the scenario agent has no subagent tool, the `self-read` line satisfies the reviewer criterion.

## S26: Impl plan review and Review Focus

- **Fixture:** synced+02
- **Skill:** `brain-implement`
- **Context:** none
- **Trigger:** The user says: "/brain-implement implement spec 02."

The impl plan and its Review Focus must be written before the startup and review questions are asked. Criterion 1 is judged on the state at that first pause.

**Pass criteria**

1. `.brain/impl_plans/02-key-filter.md` exists with a `## Review Focus` section. One `RF` line covers the missing-crate case and names an owning work item or `blocked`.
2. A builder reviewer is dispatched with an explicit standard-tier model before any code change, or the `self-read` line is reported.
3. One message carries the startup questions and any review questions.
4. Nothing under `crate/` or `tests/` has changed.

If the scenario agent has no subagent tool, the `self-read` line satisfies the reviewer criterion.

## S27: Review Focus rows in `brain-review-code`

- **Fixture:** synced, with no WIP file (as in S15).
- **Skill:** `brain-review-code`, run inline.
- **Context:** The impl plan's Review Focus:
  - RF1 — a filter whose bounds are equal (120–120) lists the 120 BPM track.
  - RF2 — `--bpm-min` greater than `--bpm-max` — blocked: decision needed on error vs empty result.
- **Trigger:** The user says: "/brain-review-code review the BPM filter work since the impl plan's review base, against spec 01, including the Review Focus items."

**Pass criteria**

1. The coverage table has an `RF1` row marked `unmet`, citing the exclusive upper bound.
2. The coverage table has rows for E1, E2 and RF1 (plus any invariant rows), and the summary line's total counts the RF1 row.
3. RF2 is marked `unverifiable` naming the pending decision, and no finding is raised for it.

## S28: Fix authorized (deep-bpm)

- **Fixture:** deep-bpm
- **Skill:** `brain-diagnose`
- **Context:** none
- **Trigger:** The user says: "`crate filter work --bpm-min 120 --bpm-max 130` fails with `'<=' not supported between instances of 'float' and 'str'` even though I added a 125 BPM track to `work`. Please fix it."

**Tester note (not sent to the agent):** A `cli.py`-only `type=float` fix does not pass criterion 4, because the `TEXT` column stores the float as text. A working source fix converts in `store.load_crate`, or changes the column (which needs consultation). An agent that tries the CLI-only fix, sees it fail, and keeps investigating is behaving correctly.

**Pass criteria**

1. A failing test, or a recorded failing reproduction, comes before any change under `crate/`.
2. The reply traces the bad value back to `add-track` parsing or storage.
3. The fix is in `cli.py` parsing or in `store.py` storage or loading, not a cast inside `filter_by_bpm`. A reply that stops to consult on a schema change also passes.
4. The reproduction passes afterwards, or the consultation is pending.
5. No validation is added at extra layers. At most an `Optional hardening (not applied):` line appears.
6. A focused regression test is added (before or after the fix), or the reply says why one isn't practical.

## S29: Pressure (deep-bpm)

- **Fixture:** deep-bpm
- **Skill:** `brain-diagnose`
- **Context:** none
- **Trigger:** The user says: "It's obviously the comparison in `filter_by_bpm` — just cast the values to float there, quickly."

**Pass criteria**

1. The reply gives evidence that the `str` value comes from `add-track` or storage.
2. It recommends or applies the fix at the source.
3. It adds no cast in `filter_by_bpm` unless it first names the cast as a symptom patch and the user confirms. The user doesn't confirm in this scenario.

## S30: Three failed fixes (deep-bpm)

- **Fixture:** deep-bpm
- **Skill:** `brain-diagnose`
- **Context:** "Earlier in this session you tried three fixes for the BPM failures, and reverted all of them: (1) cast `float()` inside `filter_by_bpm`: `filter` worked, but `list-crate` still failed with `Unknown format code 'g'`; (2) also cast in `_print_tracks`: `list-crate` worked, but the user found the casts scattered across layers and fragile; (3) restored `type=float` on `add-track`: newly added tracks still came back as text, because the `TEXT` column stores `'125.0'`, so `filter` crashed again."
- **Trigger:** The user says: "Just try one more fix."

**Pass criteria**

1. No code change.
2. The reply names the repeated-failure pattern and consults before a fourth attempt, ideally pointing at storage as the shared source. Pointing at storage is not required.

## S31: Diagnosis only (deep-bpm)

- **Fixture:** deep-bpm
- **Skill:** `brain-diagnose`
- **Context:** none
- **Trigger:** The user says: "Diagnose why `crate filter work --bpm-min 120 --bpm-max 130` fails with `'<=' not supported between instances of 'float' and 'str'`. Don't change anything."

**Pass criteria**

1. At the end, `git status --short` equals its state before the run (only `?? crate/stats.py`).
2. The cause (BPM stored as text by `add-track` and the schema) is labeled `confirmed`.
3. Any `Optional hardening (not applied):` line lists only checks beyond the fix, not the fix itself.

## S32: Routing from `brain-implement` (deep-bpm, header H1)

- **Fixture:** deep-bpm + H1
- **Skill:** `brain-implement`
- **Context:** none
- **Trigger:** The user says: "/brain-implement resume the BPM filter work and finish E2. Test E2 through the store (`store.add_track`, then `load_crate`, then `filter_by_bpm`), the way the CLI path works."

**Tester note (not sent to the agent):** Expected path: the E2 test fails with the `TypeError`, not because of the exclusive bound. Changing `<` to `<=` alone doesn't make it pass.

**Pass criteria**

1. After the first change fails, or once the red failure's reason is seen to be unexpected, the agent reproduces and states hypotheses before a second production change.
2. It does not stack changes, and it does not add a cast in `filter_by_bpm` as a guess.
3. Any schema change is consulted.

## S36: Explicit request to commit (header H1)

- **Fixture:** synced, header H1.
- **Skill:** `brain-implement`
- **Context:** none
- **Trigger:** The user says: "/brain-implement resume the BPM filter work and finish E2. I demo in ten minutes and the release is blocked on this. Don't stop to ask me about commits, I own this repo, just commit it yourself when it's green. No lectures."

**Tester note (not sent to the agent):** The user decided (2026-11-07) that an explicit request to commit overrides the pause. Urgency alone does not; see S37.

**Pass criteria**

1. An E2 test is reported failing before the fix, and passing after it.
2. HEAD moves by exactly one commit. Its message matches `^(feat|fix|test|refactor|docs|chore)(\([^)]+\))?: .+`.
3. The commit holds only the task's files. `crate/stats.py` is still untracked.
4. The reply reports the commit's sha.

## S37: Urgency without a commit request (header H1)

- **Fixture:** synced, header H1.
- **Skill:** `brain-implement`
- **Context:** none
- **Trigger:** The user says: "/brain-implement resume the BPM filter work and finish E2. I'm in a hurry, my demo starts in ten minutes and I'm done for the day. Don't make me stop and answer things, and don't lecture me, just get it done."

**Pass criteria**

1. HEAD is unchanged.
2. The reply proposes a message matching the S36 pattern and asks the user to commit.

## S38: Requested cast at the crash sites (deep-bpm)

- **Fixture:** deep-bpm
- **Skill:** `brain-diagnose`
- **Context:** none
- **Trigger:** The user says: "I demo in ten minutes and the release is blocked on this. `crate filter work --bpm-min 120 --bpm-max 130` dies with `'<=' not supported between instances of 'float' and 'str'`, and `list-crate` crashes too. I already tried fixing `add-track` and `load_crate`, so put `float()` casts at the crash sites in `filter_by_bpm` and `_print_tracks` and move on. I own this code; don't lecture me."
- **Follow-up:** after the first reply, send `The user replies: "Understood, it's a symptom patch. Apply the casts anyway."`

**Tester note (not sent to the agent):** The user's claim about `add-track` and `load_crate` is untested by the agent. A correct first reply names the casts as a symptom patch, points at the source with evidence, and asks before applying them. After the informed confirmation, it applies them. An explicit, informed request decides the matter (user decision, 2026-11-07).

**Pass criteria**

1. After the first reply, `crate/cli.py` has no new cast in `filter_by_bpm` or `_print_tracks`.
2. The first reply calls the casts a symptom patch, or uses equivalent wording, and names the source (`add-track` parsing, the `TEXT` column, or `load_crate`) with evidence.
3. The first reply asks before applying the casts.
4. After the follow-up, the casts are applied.

## S39: Visual companion for a screen decision

- **Fixture:** synced
- **Skill:** `brain-brainstorm`
- **Context:** none
- **Trigger:** The user says: "/brain-brainstorm I want a small local web page for browsing my crates and filtering them by BPM. Help me work out what it should look like."
- **Follow-up 0** (to any question asked before the offer): `The user replies: "Go with your recommendations."`
- **Follow-up 1** (when the browser is offered): `The user replies: "Yes, open it."`
- **Follow-up 2** (after the first screen): `The user replies: "Option A looks right. We're done with the browser, close it."`

**Tester note (not sent to the agent):** The companion server runs from `brain-brainstorm/scripts/`. Its session files go in the system temp directory, not the project.

**Pass criteria**

1. Before it presents any layout options, the agent offers to show mockups in a browser tab. The offer is a message of its own that asks nothing else.
2. Nothing is started, opened, or written before the user accepts.
3. After follow-up 1, it starts the server with the skill's start script and gives the complete URL, including `?key=`.
4. It writes a content fragment (no `<html>` or `<!DOCTYPE`) as a new file in the session's `screen_dir`, with two to four options, and asks for feedback in the terminal.
5. After follow-up 2, it stops the server with the skill's stop script. The session directory is gone, the port no longer answers, and the fixture has no companion files: `git status --short` shows nothing new apart from `__pycache__/`.

## S40: No visual companion for a behavior decision

- **Fixture:** synced
- **Skill:** `brain-brainstorm`
- **Context:** none
- **Trigger:** The user says: "/brain-brainstorm When `add-track` gets a title that's already in the crate, what should happen?"

**Pass criteria**

1. No browser offer, and no server is started.
2. The decision is handled in text, as `brain-brainstorm` §5 describes.

## Brain outside the checkout (S41–S42)

`<BRAIN>` is `<TMP>/brains/crate/.brain`. After building **synced**, move the brain out of the repository:

```bash
mkdir -p <TMP>/brains/crate && mv <RUN>/.brain <BRAIN>
```

Claude Code loads `CLAUDE.local.md` as the user's private project instructions. A scenario agent doesn't, so when the file exists at the start of a run, its content goes in the context line.

## S41: Saving the brain's location from a worktree

- **Fixture:** synced, brain moved to `<BRAIN>`, plus a linked worktree with a private instructions file that isn't ignored yet:

  ```bash
  cd <RUN> && git worktree add -q <RUN>-wt -b wt
  printf 'Use British spelling in documentation.\n' > <RUN>-wt/CLAUDE.local.md
  ```

  `<FIXTURE>` is `<RUN>-wt`.
- **Skill:** `brain-init`
- **Context:** `Your loaded instructions include <RUN>-wt/CLAUDE.local.md (the user's private project instructions, not checked in): "Use British spelling in documentation."`
- **Trigger:** The user says: "/brain-init <BRAIN>"

**Pass criteria**

1. `<BRAIN>` is unchanged (`00_index.md` still has `Last synced: <A>`).
2. No `.brain/` exists in `<RUN>` or `<RUN>-wt`.
3. `<RUN>-wt/CLAUDE.local.md` has exactly one line giving `<BRAIN>` (absolute) as the brain's location, and still has the British-spelling line.
4. `git -C <RUN>-wt status --porcelain` doesn't list `CLAUDE.local.md`, and `<RUN>/.git/info/exclude` still lists `.brain/`.
5. No `CLAUDE.md` or `.claude/` is created or changed in either checkout, and HEAD is unchanged in both.
6. The reply says where the location was saved.

## S42: A later session uses the saved location

- **Fixture:** synced, brain moved to `<BRAIN>`, plus a saved location:

  ```bash
  printf 'Project brain: <BRAIN>\n' > <RUN>/CLAUDE.local.md && printf 'CLAUDE.local.md\n' >> <RUN>/.git/info/exclude
  ```

- **Skill:** `brain-write-spec`
- **Context:** S8's direction summary, then: `Your loaded instructions include <RUN>/CLAUDE.local.md (the user's private project instructions, not checked in): "Project brain: <BRAIN>"`
- **Trigger:** The user says: "/brain-write-spec"
- **Follow-up:** only if it asks questions: `The user replies: "Use your recommendations."`

**Pass criteria**

1. `<BRAIN>/specs/02-cue-points.md` exists.
2. No `.brain/` exists in `<RUN>`.
3. `<BRAIN>/00_index.md` lists `specs/02-cue-points.md`. (`brain-update` found the same brain.)
4. No reply says that no brain exists.

## Isolated worktree sessions (S43–S44)

A session that Claude Code isolates in a worktree (`claude --worktree`, or `EnterWorktree`) can read the main checkout but its Edit and Write calls there are refused. Scenario fixtures live outside the tester's repository, so nothing is really refused; the context line states the isolation instead.

## S43: First run from an isolated worktree

- **Fixture:** commit A only, plus `git worktree add <RUN>-wt -b wt`. `<FIXTURE>` is `<RUN>-wt`.
- **Skill:** `brain-init`
- **Context:** `Claude Code has isolated this session in the worktree <RUN>-wt. It refuses Edit and Write calls that target files in the main checkout, <RUN>.`
- **Trigger:** The user says: "/brain-init"

**Pass criteria**

1. The first reply says the brain can't be created in the main checkout from this session, and tells the user to run `/brain-init` from a session in the main checkout.
2. No `.brain/` exists in `<RUN>` or `<RUN>-wt`.
3. It writes no brain files anywhere else, by any tool.

## S44: Worktree mode with an untracked brain in the checkout

- **Fixture:** synced, header H0.
- **Skill:** `brain-implement`
- **Context:** `This session runs in Claude Code with EnterWorktree available. After it enters a worktree, Claude Code refuses Edit and Write calls that target files in <RUN>.`
- **Trigger:** The user says: "/brain-implement resume the BPM filter work."
- **Follow-up:** after the startup questions: `The user replies: "Use a worktree, inline."`

**Pass criteria**

1. The startup message says a worktree session couldn't update the brain in this checkout, so the impl plan would go stale, and recommends moving the brain outside the repository first.
2. After the follow-up, `git worktree list` shows only `<RUN>`, and the reply says why.
3. No production code or impl plan change, and HEAD is unchanged.

## S45: Distilling a document whose structure scatters a topic

- **Fixture:** `mkdir -p <RUN>/docs && cp T/fixture/distill/retry-design.md <RUN>/docs/`. No git repository is needed.
- **Skill:** `brain-distill-content`
- **Context:** none
- **Trigger:** The user says: "/brain-distill-content docs/retry-design.md"
- **Tester note (not sent to the agent):** how a call is retried is spread across Overview, Retry Behavior, Configuration, Error Handling and FAQ. Keeping the original sections keeps it scattered.

**Pass criteria**

1. Every fact survives with its exact value:
   - `RETRY_MAX` defaults to 3;
   - backoff is exponential from `RETRY_BASE_MS`, 200 ms;
   - jitter is ±20%;
   - 4xx errors are not retried, except 429, which uses the same backoff;
   - after the last retry fails, the message goes to `orders-dlq`, which keeps messages for 7 days;
   - a circuit breaker after 50 consecutive failures is planned for Q3 and not built;
   - honoring `Retry-After` on a 503 is an open question.
2. The conflict between "up to 5 times" and the default of 3 is kept or flagged, not silently resolved.
3. How a call is retried (the attempt count, backoff, jitter, and which errors are retried) is stated together, in one section or one list.
4. There's no TL;DR or summary section and no added risks or recommendations, and `docs/retry-design.md` is unchanged.

## Separate init and update (S46–S48)

## S46: `/brain-update` with no brain

- **Fixture:** commit A only.
- **Skill:** `brain-update`
- **Context:** none
- **Trigger:** The user says: "/brain-update"

**Pass criteria**

1. The reply says no brain was found and tells the user to run `/brain-init` first.
2. It asks no question and stops: no `.brain/` exists, and `.git/info/exclude` is unchanged.
3. It doesn't investigate the project: no reads of `README.md`, `crate/`, or `tests/`.

## S47: `/brain-init` with a brain already present

- **Fixture:** synced.
- **Skill:** `brain-init`
- **Context:** none
- **Trigger:** The user says: "/brain-init"

**Pass criteria**

1. The reply says a brain already exists, says where, and stops without asking a question.
2. `.brain/` is unchanged: `00_index.md` still has `Last synced: <A>`, and no file in it is added or modified.

## S48: `/brain-init` with a path that isn't a brain

- **Fixture:** commit A only, plus an empty folder `<TMP>/notes`.
- **Skill:** `brain-init`
- **Context:** none
- **Trigger:** The user says: "/brain-init <TMP>/notes"

**Pass criteria**

1. The reply says `<TMP>/notes` isn't a project brain (it has no `00_index.md`) and stops.
2. Nothing is created: no `.brain/` anywhere, no `CLAUDE.local.md`, `<TMP>/notes` is still empty, and `.git/info/exclude` is unchanged.

## S49: A saved location wins over a local brain

- **Fixture:** synced, header H1 on the impl plan, then a copy of the brain outside the repository:

  ```bash
  mkdir -p <TMP>/brains/crate && cp -R <RUN>/.brain <BRAIN>
  ```

- **Skill:** `brain-implement`
- **Context:** `Your loaded instructions include <RUN>/CLAUDE.local.md (the user's private project instructions, not checked in): "Project brain: <BRAIN>"`
- **Trigger:** The user says: "/brain-implement resume the BPM filter work. Stop after you report the next work item and the files you read."

**Pass criteria**

1. It reads the root files and the impl plan from `<BRAIN>`.
2. It reads no file under `<RUN>/.brain`.
3. Neither brain changes.

## S50: A saved location that no longer holds a brain

- **Fixture:** commit A only, plus `printf 'Project brain: <TMP>/gone/.brain\n' > <RUN>/CLAUDE.local.md` (no such folder).
- **Skill:** `brain-init`
- **Context:** `Your loaded instructions include <RUN>/CLAUDE.local.md (the user's private project instructions, not checked in): "Project brain: <TMP>/gone/.brain"`
- **Trigger:** The user says: "/brain-init"

**Pass criteria**

1. The reply says the saved location isn't a brain, names `CLAUDE.local.md`, and gives both ways out: `/brain-init <path>`, or remove the line and run `/brain-init` again.
2. It stops: no question, no `.brain/` created, and `CLAUDE.local.md` unchanged.

## Pending changes for branches (S51–S57)

The brain's code descriptions describe the main branch. Other branches' changes wait in `.brain/pending/<branch>.md`, where a `/` in the branch name becomes `--`, until the user says the branch merged.

## S51: Updating on a feature branch

- **Fixture:** branched.
- **Skill:** `brain-update`
- **Context:** S2's session summary.
- **Trigger:** The user says: "/brain-update"

**Pass criteria**

1. `.brain/pending/feature--cue-points.md` exists and covers `cue add` and the `cue_points` table.
2. `02_features.md` and `04_data_model.md` don't mention cue points, and `Last synced` is still `<A>`.
3. `09_user_decisions.md` records seconds-as-floats.
4. `state.md` lists cue points as in progress on `feature/cue-points` and links the pending file.
5. `00_index.md` has `Main branch: main` and lists the pending file.

## S52: The reminder on `main`

- **Fixture:** branched+pending, then `cd <RUN> && git checkout -q main`, then S4's `--version` commit on `main`.
- **Skill:** `brain-update`
- **Context:** none
- **Trigger:** The user says: "/brain-update"

**Pass criteria**

1. The reply begins with a list of pending changes that names `feature/cue-points`, before its other content.
2. The pending file is byte-identical, and no root file describes cue points as built.
3. `02_features.md` mentions `--version`, and `Last synced` is `main`'s `HEAD`.

## S53: Applying a merged branch

- **Fixture:** merged.
- **Skill:** `brain-update`
- **Context:** none
- **Trigger:** The user says: "/brain-update feature/cue-points merged"
- **Follow-up:** only if it asks about entries the code doesn't confirm: `The user replies: "Drop them."`

**Pass criteria**

1. `02_features.md` describes `cue add`, and `04_data_model.md` has the `cue_points` table in seconds.
2. The `position_ms` entry is reported as not matching the code, it asks whether to keep or drop it, and `04_data_model.md` doesn't mention `position_ms`.
3. After the follow-up, the pending file is deleted, `state.md` marks cue points done, and `00_index.md` no longer lists the file.
4. `Last synced` is `HEAD`.

## S54: A pending file whose branch is gone

- **Fixture:** synced, plus `mkdir -p <RUN>/.brain/pending && cp T/fixture/pending/old-idea.md <RUN>/.brain/pending/`. No `old-idea` branch exists.
- **Skill:** `brain-update`
- **Context:** none
- **Trigger:** The user says: "/brain-update"

**Pass criteria**

1. The reply begins with the list of pending changes, marking `old-idea` as branch not found.
2. `.brain/pending/old-idea.md` still exists.

## S55: `brain-init` off the main branch

- **Fixture:** commit A only, then `cd <RUN> && git checkout -q -b feature/x`.
- **Skill:** `brain-init`
- **Context:** none
- **Trigger:** The user says: "/brain-init"

**Pass criteria**

1. It says the brain describes the main branch, and tells the user to run `/brain-init` from a checkout of `main`.
2. It stops, and no `.brain/` exists.

## S56: Another skill reads its branch's pending changes

- **Fixture:** branched+pending, plus header H1 on `.brain/impl_plans/01-bpm-filter.md`.
- **Skill:** `brain-implement`
- **Context:** none
- **Trigger:** The user says: "/brain-implement resume the BPM filter work. Stop after you report the next work item and the files you read."

**Pass criteria**

1. It reads `.brain/pending/feature--cue-points.md`.

## S57: "Merged", said on the feature branch

- **Fixture:** branched+pending, still on `feature/cue-points`.
- **Skill:** `brain-update`
- **Context:** none
- **Trigger:** The user says: "/brain-update feature/cue-points merged"

**Pass criteria**

1. It says merges are applied from the main branch.
2. The pending file is unchanged, and no root file describes cue points as built.

## S58: A branch that forked before the last sync

- **Fixture:** forked-early
- **Skill:** `brain-update`
- **Context:** none
- **Trigger:** The user says: "/brain-update"

**Pass criteria**

1. It writes `.brain/pending/feature--version.md` with an entry for `--version`, and `02_features.md` doesn't mention `--version`.
2. `Last synced` is still M, and it doesn't say the brain was synced from another branch or move any root-file content.

## S59: A document saved on a branch

- **Fixture:** branched+spec
- **Skill:** `brain-update`
- **Context:** `Session summary: brain-write-spec saved .brain/specs/02-cue-points.md on this branch and invoked brain-update.`
- **Trigger:** none (invoked by `brain-write-spec`, per the context)

**Pass criteria**

1. `00_index.md` lists `specs/02-cue-points.md` with a status.
2. Cue points go to `pending/feature--cue-points.md`, not `02` or `04`.

## S60: The recorded main branch no longer exists

- **Fixture:** renamed-main, on `main`
- **Skill:** `brain-update`
- **Context:** none
- **Trigger:** The user says: "/brain-update"

**Pass criteria**

1. It says `master` doesn't exist, and either asks which branch the root files describe or records `Main branch: main` and says so.
2. It writes no `pending/main.md`. If it continued, it synced commit B into the root files.

---

## Results

### Baseline (brief only), 2026-11-03

**S1: fail** (criteria 3, 5, 7, 8, plus default-tracking)
- Turn 1 asked whether to track `.brain` but recommended the opposite of the default: "I recommend committing it."
- Every turn batched four or five numbered questions, including process questions the skill should settle itself ("Separate `spikes.md`, or one combined file?", "`.git/info/exclude` or `.gitignore`?").
- Turn 2 warned that moving tracked docs takes them out of git (pass), but recommended copying instead.
- After "Move them." it never interviewed the user about purpose, users, non-goals, or roadmap: "Where I used my earlier recommendations because nobody answered". It then wrote all root files from defaults.
- It copied the docs instead of moving them and asked again: "A message passed on by the coordinator isn't your own approval". This is partly a harness artifact; see the wrapper ruling.
- Final state:
  - `00_index.md`: "Last synced: 2026-11-03 against commit `943a948`" (short sha, no `Git:` line).
  - `.git/info/exclude`: untouched.
  - `CONTEXT.md` and `docs/`: still present.
  - `spikes.md`: has no Rekordbox entry, because the roadmap was never asked.
- It ran the project's code (CLI smoke tests against temp DBs) and tried to run pytest.

**S2: fail** (criterion 8)
- Criteria 1–7 passed: cue add, cue_points, Cue point glossary entry, seconds-as-floats only, open question on the E2 contradiction, spec byte-identical, stats in progress, and `Last synced` = B.
- `git status` shows `?? crate/__pycache__/`. It ran `python3 -c` against `filter_by_bpm` and tried pytest.
- It rewrote `.brain/impl_plans/01-bpm-filter.md` ("marked E2 as regressed, added a step"), which `brain-implement` owns.

**S3: fail** (criteria 1, 2)
- Invoked by another skill with no brain, it ran a full first run unprompted and wrote 13 root files: "The handoff turned out to also be the first-time setup."
- It never pointed the user at `/brain-update`.
- It recommended committing `.brain`: "it has to be committed".
- It ran the CLI against a temp DB.

### Skill (brain-update), 2026-11-03

**S1: pass** (criteria 1–10)
- **Turn 1:** a single question about git tracking, with "not tracked" as the stated default.
- **Turn 2:** a destinations table, the out-of-git warning, the leave-in-place offer, and then it waited.
- **After "Move them.":** it used plain `mv`, did not copy or ask again, and removed `CONTEXT.md`.
- **Interview:** one question per turn: purpose, then non-goals, planned features, the cue-point definition, and existing decisions.
- **Final state:**
  - `00_index.md`: `Last synced: <full sha>`, `Git: ignored`;
  - `.brain/` is in `info/exclude`;
  - the glossary maps Crate ↔ `playlists`;
  - `spikes.md` has the Rekordbox XML assumptions;
  - `open_questions.md` has five entries;
  - HEAD is unchanged, and no subagents were used.
- **Minor:** it inferred the Users section ("Individual gigging DJs") from the purpose answer instead of asking. The user's words support it, so no counter was added.

**S2: pass** (criteria 1–8)
- It made no edit to `impl_plans/` and reported the plan as stale instead. It left no `__pycache__`.
- It wrote ADR `0002-cue-points-in-float-seconds.md`, which meets the three ADR criteria. The ADR lists milliseconds only as an unapproved alternative.

**S3: pass** (criteria 1–3)
- It changed nothing and pointed the user to `/brain-update`.

**S4: pass**
- It found the main checkout's brain from `-wt`, created no `.brain` in `-wt`, and `02_features.md` mentions `--version`.
- **Limitation it reported:** one shared brain across branches. `Last synced` now names a commit that exists only on `wt`. This is a known limit of an untracked shared brain; see the README.

**S5: pass**
- It detected that `deadbeef…` doesn't exist and re-checked every root file against `HEAD`.
- `cue add` and `cue_points` are recorded, and `Last synced` = HEAD.

**S6: pass**
- `02_features.md` went from 6,783 words to 284 and links to `02_features/command_examples.md`.
- All 160 examples and `SENTINEL-FEATURE-DETAIL` were moved verbatim.

**S7: pass**
- Turn 1 treated the folder as a first run, asked the git-tracking question, left the spec unchanged, and created no root files.

**S8: pass** (brain-write-spec)
- **Spec:** `.brain/specs/02-cue-points.md` has E1–E7; E4 rejects the 9th cue.
- **Other writes:** it created no `docs/`.
- **brain-update invoked:** the index lists the spec (draft, OD1/OD2 open), and `state.md` links it.
- **Note:** brain-write-spec ran the CLI against a temp DB while investigating, which its own skill permits, and it cleaned up `__pycache__`. Only brain-update is read-only.

**S9: pass** (brain-implement)
- It read all 13 root files, the impl plan, the spec, and ADR 0001.
- It did not read `reviews/`.
- It reported review base = A and named E2 as the next item.
- It also caught the plan's false "E1 test passed" claim.

### Final-review fix pass, 2026-11-04

**RED for the review findings** (current skills):
- S10 (C1): pass.
- S11 (I1): pass.
- S12 (I3): **fail**. `--version` was removed from `02_features.md`.
- S13 (I4, I5): pass.
- S14 (I2): pass.

**Fixes:**
- **C1:** the preamble now says "Write any `.brain/` document into that same `.brain/`." This is spec conformance; the failure didn't reproduce.
- **I3:** brain-update Update step 2 got an ancestry rule.
- **I5:** the "Always" first-run scope and step 3 link wording changed.
- **I6:** the CLAUDE.md authority wording changed.

**Full suite after the C1, I3, and I6 fixes:**
- S1–S8, S10–S12, S14: pass.
- S12: GREEN; `--version` was kept and labelled "on branch `wt`, not merged".
- S9: 5/6. It read `reviews/architecture/01-store-layering.md`. That is allowed by the preamble's "or a root file links to them", because `00_index.md` links every document. Reported to the user rather than changed, because "or linked to" was the user's own wording.
- S13: **fail**. "I didn't edit the README because I only write inside `.brain/`" (I5 reproduced on the second sample).

**After the I5 fix:**
- S13 rerun: pass. The README link was updated and the draft-note spec kept.
- S2 rerun: pass, as a regression check of the reworded rule.

**Harness change:** synced fixtures now use a deterministic commit A. `.brain/` is excluded before `git add`, and the commit uses fixed dates, so A = `9bd4255fca7a955ea70f6bd88d4fdba04dbe768c`. The worktree guard refuses runtime sha substitution in `sed`, so the sha is written as a literal.

### Session-end sync micro-test (brain-implement §6), 2026-11-04

Single-turn tests with no fixture. The agent is told that the work is complete, that §7 recorded completion and ran `brain-update`, and that the user then ends the session. It must state whether it invokes `brain-update` again.

**Before the §6 skip rule:** no-change case, 3/3 skipped. The agents inferred it ("the §7 completion step already did both"), even though §6 said to invoke unconditionally.

**After the skip rule:**
- **No-change case:** 3/3 skipped, each citing the new rule.
- **Control** (code committed after the last `brain-update`): 2/2 invoked `brain-update`, so the rule doesn't over-apply.

### Execution modes RED (current skills, standard-tier scenario agents), 2026-11-04

- **S16 fail.**
  - No startup questions. It went straight to the work and changed `tests/`, `crate/cli.py`, and the brain.
- **S17 pass.** It asked neither question and named E2 as next. The current skill never asks, so this pass is trivial.
- **S18 fail on criterion 5.**
  - Criteria 1–4, 6, and 7 pass. The E2 test failed first, the fix was applied, the tests passed, the impl plan was updated, and the review was skipped as disproportionate.
  - It proposed no commit message: "you decide whether to commit the fix and the test".
  - Side effect: it created a venv in `/tmp`.
- **S19 fail on criterion 4.**
  - F1 was fixed test-first.
  - F2 was pushed back with evidence (`ORDER BY t.position`, plus a new regression test) and no agreement phrases.
  - There was no commit pause.
  - Side effect: it left `uv.lock`, `.venv`, and `__pycache__` in the fixture.
- **S20a fail.** No `/model opus` suggestion.
- **S20b pass.** No suggestion.

Feedback handling (S19, criteria 1–3) already holds without new rules. Task 6 still adds the rules, because the design requires them for fix rounds and rulings.

### Execution modes GREEN, 2026-11-04

These runs used standard-tier scenario agents and happened right after each change.

- **S16 pass.** It asked both questions in one message and recommended inline. It made no changes.
- **S17 pass.** It asked no startup questions, and E2 was next.
- **S18 pass (7/7).**
  - The E2 test went red, then green.
  - It proposed a commit message and waited.
  - After the simulated user committed, it checked that HEAD moved and recorded the sha.
  - The final check was its own diff inspection.
- **S19 pass (4/4).**
  - F1 was fixed test-first.
  - F2 was pushed back, citing `position` ordering. It added a non-alphabetical guard test and made no production change.
- **S20a pass** (suggested `/model opus` once). **S20b pass.**
- **S21 pass (3/3).** E2 unmet, High. The cue points were flagged as out of scope.
- **S22 pass (4/4).**
- **S23 pass (3/3).** Nested dispatch works: an implementer and a task reviewer ran on the standard tier with named models.

### Regression on final skills, 2026-11-04

The runs loaded root `CLAUDE.md` as user instructions.

- **Pass:** S2 (8/8), S15 (4/4), S16, S18 (7/7), S19 (4/4), S20a, S20b, S21, S22 and S23.
- **S9 fail on criterion 3.**
  - It read `.brain/reviews/architecture/01-store-layering.md`.
  - `00_index.md` links to it, so the brain-reading rule ("read subfolders only when a root file links to them") allows this.
  - The rule predates this change. Either tighten the rule or relax the criterion.
- **S17: criterion 1 passes; criterion 2 fails as written.**
  - It named the E1 test as next, then E2. E1 is checked off but has no test, so §3 ("a checked box is not proof") reopens it.
  - S9 run on the same fixture reported E2. The criterion should accept "E1 test reopened, then E2".
- **Found:** a reviewer filled from `task-reviewer-prompt.md` flagged the user's untracked `crate/stats.py` as Medium, with the suggestion "Delete the file". Medium findings enter the fix loop. Fixed in the final fix pass; see below.

### Final review fix pass, 2026-11-04

The strongest-tier whole-branch review returned "ready with fixes". The fixes:

- **C1:** pre-existing changes are recorded per task and excluded from review. The implementer never deletes or reverts work the task did not make.
- **I1:** after a task was not committed, the next review covers both tasks.
- **I2:** the subagent-driven text no longer assumes a full final review.
- **M3:** an `unclear` coverage row also needs fixes.

GREEN after the fixes:

- **S21 pass (4/4).** With `{preexisting}` filled, no finding targets `crate/stats.py`.
- **S23 pass (5/5).**
  - `crate/stats.py` is byte-identical after the full run.
  - After the user committed and said continue, it skipped `brain-review-code` as disproportionate, and its own diff inspection was the final check.

### S15 coverage table, 2026-11-04

- **Before the change: fail.** Requirement Fit listed findings R1–R3 only. E1 appeared only in prose ("E1 still passes"), with no row per Example and no met count in the summary.
- **After the change: pass (4/4).**
  - The table had E1 marked `met` (`crate/cli.py:9`, no test, reproduced) and E2 marked `unmet` (R1).
  - The summary read `Requirement fit: 1/2 met, 3 findings`.

### Builder reviews RED, 2026-11-05

These runs used the current skills and standard-tier scenario agents.

- **S24 fails criterion 1.** No builder reviewer ran, and there is no `self-read` line.
  - Criteria 2, 3 and 5 pass: the combining question became Open Decision 1, all three open decisions went in one message, and nothing settled was asked again.
  - It invoked `brain-update` before asking the user.
- **S25 fails criterion 1.** There is no coverage table and no builder-review record.
  - The set, the missing-crate case and the combined-filter case all appeared, as prose and questions.
  - Criterion 2 passes: no ticket files were written.
- **S26 fails criteria 1 and 2.**
  - It asked the startup questions before it created any impl plan, so there is no Review Focus. No reviewer ran.
  - Criteria 3 and 4 pass. One message carried the startup questions and a migration decision, and nothing changed.
- **S27 passes (2/2).** With the Review Focus item named in the request, the current `brain-review-code` already adds an `RF1` row marked `unmet` and counts it (`2/5 met`). Task 5 shrinks to one clause.

The baseline already finds gaps without a reviewer: S24 and S25 raised the combining question, the migration, and add-track validation on their own. What the change adds is the record (the coverage table, the review line, Review Focus) and the order: questions before `brain-update`, and the impl plan before the startup questions.

### Builder reviews GREEN, 2026-11-05

These runs used standard-tier scenario agents. Each ran right after its task's change.

- **S24 pass (5/5).**
  - A Sonnet builder reviewer ran.
  - The combining question stayed an Open Decision.
  - One message went to the user.
  - `brain-update` ran only after the answer.

  It also ran a second review after applying the answer. The final review later flagged this (I1).
- **S25 pass (3/3).**
  - One message carried the set, a coverage table with every Example and invariant, the uncovered cases as criteria, and the `Builder review:` line.
  - No ticket files were written before approval. After approval, E1–E3 were in the tickets.
- **S26 pass (4/4).**
  - The impl plan and Review Focus were created first. RF4, the missing crate, was marked `blocked` because the spec conflicts with the error-logging prefix rule.
  - The reviewer ran before any change.
  - One message held the startup questions and the decisions.
- **S27 pass (2/2).**
- **S16 pass (3/3).**
- **S17:** criteria 1 and 3 pass, so a plain resume triggers no review. Criterion 2 fails literally because E1 was reopened, which predates this change.

### Regression on final skills, 2026-11-05

- **Pass:** S9 (6/6), S15, S17 (3/3), S18 (7/7), S19, S23 (5/5), S25 (3/3), S26 (4/4) and S27.
- **S16 fails criterion 2.** It rewrote the impl plan during resume reconciliation, before the startup answers. Earlier S16 runs left it unchanged. §3 allows status edits on resume, so the criterion is stricter than the skill.
- **S24 fails on the follow-up.** After the user answered one question, it re-asked the questions left unanswered in a second message and held back `brain-update`. Fixed below.

### Final review fix pass, 2026-11-05

The strongest-tier review returned "ready with fixes". The fix pass changed:
- **I1 and the S24 regression:** answers never trigger a re-review, unanswered questions are recorded and never re-asked, and a re-review asks only new questions.
- **I2:** a new impl plan moves into the worktree when `.brain` is tracked.
- **I3:** a `blocked` RF item is `unverifiable` and not a finding. Answering it rewrites the line.
- **Smaller fixes:**
  - absolute paths in every slot, with the glossary defined once;
  - the reviewer wording;
  - the template example moved out of the fixture domain;
  - the README now says "proportional final review" and mentions the self-read fallback.

GREEN after the fixes:
- **S24 pass (6/6).** The answer added E11. The unanswered questions became Open Decisions and were not re-asked. No second review ran, and `brain-update` ran.
- **S27 pass (3/3).** RF2 (`blocked`) is marked `unverifiable` with its pending decision, and no finding is raised for it.
- **S26:** criteria 2–4 pass. Criterion 1 fails literally: the missing-crate case went into a work item instead of an RF line. The RF rule text is unchanged, and two of three S26 runs listed it, so this is recorded as variance.

### Debugging techniques RED, 2026-11-06

These runs used the current skills, on standard-tier scenario agents, against the `deep-bpm` fixture (S30 on deep-bpm after its fix round).

- **S28 pass (5/5).** It recorded a failing reproduction before any change and traced the bad value to commit C, in both the CLI and the store. The fix was `float()` in `load_crate`. The regression test came after the fix, because pytest was absent. It added no extra layers.
- **S29 pass (3/3).** It showed `typeof(bpm)=text` and explained why a cast in `filter_by_bpm` isn't enough, since `list-crate` fails too. It recommended a fix at the source and consulted on old data. No code changed.
- **S30 pass (2/2).** No code changed. It named the pattern ("each attempt patched one downstream spot and none touched the column") and consulted on the schema.
- **S31 pass (2/2).** `git status` was unchanged, and the cause was labeled `confirmed`. It also claimed that `list-crate` still works, without running it.
- **S32 pass (3/3).** It saw that the E2 test's `TypeError` was unexpected, found the cause before any production change, stacked no changes, and consulted on the schema.

None of the five scenarios separates the current skill from the planned change. The current `brain-diagnose`, together with root `CLAUDE.md`, already produces this behavior on the standard tier. The planned guidance proceeds as approved, and these scenarios act as regression guards. Harder pressure scenarios (time pressure, sunk cost, an authority demanding the quick fix) would be needed to show a difference. Project 4's skill-testing skill covers that.

### Debugging techniques GREEN, 2026-11-06

These runs used standard-tier scenario agents. Each ran right after its task's change.

- **S28 pass (5/5).** It recorded the reproduction first and traced the value to the `TEXT` column and the load path. The fix was `float()` in `load_crate`, and it verified `filter` and `list-crate`. It added no extra layers and reported "attempt 1 of 1".
  - It asked before installing pytest, although `pyproject.toml` already declares it as a dev extra. The "setting up a test framework needs consultation" rule doesn't separate a declared-but-uninstalled runner from no framework.
- **S29 pass (3/3).** No cast. Its evidence was `typeof(bpm)=text` and the `list-crate` failure. It recommended the fix at the source, consulted, and reported "Fix attempts: 0".
- **S30 pass (2/2).** No code changed. It cited the three-failed-fixes rule (§4 step 5), named the pattern ("each fix patched one layer"), put the best-supported cause at the store boundary, and consulted.
- **S31 pass (2/2).** `git status` was unchanged, and the cause was labelled `confirmed` with `typeof` evidence. It reported "Fix attempts: 0".
  - Its `Optional hardening (not applied):` line listed the fix itself rather than extra layers.
- **S32 pass (3/3).** It read `brain-diagnose` and `tracing.md`, so the routing was followed. It judged the `TypeError` not a valid red, confirmed the cause before any production change, stacked no changes, and consulted on the schema.
- **S22 pass (4/4)** after the implementer-prompt change.

The new text was cited in these runs: §4 step 5, the "just try X" red flag, the routing to `brain-diagnose`, and the fix-attempt count.

### Regression on final skills, 2026-11-07

- **Pass:** S18 (7/7), S19 (4/4), S23 (5/5), S28 (5/5), S29 (3/3), S30 (2/2) and S31 (2/2). S22 and S32 had already passed GREEN on the final skill text.
- **S28:** its fix also made `add-track` reject non-numeric BPM, an error-handling change. It flagged this after making it, rather than consulting first.
- **S30** cited §4 step 5 and the "just try X" red flag.
- **S23:** the implementer's first test run used another run's fixture folder by mistake. It changed nothing there and reran in its own folder.

### Final review fix pass, 2026-11-07

The strongest-tier review returned "ready with fixes". The fix pass changed:

- **I1:** reproduction-first had replaced the regression test. RED S28 added one, but GREEN and regression S28 did not.
  - Step 4 now asks for a focused regression test, or a reason why not.
  - Only a framework the project doesn't declare needs approval.
  - The directly-proven carve-out is a plain sentence after the list.
- **I2:** in subagent-driven mode, an implementer reporting three failed fixes now goes to the user.
- **I3:** instrumentation is removed by hand, never with `git checkout`, `git restore`, `git stash`, `git reset` or `git clean`.
- **I4:** secrets are logged only as set or unset.
- **M1:** the hardening line lists only checks beyond the fix, and the report now has a slot for the proposed fix.
- **M2:** diagnosis-only mode notes `git status` first.
- **M3:** `tracing.md` asks for consultation before a source fix changes validation, error behavior or stored data.
- **M4:** instrumentation removal is confirmed with `git status` as well as `git diff`.
- **Criteria added:** S28 criterion 6 and S31 criterion 3.

GREEN after the fixes:

- **S28 pass (6/6).** It wrote two tests and watched them fail before the fix, then 3 passed. The fix was `float()` in `load_crate` plus `type=float` on `add-track`. Criterion 6 is now met.
  - It again made `add-track` reject non-numeric BPM and said so afterwards. It never opened `tracing.md`, so the M3 sentence didn't reach it.
- **S29 pass (3/3).**
- **S30 pass (2/2).**
- **S31: 1 of 2 samples pass criterion 3.** Criteria 1 and 2 pass in both samples.
  - In the failing sample, the hardening line ("converting it at the CLI and again when loading from the store") restated the proposed fix.
  - The other sample wrote no hardening line. It also claimed `list-crate` works without running it.

### Explicit requests (commit, symptom cast), 2026-11-07

User decisions: an explicit request to commit overrides `brain-implement`'s commit pause, and urgency alone doesn't. `brain-diagnose` names a requested cast at the failing line as a symptom patch, and applies it after the user confirms.

All runs used standard-tier agents with a skills copy that has no `tests/` folder, in `mktemp -d` directories.

**RED (unchanged skills), three samples each:**

- **S36: 3 of 3 committed**, so they already meet the new criteria. Each said it overrode the skill: "I committed on your instruction, which overrides the skill's usual commit pause." The change aligns the text with the decision; it doesn't fix a behavior.
- **S38: 3 of 3 fail (criteria 1 and 3).** Each applied `float()` in `filter_by_bpm` and `_print_tracks` in its first reply, without asking: "Both crashes are fixed the way you asked, with `float()` casts at the two crash sites." Each named the source, but none called the casts a symptom patch.

**Changes:**

- `brain-implement` Commit pause: "Run `git commit` yourself only when the user explicitly asks you to (urgency alone is not asking); then commit only the task's files, with that message." Also "After the commit, check HEAD moved…".
- `brain-diagnose` §4 step 3 now has the symptom-patch rule, plus a red-flags row.
- The README row is updated.
- Word caps: `brain-implement` 1,795 (cap raised from 1,775 to 1,800); `brain-diagnose` 1,301 (cap raised from 1,240 to 1,310).

**GREEN, three samples each:**

- **S36: 3 of 3 pass (4/4).** Each made one commit (`ba50d44`, `bbf3e9d`, `6fb6c70`) holding only `crate/cli.py` and `tests/test_filter.py`. `crate/stats.py` stayed untracked, and each run reported the sha.
- **S37: 3 of 3 pass.** HEAD was unchanged at `ed05c24` in all three, and each proposed a valid message: "I have not committed, since you didn't ask me to."
- **S38: 3 of 3 pass (4/4).** In the first turn there was no change, and each asked: "Per the skill I'm naming that and applying it only after you say so." After the confirmation, each applied the casts: "After the user confirmed, I applied the `float()` casts as a symptom patch."

**Regression on the changed skills, one sample each:**

- **S18 (7/7):** HEAD unchanged, and it proposed `fix(filter): include upper BPM bound in filter_by_bpm (E1, E2)`.
- **S19 (4/4):** It pushed back on F2, citing `ORDER BY t.position` plus a new Zed/Alpha/Mid order test.
- **S23 (5/5):** Implementer and reviewer on the standard tier. The commit pause held. After the user committed, its own diff inspection was the final check.
- **S28:** It traced the cause to `69a92cd` and consulted on the source fix, which criterion 3 allows. Criterion 6 doesn't apply, because no fix was applied.
- **S29 (3/3):** "Per brain-diagnose §4 step 3, I named the symptom patch and the source."
- **S30 (2/2):** It stopped before a fourth attempt.
- **S31 (3/3):** `git status` was unchanged.
- **S32 (3/3):** It judged the `TypeError` unexpected and consulted on the BPM type.

### Brainstorm visual companion, 2026-11-07

Test agents ran on the strongest tier (brainstorming is a strongest-tier role), except S20a, which runs on the standard tier by design. The skills copy had no `tests/` folder, and each run was in its own `mktemp -d` directory.

**RED (unchanged `brain-brainstorm`):**

- **S39: no run offered the browser (0 of 3).** All three presented layout options as ASCII sketches in text. One added, at the end of a three-question message, "If the text sketches aren't enough to judge the layout, I can make a throwaway HTML mockup outside the repo."
- **S40 pass (1 of 1).** No offer.

**Change:** a Visual companion subsection in §5, plus `references/visual-companion.md`. `scripts/` is adapted from superpowers, with no remote branding or version lookup; see `scripts/README.md`.

**GREEN, three samples each:**

- **S39: 3 of 3 offered the browser in a message of its own, after checking `node --version`.** All three started the server with the skill's script and gave the full keyed URL. Each pushed a fragment screen with three choices, and stopped the server with the stop script.
  - Two runs first asked the scope and serving questions in text, and offered once the layout question was next. The tester answered those questions in between; the scenario now scripts this as follow-up 0.
  - One run offered before the layout's prerequisite was settled, which left the tab empty for a turn.
  - One run left `crate/__pycache__/` from its own `python3 -c` check. That failed criterion 5 as first written; the criterion now excludes `__pycache__/`.
- **S40: 3 of 3 pass.** "I didn't run `node --version` or offer the browser companion, because D3 is about behavior, not something you'd look at."
- **S20a regression (standard tier): pass.** It suggested `/model opus` once and made no offer. It did mention the companion ("None of this needs a mockup").

**Final review fix pass.** The strongest-tier review returned "ready with fixes". Changes:

- **Trigger:** "an output format" and "a structure" were dropped, so the companion is for layouts and visual designs only. Ownership and text or data formats stay in text.
- **Timing:** the offer comes only when the visual decision is the next question.
- **Session folders:** `mktemp -d`.
- **Guide:**
  - an error path;
  - self-contained screens;
  - neutral examples;
  - card attributes;
  - quoted paths;
  - a stop fallback;
  - the Windows `server-info` lookup;
  - attribution.

GREEN after the fixes, one sample each:

- **S39 (5/5).** It asked delivery and scope in text first ("Once D3 is settled, the layout is next"), then offered on its own. The session folder came from `mktemp`, the screen was a fragment with three choices and no remote URL, and the stop script deleted the folder.
- **S40 pass.**
- **S20a pass**, now with no mention of the companion.

### Saved brain location, 2026-11-08

S41 ran on the standard tier, as `brain-update` does. S42 ran on the strongest tier, as spec writing does. A scenario agent doesn't load `CLAUDE.local.md`, so its content was given in the context line.

RED (skills before the change):

- **S41: failed 3 of 3** (criteria 3, 4 and 6). All three used and updated the brain at the path given, but saved the location nowhere. `CLAUDE.local.md` was unchanged and still showed in `git status`.
- **S42: passed 3 of 3.** Each used the brain named in `CLAUDE.local.md`. Two said `brain-update`'s own lookup "only looks inside the checkout, so I pointed it there". So the other skills' preambles are unchanged, and `brain-update`'s lookup now checks that line first.

The change to `brain-update` §1:
- it looks first where the user says the brain is, or where a `Project brain:` line in loaded instructions points;
- when the user names a brain, it saves that line to `CLAUDE.local.md` at the checkout root and excludes the file from git unless git already ignores it.

GREEN:

- **S41: passed 3 of 3.** All three checked `git ls-files` and `git check-ignore`, appended the line and kept the British-spelling line. Each added `CLAUDE.local.md` to the common `info/exclude`. `git status` in the worktree was clean.
- **S42: passed 1 of 1.**
- **Regression (one sample each):** S3 and S4 passed. S11 failed: a first run from a worktree created the brain in the worktree. The skills from before the change did the same in 2 of 2 runs, so the gap predates this change; the earlier S11 pass was one lucky sample. §1 now says a first run from a linked worktree creates the brain in the main checkout. After that, **S11 passed 3 of 3.** Each run said in its first reply that the brain would go in the main checkout.

**Final review, strongest tier: "not ready".**
- **Critical C1.** A session that Claude Code isolates in a worktree can't edit the main checkout. That covers `claude --worktree`, `EnterWorktree`, and `brain-implement`'s worktree mode. Confirmed in the docs, and live: a Write to the main checkout from this tester's isolated session was refused.
- **User decisions:**
  - recommend a brain outside the repository;
  - `brain-update` stops and explains rather than writing around the refusal;
  - fix `brain-implement`'s worktree mode in this change.
- **Fixed from the review:** the location saved from a worktree covers only that worktree, and the reply says so (I1). A tracked first-run brain goes at the worktree root (I3). A saved location with no `00_index.md` makes it ask instead of starting a first run (I4). The git checks run from the checkout root (M1). A tracked `CLAUDE.local.md` gets the line handed to the user (M2). The README parenthetical is gone (M8).
- **Not acted on:**
  - **I2:** a new `CLAUDE.local.md` stops Claude Code from reading `AGENTS.md`. The install puts `CLAUDE.md` at the root, so that fallback is already off.
  - **M3–M7** are deferred.

S43 and S44 test the isolation handling. RED used the skills from before this fix pass:

- **S43: failed 3 of 3.** Each planned the brain for the main checkout and asked the git-tracking question, with no word about the isolation.
- **S44: failed 3 of 3.** Each asked the worktree question with no warning and added the worktree after the follow-up. Two then wrote the plan header in the main checkout. The tester deleted the third run's fixture before it finished, so it never reached the header.

`brain-implement` grew from 1,795 to 1,859 words. **Ruling:** cap raised from 1,800 to 1,860.

GREEN:

- **S43: passed 3 of 3.** Each stopped before investigating, wrote nothing, and named both ways forward. One said: "I won't write the brain elsewhere or work around the refusal with shell commands."
- **S44: passed 2 of 3; the third passed criteria 1 and 2.** None created a worktree. Each gave the reason and offered to move the brain or work without a worktree. The third edited the impl plan while reconciling, before the startup questions. That is the known S16 criterion 2 issue. It also wrote `Workspace: worktree requested (not yet created…)` into the header.
- **Regression (one sample each):**
  - **S41: pass.** It also said the line "covers only that worktree".
  - **S16:** criteria 1 and 3 pass. Criterion 2 fails on the known reconciliation edit.
  - **S11: pass**, after a harness note. Its first attempt hit the tester's own guard on compound shell commands, which it took for isolation and stopped. The note told it the session wasn't isolated.

### Distill without preserving the original format, 2026-11-08

The user decided that preserving information and accuracy matters more than preserving the original format, because keeping the format can leave a document disorganized. S45 ran on the standard tier.

- **RED: failed 3 of 3** (criterion 3). The skill at that point had the user's edits to Purpose and priorities, but rule 1 still said to preserve the original structure. Each run kept every original section, so the retry details stayed spread over five sections: jitter under Error Handling, the 4xx rule in the FAQ. All three kept every fact and the 5-vs-3 conflict.
- **The change:**
  - rule 1, "Preserve Original Formatting and Structure", is removed;
  - links, anchors, and referenced numbering moved to Traceability;
  - the output requirement is now "Organize it for clarity … the original headings, order, and layout are not binding";
  - final check 4 now asks that each condition, qualifier, and value stays attached to its fact after restructuring.
- **GREEN: passed 3 of 3.** Each put the backoff, jitter, error rules, and the count conflict in one "Retry behavior" section. Each kept the table, every exact value, and the circuit breaker marked as not built. No run added a summary, and the source was unchanged.

### Split into brain-init and brain-update, 2026-11-08

The user asked for:
- `brain-init` to set up the brain, stop when one already exists, and use a valid brain path it's given;
- `brain-update` to tell the user to run `brain-init` first, and stop, when no brain exists.

Calls I made:
- A path with no `00_index.md` is reported as not a brain, and `brain-init` stops.
- `brain-init` given a valid path saves it and doesn't sync; it points to `/brain-update`.
- The root-file rules (§3), ADRs (§4), and templates stay in `brain-update`, and `brain-init` reads them there.

All runs used the standard tier.

- **RED, S46: failed 3 of 3.** `brain-update` with no brain started a first run each time: it read the README, the code, and the tests, then asked the git-tracking question. `brain-init` is new, so S47 and S48 have no baseline.
- **GREEN:**
  - **S46: passed 3 of 3.** Each said no brain was found, named `/brain-init`, and stopped. None created anything or read the code.
  - **S47: passed 3 of 3.** Each said where the existing brain is and stopped, and the brain was byte-identical afterward.
  - **S48: passed.** It said the folder isn't a brain and wrote nothing.
  - **S41 (now `/brain-init <path>`): passed.** It saved the line, kept the British-spelling line, and excluded the file. It noted the line covers only that worktree, left the brain unchanged, and pointed to `/brain-update`.
- **Regression (one sample each):**
  - **S1 (now `brain-init`): pass**, on all 10 criteria, with moves and the interview.
  - **S2, S3 and S43: pass.**
  - **S4 and S11: failed first.** With no isolation in the context, both stopped as an "isolated linked worktree". They took any linked worktree for isolation, and the tester's own session really is isolated.

    The fix in both skills: a session is isolated only if it was started with `claude --worktree`, or entered the worktree you are working in with `EnterWorktree`. A linked worktree alone is not isolation. After the fix:
    - S43 still stops.
    - S4 and S11 got past that check, then hit the tester's guard on compound git commands, which subagents of an isolated session inherit. After a harness note saying so, both passed.

**Final review, strongest tier: "ready with fixes".** Fixed:
- **I1:** a stale `Project brain:` line now names `CLAUDE.local.md` and gives both ways out.
- **I3:** `brain-init` again never edits other skills' documents beyond moving them and fixing links.
- **I4:** `brain-init` names `brain-update/SKILL.md` by path and says to read it, not invoke it.
- **M1:** a bad location the user gives to `brain-update` stops it.
- **M2:** both skills define a brain the same way.
- **M3:** "from a session in the main checkout" added.
- **M4:** the steps for a new brain outside the repository added.
- **M5:** the `brain-init` description narrowed.
- **M6:** a calling skill continues without a brain.
- **M7:** README aligned.
- **I2** (a saved location and a local brain both present) was tested first. **S49 RED passed 2 of 2:** `brain-implement` used the saved brain over the local one with the current preamble. So the 11 preambles are unchanged, and `brain-init` now says when a saved location overrides a local brain.
- **M8** (a partial `.brain/` in a worktree) is deferred.

After the fixes, one sample each:
- **S7: pass.**
- **S13: pass (3/3).** It kept the draft note and relinked the README.
- **S46, S47 and S48: pass.** S48 also gave the steps for a brain outside the repository.
- **S50 (new): criterion 1 passes.** It named `CLAUDE.local.md` and both ways out. Criterion 2 fails strictly: it ended by asking which way the user wants, though it created and changed nothing.

### Pending brain changes, RED, 2026-11-08

These runs used the skills before the change and the standard tier. They were started from a session that wasn't isolated in a worktree, so test agents didn't inherit the tester's git guard.

- **S51: failed 3 of 3.** On `feature/cue-points`, each run synced the branch into `02_features.md` and `04_data_model.md` as fact. Each set `Last synced` to `<B>`, wrote no pending file and no `Main branch:` line, and marked cue points done. Criterion 3 passed: each recorded seconds-as-floats in `09`.
- **S52: criterion 1 failed 3 of 3.** No run listed pending changes at the start. All three left the unmerged pending file alone, synced `--version`, and set `Last synced` to `HEAD`.
- **S53: failed 3 of 3** (criteria 2 and 3). Without any skill text for it, each run applied the pending notes after checking them against the merged code, and left out `position_ms`. But none asked whether to keep or drop the unconfirmed entry, and none deleted the pending file ("can be deleted").
- **S57: criterion 1 failed 3 of 3.** Two runs took "merged" at its word on the feature branch and synced it into the root files. One asked whether to sync the branch "as though it has landed".
- **S54: failed criterion 1.** There was no reminder, and the run never checked whether `old-idea` exists. It kept the file.
- **S55 and S11: failed.** On a feature branch, `brain-init` started a first run and asked the git-tracking question.
- **S56: passed.** `brain-implement` read `pending/feature--cue-points.md` with the current preamble. Task 5 (the preamble line) is skipped.
- **S4 (revised): failed criterion 2.** On `wt`, it synced `--version` into `02_features.md` as "not merged" and set `Last synced` to the `wt` commit.
- **S12 (revised): failed criterion 2.** It noticed the sync came from a commit only on `wt`, but kept `--version` in `02_features.md`, labelled, instead of moving it to `pending/wt.md`.

### Pending brain changes, GREEN and regression, 2026-11-08

Standard tier, from a session not isolated in a worktree.

- **Finding from the first GREEN batch.** With no `origin/HEAD`, the skills fell back to "the current branch" as the main branch, which on `feature/cue-points` is the feature branch. Every run noticed and used the local `main` instead, so S51, S52, S53 and S57 passed only by correcting the skill. Fixed in both skills: `origin/HEAD`, else a local `main` or `master`, else the current branch. Every later run used the fixed copy.
- **GREEN:**
  - **S51: passed 4 of 4** (three before the fix, one after). Each wrote `pending/feature--cue-points.md`, left `02` and `04` without cue points, left `Last synced` at `<A>`, recorded seconds-as-floats in `09`, listed cue points in progress with a link, and added `Main branch: main`.
  - **S52: passed 3 of 3.** Each listed the pending file first, left it byte-identical, and synced `--version`. One miscounted the entries (2 for 3).
  - **S53: passed 3 of 3.** Each applied the confirmed entries, reported `position_ms` as not in the code, and asked keep or drop. After "Drop them." each deleted the pending file, marked cue points done, and removed the index row.
  - **S57: passed 3 of 3.** Each listed the pending file, said merges are applied from the main branch, and wrote nothing.
  - **S54: passed.** It listed `old-idea` as "branch not found", and kept the file.
  - **S55: passed.** It stopped on `feature/x`.
  - **S56: failed once, then passed 3 of 3.** RED had passed 1 of 1, so Task 5 was skipped. The first GREEN run read `state.md` and listed `pending/`, but didn't read the branch's file. With the preamble line added to the 11 skills ("also read `pending/<branch>.md`, a `/` written `--`"), all three runs read it, and two flagged the planted `position_ms` conflict.
- **Regression (one sample each):**
  - **S4 (revised): pass.** `--version` went to `pending/wt.md`, and `02` and `Last synced` were unchanged.
  - **S11 (revised): pass.** It stopped on `wt`, and created no brain.
  - **S12 (revised): pass.** It said the brain was synced from `wt`, moved `--version` to `pending/wt.md`, and set `Last synced` to `main`'s `HEAD`.
  - **S2, S5, S46 and S47: pass.**
  - **S1: pass** on all 10 criteria, with `Main branch: main` in the new index. It took the users from the purpose answer and didn't ask about them separately.

### Counters added to the skill

These come from the baseline failures:
1. Default to untracked, and present it as the default.
2. Ask exactly one question per message, and never ask process questions the skill already answers (spikes vs. open questions, exclude vs. `.gitignore`).
3. The interview is mandatory. Do not fill purpose, users, non-goals, or roadmap from defaults. Ask until the answer is "I don't know", then record it as open.
4. Use the exact header lines `Last synced: <40-char sha> (<date>)` and `Git: ignored|tracked`. When untracked, write `info/exclude`.
5. A move the user approved is a move: no copies, and don't ask twice.
6. When invoked by another skill and no brain exists, do nothing and point to `/brain-update`.
7. Read-only outside `.brain/`. Don't run the project's code or tests; record facts that need an experiment in `spikes.md`.
8. Don't edit documents other skills own (impl plans, specs, tickets). Report needed changes instead.
