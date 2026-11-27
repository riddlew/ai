# Experimental V5 Execution Tracker

**Branch:** `feat/experimental-v5-simplified-brain`
**Base:** `9c373e362c4876a136cd2eb686e6b1ac7696d2c5`
**PR:** https://github.com/riddlew/ai/pull/25
**State:** Implementation and review complete; PR awaiting human review
**Rules:** Check a task only when its implementation is committed and evidenced. Never infer CI pass or benchmark savings.

- [x] T1 — Commit v5 plan/tracker on isolated branch and open PR. (Initial commit; PR created after commit)
- [x] T2 — Copy and isolate full v4 baseline into v5, including tooling and tests.
- [x] T3 — Simplify shared policy, document authority and project version.
- [x] T4 — Update deterministic document scaffolding/validators/tool runtimes.
- [x] T5 — Update core brainstorm/spec/design/update/implement skills.
- [x] T6 — Update remaining skills, pair modes, routing, compact and references.
- [x] T7 — Focused amendments, conflict resolution and session handoffs.
- [x] T8 — Context, verification, debugging, concise output and stop rules.
- [x] T9 — V5 README, USAGE, counts, examples and model guidance.
- [x] T10 — Tests, cross-runtime verification and CI evidence.
- [x] T11 — Full plan compliance review and final PR readiness.

## Implementation evidence

- T1: Branch created from latest `main` SHA `9c373e362c4876a136cd2eb686e6b1ac7696d2c5`; initial plan and tracker are committed before implementation.
- T2: Copied complete 193-file v4 baseline into an isolated v5 directory, retaining original file content and executable modes. Internal v4 references and contracts will be updated in subsequent tasks.
- T3: Shared v5 `CLAUDE.local.md` defines explicit project version, decision authority, controlled ownership and no approval-state gates (`0acd2e5`).
- T4: Python/Node/POSIX tooling now scaffolds independent documents without status/hash metadata; validates references, amendment anchors, conflicting supersession and cycles (`70e9f00`, `7dd95ed`, `d3ddd11`). Cross-runtime tests succeeded at `dd6b65e`; final checks pending.
- T5: Core brainstorm, spec, design, update, implement and pair skills rewritten for direct implementation, explicit-only updates and no routine approval checkpoints (`0acd2e5`).
- T6: Supporting skill entrypoints and detailed references adapted; manual `brain-compact` retained (`7dd95ed`, `6092808`, `3933d0e`, `76b0c9a`).
- T7: Explicit narrow `amends`/`supersedes` contract, validator conflict checks, optional `handoff.md` and compact `execution.md` scaffold (`70e9f00`, `6163fc3`, `d3ddd11`).
- T8: Targeted context, risk-based tests/reviews, evidence-driven retries, concise outputs and stopping rules in policy and implementation references (`0acd2e5`, `6092808`, `3933d0e`).
- T9: V5 README/USAGE, ZPL and direct-workflow examples, corrected 22 Brain skills plus write-human count, model guidance (`6163fc3`, `3933d0e` and this commit).
- T10: Added 16 purpose-built v5 tests including cross-runtime amendment conflicts and missing supersession anchors; CI executes on Ubuntu and macOS with Python/Node/POSIX validation, 116 inherited tests (56 explicitly skipped because they enforce superseded v4 behavior), and the v4 hierarchical fixture. Latest successful CI for `650028a` is [run 46075340889](https://github.com/riddlew/ai/actions/runs/46075340889) on both platforms. Python/Node regex regression fixed in `650028a`.
- T11: Reviewed the plan against v5 policy, skills, tooling, references, tests and the [comparison with main](https://github.com/riddlew/ai/compare/main...feat/experimental-v5-simplified-brain). All 197 changed files are new v5 files (196) or its dedicated CI workflow (1); v4 and existing workflows are untouched. Acceptance traceability is below.

## Verification and risks

- GitHub Actions: **passed** on Ubuntu and macOS for `650028a` — 16 purpose-built v5 tests, 116 inherited contract tests (56 skipped with explicit legacy rationale), and v4 fixture validation.
- Token-cost benchmark: not measured; no simulated measurement to be presented as real API savings.

## Final plan-to-implementation review

| Plan requirements | Evidence and review result |
|---|---|
| PR created before work, isolated branch, initial plan and tracker, incremental commits | Initial `7cd04f7`, PR #25; complete |
| V4 unchanged; V5 independent and explicitly versioned | All 193 v4 files copied to v5; version marker in `brain-init/references/CLAUDE.local.md`; compare shows no changed v4 paths; complete |
| Preserve brainstorming, direct brainstorm → implement and direct request → implement | Core `brain-brainstorm/SKILL.md`, `brain-implement/SKILL.md`, USAGE and targeted tests; complete |
| Optional specs, plans, tasks, no approval status/reapproval and no automatic update | Shared feature contract, templates, Python/Node/shell scaffolds, updated owning and supporting skills; complete |
| Narrow cross-document edits, authoritative decisions and material user control | Shared project policy and feature contract; explicit authorship/decision boundaries; complete |
| Scoped focused amendments with explicit authority/precedence and conflict detection | Python, Node and POSIX validation of `amends`/`supersedes`, anchor existence, conflict/cycles; cross-runtime tests passed; complete |
| Manual `brain-update`, safe branching/source provenance and no private notes access | `brain-update/SKILL.md`, update details and shared policy; complete |
| Default inline and opt-in subagents; three pair modes | Shared policy, pair and implement skills/references; complete |
| Concise handoffs, optional execution history and stable cross-session references | Contract, optional `execution.md` scaffold, handoff examples and README; complete |
| Targeted context, selective docs, risk-based review and test, stop condition and evidence-based debugging | Shared policy and specialized implementation/review/context references; complete |
| Optional manual preview-first `brain-compact`; other skills remain available | `brain-compact/SKILL.md`, details and skills index; complete |
| Updated README, USAGE, examples, model guidance and counts | V5 `brain-init/references/README.md` and `USAGE.md`; 22 Brain skills plus `write-human`; complete |
| Regression tests, cross-runtime parity, macOS/Ubuntu CI and v4 fixture compatibility | GitHub Actions run `46075340889`; passed; complete |

## Disclosed limits

- **Real API token-cost reduction is unmeasured.** No production Claude Code transcript, token billing, or end-to-end model-run benchmark was available; aspirational 30% input-token and 40% administrative-turn goals are not presented as attained.
- **Behavioral agent simulation was not run.** Static and deterministic contract tests, source review and cross-runtime execution passed; actual interactive Claude behavior still merits a pilot.
- **Inherited v4-specific assertions:** 56 of 116 old contract tests are explicitly skipped because they demand approval gates/status, old prompts or other v4-only contracts. These are preserved but no longer considered v5 acceptance tests; the 16 purpose-built v5 tests verify the replacement workflow and tooling behavior.
- **Human evaluation** remains necessary before merging. This PR must not be merged automatically.
