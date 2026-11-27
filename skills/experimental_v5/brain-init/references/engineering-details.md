# Engineering decision boundaries (v5)

Investigate source facts independently. The user owns unresolved consequential behavior, security, public APIs, wire protocols, state ownership, persistence, concurrency guarantees and hard-to-reverse cost. Ask only choices with material consequences; routine local implementation and reversible helper details are the implementer's discretion.

Preserve existing interfaces, ownership and integration unless the user establishes a change. Prefer the smallest maintainable solution and meaningful verification. Treat actual code as implementation facts, not a license to override requirements. One authoritative home per decision; references are preferable to duplicate normative text.

An explicit implementation request authorizes changes within the requested established scope. A request to brainstorm, document, review or explain does not authorize code edits. No doc approval gates, no mandatory blueprints, no routine per-increment approval, and no automatic `brain-update`. Default inline, subagents only on explicit opt-in. Respect worktrees, private `.brain/.notes/`, user edits, and commits only when instructed.

Use bounded context, expand on evidence gaps, debug from observed symptoms and stop when scope and verification are complete. Do not accumulate unrelated improvements.
