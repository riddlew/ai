---
name: brain-plan-feature
description: Manage large, multi-session feature planning with durable, dependency-aware planning tickets under docs/planning/. Use when an initiative has many interdependent decisions, research questions, or prototypes and will span several sessions or days; not for work that can be planned in one session.
---

# Plan Feature

Track planning state for substantial or uncertain efforts across sessions. This skill owns planning scope, planning tickets and their dependencies, and cross-session continuation. It delegates interactive decisions to `brain-brainstorm` and implementation decomposition to `brain-write-tickets`. Follow root `CLAUDE.md` for decision authority.

## Boundaries

- **Plan, do not implement.** Bounded investigations, prerequisite tasks, and minimal prototypes are permitted planning work. None of them, nor completed planning, authorizes implementing the final objective.
- **Planning state is not implementation state.** Do not create `docs/implementation/` or keep implementation checklists here. `brain-implement` tracks execution once authorized; the planning directory remains the record of planning decisions.

## Start

1. Establish the **final objective** and known exclusions.
2. Inspect project context as needed to separate known facts from open decisions.
3. Decide whether the effort warrants multi-session planning. If it can be resolved in one session, do not create a planning directory; use `brain-brainstorm` or `brain-write-spec` instead, without interrupting a straightforward authorized task to ask.

Otherwise create `docs/planning/<feature-stub>/` with a concise, stable stub:

```text
docs/planning/<feature-stub>/
├── INDEX.md
└── <NNN>-<ticket-slug>.md
```

## INDEX.md

```markdown
# <Planning effort>

## Objective

The final outcome.

## Notes and Constraints

Confirmed preferences, approved architectural decisions, relevant facts,
and explicitly marked assumptions or caveats.

## Resolved Tickets

Short linked summaries of resolved planning tickets.

## Open Areas

In-scope areas not yet precise enough to become tickets.

## Out of Scope

Work explicitly outside the objective.
```

Keep `INDEX.md` concise; detailed evidence, alternatives, and resolutions belong in tickets. Never label an unverified assumption as an approved constraint. Anything beyond the objective belongs in **Out of Scope**, not **Open Areas**.

## Planning tickets

Create a ticket when a **real, consequential** question or prerequisite can be stated precisely, even if blocked. Do not create tickets for speculative capabilities or routine implementation details.

Each ticket represents one decision, investigation, prototype question, or prerequisite; fits in one large agent session; and records its evidence, options or work, and eventual resolution. Use numbered filenames such as `001-permission-model.md`, `002-expiry-semantics.md`, `003-share-dialog-prototype.md`.

Required frontmatter:

```yaml
---
ticket-tag: consult
status: unresolved
depends-on: []
---
```

**Tags:**

- `research` — investigate project-local or external facts needed for later decisions.
- `prototype` — build the smallest artifact needed to assess a concrete behavior or appearance.
- `consult` — resolve a bounded consequential decision with the user; the default when judgment is required.
- `task` — prerequisite work that makes a later decision possible, never implementation of the objective.

**Status:** `unresolved`, `resolved`, or `excluded`.

**Dependencies:** list prerequisite ticket identifiers in `depends-on`. A ticket is actionable only when it is `unresolved` and all its dependencies are `resolved`. Blocked tickets stay in the plan; never fabricate answers to unblock them.

## Resolve tickets

Resolve **at most one non-research ticket per session**. Independent research tickets may run in parallel when dependencies permit; do not use parallel work to settle several user decisions, prototypes, or tasks.

- **Research:** investigate with repository files, tests, documentation, tools, and external evidence. Record findings, confidence, and planning implications. Research can eliminate options but cannot decide the user's priorities or approve a boundary.
- **Consult:** invoke `brain-brainstorm` with only this ticket's decision space: the question and why it matters, applicable constraints and decisions, resolved dependencies and evidence, and an explicit boundary excluding other tickets. If a new consequential choice surfaces, resolve it within this ticket when it belongs to the same decision, or record a dependent `consult` ticket. The ticket is resolved only when the user explicitly approves the outcome.
- **Prototype:** produce only the minimum artifact needed to answer the question, present it for evaluation, and record the feedback and decision. It stays unresolved until evaluation is complete.
- **Task:** perform only the prerequisite work and record its result and implications.

After resolving a ticket:

1. Record the outcome in the ticket (for `consult`: the approved decision, alternatives, and rationale).
2. Mark it `resolved`.
3. Add a short linked summary under **Resolved Tickets** in `INDEX.md`.
4. Reevaluate downstream dependencies and open areas.

## Continue an existing plan

Treat the planning directory as authoritative; do not reconstruct decisions from memory.

1. Read `INDEX.md`.
2. Take the user's selected ticket, or else the lowest-numbered actionable ticket.
3. Read that ticket and only the context its dependencies require.
4. Resolve it by tag, within the one-non-research-ticket limit.
5. Update the ticket, `INDEX.md`, dependencies, and open areas.
6. Create, change, exclude, or remove tickets only when new evidence or user decisions justify it.

## Evolve the plan

Move an open area into tickets once it can be stated as a meaningful ticket, and remove its open-area note. When a decision makes future work unnecessary, exclude or remove that work.

For a ticket outside the objective: mark it `excluded`, record it under **Out of Scope**, update dependent tickets, and do not count it as an approved resolution.

## Hand off to implementation

Implementation tickets are not required by default; the user may implement directly from a completed specification. When implementation tickets are requested:

1. Check whether any unresolved decision materially affects implementation or decomposition; if so, consult the user.
2. Otherwise invoke `brain-write-tickets`, using the planning materials as the authoritative source of **approved** decisions.
