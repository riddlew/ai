---
name: brain-init
description: Use when setting up or locating a project brain, or installing its collaboration policy and workflow guides.
---

# Brain Init

Create or reconnect **one** project Brain (`00_index.md` required), install the bundled collaboration policy and workflow guides, and discover project knowledge without guessing. Never run project code/tests or commit; do not edit feature, planning or review documents.

## Workflow

1. **Locate and authorize.** Resolve a user-specified valid Brain, saved `Project brain:`, current worktree `.brain/`, then linked worktree main checkout. A saved but invalid location is a blocker, not permission to create another Brain.

**Write access.** Follow `CLAUDE.local.md` §Worktrees and brain writes. If a required write is denied or outside the session's authorized boundaries, stop and report it; never route around the restriction or copy the Brain elsewhere.


2. **Policy and guides.** Read `${CLAUDE_SKILL_DIR}/references/CLAUDE.local.md`. Install the missing `CLAUDE.local.md` without overwriting customized instructions; merge only verified non-conflicting sections when authorized. Install the bundled `USAGE.md` and `README.md` **inside the selected Brain** (not the repository's README); preserve differing user copies. Register guide rows without changing `Last synced`. For actual commands, see `${CLAUDE_SKILL_DIR}/references/deterministic-tooling.md`; preview before `--apply`, specify an authorized root and optionally `--save-location`.
3. **If creating a new Brain:** do so from the main checkout or authorized shared location; choose tracked versus ignored with the user (ignored is the default). Inspect source, tests, manifests, docs and Git history for discoverable facts. Ask individually only about purpose, users, goals, planned features and consequential decisions not inferable from code. Record unresolved facts as questions, not assumptions.
4. **Create knowledge.** Use the root schemas in `${CLAUDE_SKILL_DIR}/../brain-update/references/templates.md`, relevant root purposes and ADR conventions in `brain-update`. Create applicable files and an index with full HEAD SHA and `Main branch:`; no fake or empty placeholder docs. Features use `01-brief/`, `02-specifications/`, `03-components/`, `04-implementation-plans/`, `05-tasks/` and separate `execution.md`, described in `${CLAUDE_SKILL_DIR}/references/feature-document-contract.md`.
5. **Report** actual Brain path, installed/preserved policy and guides, Git tracking, missing decisions and next valid workflow. `brain-update` owns root knowledge afterward.

## Exceptions requiring detailed procedure

Read `${CLAUDE_SKILL_DIR}/references/init-details.md` when reconciling an existing customized policy, a linked worktree or external Brain, a broken saved path, first-run interviews, or legacy document layouts. **Do not move, import, or translate legacy feature documents** as part of initialization. Never stage, commit or push. Do not dispatch subagents unless asked.
