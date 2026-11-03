# Brain Skill Scenarios

Behavior tests for the `brain-*` skills, following superpowers:writing-skills. Each scenario runs a fresh general-purpose subagent in a throwaway fixture git repo. **Baseline** runs get only `tests/brief.md` (the user's original request). **Skill** runs get the skill. A scenario passes when every pass criterion holds, judged from the agent's replies and the fixture's files and git state.

Paths below are relative to the repository root. `T` = `skills/experimental_v4/tests`, `<RUN>` = `T/.runs/<scenario>-<baseline|skill>`. Fixture runs are git-ignored and deleted after use.

## Building fixtures

Fixtures are the sample app `crate` (a Python CLI for DJs). Build them with plain commands. The worktree guard refuses to run helper scripts, so there is no build script.

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
  && sed -i '' 's/__A_SHA__/<A>/' <RUN>/.brain/00_index.md <RUN>/.brain/impl_plans/01-bpm-filter.md \
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

_Added in Task 5._

## S5: Missing sync commit

_Added in Task 5._

## S6: Oversized root file

_Added in Task 5._

## S7: Partial folder, first run

_Added in Task 5._

## S8: brain-write-spec

_Added in Task 6._

## S9: brain-implement resume

_Added in Task 7._

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
