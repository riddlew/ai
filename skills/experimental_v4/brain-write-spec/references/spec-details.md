# Detailed workflow — brain-write-spec

**Read only for the cases linked from SKILL.md.** This reference preserves the pre-simplification guidance; the current primary skill and central policy control where wording overlaps.


# Write Spec

**Mechanical specification creation:** When creating a new spec, use `sh "${CLAUDE_SKILL_DIR}/../brain-init/scripts/brain-tool" doc new --kind specification` for the draft path, ID and frontmatter; supply actual governing `--parent` IDs where applicable. On revision, preserve the existing document and its IDs rather than recreating it. Use `validate` for structural checks, not approvals. See `${CLAUDE_SKILL_DIR}/../brain-init/references/deterministic-tooling.md` for the command contract, preview/authorization safeguards, and runtime fallbacks.


**Project brain:** Follow `CLAUDE.local.md` §Project brain loading: read **all** root `.md` files once per session (again after compaction), plus the active branch's pending file when present. Inspect linked detail and verify task-critical facts against current source. Do not send the whole brain to subagents. If no brain exists, proceed and mention `/brain-init` once.

Record established requirements and approved decisions as a stable implementation contract. For new features, use `.brain/features/<feature-slug>/02-specifications/` and `${CLAUDE_SKILL_DIR}/../brain-init/references/feature-document-contract.md` and `${CLAUDE_SKILL_DIR}/../brain-init/references/feature-document-templates.md`. Link to a governing brief when it exists; otherwise allow a direct, sufficiently settled specification. Small, well-understood changes can proceed without a spec. Follow `CLAUDE.local.md` for decision authority.

Do not conduct a new requirements interview (the bounded builder-review questions in §5 are the only exception) or reopen settled choices. If a consequential gap remains, record it under Open Decisions; do not decide it to make the spec look complete.

## 1. Gather the evidence

Use, as relevant:

- the current conversation and referenced material, including a `brain-brainstorm` final summary;
- existing implementation, callers, and tests;
- the approved feature brief under `01-brief/` when it exists;
- `.brain/glossary.md` and `.brain/03_architecture.md`;
- applicable ADRs under `.brain/adrs/`;
- established public system boundaries.

Classify everything as:

1. **Approved decisions** — user-confirmed choices, applicable ADRs, and established contracts.
2. **Repository facts** — what the code does today; evidence, not the desired design.
3. **Open decisions** — choices requiring the user's judgment.
4. **Implementation discretion** — routine details that do not belong in the spec, unless the user deliberately approved them as constraints.

A `brain-brainstorm` decision table maps directly: **Established** rows are approved decisions, **User decision** rows are open decisions, **Deferred** rows are implementation discretion, and **Investigate** rows must be investigated before writing or listed as open.

Do not introduce a new manager, service, ownership boundary, or lifecycle model unless it is already approved. If the current design appears insufficient, record that as an open decision. Use the canonical terms in `.brain/glossary.md`.

## 2. Write behavior, invariants, and examples

State the **general rules** first: invariants, constraints, limits, ordering, and guarantees that hold for all inputs.

Give each normative requirement or invariant a stable ID (`REQ-001`, `REQ-002`, ...), preserving IDs across revisions. Then write **concrete examples** for each required behavior: a specific starting state or input and the exact expected outcome. Cover the main path and the key failure paths that apply (invalid input, missing or denied access, conflicts, partial failure, limits).

- Derive each expected outcome independently from the approved requirements. Do not copy what the current code happens to do unless the requirements say current behavior is preserved.
- Examples illustrate; they are not exhaustive. The general rules define behavior between examples.
- If an expected outcome depends on a choice nobody has made, do not write the example. Add the case to Open Decisions.
- Use concrete values. Number examples across the spec (`E1`, `E2`, …) so tasks and tests can reference them.

## 3. Define the verification strategy

Prefer existing high-level test boundaries and patterns. Add a new boundary only when existing ones cannot verify the behavior, and keep the number of distinct boundaries small. State which examples each boundary verifies. If testing would require a consequential architectural change, record it as an open decision.

## 4. Write the file

Store specifications in `.brain/features/<feature-slug>/02-specifications/<spec-slug>.md`, one file per coherent behavior area. Use unused stable `SPEC-<NNN>` IDs and the feature-document metadata contract:

```yaml
---
id: SPEC-001
kind: specification
status: draft
parents: [BRF-001]
requirements: []
depends_on: []
parent_hashes: []
---
```

When there is no brief, `parents: []` is valid. Requirements declared here live in the document body; `requirements` metadata lists externally governing requirements, otherwise `[]`. Reuse a document's ID when revising the same approved behavior. Follow this structure while preserving all existing spec quality checks:

```markdown
# <Feature Area>: Specification
## Problem and desired outcome
## Requirements and invariants
- REQ-001: <normative behavior>
## Examples
- E1: Given <state>, when <action>, then <expected outcome>.
## Technical Decisions
## Verification Strategy
## Open Decisions
## Exclusions
```

Before approving, calculate and record `parent_hashes` for any governing brief with `${CLAUDE_SKILL_DIR}/../brain-init/scripts/validate_feature_docs.py --show-parent-hashes <spec-file>`. A spec without parents uses `parent_hashes: []`. Do not refresh a stale fingerprint without reviewing the changed approved brief and obtaining any required reapproval.

Do not mark a spec approved until its contents and binding choices have actually been approved; unsettled scope remains draft or blocked. Maintain complete example and verification coverage. Applicable ADRs and decisions are references, not fabricated parent IDs.

**Revising an approved spec.** A material revision (a changed, added, or removed requirement, example, contract, or binding decision) sets `status: needs-revision` in the same edit. Keep the document ID and every existing requirement and example ID; give new items new IDs and never renumber. The user's request for a change is not approval of the written revision: show the changed requirements and examples and ask for explicit approval, and set `status: approved` only after it. Editorial changes that alter no behavior keep `approved`. Then report the impact without editing any other document:

- **Affected:** every component, plan, and task governed by this spec, directly or through its chain. The validator's stale-fingerprint errors name the direct children; follow `parents` links down for the rest. Mark which ones cite a changed requirement. Their owning skills (`brain-decompose`, `brain-blueprint`, `brain-write-tasks`) must review them and set `needs-revision`; do not change their status or `parent_hashes` yourself.
- **Unaffected:** chains governed only by other specifications, which remain approved and may proceed.

### Technical Decisions

Record **approved** decisions about responsibility and ownership boundaries, lifecycle and state ownership, design patterns chosen or rejected, contracts, persistence and schema changes, meaningful cross-component interactions, and intentional non-goals. **Usually** omit method-level details and source-file paths. **Preserve them when the user explicitly approved them or omission would lose an agreed constraint.** Identify the source of each binding technical choice. Distinguish binding decisions from illustrative implementation suggestions or tentative preferences; do not turn a suggested method signature into a requirement by accident. Keep a small agreed prototype fragment (for example, a schema or exact interface) only when essential to preserve a decision, and label it as approved or prototype-derived as appropriate. Detailed implementation design belongs in `/brain-blueprint`, not a duplicated full blueprint here.

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

Write only the spec file into `02-specifications/`; leave the index, `state.md`, and other root files to `brain-update`. After §5 is complete, invoke `brain-update` with a one-line summary of what changed.

Report the created or updated path, whether open decisions block implementation, and the `Builder review:` line.

## Boundaries

This skill owns only specifications. `brain-decompose` owns functional component documents; `brain-blueprint` owns technical implementation plans; `brain-write-tasks` owns executable tasks; `brain-implement` owns mutable `execution.md`. After a specification is approved, recommend `brain-decompose` for a feature with meaningful functional subdivisions, or `brain-blueprint` directly for smaller well-defined scope. A consequential change under implementation updates the governing spec and applicable ADR/decision before affected plans or tasks are revised. Never invent authorization to implement.
