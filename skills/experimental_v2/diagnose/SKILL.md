---
name: diagnose
description: Investigate software failures through observable evidence and discriminating hypotheses, applying a bounded verified repair when authorized and retaining reports only when useful.
---

# Diagnose

Find the cause of a bug, failing test, intermittent failure, production symptom, or regression before choosing a correction. Follow root `CLAUDE.md` for decisions requiring consultation.

Diagnosis is not authorization for repair. When the user requests diagnosis only, inspect and report without changing source code. When the user authorizes a fix, routine bounded repair is authorized; obtain a further decision only for consequential scope, behavior, or architectural changes.

## 1. Establish the symptom

Describe expected versus observed behavior, relevant inputs, environment/configuration, triggering conditions, and investigation scope. Check the relevant code, tests, specs, `CONTEXT.md`, and ADRs when needed. Don't assume a root cause from the error message or treat an old diagnosis as current evidence.

Establish the smallest repeatable reproduction available. For intermittent or production-only symptoms, use an observable baseline such as a trace, log signal, or state transition; note its limits. Avoid unsafe or destructive tests in shared environments without authorization.

## 2. Investigate with competing explanations when needed

Gather relevant logs, failing paths, recent changes, dependency behavior, configuration, tests, and runtime observations. Separate facts from inferences.

Maintain a leading hypothesis and credible alternatives **only while material uncertainty remains**. For each, identify supporting/weakening evidence and the observation that would distinguish it. Do not manufacture weak alternatives when one cause is directly proven.

Run the smallest safe discriminating check. Record the prediction, actual result, and impact on the hypotheses. Fix unrelated test-harness failures before treating them as evidence. Do not stack speculative code changes to discover the cause indirectly.

State the cause as **confirmed**, **best-supported**, or **unknown**. Do not claim root-cause certainty based only on correlation. Stop when evidence is strong enough for the next action or further investigation cannot materially improve it.

## 3. Choose an appropriately bounded correction

When repair is authorized, first consider the simplest correction within existing owners, lifecycle, interfaces, and approved behavior. Add or change a structural component only if concrete evidence makes the local correction insufficient.

If a repair requires changing product/error semantics, connection or state ownership, public/persisted contracts, dependencies, approved architecture, or substantially broader scope, consult the user with the evidence, minimum approach, meaningful alternatives, tradeoffs, and recommendation **before** making that choice. Routine local edits and regression tests do not need repeated approval.

If unapproved decisions block the fix, complete the diagnosis and record what is blocked. Don't smuggle a redesign into a bug fix.

## 4. Fix and verify when authorized

1. Make the smallest coherent change supported by the diagnosed cause.
2. Add or update a focused regression test when practical.
3. Rerun the original reproduction or observational check; run relevant adjacent tests and static checks.
4. Inspect the diff for unrelated edits, duplicate ownership, accidental API changes, and needless abstractions.
5. If verification fails, return to investigation rather than adding speculative patches.

Clearly report what passed, failed, or could not be reproduced; distinguish prior failures when evidence permits.

## 5. Decide whether a durable diagnosis helps

**Routine obvious failures:** report the symptom, confirmed cause, bounded fix if any, and verification directly in the conversation. Do not create `docs/diagnoses/` entries for every small bug or failed test.

**Significant cases:** produce a durable diagnosis if the issue is intermittent, production-impacting, difficult to reproduce, repeatedly disputed, architecturally consequential, complex enough to recur, or if the user requests documentation.

When a record is warranted, create a **new append-only** file at `docs/diagnoses/<NN>-<short-slug>.md`. Inspect existing numbered names and match their padding (two digits by default), and never overwrite prior diagnoses.

Record, as applicable:

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
Only changes actually made and checks actually run, or diagnostic checks if no fix.

## Remaining Uncertainty
Open evidence gaps, risks, and limits.
```

Omit inapplicable sections where clarity improves. A diagnosis may be complete without repair. Report the diagnosis conclusion and any artifact path actually created.
