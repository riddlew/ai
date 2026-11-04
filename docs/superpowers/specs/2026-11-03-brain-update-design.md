# Design: `brain-update` and the `.brain` project store (experimental_v4)

## Intent

AI sessions lose everything between conversations and rebuild context by re-reading code and docs. `.brain/` is a central, durable memory for one project: what it is, how it is built, what has been decided, what is still open, and what is done. A new session gets full project context by reading a bounded set of files instead of the codebase.

All project documents the skills produce move into `.brain/`, so it becomes the single place to look.

## Goals

- One `.brain/` folder at the repository root holds all skill-generated project knowledge and artifacts.
- A new session gets full project context by reading the `.brain` root files once.
- `brain-update` is the only skill that edits the shared root files, so updates stay consistent.
- The first run builds the brain from investigation plus questions to the user.
- `glossary.md` keeps terminology consistent across every document.

## Non-goals

- No subagents in `brain-update` unless the user asks for them.
- `.brain` is not committed by default.
- Root `CLAUDE.md` stays at the project root; it is policy, not project knowledge, and Claude Code only auto-loads it from there.
- Reviews and diagnoses still default to conversation-only; a saved record is written only on request.
- The superpowers-style changes discussed earlier (bootstrap hook, hard gates, subagent execution) are out of scope.
- `skills/experimental_v3/` is not modified.

## Location and naming

All work happens in a new `skills/experimental_v4/`, created as a copy of `skills/experimental_v3/`. Every skill gets a `brain-` prefix, in both its directory name and its `name:` frontmatter:

| v3 | v4 |
|---|---|
| `brainstorm` | `brain-brainstorm` |
| `diagnose` | `brain-diagnose` |
| `distill-content` | `brain-distill-content` |
| `implement` | `brain-implement` |
| `plan-feature` | `brain-plan-feature` |
| `refine-backlog` | `brain-refine-backlog` |
| `review-architecture` | `brain-review-architecture` |
| `review-code` | `brain-review-code` |
| `review-merge-request` | `brain-review-merge-request` |
| `review-security` | `brain-review-security` |
| `write-spec` | `brain-write-spec` |
| `write-tickets` | `brain-write-tickets` |
| `domain-modeling` | removed (folded into `brain-update`) |
| `handoff` | removed |
| — | `brain-update` (new) |

Every reference to another skill uses the new name. That includes prose, slash commands (`/brain-implement`), and relative paths such as `${CLAUDE_SKILL_DIR}/../brain-review-code/references/findings.md`.

The rest of this document uses v4 names.

## Layout

```text
.brain/
├── 00_index.md          Index of every .brain document with status; last-synced commit; git setting
├── 01_about.md          What the app is, who uses it, core concepts, how it works
├── 02_features.md       Capabilities grouped by module / feature
├── 03_architecture.md   Stack, framework, runtime, platforms, application design, domain boundaries
├── 04_data_model.md     Entities, schema, relationships, derived data
├── 05_settings.md       User-configurable surface
├── 06_ux_interface.md   Visual language, layouts, interactions
├── 07_integrations.md   External tools, file formats, OS APIs
├── 08_error_logging.md  Operational concerns, observability, known failure modes
├── 09_user_decisions.md Log of decisions the user made
├── glossary.md          Canonical terms (required)
├── open_questions.md    Questions only the user can answer
├── spikes.md            Technical assumptions not yet verified
├── state.md             Feature checklist: planned / in progress / done (required)
├── adrs/                NNNN-<slug>.md
├── specs/               NN-<slug>.md
├── tickets/             <feature-slug>/NN-<slug>.md
├── impl_plans/          <feature>.md
├── planning/            <feature>/INDEX.md and NNN-<slug>.md
├── diagnoses/           NN-<slug>.md
├── reviews/             architecture/NN-<slug>.md, security/NN-<slug>.md
└── NN_<topic>/          Detail split out of root file NN_<topic>.md
```

"Root files" means every `.md` file directly in `.brain/`. Everything else is a subfolder.

### Root files

| File | Contains | Rules |
|---|---|---|
| `00_index.md` | Header: `Last synced: <sha> (<date>)` and `Git: tracked` or `Git: ignored`. Then every `.brain` document (root and subfolders) with path, one-line purpose, and status. Root files that do not apply are listed as "not applicable: <reason>". | Statuses: specs `draft / approved / implemented / superseded`; ADRs `accepted / superseded`; tickets and impl plans `open / in progress / done`; planning `active / done`; diagnoses and reviews `recorded`. |
| `01_about.md` | Purpose, users, core concepts, high-level operation. | |
| `02_features.md` | What each feature does, grouped by module. | Progress lives in `state.md`, not here. |
| `03_architecture.md` | Stack, runtime, platforms, components and what each owns, dependency direction, domain boundaries (the old `CONTEXT-MAP.md` content). | |
| `04_data_model.md` – `08_error_logging.md` | As named in the layout. | |
| `09_user_decisions.md` | One entry per decision: date, decision, short rationale, source (conversation, spec, or ADR link). | Only decisions the user made or approved. Recommendations never go here. Hard-to-reverse decisions also get an ADR, linked from the entry. |
| `glossary.md` | Per term: canonical name, one-line definition, aliases to avoid, and UI label ↔ code/DB term where they differ. One section per domain when the project has several. | Required. Every other `.brain` document uses canonical terms. |
| `open_questions.md` | Questions only the user can answer, each with why it matters and what it blocks. | When answered: record in `09_user_decisions.md` and the relevant root file, then remove the question. |
| `spikes.md` | Unverified technical assumptions: `<assumption> — unverified — <why it matters>`. | Each resolves into one of three outcomes. **Confirmed:** move the fact to the relevant root file and remove the entry. **Confirmed problem:** becomes an open question or a decision in `09`. **Deferred risk:** stays, with a note. |
| `state.md` | Features with status (planned / in progress / done), each linking to its spec, tickets, and impl plan. | Required. Feature-level only; task-level progress lives in `impl_plans/`. |

The numbered files 01–09 are a starting point. Root files that do not apply to a project are omitted and marked in the index. A project-specific topic gets the next free number (for example `10_protocols.md`).

### Size limits

- When a root file passes about 4,000 words, move its detail into `.brain/NN_<topic>/<subtopic>.md`. The root file keeps a summary and links to the detail files.
- Keep all root files together under about 25,000 words. When the total goes over, condense root files by moving detail into subfolders.

## Who writes what

- **`brain-update` owns every root file and `adrs/`.** No other skill edits root files directly.
- **Skills that produce a document write it into its folder, then invoke `brain-update`** to index it and propagate what changed:

| Skill | Writes | Previously |
|---|---|---|
| `brain-write-spec` | `.brain/specs/NN-<slug>.md` | `docs/specs/` |
| `brain-write-tickets` | `.brain/tickets/<feature-slug>/NN-<slug>.md` | `docs/tickets/<feature>/issues/` |
| `brain-implement` | `.brain/impl_plans/<feature>.md` | `docs/implementation/<feature>/todo.md` |
| `brain-plan-feature` | `.brain/planning/<feature>/` | `docs/planning/<feature>/` |
| `brain-diagnose` (saved record only) | `.brain/diagnoses/NN-<slug>.md` | `docs/diagnoses/` |
| `brain-review-architecture` (saved record only) | `.brain/reviews/architecture/NN-<slug>.md` | `docs/reviews/architecture/` |
| `brain-review-security` (saved record only) | `.brain/reviews/security/NN-<slug>.md` | `docs/security/` |

- **ADRs:** `brain-update` writes one when it records a user decision that meets the criteria currently in `domain-modeling` §5 (approved; credible alternatives existed; reversal is costly). ADR numbering and template carry over from `domain-modeling`. Superseded ADRs are preserved and linked, never rewritten.

## Reading the brain

Every v4 skill except `brain-distill-content` starts with the same short preamble:

> If `.brain/00_index.md` exists (at this worktree's root, or in the main checkout when working in a linked git worktree) and you have not read its root files in this session (or they were lost to context compaction), read every root `.md` file in that `.brain/` now. Read subfolders only when a root file links to them or the task needs them. Do not load `.brain` into subagents wholesale; pass only what their task needs. Write any `.brain/` document into that same `.brain/`. If no brain exists, proceed without one and mention once that `/brain-update` can create it.

**A brain exists when `.brain/00_index.md` exists.** A `.brain/` folder without it (for example, one where `brain-write-spec` saved a spec before any first run) does not count.

**Locating `.brain`:** use the current worktree root's `.brain/` if it contains `00_index.md`. Otherwise, inside a linked git worktree, use the main checkout's `.brain/` (the parent of `git rev-parse --path-format=absolute --git-common-dir`). Writes go to the same location. With no brain anywhere, producer skills still write their documents to `.brain/<folder>/` at the current worktree root.

**When no brain exists:** other skills proceed without it and mention once that `/brain-update` can create it. They never start a first run themselves.

## `brain-update` behavior

Model-invocable, so other skills can call it. No subagents unless the user asks.

### Mode selection

- No brain, invoked directly by the user → **first run**. Existing `.brain/` subfolders are kept and indexed.
- No brain, invoked by another skill → do nothing; tell the user `/brain-update` will set it up.
- Brain present → **update**.

### First run

1. **Investigate inline:** README and docs, manifests and dependencies, entry points, module layout, tests, configuration, recent git history.
2. **Ask whether `.brain` should be tracked in git** (default: no). If no, add `.brain/` to `info/exclude` under `git rev-parse --git-common-dir` (shared by all worktrees), which ignores it locally without changing tracked files. If yes, leave it visible to git; `brain-update` never commits on its own. Record the answer in `00_index.md`.
3. **Find existing documents `.brain` replaces:** `docs/specs/`, `docs/adr/` (root and context-local), `CONTEXT.md`, `CONTEXT-MAP.md`, `docs/tickets/`, `docs/implementation/`, `docs/planning/`, `docs/diagnoses/`, `docs/reviews/`, `docs/security/`. List them with a proposed destination and wait for approval before moving anything. If `.brain` is untracked and any of these files are tracked, say that moving them takes them out of git for everyone else, and offer to leave those files in place, indexed by their current path, instead. Move with `git mv` when `.brain` is tracked, or plain `mv` when it is not (git then shows the old paths as deleted; `brain-update` does not commit). Fix links that the move breaks. `CONTEXT.md` content becomes `glossary.md` entries; `CONTEXT-MAP.md` becomes the domain-boundaries section of `03_architecture.md`; `guidance.md` content goes into the relevant root files.
4. **Question the user, one question at a time,** only about what the code cannot answer: purpose, users, goals and non-goals, priorities, planned features, domain terms, and decisions already made. Keep going until every applicable root file can be written without guessing. Never ask what the code answers.
5. **Create `.brain/`** and the applicable root files. Set `Last synced` to the current `HEAD`.
6. **Report** open questions and unverified assumptions to the user, and write them to `open_questions.md` and `spikes.md`.

### Update

1. Read the root files if not already read this session.
2. Gather what changed:
   - commits since `Last synced` (`git log` and `git diff --stat <sha>..HEAD`);
   - uncommitted changes (`git status`);
   - decisions, answers, and discoveries from the current conversation;
   - new or changed documents in `.brain` subfolders.

   If the `Last synced` commit no longer exists (for example after a rebase), re-verify every root file against the current code instead of diffing, and say so.
3. Map each change to the root files it affects. Add new information, correct what changed, and remove what is no longer true.
4. Record user decisions in `09_user_decisions.md`, and write an ADR when the criteria are met. Move answered questions out of `open_questions.md` and resolve spikes as described above.
5. Add new terms to `glossary.md`. Replace non-canonical terms in root files. In subfolder documents (specs, tickets, ADRs), report mismatches instead of editing them.
6. Update `state.md` and the statuses in `00_index.md`. Set `Last synced` to `HEAD`. Uncommitted work counts as in progress, never done.
7. Split any root file over the size limit.
8. Report the files changed and any new open questions or spikes.

### Authority rules

- **Facts:** the code wins. When the brain disagrees with the code, correct the brain.
- **Intent:** specs, ADRs, and `09_user_decisions.md` win. When the code contradicts them, add an open question and report it; do not silently rewrite intent to match the code.
- Recommendations, proposals, and review findings are never recorded as decisions.
- No session narrative. Each root file describes the current state, not history.

### When other skills invoke `brain-update`

| Skill | When |
|---|---|
| `brain-brainstorm` | After the direction is confirmed |
| `brain-write-spec`, `brain-write-tickets` | After writing files |
| `brain-plan-feature` | After resolving a planning ticket |
| `brain-implement` | At the end of each session and on completion |
| `brain-diagnose` | After a fix is applied |
| `brain-review-architecture`, `brain-review-security` | Only when a saved record was written |

The user can also run `/brain-update` at any time.

## Changes to existing skills

| Skill | Change |
|---|---|
| All except `brain-distill-content` | Add the reading preamble. Replace reads of `CONTEXT.md`, `CONTEXT-MAP.md`, and `docs/adr/` with `.brain/glossary.md`, `03_architecture.md`, and `.brain/adrs/`. |
| `brain-brainstorm` (+ `lenses/architecture.md`) | Invoke `brain-update` after confirmation. ADR references point at `.brain/adrs/`. |
| `brain-write-spec` | Write to `.brain/specs/`. Use glossary terms. Invoke `brain-update`. |
| `brain-write-tickets` | Write to `.brain/tickets/<feature-slug>/`. Spec references point at `.brain/specs/`. Invoke `brain-update`. |
| `brain-implement` | Progress file becomes `.brain/impl_plans/<feature>.md`. Drop `guidance.md` and `references/guidance-template.md`; discoveries go to root files through `brain-update`. Update `references/todo-template.md` paths. Invoke `brain-update` per the table above. |
| `brain-plan-feature` | Write to `.brain/planning/<feature>/`. Invoke `brain-update` after resolving a ticket. |
| `brain-diagnose` | Saved record goes to `.brain/diagnoses/`. Invoke `brain-update` after a fix. |
| `brain-review-architecture`, `brain-review-security` | Saved records go to `.brain/reviews/architecture/` and `.brain/reviews/security/`. |
| `brain-review-code` | Review base comes from the impl plan file. Spec lookup is `.brain/specs/`. |
| `brain-review-merge-request`, `brain-refine-backlog` | Reading preamble only. |
| `brain-distill-content` | No change. |
| `domain-modeling` | Removed. Glossary rules and ADR criteria and template move into `brain-update`. |
| `handoff` | Removed. `state.md`, `open_questions.md`, and `impl_plans/` cover continuation. |
| `CLAUDE.md` | Replace the durable-docs rule and the `todo.md` bullet with `.brain` rules: `.brain` is the project store, `brain-update` owns its root files, and root files are summaries of other sources, never authorities over specs or ADRs. |
| `README.md` | Update the install section, skills table, workflows, and the resuming section; replace "Changes from experimental_v2" with "Changes from experimental_v3". |

## Left to the builder

- Exact wording of `brain-update`'s `description`, the preamble, and section headings.
- Templates for the root files (kept in `brain-update/references/`).
- Wording of the `CLAUDE.md` and `README.md` edits.
