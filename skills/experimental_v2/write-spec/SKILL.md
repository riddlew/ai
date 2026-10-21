---
name: write-spec
description: Synthesize established decisions and repository evidence into a feature specification without inventing or reopening requirements.
disable-model-invocation: true
---

# Write Spec

Create a specification when one is needed to preserve substantial requirements, contracts, or approved decisions across implementation work. Small, well-understood changes can proceed directly without a spec.

Synthesize from existing discussion, approved decisions, and project evidence. Follow root `CLAUDE.md` for decision authority.

Do **not** conduct a new requirements interview or reopen settled choices. Do **not** silently decide a consequential product or architectural question merely to make the specification appear complete. If such a gap exists, record it as unresolved and make the limitation explicit.

## Establish the evidence base

Use, as relevant:

- current conversation and referenced project material;
- existing implementation, callers, and tests;
- root `CONTEXT-MAP.md` and the relevant context's `CONTEXT.md` (otherwise root `CONTEXT.md`);
- applicable root and context-local ADRs under `docs/adr/`;
- established public system boundaries.

Inspect the repository as needed. Use the project's domain vocabulary.

Differentiate:

1. **Approved decisions** — user-confirmed choices and applicable ADRs or established project contracts.
2. **Repository facts** — what the current code does, which may inform but not automatically dictate the desired design.
3. **Open decisions** — choices requiring the user's judgment.
4. **Implementation discretion** — routine details that should not be elevated into specification requirements.

Existing code is evidence, not automatic permission to redesign it. In particular, do not introduce a new manager, service, ownership boundary, or lifecycle model in the specification unless it is already an approved choice. If the current design appears insufficient, document the issue as an open decision instead of resolving it implicitly.

## Define the verification strategy

Determine how the required **observable behavior** should be verified.

Prefer existing high-level boundaries and test patterns. Add a new testing boundary only when existing boundaries cannot adequately verify the behavior. Keep the number of distinct test boundaries small.

Derive testing details from existing project evidence; do not turn routine testing choices into new product decisions. If a testing strategy would itself require a consequential architectural change, flag that change as unresolved.

## Write the specification

Store every specification in `docs/specs/`, using `<NN>-<short-slug>.md`.

Before writing:

1. Inspect existing numbered specs.
2. Determine the highest valid numeric prefix and increment it.
3. Match existing zero-padding, or use two digits when no convention exists.
4. Create the directory only when needed.
5. Update an existing file only if the user is explicitly revising that same specification; otherwise create a new numbered file.

Use this structure:

```markdown
# <Feature Name>

## Problem

The user-facing problem and current limitation.

## Desired Outcome

What should become possible.

## User Stories

1. As a <role>, I want <capability>, so that <benefit>.

## Technical Decisions

Approved architectural/technical decisions, and relevant existing
contracts clearly distinguished from proposed changes.

## Verification Strategy

Observable behaviors, test boundaries, and relevant existing tests.

## Open Decisions

Only unresolved consequential choices that prevent an unambiguous
implementation. Omit this section when none remain.

## Exclusions

Explicitly out-of-scope behavior. Omit if empty.

## Additional Context

Relevant assumptions, caveats, or constraints. Omit if empty.
```

### Technical Decisions

Preserve **approved** decisions about:

- responsibility and ownership boundaries;
- component lifecycle and state ownership;
- public or internal contracts that matter to the feature;
- persistence, data representation, and schema changes;
- meaningful interactions across components;
- established architectural constraints and intentional non-goals.

Make these decisions explicit when they were established; they are part of the implementation contract. Do not specify ordinary method-level details or source-file paths. Retain a small agreed prototype fragment only when essential to preserve a decision (for example, a schema or state model), identifying it as a prototype-derived decision.

Avoid presenting one possible implementation as a required architecture. The specification should preserve intent without arbitrarily restricting local implementation choices.

### Open Decisions

When a material gap remains, state:

- what is unknown;
- why implementation depends on it;
- which plausible choices exist, if known;
- that the choice requires user consultation.

Do not fabricate a default or quietly treat one option as accepted. Mark the affected scope as **not implementation-ready** if an unresolved decision blocks faithful implementation. Independent, clearly specified scope can remain implementable.

## Implementation continuity

This skill establishes the **authoritative specification**, not a task tracker. **Do not create** `todo.md`, `guidance.md`, or implementation tickets as a side effect of writing the spec. If the user requests implementation, `implement` will create or resume the feature workspace when implementation actually begins.

For a persisted specification such as `docs/specs/014-external-communication.md`, the corresponding implementation workspace is `docs/implementation/014-external-communication/`. When implementation spans sessions, `implement` maintains `todo.md` there and may add a concise `guidance.md` when useful. Neither file can amend requirements or settle open decisions.

When the user approves a consequential change to a feature already under implementation, update the specification's established decisions as appropriate; do not write the change only into `guidance.md`. The next implementation session must reconcile its progress and notes with the revised specification and actual repository state.

## Preserve the contract

The specification must contain only supported information. Do not:

- invent missing requirements or user preferences;
- promote assumptions or recommendations to approved decisions;
- reopen settled decisions;
- add speculative future requirements;
- mistake repository observations for authorization to change architecture.

Report the created/updated path and, if applicable, that user decisions remain before implementation can proceed.
