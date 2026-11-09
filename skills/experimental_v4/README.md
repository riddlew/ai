# Claude Code Skills

An opinionated set of **15 Claude Code skills** for collaborative software development, built around a **project brain**: a `.brain/` folder that holds what the project is, how it is built, what you decided, what is open, and what is done. A new session reads the brain instead of re-reading the codebase. The goal is to produce straightforward, maintainable changes while keeping consequential product and architectural decisions under your control.

The skills are **tools to use when needed**, not a mandatory pipeline. Small changes should stay small; complex or multi-session work can use more structure.

## Install

Copy `CLAUDE.md` to the root of your project and copy each skill directory into the project's `.claude/skills/` directory:

```text
project/
├── CLAUDE.md
└── .claude/
    └── skills/
        ├── brain-brainstorm/            # SKILL.md + lenses/ + references/ + scripts/
        ├── brain-diagnose/
        ├── brain-distill-content/
        ├── brain-implement/             # SKILL.md + references/
        ├── brain-init/
        ├── brain-plan-feature/
        ├── brain-refine-backlog/        # SKILL.md + references/
        ├── brain-review-architecture/
        ├── brain-review-code/           # SKILL.md + references/findings.md
        ├── brain-review-merge-request/
        ├── brain-review-security/
        ├── brain-test-skill/            # SKILL.md + references/scenario-format.md
        ├── brain-update/                # SKILL.md + references/templates.md
        ├── brain-write-spec/
        └── brain-write-tickets/
```

Merge `CLAUDE.md` with any existing root instructions rather than replacing project-specific guidance.

`brain-brainstorm/scripts/` is an optional browser companion for mockups. It needs Node.js, has no npm dependencies, and makes no network request beyond localhost. It is adapted from obra/superpowers (MIT; see `scripts/LICENSE` and `scripts/README.md`).

`brain-review-architecture`, `brain-review-security`, and `brain-review-merge-request` read the shared finding format from `brain-review-code/references/findings.md`, so install them together with `brain-review-code`. Likewise, `brain-init` uses `brain-update`'s root-file rules and templates, so install the two together.

Skills labeled **manual** use `disable-model-invocation: true` and must be explicitly invoked (for example, `/brain-implement`). Other skills may be selected when relevant, and can also be invoked explicitly.

`tests/` is not installed. It holds the behavior scenarios used to verify the skills (see [Verification](#verification)).

Then run `/brain-init` once in the project to create its brain.

## The project brain

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
├── 09_user_decisions.md Log of decisions you made
├── glossary.md          Canonical terms (required)
├── open_questions.md    Questions only you can answer
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

- **Reading:** every skill except `brain-init`, `brain-distill-content`, and `brain-test-skill` reads all root files once per session (again after context compaction), and reads subfolders only when linked or needed. Root files are kept under about 25,000 words in total; a root file over about 4,000 words moves its detail into a `NN_<topic>/` subfolder and keeps a summary.
- **Writing:** `brain-init` creates the brain; after that, `brain-update` owns the root files and `adrs/`. Other skills write only their own documents into the subfolders, then invoke `brain-update` to index them and propagate what changed. `brain-update` never runs your code, never commits, and never edits another skill's documents.
- **Git:** `.brain` is untracked by default. The first run asks, and adds `.brain/` to the repository's local `info/exclude` unless you choose to track it. Inside a linked git worktree, an untracked brain is found in the main checkout, and a first run from a worktree creates an untracked brain there, so every worktree shares it.
- **Brain elsewhere:** if a skill can't find your brain, run `/brain-init <path to .brain>`. It saves the location as a `Project brain:` line in `CLAUDE.local.md`, Claude Code's personal file for project instructions, and keeps that file out of git through `info/exclude`. Claude Code loads `CLAUDE.local.md` from the working directory and every folder above it. Saved from the main checkout, the line covers the worktrees inside it, such as `.claude/worktrees/`; saved from a linked worktree, it covers only that worktree.
- **Isolated worktree sessions:** Claude Code sessions isolated in a worktree (`claude --worktree`, `EnterWorktree`, and `brain-implement`'s worktree mode) can read a brain in the main checkout but can't edit it. If you work that way, keep the brain outside the repository (for example `~/brains/<project>/.brain`) and run `/brain-init <that path>` once from the main checkout.

**Known limit:** an untracked brain is shared by every worktree and branch, but it records a single `Last synced` commit. After syncing from one branch, the brain can describe code that another branch does not have yet; `brain-update` reports this when it notices.

## Collaboration rules

Root [`CLAUDE.md`](CLAUDE.md) contains the shared decision policy, which the skills reference instead of restating:

- **Investigate facts independently.** Read code, tests, configuration, documentation, and the brain rather than asking questions the repository can answer.
- **Respect established decisions.** Follow approved specifications, architectural decisions, ADRs, and the decisions recorded in `.brain/09_user_decisions.md`.
- **Make routine local choices.** Naming, private helpers, and ordinary test details do not need repeated approval.
- **Consult on consequential choices.** Changes to product behavior, ownership, lifecycle, public contracts, persistence, or meaningful architecture require a recommendation and your decision *before* implementation.

For example, a request to extend communication in an existing `Session` does not authorize silently moving connection ownership into a new `ConnectionManager`. Claude should explain the concrete reason for such a change, compare it with extending `Session`, and ask you which design to adopt.

## Model tiers

Skills refer to a "standard tier" and a "strongest tier". Root [`CLAUDE.md`](CLAUDE.md) maps tiers to models in one table, which is the only place to change them. At skill start, Claude suggests a `/model` switch once, and only on a clear mismatch.

## Skills

| Skill | Purpose | Use when | Typical output |
|---|---|---|---|
| `brain-init` | Creates the project brain: investigates the code and interviews you. Given a path to an existing brain, saves its location instead. Stops if a brain already exists. | A project has no brain yet, or its brain lives somewhere skills don't look. | `.brain/` root files, or a `Project brain:` line in `CLAUDE.local.md`. |
| `brain-update` | Keeps the project brain in sync with commits, decisions, and new documents. Stops and points you to `brain-init` if no brain exists. | Another skill finished work, or you want the brain synced. | Updated `.brain/` root files and ADRs. |
| `brain-brainstorm` | Resolves open requirements and design decisions through a visible decision table, lens-guided options, and dependency-ordered questions. For a decision you would look at, such as a page layout or a diagram, it offers a browser tab with mockups. | Behavior, constraints, or architectural direction is unclear. | A confirmed direction summary; decisions recorded through `brain-update`. |
| `brain-diagnose` | Investigates failures using reproduction and discriminating hypotheses; applies a bounded fix only when authorized. Reproduces the failure before fixing, traces root causes to their source, stops and consults after three failed fixes, and uses a red-flags list. | A failure, regression, or intermittent issue needs explanation. | Diagnosis in conversation; `.brain/diagnoses/` only on request. |
| `brain-distill-content` **(manual)** | Removes verbosity from technical documents while preserving all material information and accuracy, reorganizing where that reads more clearly. | AI-generated docs, MR descriptions, or RFCs are padded. | The distilled document. |
| `brain-implement` **(manual)** | Implements approved work in test-first increments, starting from specification examples, and maintains resumable progress. Asks once per feature whether to use a git worktree and which execution mode to use (subagent-driven, with a per-task reviewer, or inline). Pauses after each task for you to commit, with a suggested Conventional Commits message (it commits itself only when you explicitly ask), and ends with a review proportional to the change; a new impl plan gets a builder review, and its Review Focus reaches the final review. | You are ready to change code, with or without a formal spec. | Code, checks, and for tracked features `.brain/impl_plans/<feature>.md`. |
| `brain-plan-feature` | Tracks multi-session planning with dependency-aware research, consult, prototype, and task tickets. | An initiative has many interdependent decisions and spans days or sessions. | `.brain/planning/<feature>/INDEX.md` and planning tickets. |
| `brain-refine-backlog` | Reviews Jira stories for refinement readiness without changing them. | Preparing for backlog refinement. | Suggested gaps, draft acceptance criteria, and questions. |
| `brain-review-architecture` | Discovers architectural friction **or** assesses a selected boundary, using concrete evidence. | You want improvement candidates or a focused design evaluation. | Findings in conversation; `.brain/reviews/architecture/` only on request. |
| `brain-review-code` | Assesses a bounded change set for correctness, requirement fit, and repository fit, delegating to subagents for larger changes. | A substantive change needs review, or you request one. | Three-section findings report, with a coverage table marking each spec Example and ticket acceptance criterion met, unmet, or unverifiable. |
| `brain-review-merge-request` **(manual)** | Reviews an MR/PR against Jira acceptance criteria using `brain-review-code`, adding coverage, tests, performance, and a merge recommendation. Read-only. | You want an advisory merge assessment. | Consolidated findings and Approve / Request changes. |
| `brain-review-security` | Examines realistic threats, trust boundaries, access control, credentials, and sensitive-data flows. | Work changes a security boundary or you request an audit. | Findings in conversation; `.brain/reviews/security/` only on request. |
| `brain-test-skill` | Tests whether a skill changes what an agent does by running it in fresh agents on throwaway fixtures, before and after a change, with pressure scenarios for rules an agent may skip. It reports pass or fail per criterion with verbatim quotes, and never reports a reading of the skill as a test result. | You want to know whether a skill's rule holds, or you are creating a skill or changing what one does. | Per-criterion results in conversation, also recorded in the project's scenarios file when a skill changed. |
| `brain-write-spec` **(manual)** | Records established requirements, invariants, concrete examples, and decisions without inventing missing choices; each spec is self-checked and read by a fresh builder reviewer. | A substantial feature needs a stable implementation contract. | `.brain/specs/<NN>-<slug>.md`. |
| `brain-write-tickets` | Decomposes approved work into verifiable increments whose acceptance criteria reference spec examples, with your approval of the set; the set comes with a coverage table and a builder review before you approve it. | Work benefits from independent tickets or staged delivery. | `.brain/tickets/<feature>/<NN>-<slug>.md`. |

## Example workflows

These are **examples, not checklists**. Skip any step that does not provide value.

### First session in a project

1. Run `/brain-init`. It reads the code, asks whether `.brain` should be tracked in git (default: no), proposes moving existing specs, ADRs, and `CONTEXT.md` into `.brain`, and then interviews you one question at a time about what the code cannot show.
2. Answer what you can; "I don't know yet" is recorded in `open_questions.md`.

### Small, well-defined change

Example: Add a `--json` option to an existing export command.

1. Run `/brain-implement` directly from the request; a specification and ticket set are not required.
2. Make the smallest coherent change and validate it with targeted tests or other checks.
3. The final check is `brain-implement`'s own diff inspection. A full `brain-review-code` runs only if the change is consequential or you ask for one.
4. Update relevant existing documentation if the user-facing command changed. `brain-update` records the new option in the brain.

### Substantial feature

Example: Add a share-link capability for notes.

1. Use `brain-brainstorm` to resolve permission rules, revocation, expiration, and other consequential questions. Claude investigates existing behavior itself and tracks decisions in a table; the confirmed decisions go into the brain.
2. Use `brain-review-architecture` if ownership or another expensive-to-reverse decision needs focused evaluation. Approved hard-to-reverse decisions become ADRs through `brain-update`.
3. Use `/brain-write-spec` to capture the established behavior, invariants, and concrete examples.
4. Use `brain-write-tickets` **only if** the work benefits from multiple independently verifiable increments or separate sessions.
5. Use `/brain-implement` to execute the spec or tickets, starting from the spec's examples as tests. It asks for the execution mode at startup and pauses after each task for you to commit. Substantial or consequential changes get a final review by a fresh strongest-tier reviewer, which runs `brain-review-code`; add `brain-review-security` if the design introduces authorization, trust, or sensitive-data boundaries.

### Large, multi-session planning effort

1. Use `brain-plan-feature` to establish the objective, open areas, planning tickets, and dependencies under `.brain/planning/<feature>/`.
2. Resolve research and consult tickets one session at a time; `brain-brainstorm` handles the interactive decisions.
3. Once consequential choices are settled, use `/brain-write-spec` and optionally `brain-write-tickets`.
4. Use `/brain-implement` to execute the work with its own impl plan.

`brain-plan-feature` tracks **planning state**; it does not substitute for the impl plan.

### Diagnose and fix a failure

Example: Edits from two browser tabs occasionally overwrite one another.

1. Use `brain-diagnose` to establish what happened and test plausible causes. State whether repair is authorized or you want diagnosis only.
2. If the cause supports a small bounded correction, apply and verify it when authorized.
3. If the fix requires new conflict-resolution semantics or an ownership redesign, resolve it through `brain-brainstorm` first.
4. Add `brain-review-security` when the problem crosses an authorization or other security boundary.

### Improve or review architecture

Example: Changes to note permissions regularly require updates across several modules.

1. Use `brain-review-architecture` in **discovery mode** to identify evidence-backed friction.
2. Select a candidate for **focused review**; compare preserving the existing design and the smallest correction with larger alternatives only when justified.
3. Approve any consequential change before it is recorded through `brain-update` or implemented.
4. Write a spec and tickets only if the change is substantial or needs staged migration.

### Merge request review

1. Run `/brain-review-merge-request` with the MR/PR link and the Jira story's acceptance criteria.
2. It resolves the exact change set, runs `brain-review-code`'s three assessments, adds `brain-review-security` or `brain-review-architecture` when warranted, and reports acceptance-criteria coverage with an advisory recommendation. Nothing is posted to the hosting platform.

## Resuming implementation across sessions

For implementation based on a persisted specification or ticket set, `/brain-implement` keeps **one impl plan per feature**, not one per session or ticket:

```text
.brain/
├── state.md                          # links each feature to its spec and impl plan
├── specs/
│   └── 014-external-communication.md
├── impl_plans/
│   └── 014-external-communication.md
└── tickets/
    └── external-communication/       # Optional
```

The impl plan tracks work items, current focus, blockers, verified test results, and the original Git review base. It is a living document, not an append-only log, and it never authorizes a product or architectural decision; the specification and ADRs remain authoritative. Discoveries a later session would otherwise rediscover go into the brain's root files through `brain-update`. The template is in `brain-implement/references/`.

A fresh session reads the brain's root files, then the impl plan, and verifies progress against the repository, Git state, and tests before continuing.

The impl plan header records the worktree and execution-mode answers, so a resumed session does not ask again. It also records per-task base and commit shas, rulings, and deferred findings.

## Verification

Implementation uses focused test-first increments, starting from the specification's examples and covering stated invariants and failure paths beyond them. At completion, validation is proportional to scope and risk. `brain-review-code` runs for substantial or consequential changes, **not every trivial edit**; in subagent-driven mode each task also gets a task review with up to five fix rounds. `brain-review-security` is similarly risk-based. Review findings are handled by `brain-implement/references/review-feedback.md`: verify before acting, and push back with evidence. No task is marked done without a test run read in that session.

All review skills share one severity scale (Critical / High / Medium / Low), a separate confidence rating, and common finding fields, defined in `brain-review-code/references/findings.md`.

The skills themselves are verified with the scenarios in `tests/scenarios.md`: each runs a fresh agent against a throwaway sample project (`tests/fixture/`), first without the skill (baseline) and then with it, and checks the agent's replies and the resulting files and git state. `brain-test-skill` runs this method. Its own scenarios are in `tests/skill-test-scenarios.md`.

## Reviews

Every spec, ticket set, and new impl plan gets an author self-check, then a fresh standard-tier builder review (or, without a subagent tool, a self-read the skill reports as weaker) that reads it as someone who must build from it without asking.

| Skill | Review |
|---|---|
| `brain-brainstorm` | None |
| `brain-plan-feature` | None of its own; tickets go through `brain-write-tickets` |
| `brain-write-spec` | Write the spec → self-check → fresh reviewer |
| `brain-write-tickets` | Draft the set → self-check (coverage table) → fresh reviewer → you approve → write the files |
| `brain-implement` | New impl plan → self-check (Review Focus) → fresh reviewer → first change; per-task reviews (subagent-driven); proportional final review |

Questions only you can answer come in one message, and anything left unanswered becomes an Open Decision, a blocked ticket, or a Blocker. The impl plan's Review Focus lists failure cases no Example covers, and the final review checks each one. The shared reviewer prompt is `brain-review-code/references/builder-review.md`.

## Changes from experimental_v3

- Every skill is renamed with a `brain-` prefix (`brainstorm` → `brain-brainstorm`, and so on).
- New `brain-init` and `brain-update` skills and `.brain/` project store: `brain-init` creates the brain, and `brain-update` keeps it in sync. Every skill except `brain-distill-content` reads the brain's root files once per session.
- All generated documents move into `.brain/`: `docs/specs/` → `.brain/specs/`, `docs/adr/` → `.brain/adrs/`, `docs/tickets/<f>/issues/` → `.brain/tickets/<f>/`, `docs/implementation/<f>/todo.md` → `.brain/impl_plans/<f>.md`, `docs/planning/` → `.brain/planning/`, `docs/diagnoses/` → `.brain/diagnoses/`, `docs/reviews/architecture/` and `docs/security/` → `.brain/reviews/`.
- `domain-modeling` is removed: `CONTEXT.md` becomes `.brain/glossary.md`, `CONTEXT-MAP.md` becomes the domain-boundaries section of `.brain/03_architecture.md`, and ADR writing moves into `brain-update`.
- `handoff` is removed: `state.md`, `open_questions.md`, and impl plans cover continuation.
- `implement`'s `guidance.md` is removed; discoveries go into the brain's root files.
- Skills that write documents invoke `brain-update` afterward: `brain-brainstorm` (confirmed direction), `brain-write-spec`, `brain-write-tickets`, `brain-plan-feature` (resolved ticket), `brain-implement` (on completion, and at session end unless nothing has changed since its last `brain-update`), `brain-diagnose` (verified fix), and the review skills when a record is saved.
- `tests/` adds behavior scenarios and a sample project for verifying the skills.
