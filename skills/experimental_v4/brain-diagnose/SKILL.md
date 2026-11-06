---
name: brain-diagnose
description: Investigate software failures through observable evidence and discriminating hypotheses, applying a bounded verified repair only when authorized. Use when a bug, failing test, intermittent failure, production symptom, or regression needs explaining before it is fixed.
---

# Diagnose

**Project brain:** If `.brain/00_index.md` exists (at this worktree's root, or in the main checkout when working in a linked git worktree) and you have not read its root files in this session (or they were lost to context compaction), read every root `.md` file in that `.brain/` now. Read subfolders only when a root file links to them or the task needs them. Do not load `.brain` into subagents wholesale; pass only what their task needs. Write any `.brain/` document into that same `.brain/`. If no brain exists, proceed without one and mention once that `/brain-update` can create it.

Find the cause of a failure before choosing a correction. Follow root `CLAUDE.md` for decisions requiring consultation.

Diagnosis is not authorization to repair. When the user asks for diagnosis only, do not change source code. When the user authorizes a fix, routine bounded repair is authorized; consequential scope, behavior, or architectural changes still need a decision.

## 1. Establish the symptom

Describe expected versus observed behavior, relevant inputs, environment and configuration, triggering conditions, and investigation scope. Check relevant code, tests, specifications, the `.brain` root files, and ADRs. Read the full error and stack trace before forming any hypothesis. Do not infer the root cause from the error message or treat an old diagnosis as current evidence.

Establish the smallest repeatable reproduction available. For intermittent or production-only symptoms, use an observable baseline (trace, log signal, state transition) and note its limits. Do not run unsafe or destructive tests in shared environments without authorization.

## 2. Investigate with competing explanations

Gather relevant logs, failing paths, recent changes, dependency behavior, configuration, tests, and runtime observations. Separate facts from inferences.

Use these when they fit:
- **Failure crosses components, or the error is deep in a call chain:** follow `${CLAUDE_SKILL_DIR}/references/tracing.md`. Trace the bad value back to its origin and fix it there.
- **A similar path works:** list every difference between it and the failing path before forming a hypothesis.
- **Flaky or suite-only failure:** follow `${CLAUDE_SKILL_DIR}/references/flaky-failures.md`.

While material uncertainty remains, keep a leading hypothesis and credible alternatives, each with supporting and weakening evidence and the observation that would distinguish it. Do not manufacture weak alternatives when one cause is directly proven.

Run the smallest safe discriminating check. Record the prediction, the result, and its effect on the hypotheses. Fix unrelated test-harness failures before treating them as evidence. Do not stack speculative code changes to find the cause indirectly.

State the cause as **confirmed**, **best-supported**, or **unknown**. Correlation alone is not root-cause certainty. Stop when the evidence is strong enough for the next action or further investigation cannot materially improve it.

## 3. Choose a bounded correction

When repair is authorized, start with the simplest correction within existing owners, lifecycle, interfaces, and approved behavior. Change structure only when evidence shows the local correction is insufficient.

If the repair would change product or error semantics, state or connection ownership, public or persisted contracts, dependencies, approved architecture, or substantially broaden scope, consult the user first. If unapproved decisions block the fix, complete the diagnosis and state what is blocked. Do not smuggle a redesign into a bug fix.

## 4. Fix and verify when authorized

1. Remove any temporary instrumentation and confirm with `git diff`.
2. Write the failing reproduction:
   - If the project has a working test runner, write a test and watch it fail for the symptom's reason. The test file is part of the fix diff.
   - Otherwise, record the reproduction command and its failing output. Setting up a test framework adds a dependency, so consult the user first.
3. Make the smallest coherent change the diagnosed cause supports.
4. Rerun the reproduction, plus relevant adjacent tests and static checks. Inspect the diff for unrelated edits, duplicated ownership, accidental API changes, and needless abstractions.
5. Apply the three-failed-fixes rule. Count fix attempts per symptom; investigating between attempts does not reset the count. A fix fails when verification fails or it reveals a new problem elsewhere. After three failures, stop. Report the pattern, which suggests a design problem rather than a missing patch, and consult the user under root `CLAUDE.md` before a fourth attempt.

If verification fails, return to investigation instead of adding speculative patches.

Report what passed, failed, or could not be reproduced, distinguishing pre-existing failures where evidence permits.

After a verified fix, record the cause and fix in the conversation report (§5). Then invoke `brain-update` with a one-line summary of what changed.

## 5. Report

Report in the conversation: symptom, cause and confidence, the fix if any, the number of fix attempts, and verification. In diagnosis-only mode, confirm `git status` is unchanged from before the run. Add `Optional hardening (not applied):` only when the bad value crossed layers before failing; describe the option per `${CLAUDE_SKILL_DIR}/references/defense-in-depth.md`. Never apply it unasked.

If the investigation finds an environmental, timing, or external cause rather than a code defect, say what was investigated. Any proposed handling (a retry, a timeout, an error message, extra logging) needs the same consultation as any behavior change.

Write a durable diagnosis only when the user requests one or a workflow needs it for continuation.

A durable diagnosis is a new file at `.brain/diagnoses/<NN>-<short-slug>.md`: increment the highest existing number, matching its padding (two digits by default). Never overwrite a prior diagnosis. Include the sections that apply:

```markdown
# <Failure>

## Symptom
Expected and observed behavior.

## Reproduction or Baseline
Commands, inputs, environment, and limitations.

## Evidence
Directly verified facts with source locations.

## Hypotheses and Experiments
Credible alternatives, discriminating results, and what they establish.

## Cause and Confidence
Confirmed, best-supported, or unknown, with justification.

## Proposed Correction
Minimal justified repair, not an approval to redesign.

## Decisions Requiring Approval
Unresolved material alternatives and questions, if any.

## Fix and Regression Evidence
Only changes actually made and checks actually run.

## Fix Attempts
Per attempt: the change, and the result.

## Remaining Uncertainty
Open evidence gaps, risks, and limits.
```

Report the conclusion and any file path created.

## Red flags

Any of these means stop and return to §2.

| Thought or action | Instead |
|---|---|
| "Just try X and see" | State the hypothesis and the check that would test it. |
| "It's probably X" | Verify X with an observation. |
| Several changes at once | Revert to one change. |
| A fourth fix attempt | Stop under §4 step 5. |
| Fixing where the error appears | Trace the value to its source. |
| Temporary logging left in | Remove it and confirm with `git diff`. |
| Claiming behavior you did not observe | Run it, or say it is unverified. |
| The user says "stop guessing" or "is that not happening?" | Re-read the evidence and restart from §2. |
