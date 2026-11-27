# Experimental V5 — Brain Workflow Simplification Plan

## Objective

Create `skills/experimental_v5/` as an independently installed and tested Brain version reducing API cost, user interactions, unnecessary documents, context and handoffs without weakening decision authority, correctness, or existing Brain behavior. Preserve `experimental_v4/` unchanged.

## Workflow and authority

1. Keep interactive `brain-brainstorm`: investigate facts, discuss alternatives, ask only consequential unresolved questions, record settled decisions. For existing features, apply narrow edits directly to relevant specifications/plans when safe and authorized, without administrative routing.
2. All feature stages are optional. Support `brain-brainstorm → brain-implement`, direct `brain-implement`, and documented `brain-brainstorm → [brain-write-spec] → [brain-design-implementation] → [brain-update] → brain-implement → [brain-update]`. No spec, blueprint, tasks, brainstorm, or prior update is a prerequisite. Plan internally when no plan exists.
3. Remove `draft/approved/needs-revision` workflow gates, approval evidence and parent-hash reapproval cascades from skill contracts, scaffolds, validation, and routing. A user can inspect documents without approving document status. An explicit request remains required to edit code; user owns unresolved consequential product, architecture, API, persistence, security and other irreversible decisions.
4. `brain-update` is manual only, never invoked by other skills. Other skills may write their owned documents or narrowly scoped established cross-document updates. Manual synchronization before and/or after implementation is optional. Preserve verified Git provenance, authoritative source maps, main/worktree boundaries and `.brain/.notes/` privacy.
5. Inline execution by default. Never dispatch subagents unless explicitly requested, and do not re-ask selected modes on skill handoffs. Preserve AI-led, developer-led and Learning Mode pair-programming author boundaries without mandatory incremental approvals.
6. Implement coherent increments; verify proportionately to risk. Small changes need focused checks; significant/high-risk security, protocol, persistence, compatibility and concurrency changes need deeper checks. Test-first when helpful, not compulsory. No automatic specialist-review gate or routine approval pause. No repeated ineffective retries; diagnose changed evidence before retrying. Stop when scope and relevant verification are complete; do not add unsolicited refactors, reviews or documentation. Report actual changed files, tests and blockers briefly.
7. Concise progress, selective durable documentation, no duplicated normative requirements. Each decision has one authoritative source (spec behavior, plan design, ADR/project decision, or minimal brainstorm record when no spec). Handoffs and execution history reference decisions rather than recreate them.
8. Retain focused, traceable amendments for significant mid-implementation changes, with explicit `amends` / `supersedes` links, unaffected older decisions still governing and no implicit latest-file-wins. Minor code decisions require no document; brief execution notes when useful; focused new docs only for material changes. Detect conflicting supersession and consult the user.
9. Support a short, optional `.brain/features/<feature>/handoff.md` for Opus→Sonnet or fresh sessions (objective, decision references, source paths, unknowns, next step). It is a retrieval aid, not competing authority. `execution.md` is optional for short tasks and compact for complex/multi-session work.
10. Prefer a soft context budget: task-scoped index, relevant decisions, documents and actual code first; expand automatically when facts/dependencies require it. Avoid repeatedly reading unchanged broad knowledge. `brain-update` may use verified change-based synchronization rather than mandatory blanket root rereads, without sacrificing provenance.
11. Explicit version per project, preferably in existing installed policy/index, with v4 readable but no silent migration or metadata rewriting. Preserve V4 compatibility and rollback. Never overwrite or edit v4 skill sources.
12. Keep optional `brain-compact` standalone, manual/preview-first, preserving meanings/references; `brain-retro`, decomposition and tasks optional; simplify `brain-next`; consolidate skills only if it clearly reduces complexity and preserves capabilities.

## Implementation approach

- **T1** Baseline: create v5 branch and commit this plan plus execution tracker; open draft PR immediately.
- **T2** Mirror v4 into standalone v5 (including tools, references, tests), with install paths and guides scoped to v5. Leave v4 untouched.
- **T3** Simplify shared policy and feature document authority, ownership, metadata and compatibility; implement explicit project version.
- **T4** Adapt Python, Node and POSIX tooling, document scaffold and validation for no approvals, optional planning and amendments.
- **T5** Adapt brainstorming, writing specs, implementation plans, update and implementation, including direct implementation and no automatic updates.
- **T6** Adapt pair-programming, next, decomposition, tasks and all remaining skills/references consistently; retain optional compact.
- **T7** Implement traceable focused amendment and conflict handling; compact handoffs and cross-session execution state.
- **T8** Apply targeted context, risk-based verification, iterative debugging, completion limits and concise output across policies.
- **T9** Update v5 README, USAGE, skill counts, workflow examples and model guidance without modifying v4.
- **T10** Add regression tests for direct brainstorm-to-implement, missing plans, manual update, decision authority, document amendments/conflicts, no default subagents, modes, cross-session handoffs, version isolation, compatibility, optional compact and stop rules. Run Python/Node/shell validation and GitHub Actions; fix findings.
- **T11** Review every requirement against changed sources and tests, record evidence in tracker, finish PR without merging.

## Definition of done / acceptance

No approval/status confirmation turns; no automatic `brain-update`; no mandatory spec/plan; brainstorm-to-implement and direct implementation supported; optional decision handoff; explicit version; no default subagents; targeted context; concise output; risk-based testing; no unnecessary retry loops or over-implementation; focused amendment precedence with conflicts surfaced; user-authorized production changes; optional manual `brain-compact`; v4 unchanged; tests and CI verified; checklist evidence complete.

## Benchmark

Compare v4/v5 on direct small changes, documented multi-stage features, brainstorm-to-implement, fresh Opus→Sonnet, mid-implementation changes and high-risk/debugging work. Record API input/output/cache tokens, billed cost, calls, interactions, document writes, verification/quality, and resume accuracy when measurable. Aspirational targets: 30% lower input tokens and 40% fewer administrative interactions; do not claim targets met without measured data. Automated repository checks cannot alone prove real API cost savings.
