---
name: brain-test-skill
description: Test whether a skill changes what an agent does, by running it on scenarios in fresh agents. Use when asked to test whether a skill's rule holds, or before claiming that a new skill or a change to a skill's behavior works.
---

# Test a skill

A **skill test is a fresh agent acting in a throwaway fixture**, scored against explicit observable criteria. A reading is a review, not a test. Never claim a rule holds based on reading or one sample.

1. Specify the behavior, pressure and expected failure. Use existing scenario formats/fixtures; for a changed skill compare a **RED baseline** with a **GREEN modified** arm using the same trigger, model, wrapper and checkable criteria.
2. Write scenario pass criteria *before* any agent run. Isolate fixtures/agent outputs from criteria and other runs. A pressure scenario must cause the agent to act, not just answer what it would do.
3. Dispatch one fresh agent per run with an explicitly selected model tier; do not allow unrelated skills to satisfy the test. If no agent runner is available, report **No test run** and offer a labeled static review instead.
4. Grade actual replies, files and Git state; mark unseen behavior **unverified**. An agent that accessed hidden criteria is a void sample. One run is not a frequency estimate: require **three or more samples** before claiming a behavior generally holds/fails; narrow regression reruns may use one sample.
5. If RED already passes, strengthen pressure once; if GREEN fails, revise the failure mechanism and rerun. Report model, samples, evidence, RED/GREEN outcomes, prior-scenario regressions and limitations. Never invent run results or commit unrequested edits.

**Read when needed:** `${CLAUDE_SKILL_DIR}/references/scenario-format.md` and `${CLAUDE_SKILL_DIR}/references/skill-testing-details.md` for fixture setup, red-flag analysis, runner limits, grading and full report shape.
