---
name: review-code
description: Independently evaluate branch changes against repository engineering rules and the intended specification.
---

# Code Review

Review a bounded Git change set against repository engineering rules and the intended specification.

Produce two independent assessments:

- **Repository fit** — whether the changes follow the repository's documented engineering rules and remain maintainable.
- **Requirement fit** — whether the changes implement the applicable specification accurately and without unsupported behavior.

Keep these assessments isolated until both are complete.

## Preparation

### Resolve the comparison

Use the comparison base according to this precedence:

1. a base reference explicitly provided by the user;
2. a base reference explicitly supplied by the workflow or skill that invoked this review;
3. otherwise ask the user for the base reference and stop.

A base supplied by an invoking workflow is valid only when that workflow established it before the reviewed changes began. Do not independently guess or infer a comparison base.

For example, an implementation workflow may record the repository's `HEAD` before making changes and pass that commit to this skill for the resulting review.

Verify that the selected reference resolves before continuing.

Review the merge-base change set equivalent to:

```bash
git diff <base>...HEAD
```

Also collect branch commits equivalent to:

```bash
git log <base>..HEAD --oneline
```

If the diff contains no changes, report that and stop before starting reviewers.

### Locate authoritative material

Find repository documentation governing implementation decisions, such as coding conventions, architecture rules, testing expectations, or contribution guidance.

Include the domain records as repository rules: domain vocabulary from root `CONTEXT-MAP.md` and the relevant context's `CONTEXT.md` (otherwise root `CONTEXT.md`), and ADRs in root `docs/adr/` and the relevant context's `docs/adr/` that apply to the changed code.

Inspect relevant tooling configuration sufficiently to recognize rules already enforced automatically. Do not spend review findings on conditions that the repository's automated tooling already guarantees.

Resolve the specification using this precedence:

1. a spec path explicitly provided by the user;
2. a spec path explicitly supplied by the invoking workflow;
3. a relevant specification found under `docs/` or `specs/`;
4. ask the user when no applicable specification can be determined.

Never invent the specification.

If several specifications are plausible and repository evidence does not establish which governs the change, ask the user to identify the applicable one.

If the user or invoking workflow explicitly establishes that no specification exists, omit the requirement-fit assessment and state why.

## Build independent evidence packets

Create one evidence packet for each reviewer. Do not include conclusions from the other reviewer.

### Repository-fit evidence

Supply enough evidence to independently evaluate the change:

- reviewed Git range and changed files;
- commits belonging to the reviewed range;
- relevant repository rules and their source locations;
- changed code needed to evaluate those rules;
- the maintainability checks below;
- relevant automated-tooling guarantees.

The reviewer should inspect maintainability through these categories.

#### Cohesion

Look for:

- modules acquiring unrelated responsibilities;
- one logical behavior being distributed across unnecessarily many locations;
- names that no longer communicate purpose clearly.

#### Coupling

Look for:

- code that reaches deeply through another object's structure;
- behavior that depends excessively on another object's internals;
- pass-through functions or layers that add no meaningful responsibility.

#### Domain representation

Look for:

- important domain concepts represented only by generic primitives;
- groups of values repeatedly traveling together without a type that represents their relationship.

#### Control structure

Look for recurring conditional dispatch that indicates behavior may be represented more clearly through another structure or abstraction.

#### Duplication

Look for duplicated implementation or business logic that creates multiple places requiring synchronized changes.

#### Abstraction discipline

Look for:

- abstractions introduced without a current need;
- inheritance relationships where a subtype cannot honor substantial parts of the parent's expected behavior.

These checks are design heuristics, not repository rules.

Documented repository guidance takes precedence. Do not call a heuristic concern a violation unless an applicable repository rule independently makes it one.

### Requirement-fit evidence

Supply enough evidence to compare implementation with intent:

- reviewed Git range and changed files;
- commits belonging to the reviewed range;
- the applicable specification and its source location;
- changed code relevant to specified behavior.

The reviewer should evaluate each applicable requirement against the implementation rather than using repository-style considerations.

## Reviewer contracts

Run the two reviewers concurrently when both assessments are available.

### Repository-fit reviewer

Determine whether the changed code conflicts with repository rules or introduces material maintainability concerns.

For every reported issue, include:

- **Location** — affected changed code;
- **Basis** — repository rule or maintainability category;
- **Evidence** — what in the change creates the issue;
- **Impact** — why it matters.

When the basis is a repository rule, cite the rule and its source.

When the basis is a maintainability heuristic, explicitly identify it as advisory.

Exclude:

- issues outside the reviewed change unless necessary to explain the changed behavior;
- conditions already guaranteed by project automation;
- speculative refactoring preferences without a concrete maintenance consequence.

Report every supported issue found in the reviewed change.

Do not omit a finding because other findings are more severe or because the report is long.

Avoid duplicate findings that describe the same underlying problem.

### Requirement-fit reviewer

Trace the changed behavior against the applicable specification.

Report cases where:

- a requirement is absent or incomplete;
- implementation behavior conflicts with a requirement;
- the change introduces behavior for which the specification provides no basis.

For every finding, include:

- **Requirement** — quote or cite the relevant specification text;
- **Implementation** — the changed code or behavior being evaluated;
- **Mismatch** — the concrete difference between required and implemented behavior.

Do not report general code-quality concerns here.

Report every specification mismatch supported by concrete evidence.

Do not omit a mismatch because other findings are more severe or because the report is long.

Avoid duplicate findings that describe the same underlying mismatch.

## Final report

Preserve the independence of the two assessments.

Use:

```markdown
## Repository Fit

<repository-fit reviewer findings>

## Requirement Fit

<requirement-fit reviewer findings>
```

Do not combine, deduplicate, or reprioritize findings between sections. The same code may legitimately appear in both for different reasons.

Light editing for clarity is allowed, but do not change the reviewers' substantive conclusions.

If no specification applies, use:

```markdown
## Requirement Fit

Skipped — no applicable specification was established for this change.
```

Finish with:

```markdown
Repository fit: <N> findings
Requirement fit: <N> findings | skipped
```

Do not derive an overall verdict from the two assessments.