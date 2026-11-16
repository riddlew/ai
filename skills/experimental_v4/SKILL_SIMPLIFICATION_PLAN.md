# Experimental v4 skill simplification plan

**Status:** Implemented on `feature/simplify-brain-skills`; static and CLI validation passed, agent-level behavioral evaluation not run. Pending review and merge.  
**Base:** `main` at `4bd19eb5aafa56ef6e648f0770882bc351beb293`  
**Working branch:** `feature/simplify-brain-skills`

## Decision

Make Claude-facing skills **short, task-specific, and easy to follow**, while retaining correctness rules and deterministic tooling. **Do not simplify by deleting guarantees.** Consolidate cross-cutting policy in one authoritative location; move detailed examples and uncommon procedures into references that are opened only when applicable; use existing scripts to enforce mechanical contracts.

The target is lower **routinely loaded** instruction volume, fewer duplicated/contradictory rules, and clearer skill execution. A shorter file alone is not success: compare *actual loaded tokens*, task outcomes, and missed constraints.

**Key design principle:** The primary `SKILL.md` should answer **when to run, what inputs matter, what to do, when to stop/ask, what to produce, and which reference to read conditionally**. It should not be a complete manual.

## Baseline and observed causes

The current `experimental_v4` directory has 19 skill entry points and multiple shared references. Representative primary-file sizes from merged `main`:

| File | Approx. size | Why review |
|---|---:|---|
| `brain-implement/SKILL.md` | 19.8 KB / 126 lines | Collaboration modes, worktrees, checkpoints, review flow, and repeated shared rules |
| `brain-update/SKILL.md` | 20.6 KB / 133 lines | Root sync, branch/pending rules, indexing, source provenance, ADR workflow |
| `brain-init/SKILL.md` | 13.9 KB / 85 lines | Long policy installation/reconciliation instructions despite deterministic CLI |
| `brain-brainstorm/SKILL.md` | 13.0 KB / 160 lines | Multiple decision/visual paths in primary instructions |
| `brain-write-spec/SKILL.md` | 11.0 KB / 127 lines | Inline document example plus repeat of feature contract |
| `brain-review-code/SKILL.md` | 10.6 KB / 156 lines | Review modes and reporting details in entry point |
| `brain-init/references/CLAUDE.local.md` | 16.3 KB / 105 lines | Project-wide policy that itself includes workflow details |
| `brain-init/references/USAGE.md` | 56.8 KB / 1,291 lines | Valuable examples; never load wholesale by default |

These are **file sizes**, not measured token counts. Redundant language appears across `CLAUDE.local.md`, skill entry points, `feature-document-contract.md`, `deterministic-tooling.md`, and `safe-context-loading.md`. Inline examples and fallback instructions compete with task-specific procedures.

Current tests include static text contracts and deterministic tools. They will need **behavior-oriented** replacements where assertions are only tied to exact wording.

## Non-negotiable invariants

The simplification must preserve:

1. **Decision authority:** distinguish verified code facts, approved decisions, low-risk implementation choices, and consequential decisions that require consultation; never infer approval from a written document or passing test.
2. **Brain discovery and safety:** one valid Brain (index required), consistent resolution across linked worktrees, one shared authoritative location, explicit authorized write scope, no alternate tool or Brain copy to bypass denial.
3. **Branch isolation:** root project knowledge reflects `main`; unmerged branch facts remain in `pending/<branch>.md`; merge-time knowledge updates require verification.
4. **Feature hierarchy:** optional Brief → Specifications → Components → Plans → Tasks, stable IDs, ownership per producing skill, requirement traceability, parent hashes, stale descendants needing revision, dependency/coverage validation. Small settled work must not require ceremonial documents.
5. **Approvals and execution:** confirmed behavior and binding design before implementation; collaboration modes, blueprint gate when warranted, resumable execution with a true pre-change review base, tests and evidence, scope limits, explicit user review checkpoints when required.
6. **Code/review discipline:** inspect actual code, callers, tests, and uncommitted changes; correct Git comparison bases; evidence-backed review findings and security/architecture assessment; preserve unrelated user edits.
7. **Context completeness:** always load governing project orientation, decisions, applicable feature docs/ADRs/source maps/technical knowledge and active pending notes; discover related code and documentation. **When scope is uncertain, load more.** A scope map/hash never proves semantic coverage.
8. **Deterministic tooling:** retain Python (preferred), Node and POSIX shell fallbacks with no extra language packages, dry-run by default, explicit apply/write scope, idempotence, no silent overwrites or auto-approval. Preserve CI on Linux and macOS.
9. **Special-purpose skills:** preserve stand-alone behavior of diagnosis, backlog refinement, content distillation, writing voices, reviews and skill testing; no blanket Brain/feature workflow imposed on tools that do not need it.

This list is the **behavioral contract**, not text to paste into every skill. Use one central source with short references elsewhere.

## Proposed Claude-facing layout

**A. Central policy** — `brain-init/references/CLAUDE.local.md`

Keep a small, plainly ordered core: authority and approval; Brain location and scoped writes; project context safety; when to consult; preservation of user work. Relocate details about document schemas, Git plumbing, model tiers, collaborator prompts, review storage, and long examples to their current specialized references. Do not remove a safeguard until its owning reference and tests cover it.

**B. Skill entry points** — `brain-*/SKILL.md`

Adopt a consistent short skeleton (not a rigid line cap):

- **Purpose / trigger:** one or two sentences, with clear cases where the skill is unnecessary.
- **Inputs / preflight:** only the facts needed to perform this task; links to authoritative policy/contract.
- **Core workflow:** ~3–6 concrete steps; use CLI for file operations where available.
- **Stop conditions / approval:** the handful of task-specific blockers that would cause wrong behavior.
- **Output / handoff:** expected artifact or response; targeted link to optional reference.

Keep mandatory safety rules visible where failure is expensive (e.g., worktree scope and approval gate in `brain-implement`). Avoid including the same paragraph in every skill.

**C. On-demand references**

Retain concise, navigable references for rare/complex modes: subagents, collaborative review, architecture evaluation, source-map reconciliation, long-form templates, visual brainstorming, report formatting and troubleshooting. Each primary skill points to the applicable section with an explicit *read when* condition.

**D. Executable contracts**

Keep structural checks, filesystem operations, IDs, hashes and Git inventories in the existing tested `brain-tool` family; do not paraphrase entire command contracts inside every skill. The launcher remains a small adapter, not another set of skill-specific instructions.

## Context loading: simplify without weakening coverage

**Recommendation: do not require Claude to maintain and reason through a fingerprinted `context-map.tsv` for ordinary tasks.** That is a high-friction optimization with a real risk of an incomplete *semantic* map.

Simpler Claude workflow:

1. Read the small mandatory project context (overview, architecture, established decisions, current branch pending and active feature's approved governing docs).
2. Inspect relevant repository code, owners, callers, tests and configuration; search `.brain/knowledge/`, `.brain/sources/`, ADRs and the Brain index for task terms, feature IDs, source paths and related references.
3. Read matching technical documents **and their referenced source material**. Expand the search as new dependencies appear, including adjacent modules and integration boundaries.
4. When any coverage is unknown, a relevant source is partially mapped/stale, or a decision conflicts, **read more rather than skip**; do not proceed with unsupported assumptions.

Provide a tiny, **read-only** deterministic discovery command if testing shows value. A manifest or scope map may be used as an **optional accelerator** to propose candidates, but **must not be an exclusion list**. Avoid requiring updates to a scope map before ordinary feature work. Keep `brain-update`'s full root synchronization rule. Do not immediately delete the existing `brain-context` or its three implementations: retain compatibility during migration and decide whether to retire it only after evidence that the simpler strategy preserves coverage.

**Failure mode to test:** task changes an API, but key behavior is described in a topic document with a name unrelated to the changed code path. Claude must find that document by searches, index/references and exploration, not trust a mapping alone.

## Work packages / order

| Phase | Changes | Preserve / acceptance |
|---|---|---|
| 0. Freeze contracts | Inventory behavior, duplicate rules, reference links and exact-text tests; create scenario-based regression matrix and load-token baseline. No skill edits. | Baseline static suites and critical H7/H10 worktree/approval scenarios; documented exception list |
| 1. Simplify central policy | Reorganize `CLAUDE.local.md` into short decision/workspace/context rules and precise pointers to established contract/reference files. | No change in approval, authority, Brain discovery, authorized writes or branch isolation |
| 2. Simplify context | Replace mandatory map-protocol narration with mandatory context + targeted search + link-following + broaden-on-uncertainty. Keep `brain-context` available but optional; modify context documentation and affected skills. | Tests for hidden relevant files, indirect references, unindexed/new knowledge, stale source maps, cross-module ownership, compaction and branch pending isolation |
| 3. Simplify feature creators | `brain-init`, `brain-brainstorm`, `brain-write-spec`, `brain-decompose`, `brain-blueprint`, `brain-write-tasks`: remove inline boilerplate/templates, use existing references/CLI, keep only conditional gates. | Optional levels, stable IDs, status/approval and parent-hash semantics; scripts unchanged |
| 4. Simplify execution and sync | `brain-implement`, `brain-update`, `brain-plan`: core path only in primary skill, move worktree/recovery/subagent/source-import details behind clear links and triggers. | Safe worktrees, H10B authorization, resumable review bases, collaboration modes, no unmerged-fact promotion, full-root sync |
| 5. Simplify reviews and specialists | Code/MR/architecture/security review, diagnosis, distillation, explain-changes, backlog refinement, skill testing and `write-human` **only when measured duplication exists**. | Task-specific modes, output integrity, voice/fidelity, read-only review rules, reporting conventions |
| 6. Validate and measure | Run static + fixture + Python/Node/shell parity on Linux/macOS; rerun *bounded* agent scenarios only where instructions (not code) changed; evaluate context misses and token usage. | No material regressions, fewer routinely loaded tokens, readable entry points, transparent residual risks |

Order work in **small reviewable commits**. The order of context versus central policy is deliberate: amend the policy and context instructions together when needed to avoid temporary contradictory rules on the branch.

## Testing strategy

1. **Characterize before editing.** Save sizes and effective loaded instruction totals by skill use case. Measure what Claude actually reads; distinguish repository bytes, estimated tokens and billed/observed model tokens.
2. **Behavioral guardrails over brittle string matching.** Tests should assert a specific rule remains available and the correct reference is invoked when needed. Remove exact wording assertions only when replaced by equivalent or stronger behavior checks.
3. **Scenario matrix (high priority):** no Brain; shared Brain outside authorized workspace; ignored/tracked Brain; feature with skipped document stages; revised approved spec invalidates only affected descendants; direct small task; blueprint-required task; approved collaboration checkpoint; interrupted/resumed implementation; dirty worktree; review-only invocation; pending facts before/after merge; ambiguous or missing technical knowledge.
4. **Knowledge retrieval adversarial cases:** opaque filename for governing protocol, source doc reachable only through caller/test references, stale map, partial source extraction, overlapping subsystem names, new unindexed knowledge, conflict between code and approved spec, and branch-only pending notes.
5. **Script safety:** no change to language fallback order, version requirements, idempotent operations, Git exclusions, scope authorization, data formats or approval logic. Keep current 3-runtime suites.
6. **Agent checks only for instruction-sensitive cases:** run a limited before/after matrix with identical fixtures, controlled model/runtime/cost and scored outcomes. Static/CLI checks do not establish Claude read the right document. Stop and revise if a context miss or safety regression occurs.
7. **Success measures:** major reduction in routinely loaded instruction tokens; no drop in task completion or review accuracy; zero missed binding decisions in the tested scenarios; no unauthorized writes or approval bypass; no increase in unnecessary questions/documents. Do not optimize for shortest SKILL.md at the expense of behavior.

## Explicit exclusions

- Do **not** rewrite or remove the deterministic tool implementations, tests, or feature-document schema merely to reduce lines.
- Do **not** force one universal skill for all tasks; keep specialized skills when they have distinct user intent, permissions or output.
- Do **not** automatically trust semantic scope from filenames, a map hash or AI-generated summaries.
- Do **not** change user approval gates, `main`, or existing tracked/ignored Brain behavior.
- Do **not** run paid agent batches until static parity and an explicit baseline are established.

## Exit criteria

The simplification is ready for review when the primary entry points clearly describe the happy path and only task-critical stops; shared rules have one authoritative home; complex references are loaded conditionally; all original invariants remain covered by tests; the retrieval strategy proves it can find difficult related technical documents; and measured instruction/token costs improve without an observed safety or quality regression.

**Implementation:** See `SKILL_SIMPLIFICATION_REPORT.md` for the changed entry points, metrics, tests and limitations. Neither the plan nor implementation authorizes merging into `main`.
