# Preparing hierarchical agent behavior scenarios

These scripts prepare fixtures and prompts; **they do not run agents**. Behavioral evidence must come from fresh Claude Code agents following `brain-test-skill` and the criteria in `tests/hierarchical-scenarios.md`.

For one sample of scenario H3, from the source repository:

```bash
python skills/experimental_v4/tests/prepare_hierarchical_scenario.py H3 /tmp/brain-h3-run-1
```

The command prints the fixture path, skill, and user trigger. Use a **new destination for every run**. The destination is a fresh Git repository initialized from `tests/fixture/start-machine-app/` with only the approved document stages needed for the chosen scenario. Do not expose `tests/hierarchical-scenarios.md` or grader notes to the test agent.

Use the `brain-test-skill/references/scenario-format.md` prompt wrapper, pointing its `CLAUDE_SKILL_DIR` at the installed skill directory. Dispatch a fresh agent, capture its reply, file changes, Git state and user-approval sequence, then record the actual results in the scenario file. H1–H8 are stage-specific workflow exercises; H9 has an invalid parent; H10 sets up a linked worktree whose main checkout contains the ignored brain; H11 includes legacy feature notes that must not be migrated. Some scenarios require additional user follow-up turns, as specified in the criteria.

**Limitations:** The example app is in-memory, not a TCP server. Some scenario decisions and source-level constraints are illustrative. The fixtures are starting points, not evidence that a complete protocol implementation was approved or tested.

Fixture setup and baseline application are checked by Python static tests in CI. **H1–H11 fresh-agent behavioral test execution and RED/GREEN comparison remain pending.**
