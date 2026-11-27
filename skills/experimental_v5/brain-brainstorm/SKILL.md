---
name: brain-brainstorm
description: Explore consequential requirements and architecture interactively; record decisions without approvals or automatic synchronization.
---

# Brainstorm

Preserve interactive, evidence-based brainstorming. Investigate actual code, decisions and technical sources before asking questions. Ask only unresolved consequential questions, in dependency order, with concrete tradeoffs and recommendations. Do not invent behavior; distinguish established decisions from assumptions. Confirm the chosen direction naturally with the user, not as a document approval gate.

When discussing an existing feature, identify affected specs/plans. Once the user settles a change, apply a narrow update directly to the relevant document, respecting existing identifiers and unrelated scope; for substantial changes during implementation prefer a focused amendment with explicit `amends`/`supersedes` links. Do not invoke a separate skill merely to update a known paragraph. Do not modify application code.

When a fresh session may implement the outcome without a spec, save a short authoritative decision note or optional `.brain/features/<feature>/handoff.md` referencing existing decisions; do not generate a full specification, require approval metadata, or call `brain-update`. Same-session implementation can rely on the current conversation. Unresolved important questions remain explicit.

Read `../brain-init/references/CLAUDE.local.md` and the feature contract. Load `references/brainstorm-details.md` only for complex dependency analysis or visual companion. Default inline; no automatic subagents. Keep output concise unless the user requests a detailed exploration.
