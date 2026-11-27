---
name: brain-update
description: Manually synchronize verified durable Brain project knowledge, sources and ADRs with code and established user decisions.
disable-model-invocation: true
---

# Brain update — manual only

Run **only when the user explicitly invokes this skill**. No other Brain skill may automatically invoke it. Before/after implementation sync is optional; no approval-only sync or document-status maintenance.

Own root knowledge, `adrs/`, `sources/`, `knowledge/` and indexes. Do not silently rewrite producer-owned feature docs, plans, execution or handoffs. Exclude `.brain/.notes/` from all discovery and operations. Follow the installed v5 project policy and authorized shared Brain/worktree boundaries; never bypass denied writes.

Resolve `.brain/00_index.md`, main branch and last verified sync. Inspect committed changes, relevant actual diffs, pending/uncommitted work, new authoritative sources, and changed decisions. Prefer verified delta-based reading of affected root knowledge and dependencies rather than rereading every root document; expand when history, renames or relationships are uncertain. Keep source-section attribution, version/coverage and original authoritative document semantics.

Main-branch knowledge reflects verified main commits; branch-only changes remain provisional in `pending/<branch>.md` until confirmed on main. Record durable decisions once in their canonical location and refer to them elsewhere. Maintain source maps/ADRs/root index, stale flags and provenance. Never infer approval from historical metadata or promote suggestions to decisions. Do not run project builds/tests, dispatch subagents without explicit request, or stage/commit/push.

Report verified changes and source gaps concisely. Read `references/update-details.md` only for complex merges, indexed document ingestion or history recovery.
