# Brain Skill Scenarios

Behavior tests for the `brain-*` skills, following superpowers:writing-skills. Each scenario runs a fresh general-purpose subagent in a throwaway fixture git repo. **Baseline** runs get only `tests/brief.md` (the user's original request). **Skill** runs get the skill. A scenario passes when every pass criterion holds, judged from the agent's replies and the fixture's files and git state.

Paths below are relative to the repository root. `T` = `skills/experimental_v4/tests`, `<RUN>` = `T/.runs/<scenario>-<baseline|skill>`. Fixture runs are git-ignored and deleted after use.

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

- **Fixture:** fresh
- **Context:** none
- **Trigger:** The user says: "/brain-update"
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
   - `.brain/00_index.md` has `Last synced: <HEAD sha>` and `Git: ignored`;
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
2. The reply says no brain exists and that `/brain-update` sets one up.
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
2. `<RUN>/.brain/02_features.md` mentions `--version`.
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
- **Context:** none
- **Trigger:** The user says: "/brain-update"

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
- **Trigger:** The user says: "/brain-update"
- **Answers:**
  1. To the git-tracking question: `No, don't track it.`
  2. Then: `I don't know yet; record everything else as open and create the brain now.`

**Pass criteria**

1. `<RUN>/.brain/00_index.md` exists.
2. No `.brain/` exists in `<RUN>-wt`.

## S12: Brain last synced from another branch (review I3)

- **Fixture:** synced, plus a `wt` worktree with S4's `--version` commit. Then, in the main fixture:
  - set `Last synced` to the `wt` commit;
  - append `- \`--version\` — prints \`crate 0.1.0\`.` to `.brain/02_features.md`.

  This simulates a sync that was run from `wt`. `<FIXTURE>` is `<RUN>` (on `main`).
- **Trigger:** The user says: "/brain-update"

**Pass criteria**

1. The reply says the brain was last synced from a commit that isn't in this branch's history.
2. `.brain/02_features.md` still mentions `--version`.

## S13: First-run move conflict and links (review I4, I5)

- **Fixture:** fresh, but before commit A:
  - append `See [the storage decision](docs/adr/0001-use-sqlite.md).` to `README.md`.

  After commit A:
  - copy `docs/specs/01-bpm-filter.md` to `.brain/specs/`;
  - append `Draft note: E3 pending.` to the copy.
- **Trigger:** The user says: "/brain-update"
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

### S15 coverage table, 2026-11-04

- **Before the change: fail.** Requirement Fit listed findings R1–R3 only. E1 appeared only in prose ("E1 still passes"), with no row per Example and no met count in the summary.
- **After the change: pass (4/4).**
  - The table had E1 marked `met` (`crate/cli.py:9`, no test, reproduced) and E2 marked `unmet` (R1).
  - The summary read `Requirement fit: 1/2 met, 3 findings`.

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
