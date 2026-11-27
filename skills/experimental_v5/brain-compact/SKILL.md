---
name: brain-compact
description: Preview and coordinate information-preserving compaction of existing Brain Markdown, respecting document owners, approvals and parent fingerprints.
disable-model-invocation: true
argument-hint: "[Brain file | feature slug | .brain] [--preview-only]"
---

# Compact Existing Brain Documents

Reduce redundant prose in **existing** `.brain` Markdown without altering meaning, authority, or verification evidence. This explicitly invoked skill is a **preview-first coordinator**, not a new writer for other skills' files.

## Workflow

1. **Confirm mode and scope.** Follow `CLAUDE.local.md` `Execution mode selection`: recommend inline, but ask and wait if no mode was selected. Resolve the Brain and named file or feature; scan the whole Brain only on explicit request, in feature-sized batches. Exclude `.brain/.notes/` from every inventory, read, preview and write. Exclude installed `README.md` / `USAGE.md` unless specifically requested. Respect worktree authorization.
2. **Inspect without edits.** Read target documents, provenance, approvals, exact history and the relevant parents/children; identify each file's producing skill. Use `${CLAUDE_SKILL_DIR}/../brain-init/references/compact-writing.md`. Separate binding decisions and acceptance criteria from descriptive code facts and execution evidence. Skip material that cannot be shortened without losing relevant information.
3. **Preview changes.** Show original → proposed text or a unified diff for each proposed file, with content retained, owner, estimated savings, semantic equivalence and affected `parent_hashes`/approval dependencies. `--preview-only` ends here. Do **not write files before explicit user approval**. If equivalence cannot be supported, identify the blocker rather than guessing.
4. **Approve the preview.** User approval of specific wording changes permits **only those editorial changes**; it does not approve revised requirements, binding design or implementation. If the rewrite changes meaning or exposes a conflict with binding authority, stop and return to the appropriate owning skill's normal approval workflow.
5. **Apply through owners.** `brain-compact` **does not write producer-owned files**. If available, invoke their Skill tools with the approved diff, stable IDs, unchanged metadata and explicit documentation-only scope: `brain-brainstorm` (brief), `brain-write-spec` (spec), `brain-decompose-feature` (component), `brain-design-implementation` (plan), `brain-write-tasks` (task), `brain-implement` (`execution.md`; **no code change or increment advancement**), `brain-update` (root knowledge, ADR, sources and index), `brain-plan` (planning), and the corresponding review/diagnosis owner. Never commit or invoke implementation on the basis of compaction. If invocation is unavailable, **stop** and give a copyable owner command and context; never claim an unrun step completed.
6. **Validate and report.** After owner edits, compare actual content with the approved preview; preserve decisions, timestamps, stable IDs, actual commands/results, distinct checkpoints, statuses and source references. Run `validate_feature_docs.py` for changed feature docs where possible. **Any edited parent changes its byte fingerprint**, even for editorial-only changes: route affected child `parent_hashes` checks and renewals through their owners, with review and required user approvals. No silent hash refresh or descendant reapproval; preserve unrelated work. Report previewed/applied/blocked files and verified savings. Failure to validate means incomplete.

Do not combine distinct historical events or replace necessary self-contained requirements with vague links. No safe reduction → report that, without rewriting.

**Read on demand:** `${CLAUDE_SKILL_DIR}/references/compact-details.md` for example/owner routing; `${CLAUDE_SKILL_DIR}/../brain-init/references/compact-writing.md` for shared style; `${CLAUDE_SKILL_DIR}/../brain-init/references/feature-document-contract.md` for authority/approval/validation.

**Recommended next step:** End the final user-facing reply with one concise, evidence-based next action, naming the appropriate skill or command when useful. If blocked, identify the missing information, prerequisite, or approval instead of advancing; if complete, say no further action is needed. A recommendation is not authorization to execute another step. Keep it outside copy-ready deliverables.
