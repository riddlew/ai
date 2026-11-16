---
name: brain-diagnose
description: Investigate software failures through observable evidence and discriminating hypotheses, applying a bounded verified repair only when authorized. Use when a bug, failing test, intermittent failure, production symptom, or regression needs explaining before it is fixed.
---

# Diagnose

Find the cause of a real symptom with **minimal discriminating evidence**, then fix only when authorized. A diagnosis request does not itself authorize a repair.

## Workflow

1. Establish expected/observed behavior, environment, inputs, branch, `git status`, repeatable reproduction or best available baseline. Read governing specs, code, callers, tests and relevant technical knowledge.
2. Maintain a leading causal hypothesis and credible alternatives. Use the smallest safe experiment that distinguishes them; record prediction, result, limitations and confidence. Fix invalid test conditions before interpreting results.
3. Trace faulty values to their origin across component boundaries; prefer corrections at the root cause. For flaky runs use dedicated isolation methods; for deep call chains use causal tracing.
4. If fix is authorized, add a failing regression test where possible, make a minimal change, verify and inspect diff. **After three failed fix attempts on one symptom, stop changing code and report** evidence, attempted fixes and remaining uncertainty. A consequential design/API/ownership change needs user approval.
5. Report symptom, cause/confidence, fix or proposal, tests and attempts. In diagnosis-only mode, confirm source files weren't changed. Save a durable report only when useful/required at `.brain/diagnoses/<NN>-<short-slug>.md` via `brain-tool doc new --kind diagnosis`; invoke `brain-update` after authorized recorded changes.

**Read when needed:** `${CLAUDE_SKILL_DIR}/references/diagnose-details.md` for complete evidence templates, flaky-failure methodology, causal tracing and defense-in-depth; also see `tracing.md`, `flaky-failures.md`, `defense-in-depth.md`.
