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

Follow-up turns go to the same subagent through SendMessage, containing only the user's answer.

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

_Baseline and skill results, with failures quoted verbatim._
