# Brain v5 — Usage

## Direct brainstorm → implementation (no spec or plan)

```text
/brain-brainstorm
Design order cancellation with existing authorization preserved.
/brain-implement
Implement what we just discussed, with relevant tests.
```

In the same session, use established brainstorming decisions. A fresh session may use a short decision record or optional `.brain/features/<feature>/handoff.md` pointing to authoritative requirements. **No `brain-update` call between these commands is necessary.**

## Direct request

```text
/brain-implement
Show the most recent received UDP heartbeat timestamp in the connection panel without changing timeout behavior.
```

No preflight specification, plan, tasks, approval, mode selection or progress file required. Claude inspects code, implements, verifies, and stops.

## Optional documented feature

```text
/brain-brainstorm
/brain-write-spec               # optional
/brain-design-implementation    # optional
/brain-update                   # user invokes if useful
/brain-implement
/brain-update                   # user invokes if useful
```

Documents are created without `status: approved`, reapproval or parent-hash gates. Use actual requirements and source evidence. The explicit implementation request authorizes code work, not an unresolved consequential redesign.

## Mid-implementation design change

After starting with `PLAN-001`, the user changes the dispatch strategy. Rather than rewriting everything, create a narrow `PLAN-002`:

```yaml
id: PLAN-002
kind: implementation-plan
parents: []
requirements: []
depends_on: []
amends: [PLAN-001]
supersedes: [PLAN-001#dispatch-strategy]
```

The original must contain the named anchor; it remains authoritative elsewhere. Do not generate amendment documents for minor helpers/refactors. Conflicting supersession requires reconciliation.

## Opus → Sonnet

At the end of Opus brainstorming, optionally save `handoff.md` with objective, authoritative decision refs, relevant code paths, blockers, next action. Start a fresh Sonnet session and use `/brain-implement`. Avoid copying an entire spec/plan; verify current source.

## Pair modes without plans

```text
/brain-pair-program Learning Mode
I will implement cancellation; review my design and code.
```

AI-led: Claude edits explicitly authorized code. Developer-led: user edits code suggested by Claude. Learning Mode: user owns code, Claude mentors and reviews. No routine approval after each chunk.

## Explicit knowledge management

`/brain-update` syncs durable verified knowledge only when explicitly invoked. `/brain-compact` is optional/manual/preview-first and preserves all decisions. Neither runs automatically.

## ZPL printer example

Brainstorm label output, CLI/YAML configuration, printer errors and exact ZPL command semantics. Point to source sections of authoritative ZPL documentation. Optionally write specs/plans for complex interactions, or implement directly. Verify exact emitted ZPL bytes, configuration parsing and printer error behavior in focused tests. Only meaningful protocol/architecture changes require focused amendments. Invoke `brain-update` manually after implementation.

## Boundaries

Default inline; subagents explicitly opt-in. Preserve existing user edits and worktree scope. Never inspect `.brain/.notes/` by default, invent passing tests, repeat identical failed debugging attempts, or perform unrelated work after completion.
