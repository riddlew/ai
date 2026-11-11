---
name: brain-write-spec
description: Synthesize established decisions and repository evidence into a feature specification with concrete examples, without inventing or reopening requirements.
disable-model-invocation: true
---

# Write Spec

**Project brain:** Follow `CLAUDE.local.md` §Project brain loading: read **all** root `.md` files once per session (again after compaction), plus the active branch's pending file when present. Inspect linked detail and verify task-critical facts against current source. Do not send the whole brain to subagents. If no brain exists, proceed and mention `/brain-init` once.

Record established requirements and approved decisions as a stable implementation contract. Small, well-understood changes can proceed without a spec. Follow `CLAUDE.local.md` for decision authority.

Do not conduct a new requirements interview (the bounded builder-review questions in §5 are the only exception) or reopen settled choices. If a consequential gap remains, record it under Open Decisions; do not decide it to make the spec look complete.

## 1. Gather the evidence

Use, as relevant:

- the current conversation and referenced material, including a `brain-brainstorm` final summary;
- existing implementation, callers, and tests;
- `.brain/glossary.md` and `.brain/03_architecture.md`;
- applicable ADRs under `.brain/adrs/`;
- established public system boundaries.

Classify everything as:

1. **Approved decisions** — user-confirmed choices, applicable ADRs, and established contracts.
2. **Repository facts** — what the code does today; evidence, not the desired design.
3. **Open decisions** — choices requiring the user's judgment.
4. **Implementation discretion** — routine details that do not belong in the spec.

A `brain-brainstorm` decision table maps directly: **Established** rows are approved decisions, **User decision** rows are open decisions, **Deferred** rows are implementation discretion, and **Investigate** rows must be investigated before writing or listed as open.

Do not introduce a new manager, service, ownership boundary, or lifecycle model unless it is already approved. If the current design appears insufficient, record that as an open decision. Use the canonical terms in `.brain/glossary.md`.

## 2. Write behavior, invariants, and examples

State the **general rules** first: invariants, constraints, limits, ordering, and guarantees that hold for all inputs.

Then write **concrete examples** for each required behavior: a specific starting state or input and the exact expected outcome. Cover the main path and the key failure paths that apply (invalid input, missing or denied access, conflicts, partial failure, limits).

- Derive each expected outcome independently from the approved requirements. Do not copy what the current code happens to do unless the requirements say current behavior is preserved.
- Examples illustrate; they are not exhaustive. The general rules define behavior between examples.
- If an expected outcome depends on a choice nobody has made, do not write the example. Add the case to Open Decisions.
- Use concrete values. Number examples across the spec (`E1`, `E2`, …) so tickets and tests can reference them.

## 3. Define the verification strategy

Prefer existing high-level test boundaries and patterns. Add a new boundary only when existing ones cannot verify the behavior, and keep the number of distinct boundaries small. State which examples each boundary verifies. If testing would require a consequential architectural change, record it as an open decision.

## 4. Write the file

Store specifications in `.brain/specs/<NN>-<short-slug>.md`:

1. Inspect existing numbered specs and increment the highest valid prefix.
2. Match existing zero-padding, or use two digits.
3. Create the directory only when needed.
4. Update an existing file only when the user is revising that same specification.

```markdown
# <Feature Name>

## Problem

The user-facing problem and current limitation.

## Desired Outcome

What should become possible.

## User Stories

1. As a <role>, I want <capability>, so that <benefit>.

## Behavior and Invariants

Rules that hold for all inputs: invariants, constraints, limits,
ordering, and guarantees.

## Examples

### <Behavior>

- **E1:** Given <state or input>, when <action>, then <exact outcome>.
- **E2 (failure):** Given <state or input>, when <action>, then <exact outcome>.

## Technical Decisions

Approved architectural and technical decisions, with relevant existing
contracts clearly distinguished from approved changes.

## Verification Strategy

Test boundaries, relevant existing tests, and which examples each
boundary verifies.

## Open Decisions

Unresolved consequential choices that prevent unambiguous
implementation. Omit when none remain.

## Exclusions

Explicitly out-of-scope behavior. Omit if empty.

## Additional Context

Relevant assumptions, caveats, or constraints. Omit if empty.
```

### Technical Decisions

Record **approved** decisions about responsibility and ownership boundaries, lifecycle and state ownership, contracts that matter to the feature, persistence and schema changes, meaningful cross-component interactions, and intentional non-goals. Omit method-level details and source-file paths. Keep a small agreed prototype fragment (for example, a schema) only when essential to preserve a decision, and label it as prototype-derived. Do not present one possible implementation as required architecture.

### Open Decisions

For each gap state what is unknown, why implementation depends on it, the plausible choices if known, and that it requires the user's decision. Mark the affected scope **not implementation-ready**; independent, fully specified scope remains implementable.

## 5. Check and review

Do these in order, after the file is written.

1. **Self-check.** Fix the file until:
   - every required behavior and invariant has at least one Example, including the failure paths that apply (§2's list). Write the missing Example when approved requirements determine its outcome. Record an Open Decision only when the outcome depends on a choice nobody has made;
   - no Example settles an open choice;
   - terms match `.brain/glossary.md`;
   - Example IDs are unique;
   - the Verification Strategy names a test boundary for every Example.
2. **Builder review.** Follow `${CLAUDE_SKILL_DIR}/../brain-review-code/references/builder-review.md`, with `spec` as `{artifact_kind}`. `{sources}` is "none: the spec must stand alone".
3. **Pile-3 questions.** Ask them now, after the file is written. Wait for the reply, then apply the answers to the file. Unanswered ones go under Open Decisions. These questions are bounded to the gaps a builder hit. They are not a new requirements interview.
4. **Structural revision.** A later user revision that makes the spec gain or lose behaviors gets one more review. Applying the step-3 answers never does, even when they add Examples.
5. **Only then** go to §6. Do not invoke `brain-update` before the questions are answered and applied, or recorded as Open Decisions.

## 6. Finish

Write only the spec file into `.brain/`; leave the index, `state.md`, and other root files to `brain-update`. After §5 is complete, invoke `brain-update` with a one-line summary of what changed.

Report the created or updated path, whether open decisions block implementation, and the `Builder review:` line.

## Boundaries

- This skill writes the specification only. `brain-implement` creates its impl plan in `.brain/impl_plans/` when work begins.
- When the user approves a consequential change to a feature under implementation, update this specification, not the impl plan.
