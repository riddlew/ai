---
name: architecture-review
description: Review software architecture and the first instance of patterns before they spread, then write a durable review artifact. Use for public interfaces, persistence formats, ownership and state models, concurrency, inheritance, shared abstractions, or expensive-to-reverse structural decisions.
---

# Architecture Review

Evaluate whether a design or implementation preserves clear responsibilities and remains safe to extend. Review representative evidence before a cross-cutting pattern is propagated.

Use `$ARGUMENTS` as the architecture decision, implementation, or review boundary when provided.

## Result Artifact

Before reviewing, locate the nearest project `.claude/` directory from the working directory up to the repository root. Do not use the personal `~/.claude/` directory.

- If no project `.claude/` directory exists, ask the user where to save the result before continuing. Do not create `.claude/`, choose another location, or skip the artifact without their answer.
- Resolve the work-item directory as `.claude/results/<ISSUE-ID>/` from an explicit ticket or issue ID. Without one, use a matching existing work item or create `.claude/results/<NNN>-<short-slug>/` with the next unused three-digit sequence.
- Read available investigation, combined plan, implementation, diagnosis, and earlier review artifacts as context. If reviewing `02-plan.md`, test its proposed boundaries and abstractions before implementation. Recheck all claims against current repository evidence.
- Write a new append-only result at `reviews/<NN>-architecture-review.md`, using the next unused two-digit review sequence. Do not overwrite an earlier review.
- Put the work-item key, stage, status, updated date, reviewed revision or design boundary, and input artifact paths in YAML frontmatter. Put findings, decisions safe to preserve, and decisions requiring approval in the body.
- Report the artifact path to the user.

## Workflow

1. Establish the intended behavior, constraints, system boundary, and approved decisions.
2. Map components, responsibilities, dependencies, ownership, state, data flow, and external contracts using repository evidence.
3. Identify decisions that are expensive to reverse: public interfaces, stored formats, concurrency models, shared mutable state, inheritance hierarchies, dependency boundaries, and abstractions likely to spread.
4. Test the first instance against current use cases and a realistic extension. Look for leaky responsibilities, hidden coupling, invalid states, duplication, and infrastructure without demonstrated need.
5. Compare concrete corrections when a structural problem exists. Recommend the simplest option that satisfies the known requirements and preserves future reversibility.
6. Distinguish approved decisions, assumptions, proposed changes, deferred questions, and non-goals.
7. Do not redesign or modify code unless the user explicitly requests it.

## Output

Write the review artifact with architecture findings ordered by consequence. For each finding include:

- affected boundary, component, or pattern;
- repository evidence;
- current and future consequence;
- recommended correction and tradeoff;
- urgency and confidence.

Conclude with the decisions that are safe to preserve, decisions requiring approval, and validation needed before the pattern spreads. Do not treat aesthetic preference or hypothetical scale as an architecture defect.
