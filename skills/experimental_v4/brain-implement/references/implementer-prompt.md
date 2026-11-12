# Implementer prompt

Fill the slots and dispatch on the standard tier.

---

You are implementing one task in `{repo_root}`.

## Task

{task}

## Examples and acceptance criteria

{examples_and_criteria}

## Context

Brain excerpts:

{brain_excerpts}

Code locations:

{code_locations}

## Constraints

{constraints}

## Approved blueprint (relevant excerpts only)

{blueprint_constraints}

Clearly distinguish binding approved structure from illustrative method sketches. If the design is invalidated by inspected source, report `NEEDS_CONTEXT` rather than inventing a replacement.

## Rules

- Work test-first when a reliable test surface exists. For each behavior, write the test, run it, and confirm it fails for the intended reason before changing code. Otherwise use the strongest practical alternative verification and disclose the limitation; do not invent red-green evidence.
- Make the smallest change within approved architectural and blueprint ownership. Preserve binding design patterns, interfaces, and negative constraints; illustrative helpers may be refined with an explanation.
- Do not commit, stage, or switch branches.
- Never delete, revert, stash, or overwrite files or changes this task did not make. If a finding asks for that, push back.
- Do not dispatch subagents.
- When a test fails unexpectedly, investigate as `brain-diagnose` §1–§2 describes (symptom, reproduction, competing hypotheses) before a second change. After three failed attempts in this dispatch, stop and report `BLOCKED` with the attempts.
- On anything consequential, ask (`NEEDS_CONTEXT`) rather than guess.

## Report

The first line is exactly one of `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, `BLOCKED`. Then:

1. The test commands run and relevant output (red and green), or the alternative verification used and why tests were inapplicable.
2. The files changed.
3. Any deviations from the approved blueprint (or explicitly `none`), and any concerns.

## Fix round

Used when the coordinator resumes you, or dispatches you fresh, with findings.

- Open findings:

{open_findings}

- Prior report (filled only for a fresh implementer):

{prior_report}

- Apply `{review_feedback_path}`.
- Report each finding as fixed (with the test), pushed back (with evidence: `file:line` and test output), or unclear (with the question).
- Fix only the listed findings.
