# Running hierarchical agent behavior scenarios

Three scripts support the H1–H11 scenarios in `tests/hierarchical-scenarios.md`. **CI runs none of them against an agent**; static contract tests only check that fixtures build as described.

| Script | Does | Agent? |
|---|---|---|
| `prepare_hierarchical_scenario.py` | Builds one scenario fixture and prints where to launch the agent, its skill, context, and trigger | no |
| `run_hierarchical_scenario.py` | Exports skill arms, builds a fresh fixture per sample, runs a fresh `claude -p` session with scripted follow-ups, and stores evidence | yes |
| `grade_hierarchical_run.py` | Checks the mechanically verifiable criteria of recorded runs; prints `CHECK` for judgement calls | no |

## One fixture by hand

From the repository root:

```bash
python skills/experimental_v4/tests/prepare_hierarchical_scenario.py H6B "$(mktemp -d)/repo" \
  --policy skills/experimental_v4/brain-init/references/CLAUDE.local.md
```

Use a new destination for every sample. The committed tree is reproducible (fixed identity and dates); the brain is ignored; `CLAUDE.local.md` is installed untracked from `--policy`. H10 prints `Launch: claude --worktree h10`: start the session from the fixture's main checkout with that flag so Claude Code isolates it in the pre-built worktree. H10C/H10D also print an external brain directory to pass with `--add-dir`.

## Low-usage pilot before RED/GREEN

```bash
W=$(mktemp -d)
python skills/experimental_v4/tests/run_hierarchical_scenario.py export-arm main $W/arms/red
python skills/experimental_v4/tests/run_hierarchical_scenario.py export-arm feature/hierarchical-brain $W/arms/green
python skills/experimental_v4/tests/run_hierarchical_scenario.py batch $W/evidence \
  --arm red=$W/arms/red --arm green=$W/arms/green --jobs H3:green:1
python skills/experimental_v4/tests/grade_hierarchical_run.py $W/evidence/*
```

Arms are exported without `tests/` and `IMPLEMENTATION_PLAN.md`, and agents may read (not edit) the arm and the fixture's main checkout. Keep the evidence folder outside any fixture's parent directories. A run whose transcript references the scenarios file, the source repository, the evidence folder, or another run is void. A run whose turn ended in an error (for example a usage limit) is void and must be rerun; the batch stops launching new samples after a usage-limit error.

**Limitations:** the example app is in memory, not a TCP server. Scenario decisions are illustrative. A passing structural fixture does not show that StartMachine was implemented.

## Usage safeguards

The batch runner is now a **dry run by default**. A paid agent session requires the explicit `--execute` flag. It runs exactly one Sonnet session at a time, with no nested subagents, 30 tool steps per message (`--max-turns` caps steps within a message, not follow-up messages; recorded runs used 11–25), five minutes per message, an estimated $1 per invocation, and a $2 per-sample estimated ceiling for scripted follow-ups. Limits are not guarantees about your five-hour subscription quota. Start with only one GREEN scenario; inspect recorded evidence before authorizing any more runs. Avoid full RED/GREEN batches until important regressions justify that cost.

A single bounded pilot can be started with `--jobs H3:green:1 --parallel 1 --model sonnet --max-budget-usd 1 --sample-budget-usd 2 --max-turns 30 --timeout 300 --execute`. Omitting `--execute` only previews the job.
