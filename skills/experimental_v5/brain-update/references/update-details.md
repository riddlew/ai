# Manual Brain update — detailed cases (v5)

**Only explicitly invoked by the user.** Own root project knowledge, `adrs/`, `sources/`, `knowledge/` and indexes. Do not edit other producer-owned feature, plan, execution, handoff, diagnosis, planning or review documents. Never access `.brain/.notes/` by default.

## Evidence and branch safety

Find the shared Brain and its `Main branch`/`Last synced` anchors. Use Git committed changes, relevant actual diffs, uncommitted state and new or changed source documents to identify affected areas. Prefer targeted root reads and source references; broaden when a changed dependency, rebase, rename or conflict makes it necessary. Verify exact source identities, versions, sections and original normative contracts. Keep unverifiable statements marked as such.

On main, advance `Last synced` only after coverage of verified committed main facts; do not silently certify uncommitted work. On non-main worktrees, keep branch-only implementation details provisional in `pending/<branch>.md`. Never mix unrelated branches or treat matching names as proof of merge. Reconcile after verified main merge/confirmation, preserving unrelated root content and user history.

## Content destinations

- `00_index.md`: location, main branch, last verified sync, index and project version marker where applicable.
- `state.md`, feature lists and core architecture: verified project state and canonical references.
- `09_user_decisions.md`: durable established user choices without duplicate full specs.
- `open_questions.md` / `spikes.md`: unresolved significant choices and unverified source questions.
- `adrs/`: enduring architecture decisions with explicit supersession and evidence.
- `sources/`: authoritative document maps by exact source sections and versions; linked `knowledge/` topics summarize verified details without overriding originals.
- `pending/`: branch-only/uncommitted implementation facts clearly labeled provisional.

Preserve factual provenance and avoid unnecessary updates to unchanged documents. Do not promote speculation or historical v4 approval status into new decisions. Never automatically create new feature stages, invoke project code/build/tests, dispatch subagents, stage or commit. Validate structural feature links and report broken references to their owners rather than rewriting them.
