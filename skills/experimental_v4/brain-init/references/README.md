# Claude Code Skills

An opinionated set of **18 Claude Code skills** for collaborative software development, built around a **project brain**: a `.brain/` folder that holds what the project is, how it is built, what you decided, what is open, and what is done. A new session reads the brain instead of re-reading the codebase. The goal is to produce straightforward, maintainable changes while keeping consequential product and architectural decisions under your control.

The skills are **tools to use when needed**, not a mandatory pipeline. Small changes should stay small; complex or multi-session work can use more structure.

## Hierarchical feature documentation (current architecture)

For new feature work the canonical document structure is `.brain/features/<feature-slug>/01-brief/`, `02-specifications/`, `03-components/`, `04-implementation-plans/`, and `05-tasks/`, with mutable execution state in `execution.md`. The hierarchy is optional when work is trivial or already fully settled; never create placeholder documents. `brain-decompose` maps behavior to functional components. `brain-write-tasks` replaces the former ticket-writing skill and produces executable actions from approved implementation plans. There is no legacy feature-document layout support. The normative contracts and templates ship in `brain-init/references/feature-document-contract.md` and `feature-document-templates.md`.

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
        ├── brain-decompose/            # SKILL.md — functional component decomposition
        ├── brain-brainstorm/            # SKILL.md + lenses/ + references/ + scripts/
        ├── brain-blueprint/             # SKILL.md + references/blueprint-template.md
        ├── brain-diagnose/
        ├── brain-distill-content/
        ├── brain-explain-changes/         # SKILL.md (manual, read-only)
        ├── brain-implement/             # SKILL.md + references/
        ├── brain-init/                 # SKILL.md + references/{CLAUDE.local.md,USAGE.md,README.md}
        ├── brain-plan/
        ├── brain-refine-backlog/        # SKILL.md + references/
        ├── brain-review-architecture/
        ├── brain-review-code/           # SKILL.md + references/{findings.md,report-storage.md}
        ├── brain-review-merge-request/
        ├── brain-review-security/
        ├── brain-test-skill/            # SKILL.md + references/scenario-format.md
        ├── brain-update/                # SKILL.md + references/templates.md
        ├── brain-write-spec/
        └── brain-write-tasks/
```

`CLAUDE.local.md` holds the shared decision authority and full-brain loading policy, so the project's own `CLAUDE.md` stays about the project. `/brain-init` installs it from `${CLAUDE_SKILL_DIR}/references/CLAUDE.local.md` and preserves project-specific instructions when merging into an existing file; it asks before resolving conflicting instructions. It excludes an untracked file locally through Git's `info/exclude` (a tracked file remains tracked), and also saves a `Project brain:` line there when you specify an external brain. Claude Code loads it from the working directory and every folder above it, so worktrees inside the checkout, such as `.claude/worktrees/`, use it too. Keep `brain-init/references/CLAUDE.local.md` in sync when changing the policy. Keep `brain-init/references/USAGE.md` and `brain-init/references/README.md` in sync with the distribution guides when updating their content.

`brain-brainstorm/scripts/` is an optional browser companion for mockups. It needs Node.js, has no npm dependencies, and makes no network request beyond localhost. It is adapted from obra/superpowers (MIT; see `brain-brainstorm/scripts/LICENSE` and `brain-brainstorm/scripts/README.md`).

`brain-review-architecture`, `brain-review-security`, and `brain-review-merge-request` read the shared finding format and review-storage rules from `${CLAUDE_SKILL_DIR}/../brain-review-code/references/findings.md` and `${CLAUDE_SKILL_DIR}/../brain-review-code/references/report-storage.md`, so install them together with `brain-review-code`. Likewise, `brain-init` uses `brain-update`'s root-file rules and templates, so install the two together.

Skills labeled **manual** use `disable-model-invocation: true` and must be explicitly invoked (for example, `/brain-implement`). Other skills may be selected when relevant, and can also be invoked explicitly.

`tests/` contains development fixtures and scenarios; it is not an installed Claude Code skill. Copy only the `brain-*` directories into `.claude/skills/`. Use `brain-test-skill` for behavioral verification (see [Verification](#verification)).

See `USAGE.md` for example workflows and when to use `brain-brainstorm`, `brain-plan`, and `brain-blueprint`. `/brain-init` can also be rerun to install or reconcile the policy and missing guides in a project whose brain already exists. It never overwrites a changed `.brain/USAGE.md` or `.brain/README.md` without permission. The guides are referenced selectively rather than loaded automatically.

## The project brain

```text
.brain/
├── 00_index.md          Inventory, status, last-synced commit, main branch
├── USAGE.md             Bundled workflow guide; reference only
├── README.md            Bundled skill reference; reference only
├── 01_about.md … 09_user_decisions.md
├── glossary.md          Canonical terminology
├── open_questions.md    Outstanding user decisions
├── spikes.md            Unverified technical assumptions
├── state.md             Feature status and links
├── adrs/                Approved, durable architecture decisions
├── sources/             Mappings of authoritative technical sources
├── knowledge/           Topic-oriented technical context
├── planning/            Multi-session decision/research tickets
├── reviews/             <type>/<NN>-<slug>/review.md
├── diagnoses/           Investigation records when needed
├── pending/             Branch-specific knowledge pending merge
└── features/
    └── <feature-slug>/
        ├── 01-brief/brief.md
        ├── 02-specifications/<name>.md
        ├── 03-components/<name>.md
        ├── 04-implementation-plans/<name>.md
        ├── 05-tasks/TASK-<NNN>-<name>.md
        └── execution.md
```

The five numbered feature folders represent progressively more concrete documents, not mandatory steps. `brain-decompose` defines functional pieces; `brain-blueprint` owns stable technical implementation plans; `brain-write-tasks` turns approved plans into verifiable actions; and `brain-implement` separately maintains mutable progress in `execution.md`. No legacy feature-document paths or automatic migration are supported.

**Reading:** Project-aware skills load the project-knowledge root files once per session, excluding the bundled reference guides, and inspect relevant feature documents or technical knowledge on demand. Verify task-critical implementation facts against the current code and Git state. Avoid loading the full feature catalog into each agent context.

**Writing:** `brain-init` installs the project brain, policy, and bundled guides. `brain-update` owns root knowledge, ADRs, source maps, and the document index; each feature-producing skill exclusively owns its respective numbered level. `brain-implement` owns `execution.md`. `brain-update` indexes and reports problems with producer-owned documents without rewriting them.

**Git and worktrees:** `.brain/` is untracked by default, using the repository's local `info/exclude`. A shared brain in the main checkout cannot be written from an isolated worktree session; keep the brain outside the checkout when such sessions need to update it. Use `/brain-init <path>` to register an external location. `brain-update` keeps main-branch project facts separate from pending feature-branch changes under `pending/`.

**Authoritative sources:** Designated protocol or external specification documents remain authoritative. `brain-update` indexes them under `sources/` and organizes verified topic details under `knowledge/`; those summaries do not override original requirements.

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
| `brain-explain-changes` | **Sonnet** | **Opus** only for unusually intricate execution paths or complex concurrency; the explanation should remain simple regardless of model. |
| `brain-implement` | **Sonnet** | **Opus** for tightly coupled multi-system changes, byte-exact protocol work, concurrency/state-machine correctness, risky migrations, or repeated design/test failures. Merely changing many files does not itself require Opus. In **subagent-driven** execution, keep the main coordinator on Sonnet as the policy specifies; explicit subagent/final-review roles follow the policy table. |
| `brain-plan` | **Opus** | **Sonnet** when the architecture and requirements are settled and the work is primarily sequencing known tasks and maintaining planning state. |
| `brain-refine-backlog` | **Sonnet** | **Opus** for ambiguous cross-service requirements, major compatibility constraints, or complex dependency and acceptance-criteria conflicts. |
| `brain-review-architecture` | **Opus** | **Sonnet** for a narrow, well-understood module or interface assessment with few architectural tradeoffs. |
| `brain-review-code` | **Sonnet** | **Opus** for broad, high-risk changes involving multiple interacting services, concurrency, security boundaries, exact wire contracts, or hard-to-trace regressions. Delegated assessment subagents remain Sonnet unless the central policy is changed. |
| `brain-review-merge-request` | **Sonnet** | **Opus** for large, consequential MRs/PRs with substantial cross-module behavior, protocol/security impact, migration risk, or difficult requirement reconciliation. |
| `brain-review-security` | **Opus** | **Sonnet** only for a narrowly scoped, well-understood check with explicit threat assumptions; retain Opus for consequential trust-boundary, authentication, authorization, or cryptographic decisions. |
| `brain-test-skill` | **Sonnet** | **Opus** when designing subtle adversarial scenarios or interpreting ambiguous, high-impact behavior failures. Test agents should still run at the tier of the role being tested, as defined in the policy. |
| `brain-write-spec` | **Opus** | **Sonnet** when transcribing fully settled, unambiguous requirements with no consequential decisions remaining. |
| `brain-write-tasks` | **Sonnet** | **Opus** when dividing tightly coupled, multi-system work into safe increments requires difficult dependency or protocol reasoning. |

**Selection rule:** Prefer Sonnet for bounded execution, mechanical documentation, and routine review; use Opus when a mistake is costly and success requires reconciling ambiguous requirements, architecture, or interacting subsystems. Escalate for **reasoning difficulty and consequence**, not just feature size or file count. For a fixed task, a stronger model does not replace exact specifications, golden-vector tests, appropriate tool checks, or independent review. Keep the skill's collaborative approval checkpoints regardless of model. See [Anthropic's model-selection guidance](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model) for current model capabilities.

## Skills

| Skill | Purpose | Use when | Typical output |
|---|---|---|---|
| `brain-init` | Installs or merges `CLAUDE.local.md`, copies the bundled `USAGE.md` and `README.md` guides, then creates the project brain when needed. For an existing brain, installs any missing guides and saves a supplied brain path without rebuilding project knowledge. | A project has no brain yet, its brain lives elsewhere, or its workflow guides need installing. | `CLAUDE.local.md`, `.brain/` root knowledge and reference guides, or a `Project brain:` line. |
| `brain-update` | Keeps the brain in sync with code, decisions, and authoritative technical documents; builds section maps and topic-based knowledge with exact source references. | Another skill finished work, you want a sync, or you need to ingest or refresh a governing specification. | Updated root knowledge, ADRs, `.brain/sources/`, and `.brain/knowledge/`. |
| `brain-brainstorm` | Resolves open requirements and design decisions through a visible decision table, lens-guided options, and dependency-ordered questions. Every behavior you could observe is your decision. It keeps asking until you say to write up, and lists each change as current → new with the reason, plus what stays unchanged and any assumptions for you to confirm. For a decision you would look at, such as a page layout or a diagram, it offers a browser tab with mockups. | Behavior, constraints, or architectural direction is unclear. | A confirmed direction summary; decisions recorded through `brain-update`. |
| `brain-diagnose` | Investigates failures using reproduction and discriminating hypotheses; applies a bounded fix only when authorized. Reproduces the failure before fixing, traces root causes to their source, stops and consults after three failed fixes, and uses a red-flags list. | A failure, regression, or intermittent issue needs explanation. | Diagnosis in conversation; `.brain/diagnoses/` only on request. |
| `brain-distill-content` **(manual)** | Removes verbosity from technical documents while preserving all material information and accuracy, reorganizing where that reads more clearly. | AI-generated docs, MR descriptions, or RFCs are padded. | The distilled document. |
| `brain-decompose` **(manual)** | Maps approved requirements to coherent functional component documents, with complete traceability and explicit approval. | A feature has meaningful functional pieces that benefit from separate design. | `.brain/features/<slug>/03-components/` documents. |
| `brain-blueprint` **(manual)** | Investigates the real code, then collaborates with you on files, ownership, call flow, important signatures, method outlines, unchanged boundaries, testable increments, and design approval. Writes no production code; distinguishes binding constraints from illustrative sketches. | A substantial feature or code structure you want to influence before implementation. | Approved technical plan document(s) in `.brain/features/<feature-slug>/04-implementation-plans/`. |
| `brain-explain-changes` **(manual)** | Walks through recent changes or a selected component in plain language, tracing actual application behavior one step at a time. Not a code review; pauses for questions and never modifies files. | You want to understand code Claude wrote or how a change fits into the running app. | Read-only walkthrough in conversation. |
| `brain-implement` **(manual)** | Implements approved work in small verified behavioral increments. **Collaborative is default**: review the actual diff and tests, then approve each increment before the next. Guided uses larger increments; autonomous skips routine approval pauses. Inline/subagent execution is independent (collaborative defaults inline). Proposes commits but commits only if explicitly asked. Performs proportionate final review. | You are ready to change code, with or without a formal spec; substantial/design-sensitive work normally starts with an approved blueprint. | Code changes and verified progress in `.brain/features/<feature-slug>/execution.md`, separate from approved plans and tasks. |
| `brain-plan` | Tracks multi-session planning with dependency-aware research, consult, prototype, and task tickets. | An initiative has many interdependent decisions and spans days or sessions. | `.brain/planning/<feature>/INDEX.md` and planning tickets. |
| `brain-refine-backlog` | Reviews Jira stories for refinement readiness without changing them. | Preparing for backlog refinement. | Suggested gaps, draft acceptance criteria, and questions. |
| `brain-review-architecture` | Discovers architectural friction **or** assesses a selected boundary, checks relevant previous reviews, and records coverage and finding dispositions. | You want improvement candidates or a focused design evaluation. | Findings in conversation; standalone reviews save `.brain/reviews/architecture/<NN>-<slug>/review.md` by default when a brain is writable. |
| `brain-review-code` | Assesses a bounded change set for correctness, requirement fit, and repository fit, delegating to subagents for larger changes. | A substantive change needs review, or you request one. | Three-section findings report and requirements coverage table; optional `.brain/reviews/code/<NN>-<slug>/review.md`. |
| `brain-review-merge-request` **(manual)** | Reviews an MR/PR against Jira acceptance criteria using `brain-review-code`, adding coverage, tests, performance, and a merge recommendation. Read-only except requested report export. | You want an advisory merge assessment. | Consolidated findings and Approve / Request changes; optional `.brain/reviews/merge-request/<NN>-<slug>/review.md`. |
| `brain-review-security` | Examines realistic threats, trust boundaries, access control, credentials, and sensitive-data flows. | Work changes a security boundary or you request an audit. | Findings in conversation; optional `.brain/reviews/security/<NN>-<slug>/review.md`. |
| `brain-test-skill` | Tests whether a skill changes what an agent does by running it in fresh agents on throwaway fixtures, before and after a change, with pressure scenarios for rules an agent may skip. It reports pass or fail per criterion with verbatim quotes, and never reports a reading of the skill as a test result. | You want to know whether a skill's rule holds, or you are creating a skill or changing what one does. | Per-criterion results in conversation, also recorded in the project's scenarios file when a skill changed. |
| `brain-write-spec` **(manual)** | Records established requirements, invariants, concrete examples, and decisions without inventing missing choices; each spec is self-checked and read by a fresh builder reviewer. | A substantial feature needs a stable implementation contract. | `.brain/features/<feature-slug>/02-specifications/<NN>-<slug>.md`. |
| `brain-write-tasks` | Decomposes approved work into verifiable increments whose acceptance criteria reference spec examples, with your approval of the set; the set comes with a coverage table and a builder review before you approve it. | Approved implementation plans benefit from executable, verifiable task decomposition. | `.brain/features/<feature-slug>/05-tasks/TASK-<NNN>-<slug>.md`. |

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
4. To learn how the changed code works, run `/brain-explain-changes` (or give a file, symbol, or commit range). It traces real call paths in short, plain-language steps without making code changes.
4. Update relevant existing documentation if user-facing behavior changed. `brain-update` records the verified knowledge.

### Substantial feature

Example: Add a share-link capability for notes.

1. Use `/brain-brainstorm` to resolve permission semantics, revocation, expiration, and major design preferences. When appropriate, it saves an approved brief under `01-brief/`.
2. Use `/brain-write-spec` to record stable requirements, invariants, examples, and governing constraints in `02-specifications/`.
3. Use `/brain-decompose` when distinct functional responsibilities require explicit coverage and boundaries. Approve the resulting `03-components/` set.
4. Use `/brain-blueprint` to inspect real source code and agree on affected files, ownership, interfaces, and verification. Approve binding technical design in `04-implementation-plans/`.
5. Use `/brain-write-tasks` when executable increments improve reliability or multi-session coordination. The approved `05-tasks/` definitions reference their plans, requirements, and dependencies.
6. Use `/brain-implement` to execute authorized tasks, verify behavior, and review coherent increments. Track actual progress and approvals in `execution.md`, never by rewriting the approved implementation plans.

Skip unnecessary levels for small, settled changes. For complex unresolved decisions, `brain-plan` can organize investigations and consultations separately under `.brain/planning/`.

### Large, multi-session planning effort

1. Use `brain-plan` to record the objective, dependencies, investigations, and decisions in `.brain/planning/<feature>/`.
2. Resolve planning tickets through research, user consultation, or minimal prototypes. These are **not** executable implementation tasks.
3. Once enough behavior is settled, prepare the brief/specifications and (where useful) functional components, approved technical plans, and executable tasks.
4. Use `brain-implement` to execute approved work, resuming from `.brain/features/<feature>/execution.md` while rechecking Git, code, and verification on each session.

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

A substantial feature keeps stable design and mutable execution evidence in **different documents**:

```text
.brain/features/start-machine/
├── 02-specifications/message-contract.md
├── 03-components/message-routing.md
├── 04-implementation-plans/routing.md
├── 05-tasks/TASK-001-register-handler.md
└── execution.md
```

`brain-blueprint` approves technical plans; `brain-write-tasks` creates tasks; `brain-implement` reads those definitions and records progress, review base, branch/worktree, verification results, deviations, and user checkpoints only in `execution.md`. On resume it verifies actual source code, Git state, and tests instead of trusting old checkmarks. Binding plan changes require reapproval before affected work proceeds.

## Verification

Implementation uses focused test-first increments, starting from the specification's examples and covering stated invariants and failure paths beyond them. In collaborative/guided mode, **technically verified is not finished until you review the increment**. A user may revise code between increments; Claude compares the actual diff and reruns impacted checks rather than undoing user edits. At completion, validation is proportional to scope and risk. `brain-review-code` runs for substantial or consequential changes, **not every trivial edit**; in subagent-driven mode each task also gets a task review with up to five fix rounds. `brain-review-security` is similarly risk-based. Review findings are handled by `${CLAUDE_SKILL_DIR}/../brain-implement/references/review-feedback.md`: verify before acting, and push back with evidence. No task is marked done without meaningful verification inspected in that session; when automated tests are inapplicable, alternatives and their limitations must be recorded.

All four `brain-review-*` skills share the severity, confidence, and finding format in `${CLAUDE_SKILL_DIR}/../brain-review-code/references/findings.md`, plus the per-review folder layout in `${CLAUDE_SKILL_DIR}/../brain-review-code/references/report-storage.md`. New reports always use `.brain/reviews/<type>/<NN>-<slug>/review.md`; legacy flat reports remain readable. Standalone architecture reviews save by default when a brain is writable; other review skills save only when requested or needed by an invoking workflow.

`brain-test-skill` supports behavioral verification in fresh agents against throwaway repositories, comparing original and changed skills. The development fixtures and scenarios are included in the source archive, but are not part of the installed skills; static checks alone do not prove agent behavior. Run behavioral tests before relying on a changed rule in production.

## Reviews

Every spec, ticket set, blueprint, and newly constructed impl-plan execution checklist gets an author self-check, then a fresh standard-tier builder review (or, without a subagent tool, a self-read the skill reports as weaker) that reads it as someone who must build from it without asking.

| Skill | Review |
|---|---|
| `brain-brainstorm` | None |
| `brain-plan` | None of its own; tickets go through `brain-write-tasks` |
| `brain-write-spec` | Write the spec → self-check → fresh reviewer |
| `brain-write-tasks` | Draft the set → self-check (coverage table) → fresh reviewer → you approve → write the files |
| `brain-blueprint` | Investigate code → propose/revise design → self-check → fresh reviewer → **your explicit blueprint approval**; no production edits |
| `brain-implement` | Create/update `execution.md` without overwriting approved plans → self-check (Review Focus) → fresh reviewer → first change → **increment review with you (collaborative/guided)**; per-task reviews if subagent-driven; proportional final review |

Questions only you can answer come in one message, and anything left unanswered becomes an Open Decision, a blocked ticket, or a Blocker. A draft/needs-revision blueprint is not authorization to write production code. The execution record's Review Focus lists failure cases no Example covers, and the final review checks each one. The shared reviewer prompt is `${CLAUDE_SKILL_DIR}/../brain-review-code/references/builder-review.md`.

