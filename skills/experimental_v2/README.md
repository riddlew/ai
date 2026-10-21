# Claude Code Skills

An opinionated set of **11 Claude Code skills** for collaborative software development. The goal is to produce straightforward, maintainable changes while keeping consequential product and architectural decisions under your control.

The skills are **tools to use when needed**, not a mandatory pipeline. Small changes should stay small; complex or multi-session work can use more structure.

## Install

Copy `CLAUDE.md` to the root of your project and copy `.claude/skills/` into the project's `.claude/skills/` directory:

```text
project/
├── CLAUDE.md
└── .claude/
    └── skills/
        ├── brainstorm/SKILL.md
        ├── diagnose/SKILL.md
        ├── domain-modeling/SKILL.md
        ├── handoff/SKILL.md
        ├── implement/SKILL.md
        ├── plan-feature/SKILL.md
        ├── review-architecture/SKILL.md
        ├── review-code/SKILL.md
        ├── review-security/SKILL.md
        ├── write-spec/SKILL.md
        └── write-tickets/SKILL.md
```

Merge `CLAUDE.md` with any existing root instructions rather than replacing project-specific guidance. Remove retired skill directories if upgrading from an older version; see [MIGRATION.md](MIGRATION.md).

Skills labeled **manual** use `disable-model-invocation: true` and must be explicitly invoked (for example, `/implement`). Other skills may be selected when relevant. Explicitly invoking a skill is also an option for any skill intended for user use.

## Collaboration rules

Root [`CLAUDE.md`](CLAUDE.md) contains the shared decision policy:

- **Investigate facts independently.** Read code, tests, configuration, and documentation rather than asking questions the repository can answer.
- **Respect established decisions.** Follow approved specifications, architectural decisions, and relevant ADRs.
- **Make routine local choices.** Naming, private helpers, and ordinary test details do not need repeated approval.
- **Consult on consequential choices.** Changes to product behavior, ownership, lifecycle, public contracts, persistence, or meaningful architecture require a recommendation and your decision *before* implementation.

For example, a request to extend communication in an existing `Session` does not authorize silently moving connection ownership into a new `ConnectionManager`. Claude should explain the concrete reason for such a change, compare it with extending `Session`, and ask you which design to adopt.

## Skills

| Skill | Purpose | Use when | Typical output |
|---|---|---|---|
| `brainstorm` | Resolves meaningful open requirements and design decisions through focused questions, recommendations, and repository investigation. | The behavior, constraints, or architectural direction is unclear. | A confirmed direction in the conversation. |
| `diagnose` | Investigates bugs using observations, reproduction, and discriminating hypotheses; applies a bounded fix only when authorized. | A failure, regression, or intermittent issue needs explanation. | Diagnosis and, if authorized, verified repair; `docs/diagnoses/` report when warranted. |
| `domain-modeling` | Maintains approved domain vocabulary, context boundaries, and durable architectural decisions. | Design work establishes or changes domain meaning or context ownership. | Relevant `CONTEXT.md`, `CONTEXT-MAP.md`, or ADR updates when justified. |
| `handoff` **(manual)** | Captures the minimum information a fresh session needs, linking existing records rather than copying them. | You deliberately want a cross-session continuation document. | `handoff-<slug>.md` in the OS temporary directory. |
| `implement` **(manual)** | Implements approved work in tested increments and maintains resumable feature progress. | You are ready to change code, with or without a formal spec for a small task. | Code, checks, and for tracked features `docs/implementation/<feature>/todo.md` with optional `guidance.md`. |
| `plan-feature` | Tracks substantial planning across sessions using dependency-aware research, consultation, prototype, and prerequisite tickets. | An initiative has many interdependent decisions and will span days or sessions. | `docs/planning/<feature>/INDEX.md` and planning-ticket files. |
| `review-architecture` | Discovers architectural friction **or** assesses a selected design boundary, using concrete evidence rather than speculative cleanup. | You want architectural improvement candidates or a focused design evaluation. | Findings in conversation; durable architecture review when worthwhile. |
| `review-code` | Independently assesses repository fit and requirement fit for a bounded Git change set. | A substantive change needs an implementation review, or you explicitly request one. | Review findings in the conversation. |
| `review-security` | Examines realistic threats, trust boundaries, access control, credentials, and sensitive-data flows. | Work changes a meaningful security boundary or you request a focused security audit. | Risk-based findings; `docs/security/` report when warranted. |
| `write-spec` **(manual)** | Records established requirements, technical decisions, and a verification strategy without inventing missing choices. | A substantial feature needs a stable implementation contract. | `docs/specs/<NN>-<slug>.md`. |
| `write-tickets` | Decomposes approved work into meaningful, verifiable increments and dependencies, with your approval of the ticket set. | Work genuinely benefits from independent tickets or staged delivery. | `docs/tickets/<feature>/issues/<NN>-<slug>.md`. |

Documentation and factual research do not require dedicated skills. Perform them within the relevant task; keep a durable research note only when requested or useful later.

## Example workflows

These are **examples, not checklists**. Skip any step that does not provide value.

### Small, well-defined change

Example: Add a `--json` option to an existing export command.

1. Run `/implement` directly from the request; a specification and ticket set are not required.
2. Make the smallest coherent change and validate it using suitable targeted tests or other checks.
3. Inspect the diff. Invoke `review-code` only if the change is consequential, substantial, or you request it.
4. Update relevant existing documentation directly if the user-facing command changed.

### Substantial feature

Example: Add a share-link capability for notes.

1. Use `brainstorm` to resolve permission rules, revocation, expiration, and other consequential questions. Let Claude investigate existing repository behavior independently.
2. Use `review-architecture` if ownership or another expensive-to-reverse design decision needs focused evaluation. Record approved durable decisions through `domain-modeling` when appropriate.
3. Use `/write-spec` to capture the established behavior and decisions.
4. Use `write-tickets` **only if** the work benefits from multiple independently verifiable increments or separate implementation sessions.
5. Use `/implement` to execute the spec or tickets. Run `review-code` for a substantial change; add `review-security` if the design introduces meaningful authorization, trust, or sensitive-data boundaries.

### Large, multi-session planning effort

1. Use `plan-feature` to establish the objective, open areas, planning tickets, and genuine dependencies under `docs/planning/<feature>/`.
2. Resolve research and consultation questions in that planning system; `brainstorm` can handle the interactive decisions.
3. Once the consequential choices are settled, use `/write-spec` and optionally `write-tickets` for implementation decomposition.
4. Use `/implement` to execute the work with its separate, feature-level progress records.

`plan-feature` tracks **planning state**; it does not substitute for the implementation tracker.

### Diagnose and fix a failure

Example: Edits from two browser tabs occasionally overwrite one another.

1. Use `diagnose` to establish what happened and test the plausible causes. State whether repair is authorized or you want diagnosis only.
2. If the cause supports a small bounded correction, apply and verify it when authorized; a permanent diagnosis report is optional.
3. If the fix requires choosing new conflict-resolution semantics or redesigning ownership, consult through `brainstorm` before implementation.
4. Use `review-security` as well when the problem crosses an authorization or other security boundary.

### Improve or review architecture

Example: Changes to note permissions regularly require updates across several modules.

1. Use `review-architecture` in **discovery mode** to identify evidence-backed friction and plausible improvements.
2. Select a candidate for **focused review**; compare preserving the existing design, the smallest correction, and larger alternatives only when justified.
3. Approve any consequential change before recording it through `domain-modeling` or implementing it.
4. Write a spec and tickets only if the agreed change is sufficiently substantial or needs staged migration.

### Focused security review

Example: Audit share-link authorization before exposing it publicly.

1. Use `review-security` on the concrete trust boundary. It separates confirmed vulnerabilities from plausible, unverified risks.
2. For approved, contained mitigations, use `/implement` with relevant authorization or abuse-case tests.
3. For changes to product semantics or significant security architecture, resolve the choice with you first.

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

- **`todo.md`** tracks meaningful work items, the current focus, blockers, verified test results, and the original Git review base. It is updated as work progresses.
- **`guidance.md`** preserves useful current implementation discoveries, relevant code locations, caveats, and *references* to approved decisions. Create it only when useful.

**Both files are living documents, not append-only logs.** A fresh session reads them and then verifies progress against the actual repository, Git state, and tests before continuing. Stale notes are corrected or removed. Neither file authorizes a new product or architectural decision; the specification and applicable ADRs remain authoritative.

`implement/SKILL.md` contains concrete templates for both files. `write-spec` and `write-tickets` do not create implementation trackers before coding begins.

The `handoff` skill is optional for implementation continuation: use it when important context is not already captured by the spec, progress records, and repository. It saves its file outside the project and should reference those records rather than duplicate them.

## Verification and durable records

Implementation uses focused test-first increments when practical, together with suitable static checks and targeted tests. At completion, validation is proportional to the scope and risk. A separate `review-code` run is expected for substantial or consequential changes, **not every trivial edit**. A focused `review-security` is similarly risk-based.

Planning records, specifications, implementation tickets, and the living implementation tracker each serve distinct purposes. Diagnoses, architecture reviews, security reviews, and ADRs are persisted only when requested or when their evidence, risks, or rationale will be useful later.

For upgrading from older versions, see [MIGRATION.md](MIGRATION.md): standalone `tdd`, `improve-architecture`, `research`, and `write-documentation` have been retired or incorporated into other workflows.
