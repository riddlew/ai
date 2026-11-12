---
name: brain-update
description: Use when another skill changes project knowledge, when the user asks to sync or rebuild the project brain, or when importing or refreshing technical knowledge from authoritative project documents.
---

# Brain Update

`.brain/` is the project's central memory: what the project is, how it is built, what the user decided, what is open, and what is done. `brain-init` creates it. After that, this skill is the only writer of the root project-knowledge files, `adrs/`, `sources/`, and `knowledge/` (except that `brain-init` may register its two bundled guides in `00_index.md`). Other skills write their own documents into `.brain/` subfolders, then invoke this skill. Follow `CLAUDE.local.md` for decision authority.

**Always:**

- Write only inside `.brain/`. Verify implementation facts from code and git history; learn normative requirements from explicitly authoritative documents. Never run the project's code, tests, or build; a fact that needs an experiment goes in `spikes.md`.
- Never stage, commit, or push.
- Never dispatch subagents unless the user asks.
- Ask the user one question per message.
- Never edit documents other skills own (`specs/`, `tickets/`, `impl_plans/`, `planning/`, `diagnoses/`, `reviews/`). If one is stale or contradicted, say so in your report.

## 1. Find the brain

A brain is a folder that has `00_index.md`. Look first where the user says it is, or where a `Project brain:` line in your loaded instructions points. Then look at `.brain/` in the current worktree root. Inside a linked git worktree, then look at `.brain/` in the main checkout: the parent directory of `git rev-parse --path-format=absolute --git-common-dir`. Use the first brain you find, and write there. A `.brain/` folder without `00_index.md` (for example, one holding a spec another skill saved) is not a brain.

If the user gave a location, use it only if it is a brain, and tell them `/brain-init <path>` saves it for later sessions. If it isn't a brain, say so, and stop.

**No brain.** If none of these is a brain, change nothing and do nothing else: tell the user no brain was found and that they should run `/brain-init` first, then stop. This holds whether the user or another skill invoked you; a skill that invoked you continues without a brain. If a `Project brain:` line points to a folder that isn't a brain, say so too, and that `/brain-init <path>` points it at the right folder.

**Isolated worktree sessions.** Claude Code isolates a session in a worktree only when the session was started with `claude --worktree` or entered the worktree you are working in with `EnterWorktree`; a linked worktree alone is not isolation. An isolated session can't edit the main checkout. If this session is isolated, or an edit to the main checkout is refused, and the brain is in the main checkout, say so before investigating, and stop. Don't write the brain anywhere else or through shell commands. Tell the user to run `/brain-update` from a session in the main checkout, or to move the brain outside the repository and run `/brain-init <path>` from a session in the main checkout.

**Main branch and reminder.** Read the `Main branch:` line in `00_index.md`. If it is missing, or names a branch that doesn't exist (`git rev-parse --verify --quiet refs/heads/<name>` fails), detect the branch with `git symbolic-ref --short refs/remotes/origin/HEAD`, dropping the `origin/` prefix. If that fails, use a local `main` or `master` branch. If neither exists, ask the user which branch the root files describe. Write the line after `Git:`, replacing a stale one, and say so. Begin your reply with a list of the files in `.brain/pending/`: each one's branch, number of entries, and `Updated:` date. Mark a file "branch not found" when `git rev-parse --verify --quiet refs/heads/<branch>` fails. If `pending/` is empty or missing, list nothing.

## 2. Branches

The root files describe the main branch, and `Last synced` is always a commit on it.

**On another branch** (`git branch --show-current` isn't the main branch), write no branch-specific implementation facts or requirements from branch-only document revisions into the shared root files, `sources/`, or `knowledge/`. Instead, bring `.brain/pending/<branch>.md` up to date, writing a `/` in the branch name as `--`, from the template in `${CLAUDE_SKILL_DIR}/references/templates.md`. It covers the branch's committed change since `git merge-base <main branch> HEAD`; inspect staged, unstaged, and relevant untracked edits too, but label their effects provisional and do not present them as merged or completed. Write one entry per committed root-file change, under that file's heading, starting **Add:**, **Change:**, or **Remove:**, with a link to the spec or impl plan when there is one. Remove entries the branch's code or authoritative source documents no longer support. Record source-document changes and intended changes to `sources/` or `knowledge/` in the pending file when they exist only on this branch; index them against the authoritative source from main after merge. Before updating a pending file, check its `Branch:` header; if the `/` → `--` mapping collides with a different branch, stop and report the conflict rather than overwrite another branch's entries. Still write the user's decisions, answers, glossary terms, open questions, and spikes straight into the root files (§3 steps 4–5). In `state.md`, list the branch's work as in progress on that branch, linking the pending file. In `00_index.md`, list the pending file and any new or changed `.brain` documents with their statuses. Leave `Last synced` alone. On a detached `HEAD`, ask which branch the work belongs to.

**The user says a branch merged.** Apply a merge only on the main branch; on another branch, say merges are applied from the main branch, and apply nothing. Check each entry in that branch's pending file against the current code, and apply the ones the code confirms to the root files. Report the rest, and ask whether to keep them pending (the branch may have more to merge) or drop them. Once no entry is left, delete the file, mark its `state.md` items done, remove it from `00_index.md`, and continue with §3. If none of its changes are in the code, say so, and keep the file.

**Abandoned branches.** Delete a pending file only when the user says its branch merged or was abandoned. Report a branch that isn't found; never act on it by yourself.

**Synced from another branch.** On the main branch, if `Last synced` exists but isn't an ancestor of `HEAD` (`git merge-base --is-ancestor <sha> HEAD` fails), the brain was last synced from another branch. Say so, and re-verify every root file against the main branch. Move descriptions of code that exists only on another branch into that branch's pending file; `git branch --contains <sha>` names the branch, and if it doesn't, ask. Then set `Last synced` to `HEAD`. Skip this check on another branch: a sync on the main branch after the branch forked is normal.

## 3. Update

On the main branch:

1. Read **every project-knowledge root file**, unless already loaded in this session and still in context; include the index. This full read is intentional so changes can be checked against the entire project model. Exclude only the `USAGE.md` and `README.md` workflow guides installed by `brain-init`; consult relevant guide sections when needed.
2. Gather what changed since `Last synced`:
   - committed work: enumerate **all** paths and renames with `git log --stat <sha>..HEAD` and `git diff --name-status <sha> HEAD`, then inspect the actual diffs and surrounding source for every change that could affect project knowledge. Do not rely on commit messages or path names alone; avoid dumping unrelated large/generated diffs into context without inspecting their effects;
   - uncommitted work: inspect `git status --short`, relevant staged changes (`git diff --cached`), unstaged changes (`git diff`), and relevant untracked files (`git ls-files --others --exclude-standard`). `git status` alone is not evidence of behavior;
   - decisions, answers, and discoveries in the current conversation;
   - new or changed documents in `.brain/` subfolders;
   - authoritative source documents explicitly supplied for ingestion, plus changes to previously indexed source documents (follow §4a). Do not assume an arbitrary reference document is an approved requirement.

   If `<sha>` no longer exists (after a rebase, say), re-verify every root file against the current code instead of diffing, and say so.

   If `<sha>` exists but is not an ancestor of `HEAD`, follow §2 "Synced from another branch".
3. Apply verified changes to **every root file they affect**. Add what is new, correct what changed, and remove what is no longer true. Do not rewrite unrelated facts. Root files describe the committed main-branch implementation, not a history of tentative edits. For an authoritative document, also update the relevant source map and technical knowledge (§4a); do not force its details into the root overview.
4. Record each **durable, project-relevant** user decision in `09_user_decisions.md`, and write an ADR when one qualifies (§5). Move answered questions out of `open_questions.md`: put verified factual answers in the relevant knowledge file, and approved durable choices in `09` as appropriate. Resolve spikes (§4).
5. Add new terms to `glossary.md`, and use canonical terms in the root files you touch. Report term mismatches in subfolder documents rather than editing them.
6. Update `state.md` and the statuses in `00_index.md`, including any new `sources/` or `knowledge/` documents. Set `Last synced` to the full main-branch `HEAD` sha **only after verifying the committed changes it covers**. This SHA does not certify uncommitted changes or the version of an external source document; track document versions separately (§4a). Mark uncommitted work in progress, not done; do not present implementation facts based only on uncommitted edits as settled main-branch facts. Report those facts as provisional for a later sync after commit.
7. Split any root file over the size limit (§4).
8. Report the files you changed. For ingested documents, also report source identity/version, indexed sections, coverage gaps, and any knowledge marked stale or unverified. Then list everything that needs the user: contradictions, new open questions, new spikes, and stale documents owned by other skills.

### Authority

- **Implementation facts:** current code wins as evidence of what is implemented. When descriptive knowledge disagrees with code, correct the descriptive knowledge; do not pretend the code complies with an external requirement.
- **Intended behavior and contracts:** approved specs, ADRs, `09_user_decisions.md`, and documents explicitly designated authoritative govern their respective requirements. Source-derived `.brain/` summaries are subordinate to the original authoritative document. Report contradictions between code and requirements and between authoritative records; never silently change requirements or edit a governing specification.
- **Decisions:** only the user's decisions count. Your recommendations, review findings, and proposals the user did not approve never enter `09`, the glossary, or an ADR as decided.

## 4. Root files

| File | Holds |
|---|---|
| `00_index.md` | `Last synced`, `Git`, and `Main branch` header lines; every `.brain` document with purpose and status, including `pending/` files and the two workflow guides |
| `01_about.md` | Purpose, users, core concepts, how it works |
| `02_features.md` | What each feature does, by module (progress lives in `state.md`) |
| `03_architecture.md` | Stack, runtime, platforms, components and what each owns, dependency direction, domain boundaries |
| `04_data_model.md` | Entities, schema, relationships, derived data |
| `05_settings.md` | User-configurable surface |
| `06_ux_interface.md` | Visual language, layouts, interactions |
| `07_integrations.md` | External tools, file formats, OS APIs |
| `08_error_logging.md` | Error handling, operations, observability |
| `09_user_decisions.md` | One entry per user decision, linking its source |
| `glossary.md` | Canonical terms (required) |
| `open_questions.md` | Questions only the user can answer |
| `spikes.md` | Unverified technical assumptions |
| `state.md` | Features: planned, in progress, or done, with links (required) |

A project-specific topic gets the next free number, for example `10_protocols.md`.

**Knowledge quality:** include source file paths for implementation-specific facts and preserve behavioral contracts, ownership, invariants, non-obvious API details, and known pitfalls. Explain the system rather than duplicating code; do not discard details that would force repeated rediscovery. When a fact has not been verified on the current branch, mark the uncertainty and scope instead of asserting it as current.

**Workflow guides:** `README.md` and `USAGE.md` are read-only snapshots installed by `brain-init` and registered as `reference` in the index. Do not treat them as project facts, rewrite them during sync, or count their size toward the project-knowledge root limits.

**Size:**
- When a root file passes about 4,000 words, move its detail into `.brain/NN_<topic>/<subtopic>.md`, and keep a summary in the root file with links to the detail. Never drop content while splitting.
- Keep all root files together under about 25,000 words. Past that, condense by moving detail out.

**Spikes** resolve three ways:
- **Confirmed:** move the fact into the relevant root file and remove the entry.
- **Confirmed problem:** record the verified failure or constraint where relevant; create an open question only if a consequential choice remains, and a `09` entry only after a user-approved durable decision.
- **Deferred:** keep the entry, with a note.

**Glossary:** for each term, record what it means, what it includes and excludes, and how it differs from neighboring terms. Map UI labels to code and database names where they differ. Record aliases to avoid only when they prevent likely confusion. A new canonical term or a changed definition is a decision; confirm it with the user unless it is already established.

## 4a. Import and maintain authoritative technical documents

Use this workflow when the user asks to ingest a large technical document, points to an existing authoritative specification, or a previously indexed authoritative source changes. An external document becomes **authoritative only when the user or established project records designate it as such**; do not promote incidental reference material to requirements. Read the actual source, not only an earlier summary. This section complements normal Git syncing; it does not authorize modifying files outside `.brain/` or documents owned by other skills.

**Index once; retrieve by topic thereafter:**

1. **Identify and verify the source.** Record its **persistently accessible** repository path or stable URL, title, applicable systems, version/revision or content hash when available, and the date checked. Preserve the original in place; never replace or edit it. If the document only exists as a temporary chat attachment, report that future sessions need a stable project-accessible copy; do not imply an ephemeral path will work later. If the source cannot be opened or a section cannot be checked, mark that portion unverified rather than inventing a requirement or citation.
2. **Map the document.** Inspect its table of contents and relevant sections, tables, diagrams, appendices, and cross-references. Identify coherent technical topics (for example, framing, message formats, state machines, failure handling, and platform APIs). Create or update `.brain/sources/<source-slug>.md` using the source-map template. Map each covered topic to its **exact** source section/requirement ID and page, table, figure, or anchor where available, plus its corresponding brain knowledge file. Record coverage as `indexed`, `partial`, `unverified`, or `stale`; never claim complete coverage of unread material.
3. **Store useful technical knowledge.** Create or update topic-oriented documents under `.brain/knowledge/<domain>/<topic>.md`, using the source-derived knowledge template. Include enough verified detail for ordinary reasoning without reopening the original: behavior, interactions, constraints, invariants, significant APIs, message layouts with offsets/types/endianness where relevant, edge cases, and known pitfalls. Include precise source references beside important contracts. Distinguish **explicit source requirements**, **observed implementation**, **approved design choices**, and **unverified assumptions**. Do not transcribe the entire source, pad files with generic explanations, or reduce critical formats to vague one-line summaries.
4. **Make it discoverable without loading it all.** Keep a concise overview and links in affected root files (`03_architecture.md`, `07_integrations.md`, etc.) and register the source map and topic documents in `00_index.md`. The mandatory full-root read remains unchanged; source maps and detailed knowledge are read **on demand** through the index. Never require loading every source document or technical topic for every task.
5. **Check consistency and provenance.** Cross-check the recorded technical facts and section mappings against the original, including important tables, diagrams, and normative exceptions. For a large specification, track requirement IDs and covered sections so omitted areas are visible. Compare requirements with other applicable authoritative records and relevant current code. If they disagree, record the precise conflict and ask for the consequential decision; do not silently reconcile it or modify the governing source. Requirements in a source document do **not** become entries in `09_user_decisions.md` unless the user actually approved a separate decision.
6. **Refresh incrementally.** On subsequent syncs, check the available source's version/hash and relevant Git changes. If it changed, re-examine affected sections and update corresponding topic files and source map. If you cannot verify them, mark them `stale` and report the gap. `Last synced` describes main-branch code, **not** the freshness of external source material.

**Precision rule:** The topic document is a retrieval aid, not a replacement for the original. For exact wire bytes, validation boundaries, compatibility claims, timing guarantees, and conformance testing, follow its references and verify against the authoritative section. If an indexed detail is not supported at the cited location, correct the brain and report it. Do not manufacture page numbers, section IDs, field encodings, or completeness claims. On a feature branch, put branch-only source changes into `pending/` rather than contaminating main-branch knowledge (§2).

## 5. ADRs

Write `.brain/adrs/NNNN-<slug>.md` (the next number, or `0001` if there are none) only when all three hold:

1. The user approved the choice, or it is already an authoritative project decision.
2. Credible alternatives existed, and a future maintainer could reasonably decide differently from the code alone.
3. Reversing it would need meaningful coordination, migration, or structural change.

Link the ADR from its `09` entry. Separate the user's stated rationale from your own inferences. Never rewrite an accepted ADR. Supersede it with a new ADR, and mark the old one `superseded` in the index.
