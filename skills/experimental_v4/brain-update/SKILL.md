---
name: brain-update
description: Use when a project has no .brain/ folder and the user wants one set up, when another skill finishes work that changed project knowledge, or when the user asks to sync, update, or rebuild the project brain.
---

# Brain Update

`.brain/` is the project's central memory: what the project is, how it is built, what the user decided, what is open, and what is done. A new session reads its root files instead of re-reading the codebase. This skill is the only writer of the root files and `adrs/`. Other skills write their own documents into `.brain/` subfolders, then invoke this skill. Follow root `CLAUDE.md` for decision authority.

**Always:**

- Write only inside `.brain/`, plus `info/exclude` during a first run. Learn facts by reading code and git history. Never run the project's code, tests, or build; a fact that needs an experiment goes in `spikes.md`.
- Never stage, commit, or push.
- Never dispatch subagents unless the user asks.
- Ask the user one question per message.
- Never edit documents other skills own (`specs/`, `tickets/`, `impl_plans/`, `planning/`, `diagnoses/`, `reviews/`). If one is stale or contradicted, say so in your report.

## 1. Find the brain and choose a mode

A brain exists only when `.brain/00_index.md` exists. Look at the current worktree root first. Inside a linked git worktree, then look in the main checkout: the parent directory of `git rev-parse --path-format=absolute --git-common-dir`. Use the first `.brain/` that has `00_index.md`, and write there.

| Situation | Mode |
|---|---|
| No brain, and the user invoked you directly | First run (§2) |
| No brain, and another skill invoked you | Change nothing. Tell the user no brain exists yet and that `/brain-update` will set one up. |
| Brain exists | Update (§3) |

Another skill invoking you is never a request to set up a brain, however easy the code is to read. A `.brain/` folder without `00_index.md` (for example, one holding a spec another skill saved) is not a brain; keep its files and index them during the first run.

## 2. First run

Take these steps in order.

1. **Investigate.** Read the README and docs, manifests and dependencies, entry points, module layout, tests, configuration, and recent `git log`. Never ask the user what the repository answers: language, frameworks, commands, settings, schema.
2. **Ask about git tracking. This is your first question.** Ask whether `.brain` should be tracked in git, saying the default is **not tracked**: local to this machine. Recommend the default unless the user has said otherwise. If the answer is no or no preference, append `.brain/` to `info/exclude` under `git rev-parse --git-common-dir`. If yes, leave `.brain` visible to git. Either way, you never commit.
3. **Propose moving the documents `.brain` replaces.** List each one found, with its destination from the table below, and wait for approval. If `.brain` is untracked and any of them are tracked, say that moving them takes them out of git for everyone else, and offer to leave those in place, indexed by their current path. Once the user approves, move them. Do not copy, and do not ask again. Use `git mv` when `.brain` is tracked, or plain `mv` when it is not; git then shows the old paths as deleted, and you don't commit. Fix links the move breaks.

   | From | To |
   |---|---|
   | `docs/specs/*` | `.brain/specs/` |
   | `docs/adr/*` (root and context-local) | `.brain/adrs/`, renumbered if numbers collide |
   | `docs/tickets/<f>/issues/*` | `.brain/tickets/<f>/` |
   | `docs/implementation/<f>/todo.md` | `.brain/impl_plans/<f>.md` |
   | `docs/implementation/<f>/guidance.md` | its content into the relevant root files, then delete |
   | `docs/planning/*` | `.brain/planning/` |
   | `docs/diagnoses/*` | `.brain/diagnoses/` |
   | `docs/reviews/architecture/*`, `docs/security/*` | `.brain/reviews/architecture/`, `.brain/reviews/security/` |
   | `CONTEXT.md` | entries in `glossary.md`, then delete |
   | `CONTEXT-MAP.md` | domain-boundaries section of `03_architecture.md`, then delete |

4. **Interview the user. This step is required.** Never fill it from defaults, recommendations, or guesses. Ask one question per message about what the code cannot show:
   - purpose and the problem it solves;
   - users;
   - goals, non-goals, and priorities;
   - planned features;
   - domain terms the code doesn't define;
   - decisions already made.

   Keep asking until every applicable root file can be written without guessing. When the user doesn't know, record the question in `open_questions.md` and move on. Never ask process questions this skill answers: the file layout, where something is recorded, or how `.brain` is ignored.
5. **Write the brain.** Create the applicable root files using `${CLAUDE_SKILL_DIR}/references/templates.md`. Leave out a root file that doesn't apply, and list it in `00_index.md` as "not applicable: <reason>"; never write a placeholder file. Planned integrations whose behavior is unverified (file formats, SDKs, OS APIs) go in `spikes.md`. Set `Last synced` to the full 40-character `HEAD` sha.
6. **Report** what you created and moved, then list the open questions and unverified assumptions.

## 3. Update

1. Read every root file, unless you already have this session.
2. Gather what changed since `Last synced`:
   - the code: `git log --stat <sha>..HEAD` and `git diff <sha>..HEAD`, read in full; a commit message is not evidence of what changed;
   - uncommitted work: `git status`;
   - decisions, answers, and discoveries in the current conversation;
   - new or changed documents in `.brain/` subfolders.

   If `<sha>` no longer exists, for example after a rebase, re-verify every root file against the current code instead of diffing, and say so.
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
| `00_index.md` | `Last synced` and `Git` header lines; every `.brain` document with purpose and status |
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

**Glossary:** for each term, record what it means, what it includes and excludes, and how it differs from neighboring terms. Map UI labels to code and database names where they differ. Record aliases to avoid only when they prevent likely confusion. Prefer meaning over class names, and don't mirror the codebase. A new canonical term or a changed definition is a decision; confirm it with the user unless it is already established.

## 5. ADRs

Write `.brain/adrs/NNNN-<slug>.md` (the next number, or `0001` if there are none) only when all three hold:

1. The user approved the choice, or it is already an authoritative project decision.
2. Credible alternatives existed, and a future maintainer could reasonably decide differently from the code alone.
3. Reversing it would need meaningful coordination, migration, or structural change.

Link the ADR from its `09` entry. Separate the user's stated rationale from your own inferences. Never rewrite an accepted ADR. Supersede it with a new ADR, and mark the old one `superseded` in the index.
