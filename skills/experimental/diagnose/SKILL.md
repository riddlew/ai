---
name: diagnose
description: Diagnose a software failure using reproducible evidence and competing hypotheses, then write a durable diagnosis artifact. Use for bugs, failing tests, production symptoms, intermittent behavior, or regressions that need root-cause analysis and an authorized bounded fix.
---

# Diagnose

Find the cause of a software failure through reproducible evidence rather than speculative fixes.

Use this skill for:

- bugs;
- failing tests;
- production symptoms;
- intermittent behavior;
- regressions;
- other failures requiring root-cause analysis.

Diagnosis and repair are separate activities. Do not modify code unless the user has authorized a fix.

## Define the failure

Start by stating the observed symptom precisely.

Establish:

- expected behavior;
- actual behavior;
- relevant inputs or triggering conditions;
- environment or configuration that may affect the failure;
- the boundary of the investigation.

Avoid beginning with a presumed cause.

## Establish a baseline

Create a reliable reproduction when possible.

Record enough information to reproduce or observe the failure again, including relevant:

- commands;
- inputs;
- environment;
- configuration;
- test cases;
- runtime conditions.

For intermittent or production-only failures where deterministic reproduction is unavailable, establish another observable baseline that can distinguish successful from failing behavior.

## Gather evidence

Collect relevant evidence before editing the system.

Inspect only what is needed to understand the failure, such as:

- logs and traces;
- runtime state;
- failing tests;
- relevant code paths;
- configuration;
- recent changes;
- persisted data;
- dependency behavior.

Keep confirmed observations separate from interpretation.

Recheck prior documentation, earlier diagnoses, or reported assumptions against the current repository and runtime evidence before relying on them.

## Build competing hypotheses

Record the leading explanation and any credible alternatives.

For each hypothesis, identify:

- what evidence supports it;
- what evidence weakens it;
- what observation would distinguish it from competing explanations.

Do not prematurely collapse the investigation to one explanation merely because it appears plausible.

Do not stack speculative fixes in an attempt to discover the cause indirectly.

## Run discriminating experiments

Choose the smallest experiment that meaningfully separates competing hypotheses.

Change one meaningful variable at a time when practical.

For each experiment, record:

- what was tested;
- what result was expected under the relevant hypotheses;
- what actually occurred;
- how the result changes the hypothesis set.

Update, weaken, or reject hypotheses based on observed results.

Continue until the evidence supports a cause strongly enough to justify the conclusion, or until available evidence is insufficient.

Do not claim root cause when the evidence establishes only correlation.

## Apply a bounded fix when authorized

If the user authorized repair:

1. make the smallest correction consistent with the best-supported cause;
2. keep the change inside the established task boundary;
3. add or strengthen a regression test when practical;
4. rerun the original reproduction;
5. run relevant surrounding checks to detect regressions.

If the user requested diagnosis only, do not modify code.

Stop and surface the conflict when the confirmed cause requires:

- material redesign;
- substantially broader scope;
- additional authority;
- changing an unapproved public contract;
- changing an unapproved persisted or serialized contract.

Do not quietly expand the fix beyond the authorized boundary.

## Write the durable diagnosis

Every diagnosis produces a new append-only Markdown artifact under:

```text
docs/diagnoses/
```

Use filenames shaped like:

```text
<NN>-<short-slug>.md
```

Before creating the file:

1. inspect existing diagnosis filenames in `docs/diagnoses/`;
2. find the highest valid numeric prefix;
3. increment it;
4. zero-pad consistently with existing files, or use two digits when no convention exists.

Create `docs/diagnoses/` only when the first diagnosis is written.

Never overwrite or replace an earlier diagnosis.

Choose a concise slug describing the failure being investigated.

## Diagnosis structure

The diagnosis must contain:

## Symptom

Describe the observed failure and the expected versus actual behavior.

## Reproduction or Baseline

Record the reproduction procedure or other observable baseline, including relevant environment, inputs, and commands.

## Evidence

Record confirmed observations gathered from the repository, runtime, tests, configuration, logs, or other relevant sources.

Keep factual evidence distinct from interpretation.

## Hypotheses

Record the leading and credible competing hypotheses, including evidence that supports or weakens each one.

## Experiments

Record the experiments performed, their results, and how those results changed the hypotheses.

## Cause

State the confirmed or best-supported cause and the confidence in that conclusion.

If the evidence does not establish root cause, say what is known without overstating certainty.

## Fix

Include this section only when a fix was authorized.

Record the bounded correction that was made and why it addresses the supported cause.

## Regression Evidence

Record the original reproduction result after the fix and any relevant surrounding validation.

If no fix was performed, record any tests or observations that strengthened the diagnosis.

## Remaining Uncertainty

Identify unresolved questions, missing evidence, intermittent conditions, or alternative explanations that have not been eliminated.

Report the created diagnosis path to the user.