# Engineering Collaboration Policy

The user owns consequential product and architecture decisions. This policy applies to all Brain skills; follow applicable repository guidance, approved specifications and ADRs. Read detailed procedures only when the situation requires them.

## Decision authority

- **Verify facts** from current source, tests, configuration, documentation and experiments. Distinguish implemented behavior from required behavior and disclose uncertainty.
- **Honor established choices:** approved specifications, ADRs and `09_user_decisions.md` govern intent; don't reopen them silently. Source documents explicitly designated authoritative govern their contracts over derived summaries.
- **Decide routine details:** low-risk, local, reversible implementation choices consistent with approved design need no user question.
- **Consult for consequences:** changes to user-visible behavior, ownership/lifecycle, API/protocol/persistence/security, concurrency guarantees, important architecture or irreversible cost require explicit approval **before acting**. A recommendation, draft or test result is not approval of a consequential choice.
- **Implementation authorization:** An explicit request to implement authorizes routine code changes within the agreed scope, not unapproved redesign or unresolved consequential decisions. Automatic skill invocation, a request to investigate or draft a plan, or approval of a specification, implementation plan or task list does **not** independently authorize implementation.
- First investigate discoverable facts and approved decisions. Ask only unresolved, material choices with a concise recommendation; wait for the answer. If approved records conflict without an explicit later supersession, stop the affected scope and consult.

For decision tradeoffs and review discipline, consult `brain-init/references/engineering-details.md` only when relevant. Preserve project-specific instructions alongside this policy.

## Project brain loading

**Private notes boundary:** `.brain/.notes/` is user-owned and outside Brain knowledge, discovery, and maintenance. Never list, search, scan, read, index, summarize, copy, sync, edit, move, or delete anything inside it by default. Read specified notes **only when the user explicitly requests it**; authorization to read never authorizes modification. Exclude this subtree from broad file traversal, context maps, inventories, and subagent context. Do not treat notes as governing requirements or project facts without explicit user direction.

Locate **one** Brain (must contain `00_index.md`) in order: explicitly supplied valid location; saved `Project brain:` path; current worktree's `.brain/`; main checkout's `.brain/` in a linked worktree. If none exists, follow the active skill's no-brain policy and mention `/brain-init` once.

**Read context based on the actual task, not a mandatory context-map maintenance ritual:**

1. Inventory the names of root-level project-knowledge `.md` files without reading every file (exclude workflow guides `README.md` and `USAGE.md`; never enter `.notes/`). Read available core project orientation (`00_index.md`, `01_about.md`, `02_features.md`, `03_architecture.md`, `09_user_decisions.md`, `state.md`, `open_questions.md`, `glossary.md`), other root documents relevant to the task (such as `04_data_model.md`, `05_settings.md`, `07_integrations.md` or `spikes.md`), and the active branch's `pending/<branch>.md` when present (`/` becomes `--`).
2. Read the active feature's governing **approved** brief, specifications, components, implementation plans, tasks and execution state where applicable. Consult root topic knowledge and ADRs that govern the scope.
3. Inspect actual code, owners, callers, tests and configuration. Search the Brain index, `adrs/`, `sources/`, `knowledge/` and linked files by feature, behavior, identifiers and **source paths**. Read matching documents and their references; verify exact contracts against original authoritative sources.
4. Expand as new dependencies emerge. If naming or scope is ambiguous, the task crosses multiple areas, or an important source map is stale or incomplete, **read more**, not less; a broad read of root project knowledge is preferable to missing governing facts. After compaction, reload applicable context.

The installed `brain-context plan` (Python / Node / POSIX shell) and reviewed `context-map.tsv` remain available as **optional discovery accelerators**, not a gate or an exclusion list. No matching row or successful fingerprint is proof that all relevant documentation has been found. See `brain-init/references/safe-context-loading.md` for the short discovery procedure. Never load an unrelated branch's pending facts as current. `brain-update` still reads **every** root project-knowledge file during main-branch synchronization.

`README.md` and `USAGE.md` installed in the Brain are workflow guides, not authoritative project-knowledge root files; read only useful sections. Do not give subagents the whole Brain by default; provide verified, relevant facts and references.

**Worktrees and brain writes.** Every Git worktree of the project uses the brain located above, so worktrees share one brain, whether it sits in the main checkout or outside the repository, and may update it when the session is authorized to write there. Before writing to a brain outside the active workspace, respect the session's authorized filesystem boundaries: technical writeability alone does not establish authorization. Never use shell commands, scripts, alternative tools, or a copy of the brain to get around those boundaries or a denied write; scripted brain maintenance within them is fine. If a required brain write is denied or outside those boundaries, say what could not be recorded and ask the user how to proceed. On a branch other than the index's `Main branch:`, unmerged branch-specific facts go in `pending/<branch>.md` (written by `brain-update`), not in the main-branch root files.

The Brain gives orientation, not proof of freshness. Check code, Git history and uncommitted changes before relying on implementation claims. Source maps and topic knowledge are retrieval aids; original authoritative source sections govern exact protocols and conformance.

## Feature documents and ownership

Use `brain-init/references/feature-document-contract.md` for the exact hierarchy, metadata, approvals, requirements, dependency/coverage rules and parent fingerprints. Available levels: brief → specification → component → implementation plan → task; `execution.md` records mutable evidence **separately**. Skip unnecessary levels; a small, settled change can be implemented directly. Never create placeholders.

`brain-brainstorm` owns briefs; `brain-write-spec` specifications; `brain-decompose-feature` components; `brain-design-implementation` binding plans; `brain-write-tasks` tasks; `brain-implement` execution state. `brain-update` alone maintains shared root knowledge, ADRs, source maps, technical knowledge and the index after initialization. `brain-plan` owns separate planning records. `brain-next` is read-only by default: it uses `state.md` only for feature discovery and uses each feature's governing documents, `execution.md`, task dependencies and actual Git/code evidence to recommend the next action. Only an explicit reconciliation request can coordinate owning skills; it never writes or approves their documents or implements code. No global current-step file is required.

**Authority boundaries:** Approved specifications, ADRs and `09_user_decisions.md` define required behavior and durable decisions; approved implementation plans bind agreed code structure but cannot override those authorities. Current code and descriptive root knowledge report what exists, not what is required; `execution.md` records work and verification, not new requirements. `glossary.md` governs terminology.

**Approval integrity:** a material revision to a governing approved document invalidates affected descendants until reviewed and renewed by their owning skills; unaffected work can proceed. Never silently refresh parent hashes or mark revised documents approved. Tasks are not permission to contradict specs or approved binding plans. If an authoritative conflict remains, consult.

## Implementation and reviews

Prefer the smallest verified change within agreed ownership. Inspect relevant code and tests. For substantial or design-sensitive work, obtain binding blueprint approval before editing. `brain-implement` defaults to **collaborative**, inline execution: after each coherent verified increment, show diff and tests and wait for approval; guided and autonomous modes require opt-in and never waive consequential decision approval. Maintain actual review-base and verification evidence; do not infer completion from checkboxes.

Save reports when requested or required; **standalone `brain-review-architecture` saves a baseline by default** when the Brain is writable. A specialist invoked solely for another review does not save a report unless requested. Use the appropriate review or diagnosis skill for detailed evidence and response formats.

## Development guides

`.brain/USAGE.md` describes example workflows; `.brain/README.md` is the catalog. Read relevant sections only. They never supersede applicable skills, this policy, approved decisions or authoritative contracts.

## Model tiers

Skills refer to "standard tier" and "strongest tier"; this table is the only place that maps tiers to models.

| Role | Tier | Model today |
|---|---|---|
| Task implementer, task reviewer, scoped re-review, spec, ticket-set, blueprint, and impl plan builder reviews | standard | Sonnet |
| Fix-round 4–5 implementer, final reviewer, final fix pass | strongest | Opus |
| Main session: brainstorming, writing specs, collaborative blueprints, architecture review | strongest | Opus |
| Main session: coordinating subagent-driven mode | standard | Sonnet |
| `brain-review-code` delegated assessment subagents | standard | Sonnet |
| `brain-test-skill` test agents, unless the role under test is strongest tier | standard | Sonnet |

Rules:
- Every subagent dispatch names its model explicitly, using this table.
- When a `brain-` skill starts, suggest switching only on a clear mismatch, say so once, and continue either way:
  - Sonnet while brainstorming, writing a spec, collaboratively designing a blueprint, or reviewing architecture → suggest `/model opus`.
  - Opus while coordinating subagent-driven mode → suggest `/model sonnet`.
- Inline implementation gets no suggestion (task difficulty varies); the inline final fix pass runs on the session model.
- To change models later, edit only this table.
