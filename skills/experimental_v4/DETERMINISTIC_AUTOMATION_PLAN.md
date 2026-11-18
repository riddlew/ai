# Deterministic automation plan for experimental_v4

Status: **Core command families implemented and verified in 77 static/cross-runtime tests on Linux and macOS; ready for PR review. Selective-loading policy changes remain deferred.**
Base: main at c8713000ac3437ab295ca58053b82334d74c3a20
Work branch: feature/deterministic-brain-tooling

## Goal and scope

Replace repeatable Brain-skill operations with deterministic, locally executable code. Keep AI responsible for judgment: understanding the project, selecting meaningful feature boundaries, drafting requirements/designs/tasks, reconciling conflicting evidence, and obtaining approvals. Move path selection, scaffolding, ID assignment, metadata management, structural checking, Git inventories, indexes, and evidence bookkeeping into scripts.

This plan covers five phases and all relevant skills under skills/experimental_v4/. It does not change the five document types, document ownership, the lightweight direct-implementation path, or the user's approval gates. No script can infer approval from a successful validation, test result, or user request to create a document.

## Runtime contract (mandatory for every phase)

**Three implementations of every logical executable: Python, JavaScript, and shell.** Python is preferred; if unavailable use Node.js; if both are unavailable use POSIX shell. No Python packages or npm packages may be required: use only the Python standard library, Node.js built-ins, and POSIX shell/standard utilities. Git is an explicit prerequisite only for commands that inspect or modify Git metadata, calculate Git blob hashes, or manage worktrees. Do not rely on jq, yq, PyYAML, npm, pip, curl, GNU-only flags, or a network service. Node scripts use .mjs and the built-in node modules; Python scripts use .py; shell scripts use .sh.

A tiny POSIX-shell launcher, brain-tool, selects the runtime once, in this order:
1. If BRAIN_RUNTIME is explicitly set to python, node, or sh, use that runtime or fail clearly if unavailable.
2. Otherwise use python3 when a supported interpreter is available, else node when a supported interpreter is available, else /bin/sh.
3. Once selected, a failed command must fail visibly; **never retry a mutating operation using another runtime**. Runtime selection is not authorization to cross filesystem boundaries.

Implementation layout (all six families exist in **each** language-specific entry point; consolidating them avoids 18 tiny wrappers):

| Families | Python | Node.js | POSIX shell |
|---|---|---|---|
| init, doc, validate, git, record, context | `scripts/brain-tool.py` | `scripts/brain-tool.mjs` | `scripts/brain-tool.sh` |

The shell validator uses bundled `brain-tool-scan.awk` and `brain-tool-validate.awk`. The shared scaffolds live in `scripts/scaffolds/`. The selector is `scripts/brain-tool`. This consolidation changes file organization, **not** the requirement for independent behavior in all three runtimes.

The launcher is only a shell runtime selector, not a fourth implementation of domain logic. Prefer a small common command contract over many one-off scripts. Reuse existing Python validation logic in brain-init/scripts/validate_feature_docs.py; retain that entry point for compatibility or make it a thin Python wrapper once equivalent implementations exist. Source and templates remain bundled with the skills and resolved relative to the installed skill directory, never the caller's current working directory.

**Cross-runtime rules:**
- Same subcommands, argument names, defaults, exit codes, input constraints, output fields, and observable file results in all three runtimes. Return concise human-readable output and optional structured JSON; test identical semantics across runtimes. Shell must have its own parser/serializer for the supported bounded formats, not invoke Python or Node.
- UTF-8, LF, canonical ordering, stable IDs, and no hidden timestamps in reproducible artifacts. When time is necessary, allow a supplied value for testing; otherwise record actual UTC time.
- Only parse the documented minimal YAML frontmatter subset; reject unsupported syntax with a clear diagnostic. Do not implement a general YAML parser independently in three languages.
- Commands that write default to preview/dry-run; require explicit --apply. Never silently overwrite, renumber, delete, update an approved document's parent hashes, or mark a draft approved. Respect the selected brain's location and authorized write scope. A script's ability to write a path does not grant authorization.
- Use exclusive create for new files, check conflicts before changing existing files, and make repeated runs idempotent. For multi-file changes, preview the complete change set first and report any partial failure; do not claim an atomic multi-file transaction unless implemented and tested. Avoid shell-specific unsafe quoting/eval and path traversal. Reject malformed slugs, unexpected symlinks, and paths outside the intended brain.
- Code may prepare changed content and report a diff, but consequential reconciliation requires explicit confirmation from the invoking skill/user. No network access, installation step, or hidden dependencies.
- The script's version and selected runtime appear in diagnostic output; normal successful output stays short. All substantive decisions and approval rules remain in the skills, not encoded as optimistic script assumptions.

## Phase 1 — Brain initialization and bundled-file installation

**Skills:** brain-init (primary), brain-update (index format), shared policy.

Implement brain-tool init:
- discover/select a valid brain using the explicit path, saved Project brain line, current worktree, and main-checkout fallback in the documented order;
- initialize a new brain only at an explicitly authorized location and chosen Git-tracking mode; create 00_index.md and only the applicable root structure; do not fabricate project-knowledge content;
- install bundled README.md and USAGE.md exactly, skipping identical files and preserving differing user-edited copies; register both as reference documents without duplicating index rows;
- install CLAUDE.local.md when absent; on existing customized policy produce a proposed section-aware diff/conflict report, not a blind overwrite or claim of complete semantic merge;
- manage exactly one intended Git info/exclude entry when ignored, and set or update Project brain only after checking for conflicting saved paths;
- report installed/existing/conflicting files and whether the Brain setup is complete; do not stage or commit.

**AI retains:** choosing tracked versus ignored setup with the user, investigation of project facts, determining which root knowledge files apply, drafting their substance, and deciding how to reconcile customized policies.

**Acceptance:** all three runtimes produce the same created files and results from empty, existing, partially configured, linked-worktree, conflicting-policy, and read-only fixtures; repeated --apply changes nothing; a denied write causes no fallback copy. Existing brain-init behavior remains available until these tests pass.

## Phase 2 — Feature document, planning, and report scaffolding

**Skills:** brain-brainstorm, brain-write-spec, brain-decompose-feature, brain-design-implementation, brain-write-tasks; also brain-plan, brain-diagnose, review skills where numbering is mechanical.

Implement brain-tool doc:
- create one requested draft at a time: brief, specification, component, implementation plan, or task; use existing feature-document-templates.md and the canonical feature folders; never generate five empty levels as a ritual;
- validate slugs and user-specified parent IDs; allocate the next available stable ID within the feature and kind, without reusing IDs; honor existing IDs on updates and fail rather than overwrite a conflicting filename;
- add required frontmatter, correct initial draft status, empty/default metadata lists, and a minimal body template with slots for AI-authored text; do not invent requirements, examples, dependencies, design constraints, or approvals;
- allow a supplied body or a separately reviewed edit after scaffolding; preservation of approved content and IDs is mandatory;
- scaffold planning INDEX.md and numbered planning tickets, diagnosis files, review report folders, and optional execution.md only when their owning skill explicitly requests them; preserve their current distinct ownership and numbering rules;
- provide a read-only inventory/list command, with IDs, paths, kinds, and statuses, so agents need not reconstruct the tree in text.

**AI retains:** whether a feature needs any particular level, semantic splitting and task decomposition, actual content, requirement/example definitions, dependencies, design approval, and whether an editorial change is materially behavioral.

**Acceptance:** correctly named files and parsable frontmatter for each type; optional/skipped levels work; deterministic ID allocation; no overwrite or duplicate ID under simulated collisions; exact parity across Python/Node/shell. A script must never auto-approve a created document.

## Phase 3 — Structural validation, fingerprints, coverage, and impact analysis

**Skills:** all five feature-document producers, brain-update, brain-implement.

Extend the existing structural validator through brain-tool validate, preserving the current CLI:
- validate required metadata, document kind/level, unique IDs, parent ordering, same-level dependencies, cycles, qualified requirement references, approved dependency status, and approved parent fingerprints;
- compute/read Git-blob SHA-1 for ignored/untracked parent documents (Git is required for this subcommand), with the same digest bytes in all runtimes;
- provide --show-parent-hashes and --check-coverage; print missing/extra hashes without editing the child, and keep the per-participating-specification coverage rule;
- add read-only impact graph and affected-documents reports from a changed parent/requirement, identifying direct and transitive descendants and independent unaffected chains;
- distinguish structural coverage from **semantic** completeness; report evidence gaps rather than asserting that requirement behavior is implemented;
- optionally prepare a proposed metadata patch for a draft, with human review required before applying; never silently refresh hashes on approved descendants or grant approval.

**AI retains:** interpreting requirement ownership, assessing testability and actual behavior coverage, reviewing revised approvals, and resolving intentional exclusions.

**Acceptance:** golden valid and invalid fixtures produce equivalent diagnostics across runtimes; all existing validator fixtures still pass; intentionally stale children are flagged; unrelated chains are not invalidated; no validation operation mutates files. Approval preservation is checked with negative tests.

## Phase 4 — Git summaries, indexes, pending changes, and execution evidence

**Skills:** brain-update, brain-implement, brain-plan, brain-review-code, brain-review-merge-request, brain-review-architecture, brain-review-security, brain-diagnose.

Implement brain-tool git:
- collect branch/HEAD/main-branch information, merge base, last synced SHA, committed change list, staged/unstaged changes, and relevant untracked files; output a bounded, factual manifest, not an AI-written explanation;
- identify renamed paths and missing/non-ancestor sync SHAs; report rather than guessing recovery or inventing historical facts;
- create or reconcile a pending/<branch>.md **skeleton** from verified branch identity, with branch/path collision detection and provisional markers for uncommitted work; do not infer or apply substantive Add/Change/Remove statements;
- prepare index inventory updates from actual document paths/status metadata, preserving human-written summaries and ownership rules; never promote branch-only implementation facts into main-root knowledge or rewrite normative feature docs;
- after a declared merge, prepare a diff/verification checklist for pending entries; applying semantic facts to main-root files still requires their current-code verification.

Implement brain-tool record:
- initialize and append structured execution checkpoints, task IDs, workspace/review-base pointers, test command/exit code/evidence paths, and verified Git SHAs; never mark work approved or done solely because a command exited successfully;
- record code-review evidence packets (base, changed files, local modifications, relevant paths, CI status when supplied locally) without substituting for a correctness review;
- allocate collision-free numbered planning, diagnosis, and review records and keep their basic indexes current; content and conclusions stay with the owning skills;
- require scoped, explicit updates so a record never overwrites a user's edits or resets review history.

**AI retains:** selecting meaningful facts from diffs, writing root knowledge, categorizing decisions/ADRs, interpreting failed checks, approving completed increments, reconciling pending facts after merge, and reviewing code/security/architecture.

**Acceptance:** dirty-tree and multi-branch fixtures retain user edits; cross-runtime manifests match; pending entries never leak unmerged facts into main; review bases and timestamps are preserved on resume; repeat operations avoid duplicate entries; no implicit git add/commit/push or approval.

## Phase 5 — Context-loading efficiency and measured token reduction

**Skills:** all skills using CLAUDE.local.md's full-root-read rule; brain-update for source maps and knowledge.

Implement brain-tool context:
- emit a compact deterministic manifest of root documents, paths, sizes, stored purposes/statuses, current branch and pending document, active feature chain, ADR links, and source fingerprints;
- support focused retrieval by explicit feature/ID/topic/path and show which documents were selected, omitted, and stale; use only metadata, explicit references, deterministic file matching, and Git state, **not** generated semantic summaries;
- compute changed-document and unchanged-document fingerprints to avoid redundant re-reading within a session when the assistant retains reliable prior content; never assume a hash alone captures the meaning of a source;
- produce a stable context packet or file-list suitable for the coding assistant, with explicit boundaries/limitations and citations back to source paths;
- add optional measurements of bytes/tokens **estimated** before/after, actual agent usage where available, missed-constraint rate, and file-read count. Treat estimated token counts as estimates, not billing facts.

**Critical gate:** the current policy intentionally requires reading every project-knowledge root .md file once per session. Keep that default until targeted behavior tests demonstrate selective loading does not omit approved decisions, security/architecture constraints, relevant pending changes, or critical project facts. This is a separate policy decision, not an automatic side effect of adding context-tool scripts.

**AI retains:** interpreting project knowledge, selecting additional sources when evidence is insufficient, resolving apparent conflicts, and deciding whether a manifest lacks enough context.

**Acceptance:** all three runtimes create equivalent manifests and focused packets; changing a governing decision or branch pending item invalidates the relevant cache; an explicit full-context mode remains available; measured reduction is reported with missed-decision checks. Do not change the mandatory read policy without user approval.

## Delivery sequence and work packages

| Order | Work package | Dependencies | Deliverable and verification |
|---|---|---|---|
| 0 | Runtime selector, command/error schema, threat model, fixture framework | none | launcher, three-runtime invocation tests, authorized-write guard; no domain changes |
| 1 | Phase 1 init/install | 0 | first production triad; idempotent setup fixtures; brain-init calls CLI |
| 2 | Phase 2 scaffolding | 0, 1 | document/record creation triad; producer skills call CLI |
| 3 | Phase 3 validator + graph | 2 | validator triad and compatibility wrapper; all existing fixtures pass |
| 4 | Phase 4 Git/record tools | 1–3 | Git and record triads; branch/dirty-state fixtures |
| 5 | Phase 5 context pack | 1–4 | context triad; measured usage and safety study; policy change only with approval |

Each work package includes source for **all three runtimes**, fixtures/tests for each, a short skill-integration patch, and a cross-runtime parity check. A phase is not complete if it works only in Python. Implement each phase on the same dedicated feature branch, but keep commits scoped so it can be reviewed separately; never modify main directly. Prefer simple independently testable operations and avoid a framework that creates more maintenance than it saves.

## Testing strategy without paid agent batches

1. Use Python unittest from the standard library for orchestration when Python is present; separately provide shell-based smoke tests so fallback behavior is testable when Python is absent. Use Node's built-in node:test/assert for Node-only testing. No third-party test framework.
2. Execute the same deterministic fixture cases with BRAIN_RUNTIME=python, node, and sh; compare normalized output, created-file contents, exit codes, and absence of unrelated changes.
3. Test the fallback selector using a controlled PATH (Python absent, Node present; both absent) and direct shell execution; never have the shell implementation call Python or Node internally.
4. Test read-only directories, path traversal, symlinks, unusual filenames, collision/rerun behavior, LF/UTF-8, stale hashes, mixed statuses, dirty Git state, worktrees, and wrong/absent Git metadata.
5. Keep each test completely local with temporary repositories. The normal verification path is deterministic CLI/unit tests, not fresh AI agent batches.
6. For significant changes to skill instructions, do one bounded fresh-agent **integration** test only when the deterministic tests cannot establish instruction-following; report untested behaviors rather than claiming them verified.

## Risks and tradeoffs

- **Triple maintenance cost:** three independently working versions multiply review and regression effort. Contain this with a small stable schema, a shared language-neutral fixture suite, and a limited number of command families; avoid feature-only special cases.
- **Shell limitations:** POSIX shell is suitable for predictable file operations and a bounded metadata grammar, not a general YAML/Markdown engine. Explicitly constrain the grammar and fail on unsupported input; do not silently reduce safety or validation in fallback mode. If faithful parity proves prohibitively complex, reconsider the three-runtime requirement with the user rather than shipping divergent behavior.
- **Scope authorization:** shell/Python/Node can sometimes physically write outside an agent's authorized workspace. The invoking skill must establish permitted destinations; every mutating tool must enforce the supplied explicit root and reject paths outside it. This is an application-level check, not a sandbox/security boundary.
- **State integrity:** multi-file edits can fail halfway; plan and preflight writes, preserve backups/previous data when needed, and explicitly report incomplete transactions.
- **Approval integrity:** mechanically valid docs and passing tests are not evidence of approval or semantic correctness. Never refresh stale fingerprints or mark execution done without the required review/approval.
- **Context optimization:** a smaller prompt can omit a decisive constraint. Preserve full-read behavior until measured quality supports changing it.

## Definition of done

- All six command families are implemented in the Python, Node and POSIX shell entry points, with shared language-neutral templates and no third-party language dependencies.
- Python preferred; Node fallback and shell fallback work without installing any packages; Git-only commands clearly require Git.
- Existing experimental_v4 skills invoke commands for mechanical work and stop rebuilding metadata/structure by hand, without shifting approval or document ownership.
- All old static/structural fixtures pass and new per-runtime parity, idempotence, permission, collision, and branch-safety tests pass in CI.
- No regression in optional document levels, tracked/ignored Brain behavior, shared-brain worktrees, stale approved-parent detection, pending-branch isolation, or resumable execution.
- Context savings and quality are measured; the full-root-read policy changes only in a separately approved decision.
- All changes remain on feature/deterministic-brain-tooling until reviewed and explicitly merged.


## Implemented scope and deliberate boundaries

The first implementation covers the repeatable, checkable operations across all five phases:

| Phase | Implemented | Retained for AI/user approval |
|---|---|---|
| 1 | Initialize index, install bundled guides and missing policy, preserve differing files, manage Git exclusions | Project-fact discovery, policy reconciliation for customized files, external Brain setup spanning separately authorized roots |
| 2 | Feature drafts with IDs/frontmatter, planning indexes/tickets, execution records, numbered diagnosis and review scaffolds | Content, scope, decisions, approval, revision of existing normative documents |
| 3 | Bounded YAML frontmatter, graph and reference checks, parent fingerprints, coverage, transitive affected-document reporting | Semantic completeness, approval status changes, fixing stale downstream documents |
| 4 | Git manifest, branch pending skeleton, unique factual execution checkpoints | Interpretation of branch changes, substantive pending entries, indexing human summaries, post-merge semantic reconciliation |
| 5 | Compact inventory, focused file reads, content fingerprints, estimated bytes/token volume | Mandatory full-root-read policy and quality-gated selective retrieval |

**Not automated by the current CLI:** section-aware merging of customized `CLAUDE.local.md`; applying or semantically reconciling existing index/pending entries; selecting what source facts are authoritative; measured agent token savings; selective-root-loading policy changes. These require user decisions, project-specific reasoning, or additional validation and are **not** silently treated as completed.

Verification uses Python unittest, standard Node built-ins, and POSIX shell/awk with no pip or npm dependencies. The CI matrix runs on Ubuntu and macOS, exercising macOS path aliases and BSD awk compatibility. The pre-existing Python validator remains the compatibility implementation. New cross-runtime tests check identical file results, script fallbacks, authorized-root protections, symlink denial, block YAML, stale hashes, bad references, collisions, and estimates; GitHub Actions runs these plus the existing static contracts and fixture validator. No paid AI agent batch is needed for deterministic contracts.
