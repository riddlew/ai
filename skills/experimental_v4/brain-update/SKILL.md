---
name: brain-update
description: Use when another skill changes project knowledge, when the user asks to sync or rebuild the project brain, or when importing or refreshing technical knowledge from authoritative project documents.
---

# Brain Update

Keep the **single shared Brain** accurate and attributable to the proper main branch. This skill owns root project knowledge, `adrs/`, `sources/`, `knowledge/`, and indexes—not producer-owned feature, execution, planning, diagnosis or review files.

**Always:** Exclude `.brain/.notes/` from all discovery, indexing, imports, and synchronization. Never read it unless the user explicitly requests specific notes, and never modify its contents. Read facts from current source and Git evidence; requirements from approved authoritative documents. **Never run the project's code/tests/build, dispatch subagents, or stage/commit/push.** Write only inside the authorized Brain. Never turn unapproved recommendations into decisions or silently edit normative producer-owned docs.

## 1. Resolve and protect the Brain

Locate a valid `00_index.md` Brain from user path, saved `Project brain:`, current worktree, then linked main checkout. If missing, stop and request `/brain-init`. Use the index's `Main branch:`, checking Git if missing. **Write access.** Follow `CLAUDE.local.md` §Worktrees and brain writes. If a required write is denied or outside the session's authorized boundaries, report it and **never route around the restriction**.

## 2. Keep branches isolated

- **Main:** `Last synced` must identify a verified ancestor of main `HEAD`; if it doesn't, re-verify root descriptions before syncing. Never certify uncommitted work as committed.
- **Other branch:** committed and uncommitted branch-only implementation facts go in `pending/<branch>.md`, not main-root files or main source knowledge. Separate provisional uncommitted facts. Continue recording genuine user decisions/open questions in their root homes. Do not overwrite a pending filename collision.
- **Merged/abandoned:** only reconcile/remove pending entries on main after user confirmation and verification against actual merged code; report any unsupported entries. Never infer a merge from a branch name or status.

## 3. Sync the evidence

1. Read **every project-knowledge root file**, unless already retained accurately this session; exclude the bundled `USAGE.md` and `README.md`. **Do not use selective context loading** to skip root files during main-branch sync.
2. Gather full commits/renames since `Last synced`, staged/unstaged and relevant untracked content, session decisions, changed Brain documents and external source updates. Use `brain-tool git` for inventories if helpful; **inspect actual diffs and relevant source**, not just names or messages.
3. Apply verified main-branch facts to every affected root file, keeping unrelated facts. Record approved durable user choices in `09_user_decisions.md`, significant hard-to-reverse alternatives as ADRs, pending questions in `open_questions.md`, unknown source claims in `spikes.md`, and canonical terminology in `glossary.md`.
4. Keep source maps and topic-specific technical knowledge traceable to source identities, versions, exact sections and coverage statuses. Verify exact protocols and conformance against originals; a summary never overrides its authority. Mark stale/unverified parts, don't invent contents or promote incidental references to requirements.
5. Update `state.md`, `00_index.md`, branch pending inventory and document statuses. Report broken feature relationships with `validate_feature_docs.py` but leave correction to producers. Update `Last synced` to full main HEAD **only after** verifying the committed facts covered. Do not claim completeness for provisional/uncommitted changes.
6. Report files updated, source provenance/coverage gaps, unresolved contradictions, and next owner actions.

## 4. Read detailed instructions only when applicable

- `${CLAUDE_SKILL_DIR}/references/update-details.md`: branch merge and rebase recovery, indexed technical document ingestion, source coverage, exact root-file destinations, size limits, ADR supersession, stale status, and full pending-entry template.
- `${CLAUDE_SKILL_DIR}/references/templates.md`: root, source, knowledge and ADR document shapes.
- `${CLAUDE_SKILL_DIR}/../brain-init/references/feature-document-contract.md`: approval/traceability validation; never modify producer-owned feature documents.
- `${CLAUDE_SKILL_DIR}/../brain-init/references/deterministic-tooling.md`: file scaffolds, factual Git inventories and authorized write scope.

Keep the root schema and source/ADR semantics intact. The user—not synchronization—approves consequential decisions.

**Recommended next step:** End the final user-facing reply with one concise, evidence-based next action, naming the appropriate skill or command when useful. If blocked, identify the missing information, prerequisite, or approval instead of advancing; if complete, say no further action is needed. A recommendation is not authorization to execute another step. Keep it outside copy-ready deliverables.
