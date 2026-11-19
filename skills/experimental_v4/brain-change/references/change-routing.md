# Change routing and handoff (read when needed)

This reference supports `brain-change/SKILL.md`. The installed `CLAUDE.local.md` and feature-document contract control decisions, write ownership and approvals. `brain-change` coordinates: **only the producer skills edit or approve their feature documents**.

## First necessary owning skill

| Change detected | First owner | Check downstream only where affected |
|---|---|---|
| New/changed behavior, invariant, error semantics, compatibility or acceptance example | `brain-write-spec` | `brain-decompose-feature` → `brain-design-implementation` → `brain-write-tasks` |
| Functional responsibility/coverage boundaries without behavioral change | `brain-decompose-feature` | `brain-design-implementation` → `brain-write-tasks` |
| Binding implementation architecture, API, lifecycle, threading or flow with unchanged behavior | `brain-design-implementation` | `brain-write-tasks` |
| Task definitions, dependencies or verifiable increments under unchanged binding design | `brain-write-tasks` | No earlier stage unless source authority actually changed |
| Reversible private helper, illustrative suggestion, or execution progress consistent with approved design | No feature-document revision | May be handled by `brain-implement` in a separately authorized session |
| Root project knowledge, ADRs, index, source maps (not feature-owned docs) | `brain-update` | If a feature requirement or plan changed, route to its own producer first |

Use `brain-brainstorm` only if consequential choices remain unresolved. A confirmed direction from a regular conversation works without brainstorming, but an earlier session's unrecorded decisions must be supplied or verified. An explicit request to change an artifact is **not** automatic approval of its revised written content.

## Safety and revision ordering

1. Read the current governing specification(s), optional component(s), binding plan(s), optional task(s), `execution.md` and relevant source and tests. Do not scan `.brain/.notes/`.
2. Classify changed and preserved requirements/design, identify affected descendants by `parents`, requirement IDs and actual semantic impact. Never mark unrelated documents stale as ceremony.
3. The specification owner preserves stable IDs, records material revisions as `needs-revision` and requests approval of the written revision. After this, affected child owners examine changed parents, reconcile metadata/content and renew approvals if required. An unchanged plan body does not justify automatically refreshing a stale parent fingerprint.
4. A component owner reviews coverage when requirement ownership or an existing component parent changed. A plan owner revalidates binding design and parent hashes even if the design ultimately remains unchanged. A task owner validates changed governing plans and acceptance evidence. Do not bypass ownership with direct file edits.
5. Preserve real implementation progress and recorded review-base/test evidence. If code was already changed, evaluate it against new approved requirements without retroactive approvals. Keep affected implementation paused until its governing artifacts are current and approved.
6. Invoke `brain-update` for shared project-knowledge synchronization after the relevant producing skill(s). It does not revise producer-owned specs/plans/tasks.

## Example after recorded brainstorming

`/brain-change yaml-cli`

"Reconcile the confirmed decision to warn rather than reject unknown YAML keys. Inspect the existing approved docs; use only affected owning skills and obtain required approvals. Do not implement."

## Example after an ordinary conversation

`/brain-change yaml-cli`

"I want unknown YAML keys to produce warnings instead of errors. First determine whether warning format, nested fields and CLI exit code are decided. Resolve any consequential gaps, then update affected specs, plans and tasks through their owning skills. Do not implement."

## Example for design-only revisions

`/brain-change tcp-server`

"The approved behavior is unchanged, but I want to change the connection's event-loop ownership. Review the binding design and impacted tasks, not the behavioral spec unless it contains a contradictory binding constraint."

## When skill invocation is unavailable

Give the exact next step, e.g.:
`/brain-write-spec Revise SPEC-001 for approved unknown-field warnings. Preserve IDs and report affected descendants; do not implement.`

State what actually completed and what did not. A later `brain-change` run should re-read the real document/approval state. Do not shell out to `claude` to bypass missing tools. Once reconciliation is complete, suggest `/brain-implement` as a **user-invoked** next action only.
