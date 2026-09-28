---
name: write-spec
description: "Synthesize the current discussion and project evidence into a complete feature specification without collecting new requirements."
disable-model-invocation: true
---

# Write Spec

Create a feature specification from decisions and context that already exist.

Do not interview the user, ask for additional requirements, or reopen decisions that have already been established.

Where information can be determined from the repository, inspect the project directly rather than asking the user.

## Establish the evidence base

Before writing, collect enough evidence to describe the feature accurately.

Use:

- the current conversation;
- referenced project material;
- the existing implementation;
- domain vocabulary: root `CONTEXT-MAP.md` to locate the relevant context's `CONTEXT.md`, otherwise root `CONTEXT.md`;
- applicable ADRs in root `docs/adr/` and the relevant context's `docs/adr/`;
- existing tests;
- public system boundaries.

Inspect the repository when the available context is insufficient.

Use domain language defined by the project rather than inventing alternate terminology.

Treat applicable ADRs and other established architectural decisions as constraints on the specification.

Distinguish established information from assumptions. Do not manufacture missing product decisions merely to make the specification appear complete.

## Define the verification strategy

Determine how the resulting behavior should be verified before finalizing the specification.

Prefer verification through an existing high-level boundary that exposes behavior users or external callers actually observe.

Introduce a new testing boundary only when existing boundaries cannot adequately express the required behavior.

Keep the number of distinct test boundaries as small as practical.

Derive the verification strategy from repository evidence and established discussion. Do not pause to ask the user to approve the testing approach.

## Write the specification

Every specification is stored under:

```text
docs/specs/
```

Use filenames shaped like:

```text
<NN>-<short-slug>.md
```

Before creating the file:

1. inspect existing specification filenames in `docs/specs/`;
2. find the highest valid numeric prefix;
3. increment it;
4. zero-pad consistently with existing files, or use two digits when no convention exists.

Create `docs/specs/` only when the first specification is written.

Choose a concise slug describing the feature.

If the specification already exists and the user is explicitly updating that same specification, update the existing file rather than creating a duplicate. Otherwise create a new numbered specification.

## Specification structure

Use the following structure.

```markdown
# <Feature Name>

## Problem

Explain the user-facing problem and why the current behavior is insufficient.

## Desired Outcome

Describe what should become possible from the user's perspective once the feature exists.

## User Stories

List the behaviors and scenarios the feature must support as numbered user stories.

1. As a <role>, I want <capability>, so that <benefit>.

Cover meaningful variations and edge cases already established by the discussion or project evidence.

## Technical Decisions

Record implementation decisions that are already established or can be concluded from existing project context.

Include relevant decisions about:

- affected system responsibilities;
- module or component boundaries;
- public or internal interfaces;
- architectural constraints;
- data representation;
- schema changes;
- API contracts;
- interactions between parts of the system;
- developer-specified constraints or clarifications.

Describe durable decisions rather than volatile implementation details.

Do not include source-file paths or ordinary code snippets.

A small prototype fragment may be retained when it is the clearest representation of an agreed design decision, such as a schema, state model, reducer shape, or type structure. Include only the portion necessary to preserve the decision and note that it originated from a prototype.

## Verification Strategy

Describe how the feature's externally observable behavior will be validated.

Include:

- the behaviors that must be proven;
- the system boundary or module through which they will be tested;
- relevant existing tests that provide a pattern for the new coverage.

Prefer verification of observable behavior over tests coupled to internal implementation details.

## Exclusions

List related work or behavior deliberately outside the feature.

## Additional Context

Preserve constraints, assumptions, caveats, or established decisions important for implementation that do not fit naturally elsewhere.
```

`Exclusions` and `Additional Context` may be omitted when they have no content. Keep every other section.

## Preserve the contract

The finished specification must contain only information supported by established discussion or project evidence.

Do not:

- invent missing requirements;
- silently resolve open product decisions;
- reopen decisions already settled;
- add speculative future requirements;
- confuse implementation possibilities with established decisions.

If an unresolved gap materially prevents the feature from being specified accurately, identify the gap in the specification rather than choosing an answer for the user.

Report the created or updated specification path to the user.