# Claude Code Skills

An opinionated set of **16 Claude Code skills** for collaborative software development, built around a **project brain**: a `.brain/` folder that holds what the project is, how it is built, what you decided, what is open, and what is done. A new session reads the brain instead of re-reading the codebase. The goal is to produce straightforward, maintainable changes while keeping consequential product and architectural decisions under your control.

The skills are **tools to use when needed**, not a mandatory pipeline. Small changes should stay small; complex or multi-session work can use more structure.

## Install

Copy each skill directory into the project's `.claude/skills/` directory, then run `/brain-init`. It installs or merges `CLAUDE.local.md`, and copies its bundled `USAGE.md` and `README.md` into the selected project brain (normally `.brain/`). These guides are installed from `brain-init/references/`, so installation works even when the skill is installed independently:

```text
project/
├── CLAUDE.local.md
├── .brain/                       # created by brain-init
│   ├── USAGE.md                  # workflow examples (reference only)
│   └── README.md                 # skill catalog (reference only)
└── .claude/
    └── skills/
        ├── brain-brainstorm/            # SKILL.md + lenses/ + references/ + scripts/
        ├── brain-blueprint/             # SKILL.md + references/blueprint-template.md
        ├── brain-diagnose/
        ├── brain-distill-content/
        ├── brain-implement/             # SKILL.md + references/
        ├── brain-init/                 # SKILL.md + references/{CLAUDE.local.md,USAGE.md,README.md}
        ├── brain-plan-feature/
        ├── brain-refine-backlog/        # SKILL.md + references/
        ├── brain-review-architecture/
        ├── brain-review-code/           # SKILL.md + references/{findings.md,report-storage.md}
        ├── brain-review-merge-request/
        ├── brain-review-security/
        ├── brain-test-skill/            # SKILL.md + references/scenario-format.md
        ├── brain-update/                # SKILL.md + references/templates.md
        ├── brain-write-spec/
        └── brain-write-tickets/
```

`CLAUDE.local.md` holds the shared decision authority and full-brain loading policy, so the project's own `CLAUDE.md` stays about the project. `/brain-init` installs it from `brain-init/references/CLAUDE.local.md` and preserves project-specific instructions when merging into an existing file; it asks before resolving conflicting instructions. It excludes an untracked file locally through Git's `info/exclude` (a tracked file remains tracked), and also saves a `Project brain:` line there when you specify an external brain. Claude Code loads it from the working directory and every folder above it, so worktrees inside the checkout, such as `.claude/worktrees/`, use it too. Keep `brain-init/references/CLAUDE.local.md` in sync when changing the policy. Keep `brain-init/references/USAGE.md` and `brain-init/references/README.md` in sync with the distribution guides when updating their content.

`brain-brainstorm/scripts/` is an optional browser companion for mockups. It needs Node.js, has no npm dependencies, and makes no network request beyond localhost. It is adapted from obra/superpowers (MIT; see `scripts/LICENSE` and `scripts/README.md`).

`brain-review-architecture`, `brain-review-security`, and `brain-review-merge-request` read the shared finding format and review-storage rules from `brain-review-code/references/{findings.md,report-storage.md}`, so install them together with `brain-review-code`. Likewise, `brain-init` uses `brain-update`'s root-file rules and templates, so install the two together.

Skills labeled **manual** use `disable-model-invocation: true` and must be explicitly invoked (for example, `/brain-implement`). Other skills may be selected when relevant, and can also be invoked explicitly.

`tests/` contains development fixtures and scenarios; it is not an installed Claude Code skill. Copy only the `brain-*` directories into `.claude/skills/`. Use `brain-test-skill` for behavioral verification (see [Verification](#verification)).

See `USAGE.md` for example workflows and when to use `brain-brainstorm`, `brain-plan-feature`, and `brain-blueprint`. `/brain-init` can also be rerun to install or reconcile the policy and missing guides in a project whose brain already exists. It never overwrites a changed `.brain/USAGE.md` or `.brain/README.md` without permission. The guides are referenced selectively rather than loaded automatically.

## The project brain

```text
.brain/
├── 00_index.md          Index of every .brain document with status; last-synced commit; git setting
├── USAGE.md             Workflow examples (reference; not auto-loaded)
├── README.md            Skills reference (reference; not auto-loaded)
├── 01_about.md          What the app is, who uses it, core concepts, how it works
├── 02_features.md       Capabilities grouped by module / feature
├── 03_architecture.md   Stack, framework, runtime, platforms, application design, domain boundaries
├── 04_data_model.md     Entities, schema, relationships, derived data
├── 05_settings.md       User-configurable surface
├── 06_ux_interface.md   Visual language, layouts, interactions
├── 07_integrations.md   External tools, file formats, OS APIs
├── 08_error_logging.md  Operational concerns, observability, known failure modes
├── 09_user_decisions.md Log of decisions you made
├── sources/             Maps authoritative documents to sections and brain topics
├── knowledge/           Detailed technical knowledge with source references
├── glossary.md          Canonical terms (required)
├── open_questions.md    Questions only you can answer
├── spikes.md            Technical assumptions not yet verified
├── state.md             Feature checklist: planned / in progress / done (required)
├── adrs/                NNNN-<slug>.md
├── specs/               NN-<slug>.md
├── tickets/             <feature-slug>/NN-<slug>.md
├── impl_plans/          <feature>.md: approved blueprint + execution tracking
├── planning/            <feature>/INDEX.md and NNN-<slug>.md
├── reviews/             <type>/<NN>-<slug>/review.md (one folder per saved review)
├── diagnoses/           NN-<slug>.md
├── reviews/             architecture/NN-<slug>.md, security/NN-<slug>.md
├── pending/             <branch>.md: changes waiting for a branch to merge
└── NN_<topic>/          Detail split out of root file NN_<topic>.md
```

- **Reading:** every skill except `brain-init`, `brain-distill-content`, and `brain-test-skill` reads **all project-knowledge root files** once per session (again after context compaction), excluding only the installed `USAGE.md` and `README.md` guides, and reads subfolders only when linked or needed. Source maps in `sources/` and technical knowledge in `knowledge/` are loaded by topic; exact contracts are verified against the original authoritative source. This intentional full root read minimizes missed cross-domain constraints; task-critical code facts must still be verified against current source. Root files are kept under about 25,000 words in total; a root file over about 4,000 words moves its detail into a `NN_<topic>/` subfolder and keeps a summary.
- **Writing:** `brain-init` creates the brain and maintains the two installed guide files and their index inventory rows; after that, `brain-update` owns the root project-knowledge files, `adrs/`, `sources/`, and `knowledge/`. Other skills write their documents into subfolders and invoke `brain-update` to index them. In `.brain/impl_plans/`, `brain-blueprint` owns the design and approval metadata, while `brain-implement` maintains execution sections **in the same file**. `brain-update` never runs your code, never commits, and never edits another skill's documents.
- **Git:** `.brain` is untracked by default. The first run asks, and adds `.brain/` to the repository's local `info/exclude` unless you choose to track it. Inside a linked git worktree, an untracked brain is found in the main checkout, and a first run from a worktree creates an untracked brain there, so every worktree shares it.
- **Brain elsewhere:** if a skill can't find your brain, run `/brain-init <path to .brain>`. It installs or merges the collaboration policy and saves the location as a `Project brain:` line in `CLAUDE.local.md`. It locally ignores an untracked file through `info/exclude`; a tracked file remains tracked. Claude Code loads `CLAUDE.local.md` from the working directory and every folder above it. Saved from the main checkout, the line covers the worktrees inside it, such as `.claude/worktrees/`; saved from a linked worktree, it covers only that worktree.
- **Isolated worktree sessions:** Claude Code sessions isolated in a worktree (`claude --worktree`, `EnterWorktree`, and `brain-implement`'s worktree mode) can read a brain in the main checkout but can't edit it. If you work that way, keep the brain outside the repository (for example `~/brains/<project>/.brain`) and run `/brain-init <that path>` once from the main checkout. For a new project, run `/brain-init` in the main checkout first, then move the folder out.

**Authoritative technical documents:** `/brain-update` can index a user-designated governing document (for example, a large protocol PDF) without duplicating it. It creates `.brain/sources/<slug>.md` with source version and section-level coverage, plus topic-specific `.brain/knowledge/<domain>/<topic>.md` with useful technical constraints, exact references, and uncertainties. Root files summarize and link to those details; the original document remains authoritative. Re-run `/brain-update` when a source changes to refresh affected knowledge. The extra documents are excluded from full-root loading and are read as needed.

**Branches:** the root files describe the main branch (`Main branch:` in `00_index.md`), so one shared brain stays true in every worktree. Run `/brain-update` on another branch, and that branch's changes go to `.brain/pending/<branch>.md` instead, while decisions, glossary terms, and open questions still go straight into the root files. After a branch merges, run `/brain-update <branch> merged` on the main branch; it checks each pending entry against the merged code before applying it, and every run starts by listing the pending files, so none are forgotten.

## Collaboration rules

`CLAUDE.local.md` contains the decision policy, which the skills reference instead of restating:

- **Investigate facts independently.** Read code, tests, configuration, documentation, and the brain rather than asking questions the repository can answer.
- **Respect established decisions.** Follow approved specifications, architectural decisions, ADRs, and the decisions recorded in `.brain/09_user_decisions.md`.
- **Make routine local choices.** Naming, private helpers, and ordinary test details do not need repeated approval.
- **Consult on consequential choices.** Changes to product behavior, ownership, lifecycle, public contracts, persistence, or meaningful architecture require a recommendation and your decision *before* implementation.
- **Preserve your code design.** Confirmed preferences for patterns, component owners, interfaces, and exact signatures are respected. A blueprint exposes implementation structure for review; illustrative examples are allowed to evolve without pretending every helper was prescribed.
- **Review code incrementally by default.** `brain-implement` uses collaborative mode unless you explicitly select guided or autonomous. The collaboration mode (approval frequency) is separate from inline/subagent execution mode.

For example, a request to extend communication in an existing `Session` does not authorize silently moving connection ownership into a new `ConnectionManager`. Claude should explain the concrete reason for such a change, compare it with extending `Session`, and ask you which design to adopt.

## Model tiers and recommended models

`CLAUDE.local.md` is the **authority for role-to-model assignments**: standard tier = Sonnet and strongest tier = Opus. The recommendations below are **starting points for the main session**, not hard requirements or overrides of the policy. Use the latest available model in each family; do not pin these recommendations to a version. Existing skill rules govern whether Claude suggests a `/model` switch, and delegated subagents continue to use the explicit assignments in `CLAUDE.local.md` (including Sonnet implementers/reviewers and Opus final review/fix roles).

| Skill | Default main-session model | When to deviate |
|---|---|---|
| `brain-init` | **Sonnet** | **Opus** for a large or unfamiliar repository, contradictory legacy documentation, or tricky project/brain migration decisions. |
| `brain-update` | **Sonnet** | **Opus** for importing a large, dense multi-system specification, reconciling conflicting authoritative records, complex rebases, or broad re-verification after history changes. |
| `brain-brainstorm` | **Opus** | **Sonnet** if requirements and ownership are already settled and only a narrow, low-risk choice remains. |
| `brain-diagnose` | **Sonnet** | **Opus** for intermittent concurrency bugs, distributed client/server failures, intricate lifecycle issues, or evidence supporting several competing root causes. |
| `brain-distill-content` | **Sonnet** | **Opus** for lengthy, deeply interdependent technical or protocol material where losing a qualification could change the meaning. Check exact contractual wording regardless of model. |
| `brain-blueprint` | **Opus** | **Sonnet** for a small, familiar change with established architecture and straightforward interfaces; use Opus for consequential ownership, API, or cross-service design. |
| `brain-implement` | **Sonnet** | **Opus** for tightly coupled multi-system changes, byte-exact protocol work, concurrency/state-machine correctness, risky migrations, or repeated design/test failures. Merely changing many files does not itself require Opus. In **subagent-driven** execution, keep the main coordinator on Sonnet as the policy specifies; explicit subagent/final-review roles follow the policy table. |
| `brain-plan-feature` | **Opus** | **Sonnet** when the architecture and requirements are settled and the work is primarily sequencing known tasks and maintaining planning state. |
| `brain-refine-backlog` | **Sonnet** | **Opus** for ambiguous cross-service requirements, major compatibility constraints, or complex dependency and acceptance-criteria conflicts. |
| `brain-review-architecture` | **Opus** | **Sonnet** for a narrow, well-understood module or interface assessment with few architectural tradeoffs. |
| `brain-review-code` | **Sonnet** | **Opus** for broad, high-risk changes involving multiple interacting services, concurrency, security boundaries, exact wire contracts, or hard-to-trace regressions. Delegated assessment subagents remain Sonnet unless the central policy is changed. |
| `brain-review-merge-request` | **Sonnet** | **Opus** for large, consequential MRs/PRs with substantial cross-module behavior, protocol/security impact, migration risk, or difficult requirement reconciliation. |
| `brain-review-security` | **Opus** | **Sonnet** only for a narrowly scoped, well-understood check with explicit threat assumptions; retain Opus for consequential trust-boundary, authentication, authorization, or cryptographic decisions. |
| `brain-test-skill` | **Sonnet** | **Opus** when designing subtle adversarial scenarios or interpreting ambiguous, high-impact behavior failures. Test agents should still run at the tier of the role being tested, as defined in the policy. |
| `brain-write-spec` | **Opus** | **Sonnet** when transcribing fully settled, unambiguous requirements with no consequential decisions remaining. |
| `brain-write-tickets` | **Sonnet** | **Opus** when dividing tightly coupled, multi-system work into safe increments requires difficult dependency or protocol reasoning. |

**Selection rule:** Prefer Sonnet for bounded execution, mechanical documentation, and routine review; use Opus when a mistake is costly and success requires reconciling ambiguous requirements, architecture, or interacting subsystems. Escalate for **reasoning difficulty and consequence**, not just feature size or file count. For a fixed task, a stronger model does not replace exact specifications, golden-vector tests, appropriate tool checks, or independent review. Keep the skill's collaborative approval checkpoints regardless of model. See [Anthropic's model-selection guidance](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model) for current model capabilities.

## Skills

| Skill | Purpose | Use when | Typical output |
|---|---|---|---|
| `brain-init` | Installs or merges `CLAUDE.local.md`, copies the bundled `USAGE.md` and `README.md` guides, then creates the project brain when needed. For an existing brain, installs any missing guides and saves a supplied brain path without rebuilding project knowledge. | A project has no brain yet, its brain lives elsewhere, or its workflow guides need installing. | `CLAUDE.local.md`, `.brain/` root knowledge and reference guides, or a `Project brain:` line. |
| `brain-update` | Keeps the brain in sync with code, decisions, and authoritative technical documents; builds section maps and topic-based knowledge with exact source references. | Another skill finished work, you want a sync, or you need to ingest or refresh a governing specification. | Updated root knowledge, ADRs, `.brain/sources/`, and `.brain/knowledge/`. |
| `brain-brainstorm` | Resolves open requirements and design decisions through a visible decision table, lens-guided options, and dependency-ordered questions. Every behavior you could observe is your decision. It keeps asking until you say to write up, and lists each change as current → new with the reason, plus what stays unchanged and any assumptions for you to confirm. For a decision you would look at, such as a page layout or a diagram, it offers a browser tab with mockups. | Behavior, constraints, or architectural direction is unclear. | A confirmed direction summary; decisions recorded through `brain-update`. |
| `brain-diagnose` | Investigates failures using reproduction and discriminating hypotheses; applies a bounded fix only when authorized. Reproduces the failure before fixing, traces root causes to their source, stops and consults after three failed fixes, and uses a red-flags list. | A failure, regression, or intermittent issue needs explanation. | Diagnosis in conversation; `.brain/diagnoses/` only on request. |
| `brain-distill-content` **(manual)** | Removes verbosity from technical documents while preserving all material information and accuracy, reorganizing where that reads more clearly. | AI-generated docs, MR descriptions, or RFCs are padded. | The distilled document. |
| `brain-blueprint` **(manual)** | Investigates the real code, then collaborates with you on files, ownership, call flow, important signatures, method outlines, unchanged boundaries, testable increments, and design approval. Writes no production code; distinguishes binding constraints from illustrative sketches. | A substantial feature or code structure you want to influence before implementation. | The `Implementation Design` section and approval metadata in `.brain/impl_plans/<feature>.md`. |
| `brain-implement` **(manual)** | Implements approved work in small verified behavioral increments. **Collaborative is default**: review the actual diff and tests, then approve each increment before the next. Guided uses larger increments; autonomous skips routine approval pauses. Inline/subagent execution is independent (collaborative defaults inline). Proposes commits but commits only if explicitly asked. Performs proportionate final review. | You are ready to change code, with or without a formal spec; substantial/design-sensitive work normally starts with an approved blueprint. | Code, checks, and mutable execution tracking in the **same** `.brain/impl_plans/<feature>.md`. |
| `brain-plan-feature` | Tracks multi-session planning with dependency-aware research, consult, prototype, and task tickets. | An initiative has many interdependent decisions and spans days or sessions. | `.brain/planning/<feature>/INDEX.md` and planning tickets. |
| `brain-refine-backlog` | Reviews Jira stories for refinement readiness without changing them. | Preparing for backlog refinement. | Suggested gaps, draft acceptance criteria, and questions. |
| `brain-review-architecture` | Discovers architectural friction **or** assesses a selected boundary, checks relevant previous reviews, and records coverage and finding dispositions. | You want improvement candidates or a focused design evaluation. | Findings in conversation; standalone reviews save `.brain/reviews/architecture/<NN>-<slug>/review.md` by default when a brain is writable. |
| `brain-review-code` | Assesses a bounded change set for correctness, requirement fit, and repository fit, delegating to subagents for larger changes. | A substantive change needs review, or you request one. | Three-section findings report and requirements coverage table; optional `.brain/reviews/code/<NN>-<slug>/review.md`. |
| `brain-review-merge-request` **(manual)** | Reviews an MR/PR against Jira acceptance criteria using `brain-review-code`, adding coverage, tests, performance, and a merge recommendation. Read-only except requested report export. | You want an advisory merge assessment. | Consolidated findings and Approve / Request changes; optional `.brain/reviews/merge-request/<NN>-<slug>/review.md`. |
| `brain-review-security` | Examines realistic threats, trust boundaries, access control, credentials, and sensitive-data flows. | Work changes a security boundary or you request an audit. | Findings in conversation; optional `.brain/reviews/security/<NN>-<slug>/review.md`. |
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

1. Run `/brain-implement` directly from the request; a specification, tickets, and a separate blueprint are optional for this small settled change.
2. Claude makes the smallest coherent change and runs targeted verification.
3. In default **collaborative** mode, review the actual diff and tests; request edits or approve the increment. You do **not** need to commit to continue. The final check is `brain-implement`'s own diff inspection; full `brain-review-code` runs when consequential or requested.
4. Update relevant existing documentation if user-facing behavior changed. `brain-update` records the verified knowledge.

### Substantial feature

Example: Add a share-link capability for notes.

1. Use `/brain-brainstorm` to resolve permission rules, revocation, expiration, and architectural preferences (for example, "keep ownership in `Session`" or "use an Observer pattern"). Claude investigates current code and evaluates your proposed design rather than silently replacing it.
2. Use `brain-review-architecture` if a high-cost ownership decision needs focused analysis. Approved durable decisions become ADRs through `brain-update`.
3. Use `/brain-write-spec` to record desired behavior, invariants, examples, and **approved technical constraints** (including explicitly requested interfaces or patterns). Suggested signatures remain illustrative unless explicitly approved.
4. Use `brain-write-tickets` **only if** separate implementation tickets offer value.
5. Use `/brain-blueprint` to inspect affected source files and collaboratively design components, call/data flow, critical method signatures or pseudocode, unchanged boundaries, and the increment order. Revise it until you **explicitly approve** the blueprint. This writes only the `Implementation Design` section of the one feature impl plan, **not code**.
6. Use `/brain-implement` in default **collaborative** mode. For each verified end-to-end behavioral increment, Claude shows the code diff, tests, and deviations from the blueprint, then **waits for your review** before continuing. You may manually edit code; Claude must preserve and recheck those edits. Commits are optional and never automatic. Substantial or consequential changes get a final review with `brain-review-code`; add `brain-review-security` if relevant.

### Large, multi-session planning effort

1. Use `brain-plan-feature` to establish the objective, open areas, planning tickets, and dependencies under `.brain/planning/<feature>/`.
2. Resolve research and consult tickets one session at a time; `brain-brainstorm` handles the interactive decisions.
3. Once consequential choices are settled, use `/brain-write-spec` and optionally `brain-write-tickets`.
4. Use `/brain-blueprint` to approve the code-level design in `.brain/impl_plans/<feature>.md`.
5. Use `/brain-implement` to execute and review increments, adding execution tracking to that **same** impl plan.

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

## Implementation collaboration modes

`brain-implement` has **two independent settings**:

| Collaboration mode | Review checkpoint | Typical use |
|---|---|---|
| **Collaborative (default)** | Agree on important code structure in `/brain-blueprint`, then review each small verified increment; inline execution by default. | You want to shape actual classes, interfaces, and source changes. |
| **Guided** | Approve a blueprint and review larger coherent increments. | You care about architecture but not every method detail. |
| **Autonomous** | No routine increment pauses; final review and consequential-decision consultation still apply. | Stable, approved design and a well-scoped implementation. |

**Execution mode** is separate: `inline` uses the main Claude session to code, while `subagent-driven` delegates implementation and per-task reviews. The latter is usually better only after the design is settled. Switching collaboration modes requires your direction, not an inferred preference. A full blueprint is optional for a trivial direct fix, but an **existing unapproved blueprint must not be treated as approved**.

**Collaborative checkpoint:** Claude shows the changed files/diff, coverage, actual test results, and any design deviation. You can request revisions, edit the code yourself, or approve. A response to proceed approves **only the increment shown**, not future increments. Commits are suggested, not required; Claude commits only at your explicit request.

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

The **one impl plan** can be created by `/brain-blueprint` before code changes; it then holds the approved `Implementation Design` and its source-code assumptions. `/brain-implement` appends progress, work items, blockers, observed test results, and a separate Git `Review base` captured before editing code. It does not overwrite blueprint approval or approved design. This file never overrides the spec or ADRs; code changes that require a consequential design revision return through approval. Templates are in `brain-blueprint/references/` and `brain-implement/references/`.

A fresh session reads the brain's root files, then the impl plan, and verifies progress against the repository, Git state, and tests before continuing.

The impl plan header records blueprint status, **collaboration mode** (`collaborative` by default), worktree, and execution mode (inline by default). Resumed sessions do not re-ask established choices. The plan also tracks per-task bases, optional commit SHAs, rulings, and deferred findings.

## Verification

Implementation uses focused test-first increments, starting from the specification's examples and covering stated invariants and failure paths beyond them. In collaborative/guided mode, **technically verified is not finished until you review the increment**. A user may revise code between increments; Claude compares the actual diff and reruns impacted checks rather than undoing user edits. At completion, validation is proportional to scope and risk. `brain-review-code` runs for substantial or consequential changes, **not every trivial edit**; in subagent-driven mode each task also gets a task review with up to five fix rounds. `brain-review-security` is similarly risk-based. Review findings are handled by `brain-implement/references/review-feedback.md`: verify before acting, and push back with evidence. No task is marked done without meaningful verification inspected in that session; when automated tests are inapplicable, alternatives and their limitations must be recorded.

All four `brain-review-*` skills share the severity, confidence, and finding format in `brain-review-code/references/findings.md`, plus the per-review folder layout in `brain-review-code/references/report-storage.md`. New reports always use `.brain/reviews/<type>/<NN>-<slug>/review.md`; legacy flat reports remain readable. Standalone architecture reviews save by default when a brain is writable; other review skills save only when requested or needed by an invoking workflow.

`brain-test-skill` supports behavioral verification in fresh agents against throwaway repositories, comparing original and changed skills. The development fixtures and scenarios are included in the source archive, but are not part of the installed skills; static checks alone do not prove agent behavior. Run behavioral tests before relying on a changed rule in production.

## Reviews

Every spec, ticket set, blueprint, and newly constructed impl-plan execution checklist gets an author self-check, then a fresh standard-tier builder review (or, without a subagent tool, a self-read the skill reports as weaker) that reads it as someone who must build from it without asking.

| Skill | Review |
|---|---|
| `brain-brainstorm` | None |
| `brain-plan-feature` | None of its own; tickets go through `brain-write-tickets` |
| `brain-write-spec` | Write the spec → self-check → fresh reviewer |
| `brain-write-tickets` | Draft the set → self-check (coverage table) → fresh reviewer → you approve → write the files |
| `brain-blueprint` | Investigate code → propose/revise design → self-check → fresh reviewer → **your explicit blueprint approval**; no production edits |
| `brain-implement` | Add execution checklist without overwriting the blueprint → self-check (Review Focus) → fresh reviewer → first change → **increment review with you (collaborative/guided)**; per-task reviews if subagent-driven; proportional final review |

Questions only you can answer come in one message, and anything left unanswered becomes an Open Decision, a blocked ticket, or a Blocker. A draft/needs-revision blueprint is not authorization to write production code. The impl plan's Review Focus lists failure cases no Example covers, and the final review checks each one. The shared reviewer prompt is `brain-review-code/references/builder-review.md`.

## Changes in the collaborative-blueprint revision

- Added manual `/brain-blueprint`: collaborative code design and explicit approval before substantial/design-sensitive implementation. Blueprints live **inside** the existing `.brain/impl_plans/<feature>.md` alongside execution tracking.
- Set `brain-implement` collaboration mode to **collaborative by default**, preserving separate `inline`/`subagent-driven` execution modes. Guided and autonomous are opt-in. Increment approval is separate from optional Git commits.
- `brain-brainstorm` and `brain-write-spec` now preserve explicitly approved user preferences for ownership, design patterns, and code-level contracts rather than automatically deferring them.
- Updated the top-level `CLAUDE.local.md` and `brain-init/references/CLAUDE.local.md` **identically**, along with builder-review and implementation handoffs.

## Changes from experimental_v3

- Every skill is renamed with a `brain-` prefix (`brainstorm` → `brain-brainstorm`, and so on).
- New `brain-init` and `brain-update` skills and `.brain/` project store: `brain-init` creates the brain, and `brain-update` keeps it in sync. Every skill except `brain-init`, `brain-distill-content`, and `brain-test-skill` reads the brain's root files once per session.
- All generated documents move into `.brain/`: `docs/specs/` → `.brain/specs/`, `docs/adr/` → `.brain/adrs/`, `docs/tickets/<f>/issues/` → `.brain/tickets/<f>/`, `docs/implementation/<f>/todo.md` → `.brain/impl_plans/<f>.md`, `docs/planning/` → `.brain/planning/`, `docs/diagnoses/` → `.brain/diagnoses/`, `docs/reviews/architecture/` and `docs/security/` → individual `.brain/reviews/<type>/<NN>-<slug>/review.md` files.
- `domain-modeling` is removed: `CONTEXT.md` becomes `.brain/glossary.md`, `CONTEXT-MAP.md` becomes the domain-boundaries section of `.brain/03_architecture.md`, and ADR writing moves into `brain-update`.
- `handoff` is removed: `state.md`, `open_questions.md`, and impl plans cover continuation.
- `implement`'s `guidance.md` is removed; discoveries go into the brain's root files.
- Skills that write documents invoke `brain-update` afterward: `brain-brainstorm` (confirmed direction), `brain-write-spec`, `brain-blueprint` (approved or materially revised design), `brain-write-tickets`, `brain-plan-feature` (resolved ticket), `brain-implement` (on completion, and at session end unless nothing has changed since its last `brain-update`), `brain-diagnose` (verified fix), and the review skills when a record is saved.
- `tests/` adds behavior scenarios and a sample project for verifying the skills.
