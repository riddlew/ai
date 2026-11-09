---
name: brain-update
description: Use when another skill finishes work that changed project knowledge, or when the user asks to sync, update, or rebuild the project brain.
---

# Brain Update

`.brain/` is the project's central memory: what the project is, how it is built, what the user decided, what is open, and what is done. `brain-init` creates it. After that, this skill is the only writer of the root files and `adrs/`. Other skills write their own documents into `.brain/` subfolders, then invoke this skill. Follow root `CLAUDE.md` for decision authority.

**Always:**

- Write only inside `.brain/`. Learn facts by reading code and git history. Never run the project's code, tests, or build; a fact that needs an experiment goes in `spikes.md`.
- Never stage, commit, or push.
- Never dispatch subagents unless the user asks.
- Ask the user one question per message.
- Never edit documents other skills own (`specs/`, `tickets/`, `impl_plans/`, `planning/`, `diagnoses/`, `reviews/`). If one is stale or contradicted, say so in your report.

## 1. Find the brain

A brain is a folder that has `00_index.md`. Look first where the user says it is, or where a `Project brain:` line in your loaded instructions points. Then look at `.brain/` in the current worktree root. Inside a linked git worktree, then look at `.brain/` in the main checkout: the parent directory of `git rev-parse --path-format=absolute --git-common-dir`. Use the first brain you find, and write there. A `.brain/` folder without `00_index.md` (for example, one holding a spec another skill saved) is not a brain.

If the user gave a location, use it only if it is a brain, and tell them `/brain-init <path>` saves it for later sessions. If it isn't a brain, say so, and stop.

**No brain.** If none of these is a brain, change nothing and do nothing else: tell the user no brain was found and that they should run `/brain-init` first, then stop. This holds whether the user or another skill invoked you; a skill that invoked you continues without a brain. If a `Project brain:` line points to a folder that isn't a brain, say so too, and that `/brain-init <path>` points it at the right folder.

**Isolated worktree sessions.** Claude Code isolates a session in a worktree only when the session was started with `claude --worktree` or entered the worktree you are working in with `EnterWorktree`; a linked worktree alone is not isolation. An isolated session can't edit the main checkout. If this session is isolated, or an edit to the main checkout is refused, and the brain is in the main checkout, say so before investigating, and stop. Don't write the brain anywhere else or through shell commands. Tell the user to run `/brain-update` from a session in the main checkout, or to move the brain outside the repository and run `/brain-init <path>` from a session in the main checkout.

**Main branch and reminder.** Read the `Main branch:` line in `00_index.md`. If it is missing, detect the branch with `git symbolic-ref --short refs/remotes/origin/HEAD`, dropping the `origin/` prefix, or use the current branch if that fails; add the line after `Git:`, and say so. Begin your reply with a list of the files in `.brain/pending/`: each one's branch, number of entries, and `Updated:` date. Mark a file "branch not found" when `git rev-parse --verify --quiet refs/heads/<branch>` fails. If `pending/` is empty or missing, list nothing.

## 2. Branches

The root files describe the main branch, and `Last synced` is always a commit on it.

**On another branch** (`git branch --show-current` isn't the main branch), write no code facts into the root files. Instead, bring `.brain/pending/<branch>.md` up to date, writing a `/` in the branch name as `--`, from the template in `${CLAUDE_SKILL_DIR}/references/templates.md`. It covers the branch's whole change since `git merge-base <main branch> HEAD`: one entry per root-file change, under that file's heading, starting **Add:**, **Change:**, or **Remove:**, with a link to the spec or impl plan when there is one. Remove entries the branch's code no longer supports. Still write the user's decisions, answers, glossary terms, open questions, and spikes straight into the root files (§3 steps 4–5). In `state.md`, list the branch's work as in progress on that branch, linking the pending file, and list the file in `00_index.md`. Leave `Last synced` alone. On a detached `HEAD`, ask which branch the work belongs to.

**The user says a branch merged.** Apply a merge only on the main branch; on another branch, say merges are applied from the main branch, and apply nothing. Check each entry in that branch's pending file against the current code, and apply the ones the code confirms to the root files. Report the rest, and ask whether to keep them pending (the branch may have more to merge) or drop them. Once no entry is left, delete the file, mark its `state.md` items done, remove it from `00_index.md`, and continue with §3. If none of its changes are in the code, say so, and keep the file.

**Abandoned branches.** Delete a pending file only when the user says its branch merged or was abandoned. Report a branch that isn't found; never act on it by yourself.

**Synced from another branch.** If `Last synced` exists but isn't an ancestor of the main branch's `HEAD` (`git merge-base --is-ancestor <sha> HEAD` fails), the brain was last synced from another branch. Say so, and re-verify every root file against the main branch. Move descriptions of code that exists only on another branch into that branch's pending file; `git branch --contains <sha>` names the branch, and if it doesn't, ask. Then set `Last synced` to `HEAD`.

## 3. Update

On the main branch:

1. Read every root file, unless you already have this session.
2. Gather what changed since `Last synced`:
   - the code: `git log --stat <sha>..HEAD` and `git diff <sha>..HEAD`, read in full; a commit message is not evidence of what changed;
   - uncommitted work: `git status`;
   - decisions, answers, and discoveries in the current conversation;
   - new or changed documents in `.brain/` subfolders.

   If `<sha>` no longer exists (after a rebase, say), re-verify every root file against the current code instead of diffing, and say so.

   If `<sha>` exists but is not an ancestor of `HEAD`, follow §2 "Synced from another branch".
3. Apply each change to every root file it affects. Add what is new, correct what changed, and remove what is no longer true. Root files describe the present, not history.
4. Record each user decision in `09_user_decisions.md`, and write an ADR when one qualifies (§5). Move answered questions out of `open_questions.md` into `09` and the relevant root file. Resolve spikes (§4).
5. Add new terms to `glossary.md`, and use canonical terms in the root files you touch. Report term mismatches in subfolder documents rather than editing them.
6. Update `state.md` and the statuses in `00_index.md`, and set `Last synced` to the full `HEAD` sha. Uncommitted work is in progress, never done.
7. Split any root file over the size limit (§4).
8. Report the files you changed. Then list everything that needs the user: contradictions, new open questions, new spikes, and stale documents owned by other skills.

### Authority

- **Facts:** the code wins. When a root file disagrees with the code, correct the root file.
- **Intent:** specs, ADRs, and `09_user_decisions.md` win. When the code contradicts them, add an open question that names both, and report it. Never rewrite intent to match the code, and never edit the spec.
- **Decisions:** only the user's decisions count. Your recommendations, review findings, and proposals the user did not approve never enter `09`, the glossary, or an ADR as decided.

## 4. Root files

| File | Holds |
|---|---|
| `00_index.md` | `Last synced`, `Git`, and `Main branch` header lines; every `.brain` document with purpose and status, including `pending/` files |
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

**Size:**
- When a root file passes about 4,000 words, move its detail into `.brain/NN_<topic>/<subtopic>.md`, and keep a summary in the root file with links to the detail. Never drop content while splitting.
- Keep all root files together under about 25,000 words. Past that, condense by moving detail out.

**Spikes** resolve three ways:
- **Confirmed:** move the fact into the relevant root file and remove the entry.
- **Confirmed problem:** it becomes an open question, or a decision in `09`.
- **Deferred:** keep the entry, with a note.

**Glossary:** for each term, record what it means, what it includes and excludes, and how it differs from neighboring terms. Map UI labels to code and database names where they differ. Record aliases to avoid only when they prevent likely confusion. A new canonical term or a changed definition is a decision; confirm it with the user unless it is already established.

## 5. ADRs

Write `.brain/adrs/NNNN-<slug>.md` (the next number, or `0001` if there are none) only when all three hold:

1. The user approved the choice, or it is already an authoritative project decision.
2. Credible alternatives existed, and a future maintainer could reasonably decide differently from the code alone.
3. Reversing it would need meaningful coordination, migration, or structural change.

Link the ADR from its `09` entry. Separate the user's stated rationale from your own inferences. Never rewrite an accepted ADR. Supersede it with a new ADR, and mark the old one `superseded` in the index.
