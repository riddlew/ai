---
name: review-architecture
description: Review a specific architectural decision, design, implementation, or pattern before it becomes expensive to change or propagate.
---

# Architecture Review

Use this skill when the user wants focused review of a known architectural area, especially:

- public interfaces;
- persistence or serialization formats;
- ownership and state models;
- concurrency;
- shared abstractions;
- inheritance;
- dependency relationships;
- patterns likely to spread;
- other structural decisions that may become expensive to reverse.

Review the selected boundary using current repository evidence. Do not broaden the task into a general architecture audit.

## Establish the review boundary

Before evaluating the architecture, determine:

- intended behavior;
- known constraints;
- the system boundary under review;
- previously approved decisions;
- relevant intentional non-goals.

Before questioning established architectural choices, read the domain records: root `CONTEXT-MAP.md` and the relevant contexts' `CONTEXT.md` (otherwise root `CONTEXT.md`), and relevant ADRs in root `docs/adr/` and each relevant context's `docs/adr/`.

Treat existing ADRs as intentional decisions unless current repository evidence gives a substantive reason to reconsider them.

## Inspect current evidence

Inspect the implementation and documentation necessary to understand the selected boundary.

Read only as much surrounding material as required to establish:

- responsibilities;
- dependencies;
- ownership;
- state;
- data flow;
- externally visible contracts.

Recheck claims against the current repository rather than relying solely on plans, documentation, earlier reviews, or assumptions.

Keep these categories distinct throughout the review:

- established decisions;
- factual observations;
- assumptions;
- proposed changes;
- unresolved questions;
- intentional non-goals.

Do not present an assumption as repository evidence.

## Evaluate the architecture

Pay particular attention to decisions whose cost of change increases substantially after wider adoption.

Test the reviewed design against:

1. existing use cases; and
2. at least one realistic future extension.

Look for structural problems such as:

- unclear or leaking responsibilities;
- hidden coupling;
- invalid or inconsistent states;
- duplicated responsibility;
- poor test surfaces;
- abstractions that expose nearly as much complexity as they hide;
- unnecessary infrastructure;
- unnecessary abstraction.

Do not classify aesthetic preference, stylistic disagreement, or speculative future scale as an architectural defect.

## Compare corrections

When a structural problem exists, compare concrete ways to correct it.

Prefer the simplest correction that:

- satisfies known requirements;
- preserves clear responsibility and ownership;
- provides an adequate test surface;
- avoids unnecessary coupling or lock-in;
- does not introduce infrastructure or abstraction without demonstrated need.

Do not redesign the system beyond what is necessary to evaluate the reviewed boundary.

Do not modify production code or perform implementation work unless the user explicitly requests it.

## Write the durable review

Every review produces a new append-only Markdown artifact under:

```text
docs/reviews/architecture/
```

Use filenames shaped like:

```text
<NN>-<short-slug>-review.md
```

Before creating the file:

1. inspect existing review filenames in `docs/reviews/architecture/`;
2. find the highest valid numeric prefix;
3. increment it;
4. zero-pad consistently with the existing files, or use two digits when no convention exists.

Create the directory only when the first architecture review is written.

Never overwrite or replace an earlier review.

## Review structure

The review must identify:

- what architecture, implementation, design, or revision was reviewed;
- the relevant source artifacts and repository evidence;
- any established decisions or constraints that materially shaped the review.

Order findings by consequence.

For each finding include:

- **Architectural area** — the boundary, responsibility, component, or pattern affected.
- **Evidence** — concrete repository evidence supporting the finding.
- **Current consequence** — what problem the structure causes now.
- **Consequence if adopted broadly** — what is likely to become harder or riskier if the pattern spreads.
- **Recommended correction** — the smallest architectural change that addresses the problem.
- **Tradeoffs** — meaningful costs or disadvantages of the correction.
- **Urgency** — how soon the issue should be addressed relative to wider adoption.
- **Confidence** — how certain the finding is given the available evidence.

Make uncertainty explicit when the evidence is incomplete.

Conclude with:

## Decisions Safe to Preserve

Architectural decisions that the available evidence supports retaining.

## Decisions Requiring Approval

Changes or unresolved architectural choices that require user judgment before adoption.

## Validation Before Wider Adoption

Tests, experiments, repository checks, or other evidence still required before the reviewed pattern should spread.

Report the created review path to the user.

## Record approved decisions

When the user approves a decision from **Decisions Requiring Approval**, invoke `domain-modeling` to record it. That skill decides whether the decision meets its ADR policy and updates `CONTEXT.md` or `CONTEXT-MAP.md` when the decision changes domain terms or boundaries.

Reference the review path as the source of the decision's evidence. Do not edit the review to record the approval; it remains an append-only record of the assessment.