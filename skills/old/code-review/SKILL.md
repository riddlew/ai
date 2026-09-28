---
name: code-review
description: Review a software change for correctness against requirements and repository evidence, then write a durable review artifact. Use for diffs, pull requests, completed implementations, or change sets that need defect, regression, compatibility, and test-coverage findings.
---

# Code Review

Critically review a completed or proposed change. Find actionable defects; do not rewrite the implementation or report style preferences as correctness problems.

Use `$ARGUMENTS` as the change set, ticket, requirements, or review scope when provided.

## Result Artifact

Before reviewing, locate the nearest project `.claude/` directory from the working directory up to the repository root. Do not use the personal `~/.claude/` directory.

- If no project `.claude/` directory exists, ask the user where to save the result before continuing. Do not create `.claude/`, choose another location, or skip the artifact without their answer.
- Resolve the work-item directory as `.claude/results/<ISSUE-ID>/` from an explicit ticket or issue ID. Without one, use a matching existing work item or create `.claude/results/<NNN>-<short-slug>/` with the next unused three-digit sequence.
- Read available investigation, combined plan, implementation, diagnosis, and earlier review artifacts as context. If the target is `02-plan.md`, review its design and proposed tasks against the requirements and repository rather than expecting a diff. Otherwise recheck the artifacts against the current diff and repository state.
- Write a new append-only result at `reviews/<NN>-code-review.md`, using the next unused two-digit review sequence. Do not overwrite an earlier review.
- Put the work-item key, stage, status, updated date, reviewed revision or diff boundary, and input artifact paths in YAML frontmatter. Put findings and validation gaps in the body.
- Report the artifact path to the user.

## Workflow

1. Read the requirements, approved plan, repository instructions, and the complete review target: either `02-plan.md` or the implementation diff.
2. Inspect relevant surrounding code, callers, tests, configuration, and documentation rather than reviewing changed lines in isolation.
3. Check observable behavior, edge cases, error handling, state transitions, concurrency where relevant, compatibility, and failure recovery.
4. Confirm that tests exercise the acceptance criteria and important regressions. Distinguish missing coverage from an actual demonstrated defect.
5. Trace public API, data-format, dependency, or operational changes to downstream consumers.
6. Rank findings by concrete impact and likelihood. Omit speculative concerns without a plausible failure path.
7. Do not modify code unless the user explicitly requests corrections.

## Output

Write the review artifact with findings ordered by severity. For each finding include:

- severity and concise title;
- precise file location or symbol;
- supporting evidence;
- concrete impact or failure scenario;
- recommended correction;
- confidence or missing evidence when uncertain.

Separate confirmed defects, risks, questions, and optional improvements. If no material findings remain, say so and identify any validation gap or residual risk.
