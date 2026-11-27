# Experimental V5 Execution Tracker

**Branch:** `feat/experimental-v5-simplified-brain`
**Base:** `9c373e362c4876a136cd2eb686e6b1ac7696d2c5`
**PR:** https://github.com/riddlew/ai/pull/25
**State:** In progress
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
- [ ] T10 — Tests, cross-runtime verification and CI evidence.
- [ ] T11 — Full plan compliance review and final PR readiness.

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
- T10: V5 regression suite and GitHub Actions added (`50f5404`); inherited v4-only assertions explicitly skipped with explanation while unaffected historical tests continue (`dd6b65e`). Latest Actions verification pending.
- T11: Final compliance review pending.

## Verification and risks

- GitHub Actions: Ubuntu/macOS v5 checks passed for commit `dd6b65e`; latest amendment-anchor changes still under CI verification. Active tests include 15 original v5 cases plus a new runtime anchor case. Legacy v4-only assertions have documented skips; unaffected inherited tests still run.
- Token-cost benchmark: not measured; no simulated measurement to be presented as real API savings.
