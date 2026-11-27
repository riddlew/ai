# Brainstorming details (v5)

**Preserve interactive, evidence-based brainstorming.** Brainstorming is not a specification-writing or code-editing authorization.

## Discovery and decision table

Read relevant project guidance, authoritative user decisions, source, interfaces and tests. Maintain a small table of `Established`, `Investigate`, `User decision`, `Deferred`. Confirm discoverable facts from code rather than interrogating the user. Ask the smallest useful set of dependency-ordered consequential questions (often 1–3), showing viable alternatives, tradeoffs and a recommendation.

Use lenses when relevant: behavior/observability, architectural ownership, API/wire contracts, data lifecycle, failure handling, security, concurrency, boundary compatibility and preservation of existing behavior. Do not invent speculative requirements or insist on every lens for simple changes.

## Design conversation

Let the user describe intended code structure and patterns if they care. Distinguish explicitly established binding preferences from tentative ideas and local implementation discretion. Identify concrete examples, failure and compatibility behavior, non-goals and meaningful unknowns. Discuss until the user settles the direction; confirmation of direction is **not a document approval status transition**.

## Result

Give a concise summary: intended outcome, changed and preserved behavior, agreed technical constraints, remaining questions, known dependencies and recommended action. The user may immediately invoke `brain-implement` without a spec, plan, tasks, approval or `brain-update`. No additional skill invocation is required.

For a new feature needing cross-session continuity, optionally save a brief/minimal authoritative decision record or `handoff.md` with references to existing decisions; avoid duplicated requirements. For an existing feature, directly update narrowly affected spec/plan sections when safe; for material mid-implementation changes, prefer a focused amendment with explicit supersession.

Only show a visual companion when helpful and requested/appropriate. Use source evidence; do not call `brain-update` or edit production code automatically.
