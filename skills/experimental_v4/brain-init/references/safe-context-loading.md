# Finding relevant Brain knowledge (default)

**Do not trust filenames or a maintained scope map to decide what can be skipped.**

1. Resolve the single project Brain and current branch using `CLAUDE.local.md`.
2. Read the core root project context, active feature documents and the current branch's pending notes described in the policy. Never promote another branch's pending notes into the current implementation.
3. Inspect code owners, callers, tests and configuration. Search `00_index.md`, ADRs, `sources/`, `knowledge/` and linked documents using feature names, behavior, requirement IDs, source paths, error names and integration boundaries.
4. Read matching topic documents and **follow their links to siblings and original sources**. Read exact protocol/API requirements in their authoritative source, not only in a summary.
5. When a new owner, caller, dependency or unknown constraint appears, expand the search and read more. If coverage is unclear, use a broad read of project knowledge. Rerun after losing context to compaction.

The original deterministic `brain-context` planner, map generator and three runtime fallbacks **remain available**. They are optional candidate-discovery tools, **not mandatory**, and a reviewed fingerprinted map is **not an exclusion list**. They may still return `MODE=full` for stale or incomplete maps. The separate `safe-context-map-protocol.md` documents the existing four-field `context-map.tsv` format and planner flags for projects that already use it. Do not create or maintain a map just to follow the normal skill workflow.

`brain-update` still reads **all** root project-knowledge files when synchronizing. Neither this procedure nor the optional planner changes user approval, authoritativeness, Brain write boundaries or source-document provenance.

## Practical discovery (no scope map required)

A feature can be governed by a document whose filename does not resemble the code path. After inspecting code owners/callers/tests, search both **paths and behavior terms**, including protocol IDs, error names, configuration keys and integration boundaries. For an ignored or external Brain, search its actual filesystem contents rather than assuming `git grep` can see them. For example, use `grep -RniE 'payment|timeout|src/payments/' "$BRAIN/knowledge" "$BRAIN/sources" "$BRAIN/adrs"` for directories that exist. Follow matching documents' references and inspect the original authoritative source for exact contracts. Do not treat zero matches as proof there is no governing document; broaden to root knowledge and adjacent modules when uncertain.
