# Claude Code Skills

An opinionated set of **14 Claude Code skills** for collaborative software development. The goal is to produce straightforward, maintainable changes while keeping consequential product and architectural decisions under your control.

The skills are **tools to use when needed**, not a mandatory pipeline. Small changes should stay small; complex or multi-session work can use more structure.

## Install

Copy `CLAUDE.md` to the root of your project and copy each skill directory into the project's `.claude/skills/` directory:

```text
project/
├── CLAUDE.md
└── .claude/
    └── skills/
        ├── brainstorm/          # SKILL.md + lenses/
        ├── diagnose/
        ├── distill-content/
        ├── domain-modeling/
        ├── handoff/
        ├── implement/           # SKILL.md + references/
        ├── plan-feature/
        ├── refine-backlog/      # SKILL.md + references/
        ├── review-architecture/
        ├── review-code/         # SKILL.md + references/findings.md
        ├── review-merge-request/
        ├── review-security/
        ├── write-spec/
        └── write-tickets/
```

Merge `CLAUDE.md` with any existing root instructions rather than replacing project-specific guidance.

`review-architecture`, `review-security`, and `review-merge-request` read the shared finding format from `review-code/references/findings.md`, so install them together with `review-code`.

Skills labeled **manual** use `disable-model-invocation: true` and must be explicitly invoked (for example, `/implement`). Other skills may be selected when relevant, and can also be invoked explicitly.

## Collaboration rules

Root [`CLAUDE.md`](CLAUDE.md) contains the shared decision policy, which the skills reference instead of restating:

- **Investigate facts independently.** Read code, tests, configuration, and documentation rather than asking questions the repository can answer.
- **Respect established decisions.** Follow approved specifications, architectural decisions, and relevant ADRs.
- **Make routine local choices.** Naming, private helpers, and ordinary test details do not need repeated approval.
- **Consult on consequential choices.** Changes to product behavior, ownership, lifecycle, public contracts, persistence, or meaningful architecture require a recommendation and your decision *before* implementation.

For example, a request to extend communication in an existing `Session` does not authorize silently moving connection ownership into a new `ConnectionManager`. Claude should explain the concrete reason for such a change, compare it with extending `Session`, and ask you which design to adopt.

## Skills

| Skill | Purpose | Use when | Typical output |
|---|---|---|---|
| `brainstorm` | Resolves open requirements and design decisions through a visible decision table, lens-guided options, and dependency-ordered questions. | Behavior, constraints, or architectural direction is unclear. | A confirmed direction summary with its decision table. |
| `diagnose` | Investigates failures using reproduction and discriminating hypotheses; applies a bounded fix only when authorized. | A failure, regression, or intermittent issue needs explanation. | Diagnosis in conversation and, if authorized, a verified repair. |
| `distill-content` **(manual)** | Removes verbosity from technical documents while preserving all material information and structure. | AI-generated docs, MR descriptions, or RFCs are padded. | The distilled document. |
| `domain-modeling` | Maintains approved domain vocabulary, context boundaries, and durable architectural decisions. | Design work establishes or changes domain meaning or context ownership. | `CONTEXT.md`, `CONTEXT-MAP.md`, or ADR updates when justified. |
| `handoff` **(manual)** | Captures the minimum a fresh session needs, linking existing records rather than copying them. | You want a cross-session continuation document. | `handoff-<slug>.md` in the OS temporary directory. |
| `implement` **(manual)** | Implements approved work in test-first increments, starting from specification examples, and maintains resumable progress. | You are ready to change code, with or without a formal spec. | Code, checks, and for tracked features `docs/implementation/<feature>/todo.md`. |
| `plan-feature` | Tracks multi-session planning with dependency-aware research, consult, prototype, and task tickets. | An initiative has many interdependent decisions and spans days or sessions. | `docs/planning/<feature>/INDEX.md` and planning tickets. |
| `refine-backlog` | Reviews Jira stories for refinement readiness without changing them. | Preparing for backlog refinement. | Suggested gaps, draft acceptance criteria, and questions. |
| `review-architecture` | Discovers architectural friction **or** assesses a selected boundary, using concrete evidence. | You want improvement candidates or a focused design evaluation. | Findings in conversation. |
| `review-code` | Assesses a bounded change set for correctness, requirement fit, and repository fit, delegating to subagents for larger changes. | A substantive change needs review, or you request one. | Three-section findings report. |
| `review-merge-request` **(manual)** | Reviews an MR/PR against Jira acceptance criteria using `review-code`, adding coverage, tests, performance, and a merge recommendation. Read-only. | You want an advisory merge assessment. | Consolidated findings and Approve / Request changes. |
| `review-security` | Examines realistic threats, trust boundaries, access control, credentials, and sensitive-data flows. | Work changes a security boundary or you request an audit. | Risk-based findings in conversation. |
| `write-spec` **(manual)** | Records established requirements, invariants, concrete examples, and decisions without inventing missing choices. | A substantial feature needs a stable implementation contract. | `docs/specs/<NN>-<slug>.md`. |
| `write-tickets` | Decomposes approved work into verifiable increments whose acceptance criteria reference spec examples, with your approval of the set. | Work benefits from independent tickets or staged delivery. | `docs/tickets/<feature>/issues/<NN>-<slug>.md`. |

Reviews and diagnoses are delivered in the conversation. They are saved under `docs/` only when you request a record or a workflow needs one for continuation.

## Example workflows

These are **examples, not checklists**. Skip any step that does not provide value.

### Small, well-defined change

Example: Add a `--json` option to an existing export command.

1. Run `/implement` directly from the request; a specification and ticket set are not required.
2. Make the smallest coherent change and validate it with targeted tests or other checks.
3. Inspect the diff. Invoke `review-code` only if the change is consequential, substantial, or you request it.
4. Update relevant existing documentation if the user-facing command changed.

### Substantial feature

Example: Add a share-link capability for notes.

1. Use `brainstorm` to resolve permission rules, revocation, expiration, and other consequential questions. Claude investigates existing behavior itself and tracks decisions in a table.
2. Use `review-architecture` if ownership or another expensive-to-reverse decision needs focused evaluation. Record approved durable decisions through `domain-modeling` when appropriate.
3. Use `/write-spec` to capture the established behavior, invariants, and concrete examples.
4. Use `write-tickets` **only if** the work benefits from multiple independently verifiable increments or separate sessions.
5. Use `/implement` to execute the spec or tickets, starting from the spec's examples as tests. Run `review-code` for a substantial change; add `review-security` if the design introduces authorization, trust, or sensitive-data boundaries.

### Large, multi-session planning effort

1. Use `plan-feature` to establish the objective, open areas, planning tickets, and dependencies under `docs/planning/<feature>/`.
2. Resolve research and consult tickets one session at a time; `brainstorm` handles the interactive decisions.
3. Once consequential choices are settled, use `/write-spec` and optionally `write-tickets`.
4. Use `/implement` to execute the work with its own feature-level progress records.

`plan-feature` tracks **planning state**; it does not substitute for the implementation tracker.

### Diagnose and fix a failure

Example: Edits from two browser tabs occasionally overwrite one another.

1. Use `diagnose` to establish what happened and test plausible causes. State whether repair is authorized or you want diagnosis only.
2. If the cause supports a small bounded correction, apply and verify it when authorized.
3. If the fix requires new conflict-resolution semantics or an ownership redesign, resolve it through `brainstorm` first.
4. Add `review-security` when the problem crosses an authorization or other security boundary.

### Improve or review architecture

Example: Changes to note permissions regularly require updates across several modules.

1. Use `review-architecture` in **discovery mode** to identify evidence-backed friction.
2. Select a candidate for **focused review**; compare preserving the existing design and the smallest correction with larger alternatives only when justified.
3. Approve any consequential change before recording it through `domain-modeling` or implementing it.
4. Write a spec and tickets only if the change is substantial or needs staged migration.

### Merge request review

1. Run `/review-merge-request` with the MR/PR link and the Jira story's acceptance criteria.
2. It resolves the exact change set, runs `review-code`'s three assessments, adds `review-security` or `review-architecture` when warranted, and reports acceptance-criteria coverage with an advisory recommendation. Nothing is posted to the hosting platform.

## Resuming implementation across sessions

For implementation based on a persisted specification or ticket set, `/implement` creates **one feature workspace**, not one per session or ticket:

```text
docs/
├── specs/
│   └── 014-external-communication.md
├── implementation/
│   └── 014-external-communication/
│       ├── todo.md
│       └── guidance.md       # Optional
└── tickets/
    └── external-communication/
        └── issues/           # Optional
```

- **`todo.md`** tracks work items, current focus, blockers, verified test results, and the original Git review base.
- **`guidance.md`** preserves useful implementation discoveries, code locations, caveats, and *references* to approved decisions. Created only when useful.

**Both files are living documents, not append-only logs.** A fresh session reads them and verifies progress against the repository, Git state, and tests before continuing. Neither file authorizes a product or architectural decision; the specification and ADRs remain authoritative. Templates are in `implement/references/`.

The `handoff` skill is optional for implementation continuation: use it when important context is not already captured by the spec, progress records, and repository.

## Verification

Implementation uses focused test-first increments, starting from the specification's examples and covering stated invariants and failure paths beyond them. At completion, validation is proportional to scope and risk. `review-code` runs for substantial or consequential changes, **not every trivial edit**; `review-security` is similarly risk-based.

All review skills share one severity scale (Critical / High / Medium / Low), a separate confidence rating, and common finding fields, defined in `review-code/references/findings.md`.

## Changes from experimental_v2

- `review-code` adds a **Correctness** assessment, a stricter base-resolution order (never the upstream tracking branch), proportional subagent delegation, and a consolidate-and-validate step.
- `write-spec` adds **Behavior and Invariants** and numbered **Examples**; `implement` starts tests from them and `write-tickets` references them in acceptance criteria.
- `brainstorm` adds a published decision table, an option-generation step, explicit evaluation of the current design, on-demand lenses (`architecture`, `data`, `contracts`, `failure`), and a fixed final summary that `write-spec` consumes.
- `review-merge-request` delegates analysis to `review-code` and keeps only merge-specific inputs, checks, and the recommendation.
- Review and diagnosis reports are conversation-first; all reviews use the shared finding format.
- Model-invoked skills have "Use when…" descriptions; restated policy and repeated examples were removed.
- `refine-backlog` no longer references the nonexistent bundled Jira script.
