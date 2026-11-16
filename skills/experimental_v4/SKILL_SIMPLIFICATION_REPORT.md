# Experimental v4 skill simplification — implementation report

**Branch:** `feature/simplify-brain-skills` (created from merged `main`; no direct `main` edits)

## What changed

- Replaced the primary instructions of **all 19 skill entry points** with concise task-specific happy paths, stop/approval conditions, outputs and conditional references.
- Retained all previous detailed procedures as **on-demand references**. Updated stale context-loading statements in the new references to point back to the current authoritative shared policy. Existing specialist references, schema/template files, scripts and runtime controls remain in place.
- Simplified the shared `CLAUDE.local.md`, preserving the worktree-write safety section, approved requirements and decisions, branch isolation, default collaborative checkpoints, review policy and model tier table. Uncommon decision/implementation discipline moved to `engineering-details.md`.
- Replaced mandatory `context-map.tsv` upkeep with **core project context + search code owners/callers/tests + search the Brain by behavior/source paths + read relevant documents and references + broaden when uncertain**. The Python/Node/POSIX `brain-context` implementations and map protocol remain available **optionally**, unchanged.
- Clarified the first-run policy migration: existing project `CLAUDE.local.md` files must be reconciled without silently overwriting customization, stacking conflicting policies or changing saved Brain locations.
- Added static regression checks for concise packaging, required safety rules, relevance discovery and intact on-demand references.

## Size measurement

Measured by primary file character count from `main` versus the feature branch during implementation (UTF-8 byte size is similar; these are **not actual model token counts**):

| Source | Before | After, approximate | Change |
|---|---:|---:|---:|
| 19 `SKILL.md` primary files | 184,883 characters | about 47,500 characters | about **74% smaller** |
| Bundled `CLAUDE.local.md` | 16,321 characters | 8,583 characters | about **47% smaller** |

Long-form references retain rare-case detail, so **repository size** is not reduced proportionately and tokens will be saved only when those references are not loaded. Actual Claude token savings have **not** been measured.

## Behaviors explicitly preserved

1. Approval and ownership of briefs/specs/components/plans/tasks; optional feature levels; stable IDs; parent hashes and reapproval after material changes.
2. Same single Brain across worktrees; denied-write reporting, no copying/alternate-tool workaround; branch pending facts isolated until merge.
3. True pre-change review base, resumability, preservation of user edits, evidence-backed verification and collaborative/guided approval checkpoints.
4. Brain-update's full-root sync, authority/provenance rules, technical source maps, ADRs and protected producer documents.
5. Read-only specialist review/backlog/distillation/explanation contracts, write-human explicit voice+mode validation, and skill-testing RED/GREEN criteria.
6. Existing deterministic Python, Node and POSIX shell commands, no third-party dependencies and no automated approval.

## Verification and caveats

- Existing static/feature/worktree/approval/review/context contracts and the new skill-simplification contracts run in Ubuntu and macOS CI.
- Existing `brain-context` parity tests remain intact even though calling it is no longer mandatory.
- **No fresh Claude-agent behavior evaluation** was run. Static tests establish that instructions and references are present, not that a real agent will find an opaque-named technical specification, observe every checkpoint or consult at the right time. Such scenarios remain the next quality gate for claims about unchanged agent reliability.
- Existing projects continue to use any **already installed** `CLAUDE.local.md` until explicitly reconciled. A merged change to the bundled policy does not retroactively update user-specific project files.
- Do not automatically merge; review the shortened primary instructions, the authoritative policy, and the on-demand details.

