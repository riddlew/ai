# Reliability evaluation

This branch implements the initial measurement and coverage layer, not a claim that changed agent behavior is effective.

- `behavioral-coverage.json` inventories rules, existing scenarios and explicit gaps.
- `routing-cases.json` defines unrun ambiguous routing probes. Current hierarchical agent fixtures preselect the skill and cannot establish routing accuracy.
- `check_behavioral_coverage.py` validates scenario references and reports missing scenario coverage.
- `summarize_agent_evidence.py` summarizes actual recorded Claude runs, distinguishing potentially gradable executions from errors and skipped follow-ups. It does not assign pass/fail grades.
- `test_behavioral_coverage_contract.py` and `test_agent_evidence_contract.py` check only the static measurement contracts.

## Static checks

```bash
python -m unittest discover -s skills/experimental_v4/tests -p 'test_*_contract.py' -v
python skills/experimental_v4/tests/check_behavioral_coverage.py --json
```

## Real agent testing

The existing runner in `tests/run_hierarchical_scenario.py` requires the explicit `--execute` flag to incur agent usage. Run against fresh fixture directories outside the repository, with fixed model and prompt configuration. Retain raw logs, diff snapshots and the true review base. Review leakage of scenario criteria and declare contaminated runs void. After collecting runs:

```bash
python skills/experimental_v4/tests/summarize_agent_evidence.py /path/to/evidence --json
python skills/experimental_v4/tests/grade_hierarchical_run.py /path/to/evidence/H6B-candidate-1
```

Agent success requires criterion-level grading of actual files, outputs and Git state. Three independent valid runs is a minimum for a general descriptive claim, not evidence of 95% reliability. The existing hierarchical runner tests explicit skill invocation and is not suitable for routing accuracy until it gains a no-preselection mode.

## Remaining work, ordered by risk

1. Add fresh-agent scenarios for approval continuation scope, stale binding blueprint and unapproved ownership deviations.
2. Run independent no-preselection routing cases and compare real agent decisions with `routing-cases.json`.
3. Profile Brain synchronization token/tool costs and actual information gains on realistic fixtures.
4. Test whether agents load necessary references and avoid irrelevant ones.
5. Modify skill instructions only where repeated RED runs reveal failures; verify GREEN behavior and old regression scenarios.

**Current evidence:** static coverage inventory and summary tooling only. No new agent behavior evaluations have been executed on this branch.
