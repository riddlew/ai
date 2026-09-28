---
name: diagnose
description: Diagnose a software failure using reproducible evidence and competing hypotheses, then write a durable diagnosis artifact. Use for bugs, failing tests, production symptoms, intermittent behavior, or regressions that need root-cause analysis and an authorized bounded fix.
---

# Diagnose

Find the cause of a software failure through evidence rather than speculative fixes.

Use `$ARGUMENTS` as the symptom, reproduction, or debugging scope when provided.

## Result Artifact

Before diagnosing, locate the nearest project `.claude/` directory from the working directory up to the repository root. Do not use the personal `~/.claude/` directory.

- If no project `.claude/` directory exists, ask the user where to save the result before continuing. Do not create `.claude/`, choose another location, or skip the artifact without their answer.
- Resolve the work-item directory as `.claude/results/<ISSUE-ID>/` from an explicit ticket or issue ID. Without one, use a matching existing work item or create `.claude/results/<NNN>-<short-slug>/` with the next unused three-digit sequence.
- Read available investigation, combined plan, implementation, review, and verification artifacts for context, then recheck relevant claims against current repository and runtime evidence.
- Write a new append-only result at `diagnoses/<NN>-<short-slug>.md`, using the next unused two-digit sequence. Do not overwrite an earlier diagnosis.
- Put the work-item key, stage, status, updated date, repository revision or working-tree state, and input artifact paths in YAML frontmatter. Put evidence, hypotheses, experiments, outcome, and unresolved questions in the body.
- Report the artifact path to the user.

## Workflow

1. State the observed symptom precisely, including expected versus actual behavior.
2. Establish a reliable reproduction or another observable baseline. Record the relevant environment, inputs, and commands.
3. Gather logs, traces, state, code paths, recent changes, and test results before editing. Separate confirmed facts from inferences.
4. Record the leading hypothesis and credible competing hypotheses. For each, identify the evidence that supports or weakens it.
5. Run the smallest experiment that distinguishes among the hypotheses. Change one meaningful variable at a time.
6. Update or reject hypotheses from the result. Do not stack speculative fixes.
7. If a fix is authorized, make the smallest correction consistent with the confirmed cause and existing task boundary. If the user asked only for diagnosis, do not modify code.
8. Add or strengthen a regression test where practical, then rerun the original reproduction and relevant surrounding checks.

Stop and report the conflict if the confirmed cause requires a material redesign, broader scope, new authority, or a change to an unapproved public or persisted contract.

## Output

Write and report:

- symptom and reproduction;
- evidence gathered;
- leading and competing hypotheses;
- experiments and results;
- confirmed or best-supported cause, with confidence;
- bounded fix, only when authorized;
- regression evidence and remaining uncertainty.

Do not claim root cause when the evidence only establishes correlation.
