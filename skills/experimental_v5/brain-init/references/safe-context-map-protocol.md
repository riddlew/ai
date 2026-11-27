# Optional deterministic context-map protocol (legacy-compatible)

This reference describes the optional scope-map workflow, **not a mandatory loading gate**. If a project uses it, run the bundled `brain-context` planner for candidate documents, read every selected document, and independently search for related files. Its mapped paths and fingerprints never prove semantic completeness.

# Safe selective Brain context loading

The objective is to **avoid repeatedly sending unrelated Brain documents into Claude's context** while preserving applicable constraints and verified technical details. This is a conservative retrieval plan, not a replacement for inspecting source code, tests, external authoritative sources, or project instructions.

## Runtime and selection

The bundled launcher is in the installed brain-init skill's scripts/brain-context. Run it with sh. It prefers Python 3.10+, falls back to Node.js 18+, then POSIX shell/awk/Git; no pip/npm dependencies.

First locate the **single** project Brain according to CLAUDE.local.md. Determine the actual Git branch, relevant feature slugs, and **all known candidate source paths** before planning. A guessed or narrowed path list is not coverage. Claude must expand paths after inspecting owners, callers, tests, configuration and related modules.

    sh "${CLAUDE_SKILL_DIR}/../brain-init/scripts/brain-context" plan \
      --brain /absolute/path/to/.brain \
      --branch feature/payment-retry \
      --feature payment-retry \
      --path src/payments/gateway.py \
      --path tests/test_gateway.py

Inside brain-init use the local scripts/brain-context instead. Repeat --feature and --path for each relevant part. Paths refer to the repository root, not to the Brain.

The command returns MODE (selective or full), REASON, ordered READ paths relative to the Brain, and BYTES (selected/total). **Actually read every READ file** before proceeding. Never treat the list as a semantic summary. If the command errors, falls back, the map is incomplete, task scope is unclear, or a discovered cross-module dependency is not in the original scope, read broadly rather than forcing a smaller result.

## Guaranteed initial context

When they exist, the following are always selected in selective mode:

- 00_index.md, 01_about.md, 02_features.md, 03_architecture.md
- 09_user_decisions.md, open_questions.md, state.md, glossary.md

The planner selects the active branch's pending file, not other branches' pending files, plus the entire selected feature folder (brief, specs, components, approved plans, tasks, execution evidence), and explicitly scoped ADR/source-map/technical-knowledge documents. It follows document-path and filename references in both directions, conservatively including multiple same-named candidates when ambiguous; purely navigational index/state links do not automatically load every listed document. It also checks Brain text for exact source-path and feature-path mentions.

All task-relevant repository guidance, existing code owners, callers, tests, external specifications and documentation must still be read separately. A source map is a pointer to authority, not proof of protocol bytes or conformance. A verified hash proves unchanged bytes, not correct applicability.

## Scope map

The Brain root may contain a reviewed **context-map.tsv** (UTF-8, tabs). It is a deterministic inventory, not semantic search. Generate a safe all-global starting point:

    sh "${CLAUDE_SKILL_DIR}/../brain-init/scripts/brain-context" map \
      --brain /absolute/path/to/.brain

Example fields, with literal tab separators:

    # brain-context-map v1
    03_architecture.md	global	-	<Git blob SHA-1>
    07_integrations.md	scoped	path:src/integrations/	<Git blob SHA-1>
    knowledge/payments/retries.md	scoped	feature:checkout;path:src/payments/	<Git blob SHA-1>

Each data row has four fields: Brain-relative path, mode (global/scoped), selectors, and content hash. Global uses "-" and always loads. Scoped needs feature:<slug>, path:<exact-file>, or path:<directory/>. Multiple selectors are separated with semicolons. Directory matching respects boundaries: src/payments/ does not match src/payments-old/.

Map **every** root project-knowledge Markdown file and every ADR, source map, technical knowledge, planning, diagnosis and review Markdown file. Feature documents and pending files are loaded through the active feature and branch and need no map rows. Unknown or newly created documents, changed fingerprints, malformed/duplicate rows, absent maps or unknown task scope force full loading. A mapping is a reviewed assertion of which modules each document governs, not a guess. Use global when uncertain.

Do not refresh changed hashes merely to re-enable selective mode. Recheck content, scope, neighboring owners and links after meaningful changes. brain-update owns this map and **still reads all root project-knowledge files** during synchronization. Existing authoritativeness, approval and provenance rules are unchanged.

## Context expansion and fail-safe behavior

1. Identify branch, features and likely affected source paths, including cross-module owners/callers.
2. Run the planner and read every selected file. If MODE=full, read all returned files. Full fallback omits pending files belonging to other branches.
3. Read additional applicable ADRs, specs, knowledge, original sources, instructions, code and tests discovered during the work. The plan is a minimum set, **never an exclusion rule**.
4. When new owner/caller/test/module paths appear, rerun the plan using all of them. If mappings cannot prove coverage, read broadly.
5. After compaction or a governing content revision, rerun and reload lost context.
6. Address conflicting requirements and stale approvals through existing workflow gates, not assumptions.

The initial map is intentionally all-global. Token savings begin only when a reviewer scopes particular long documents responsibly. No deterministic path map can prove semantic completeness; measure actual tokens and run missed-constraint checks before claiming effectiveness. Do not change approval gates or the ownership of root project knowledge.
