---
name: brain-test-skill
description: Test whether a skill changes what an agent does, by running it on scenarios in fresh agents. Use when asked to test whether a skill's rule holds, or before claiming that a new skill or a change to a skill's behavior works.
---

# Test a skill

A skill is tested by running it. A test is a fresh agent, a throwaway fixture, a trigger, and pass criteria checked against what the agent did: its replies, the files, the git state. Reading the skill finds wording gaps; that is a review. Never report a reading as a test result, and never conclude from one that a rule "holds".

Follow `CLAUDE.local.md` for decisions requiring consultation. This skill dispatches test agents; it changes no skill text unless the user asked for a change.

## 1. Define the test

- Name the behavior under test and the failure it guards against. The kind of rule sets the scenario:
  - a discipline rule (something an agent may skip when it is costly): pressure scenarios;
  - a technique: apply it to a case the skill doesn't show;
  - reference material: find and use a fact from it.
- Find the project's scenarios file (for example `tests/scenarios.md`) and reuse its fixtures, prompt wrapper, and criteria style. If none exists and you are changing a skill, create `tests/scenarios.md` next to the skills folder and say where.
- For a change, the test has two arms: RED runs the current skill (or no skill, for a new one); GREEN runs the changed skill. Both use the same scenarios, model tier, and wrapper.
- A change that can't alter what an agent does (a heading, a typo, a link) needs no run; say so.

## 2. Write the scenarios before any run

Use `${CLAUDE_SKILL_DIR}/references/scenario-format.md` for the scenario fields, the prompt wrapper, and the pressure types.

- Write each scenario's pass criteria first. Each criterion is checkable from the reply, the files, or the git state.
- For a discipline rule, combine three or more pressures in the context and trigger, and make the agent act in the fixture. "What would you do?" tests recall, not behavior.
- Build fixtures as throwaway git repos with plain commands, and record the build in the scenarios file.
- Keep criteria and tester notes out of the test agent's reach: not in the fixture, and not in a folder above it. When the scenarios file sits near the fixtures, build each run in a fresh `mktemp -d` directory.

## 3. Run

- Dispatch one fresh subagent per run, and name its model explicitly. Use the tier of the role being tested in `CLAUDE.local.md`; standard unless the table maps that role to strongest.
- Tell the test agent to use only the skills named in its prompt and the skills they mention, so another installed skill can't stand in for the one under test.
- Send follow-up turns to the same agent, prefixed `The user replies:`.
- Run RED before GREEN, and before any edit to the skill under test.
- If you have no subagent tool, say the skill can't be tested in this session. Offer a reading instead, labelled as a review.

## 4. Judge

Grade each criterion from evidence you saw: the agent's words, `git status`, the files. A criterion you couldn't check is `unverified`, not passed. Read each test agent's file list: a run that read the scenarios file or another run's folder is void, so discard it and rerun.

One run shows what can happen, not how often. Before saying a rule holds or fails, run its scenario three or more times and report the split (for example, held in 2 of 3). Regression reruns may use one sample each.

- **RED passes** (the baseline already complies): there is no failure to fix. Strengthen the scenario once, with more pressure or a harder case, and rerun. If it still passes in three or more samples, tell the user the current skill holds, and ask before adding text.
- **RED fails, GREEN passes:** the change works for that scenario. Then rerun the earlier scenarios that cover the same skill. The change isn't verified until they pass.
- **GREEN fails:** revise and rerun the same scenarios. Match the fix to the failure:
  - a rule skipped under pressure: name the exact rationalization in a red-flags row;
  - a missing element: add a slot to the template the agent fills in;
  - output with the wrong shape: describe the right shape instead of listing what not to do.

## 5. Report

Report in the conversation. When you changed a skill, also record the results in the scenarios file's Results section with the date; for a test only, offer to record them. For each scenario give:

1. the trigger and the pressures used;
2. the criteria;
3. the runs: RED or GREEN, the model, and the number of samples;
4. pass, fail, or `unverified` per criterion, each with a verbatim quote from the test agent or the observed state;
5. for a change, the earlier scenarios rerun and their results, or `not rerun`, which leaves the change unverified;
6. the verdict, plus the next step when anything failed.

With no run, there is nothing to fill in: write `No test run` and give the reading separately, labelled as a review. Delete run fixtures after you report.

## Red flags

| Thought | Reality |
|---|---|
| "I'll read the skill and report whether it holds" | That's a review. Run a test agent. |
| "The agent clearly meant to comply" | Grade what it did, from quotes and state. |
| "One sample passed" | Run three or more before calling it. |
| "I'll summarize what the agent said" | Quote it. |
