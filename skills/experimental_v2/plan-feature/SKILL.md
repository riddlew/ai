---
name: plan-feature
description: Manage large, multi-session feature-planning efforts with durable, dependency-aware planning tickets under docs/planning/.
---

# Plan Feature

Use this skill for substantial or uncertain efforts that require planning across multiple sessions or days. Its persistent ticket structure is intentional; **do not use it for ordinary changes that can be planned in one session**.

Store planning state under:

```text
docs/planning/<feature-stub>/
├── INDEX.md
└── <ticket-files>.md
```

This skill owns planning scope, persistent state, planning-ticket decomposition and dependencies, cross-session continuation, and handoff to implementation-ticket generation. Delegate the interactive resolution of a `consult` ticket to `brainstorm`.

Use root `CLAUDE.md` for decision authority. This skill owns durable planning state, not permission to approve architecture or requirements.

Plan by default. Do not implement the final objective unless the planning material explicitly authorizes execution.

## Start

Planning may begin from a new idea, conversation context, or a linked plan/specification.

1. Establish the **final objective** and known exclusions.
2. Inspect existing project context where needed to distinguish known facts from open decisions.
3. Determine whether the effort warrants multi-session planning.

If it can reasonably be resolved in one session, **do not** create a planning directory. Use `brainstorm` or `write-spec` where appropriate rather than forcing this process. Do not interrupt a straightforward user-authorized task merely to ask whether the lighter workflow is acceptable.

Otherwise create `docs/planning/<feature-stub>/` with a concise, stable stub.

## INDEX.md

Use this structure:

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

Keep `INDEX.md` concise; put detailed evidence, alternatives, reasoning, questions, and resolutions in tickets. Do not label an unverified assumption as an approved constraint.

Anything beyond the objective belongs in **Out of Scope**, not **Open Areas**.

## Planning tickets

Create a ticket when a **real, consequential** question or prerequisite can be stated precisely, even if blocked. Do not generate tickets for speculative capabilities or routine implementation details merely to make the plan exhaustive.

Every ticket must:

- represent one decision, investigation, prototype question, or prerequisite;
- fit in one large agent session;
- declare its type, status, and genuine dependencies;
- record its evidence, options or work, and eventual resolution.

Use numbered filenames, for example:

```text
001-connection-ownership.md
002-failure-semantics.md
003-interaction-prototype.md
```

Required frontmatter:

```yaml
---
ticket-tag: consult
status: unresolved
depends-on: []
---
```

### Ticket tags

- `research` — investigate project-local or external facts needed for later decisions.
- `prototype` — create the smallest artifact needed to assess a concrete behavior or appearance.
- `consult` — resolve a bounded consequential decision with the user; default when judgment is required.
- `task` — perform prerequisite work necessary to make a later decision possible, **not** implementation of the final objective.

### Status

- `unresolved`
- `resolved`
- `excluded`

### Dependencies

List prerequisite ticket identifiers or filenames in `depends-on`. A ticket is actionable only if it is `unresolved` and all dependencies are `resolved`. Blocked tickets stay in the plan; do not fabricate answers to unblock them.

## Resolve tickets

Resolve **at most one non-research ticket per session**. Independent research tickets may be investigated in parallel if their dependencies permit it.

Do not use parallel work to settle multiple user decisions, run separately evaluated prototypes, or resolve multiple prerequisite tasks in one session.

### Research

Investigate using repository files, tests, documentation, available tools, and external evidence as appropriate. Record findings, confidence, and planning implications.

A research finding can eliminate impossible options, but **cannot decide the user's priorities or approve a new architectural boundary**.

### Consult

Invoke `brainstorm` with **only** the selected ticket's decision space:

- ticket question and reason it matters;
- applicable established constraints and decisions;
- resolved dependencies and needed evidence;
- clear boundary excluding unrelated tickets.

If the discussion reveals a newly consequential architectural choice, such as moving connection ownership into a new manager, either resolve it with the user when it belongs to the same bounded decision or record a separate dependent `consult` ticket. Do not silently adopt it.

A `consult` ticket is not resolved until the user explicitly approves its outcome. Then:

1. Record the approved decision, alternatives, and rationale in the ticket.
2. Mark the ticket `resolved`.
3. Add a short linked summary under `Resolved Tickets` in `INDEX.md`.
4. Reevaluate downstream dependencies.

Never infer the user's preferences or treat an assistant recommendation as a decision.

### Prototype

Produce only the minimum artifact needed to answer the ticket's question. Present it for user evaluation where judgment is required. Record the feedback and decision. The ticket remains unresolved until required evaluation is complete.

A prototype is planning evidence, not automatic authorization to implement production behavior.

### Task

Perform only prerequisite work needed to make a later planning choice possible. Record the result and implications. Do not implement the final objective by disguising implementation as a planning task.

## Continue an existing plan

Treat the planning directory as persistent authoritative state.

1. Read `INDEX.md`.
2. Use the user's selected ticket, if given; otherwise take the lowest-numbered actionable ticket.
3. Read that ticket and only the related context required for its dependencies.
4. Resolve it according to its tag, observing the one-non-research-ticket limit.
5. Update its status and detailed outcome.
6. Update the linked summary in `INDEX.md`.
7. Reevaluate dependencies and open areas.
8. Create, change, exclude, or remove tickets only when new evidence or user decisions justify it.

Do not reconstruct approved decisions from memory when the recorded planning files exist.

## Evolve the plan

Keep a genuinely undefined in-scope area in `Open Areas` until it can be expressed as a meaningful ticket. Then create its ticket(s) and dependencies and remove the corresponding open-area note.

When a decision makes future work unnecessary, exclude or remove that work instead of preserving it for completeness.

If a ticket falls outside the objective:

- mark it `excluded`;
- record the exclusion under `Out of Scope`;
- update dependent tickets;
- do not count it as an approved resolution.

## Execution boundary

The final feature is not authorized for implementation merely because planning is complete.

Permitted planning work includes bounded investigations, prerequisites needed for decisions, and minimal prototypes. None implicitly authorizes production implementation.

## Separate planning state from implementation state

The files under `docs/planning/` preserve **planning decisions and unresolved dependencies**. They are not execution trackers. Do not create `docs/implementation/` as part of planning and do not keep implementation checklists in `INDEX.md` or planning tickets.

When the user authorizes implementation, `implement` will create/resume one feature-level `todo.md` (and optional `guidance.md`) from the approved specification or ticket set. The feature's planning directory remains authoritative for planning history; the spec/tickets govern implementation, and the implementation workspace tracks progress. Do not duplicate state between these layers.

## Implementation handoff

Planning does not require implementation tickets by default. The user may implement directly from a completed specification or use `write-tickets` when the work spans multiple implementable sessions, independent increments, or an approved staged migration.

When implementation tickets are requested:

1. Check whether any unresolved decision materially affects implementation or decomposition.
2. If so, consult the user instead of choosing an architecture to move forward.
3. Otherwise invoke `write-tickets` using the planning materials as authoritative sources for **approved** decisions.
4. Let `write-tickets` own implementation decomposition, dependencies, acceptance criteria, user review, and `docs/tickets/...` creation.

Do not duplicate implementation-ticket generation here. The planning directory remains the durable record of decisions.
