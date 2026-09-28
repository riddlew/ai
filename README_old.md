# Software Engineering Workflow Skills for Claude Code

Eight Claude Code skills covering five workflow stages, from initial investigation through verified handoff:

```text
Investigate
    ↓
Plan ───────────────┐
    ├── Review      │ optional findings or scope loop
    ↓               │
Implement ──────────┘
    ↓
Diagnose / Review
    ├── Diagnose
    ├── Code Review
    ├── Architecture Review
    └── Security Review
    ↓
Verify and Hand Off
```

Each skill is stored at `skills/<skill-name>/SKILL.md`. This is the layout used inside a Claude Code plugin. To use them as personal standalone skills, copy the eight skill directories into `~/.claude/skills/`. To use them in one project, copy them into that project's `.claude/skills/` directory.

## Result Artifacts

The skills create a durable record under the nearest project `.claude/` directory. They do not use the personal `~/.claude/` directory for project results.

When a ticket or issue ID is available, it identifies the work item:

```text
.claude/results/PAY-1842/
├── 01-investigation.md
├── 02-plan.md
├── diagnoses/
│   └── 01-duplicate-provider-request.md
├── reviews/
│   ├── 01-code-review.md
│   ├── 02-architecture-review.md
│   └── 03-security-review.md
├── 03-implementation.md
└── 04-verification-handoff.md
```

Without an issue ID, the investigation skill creates the next unused three-digit work-item directory with a short slug, such as `.claude/results/007-fix-checkout-retries/`. Later skills reuse that directory instead of creating disconnected records.

If no project `.claude/` directory can be found between the working directory and repository root, every skill asks where to save its result before continuing. It does not create `.claude/`, silently use `~/.claude/`, or skip the artifact.

Each artifact begins with stable YAML metadata:

```yaml
---
work_item: PAY-1842
stage: plan
status: ready
updated: 2026-09-14
revision: working-tree
inputs:
  - 01-investigation.md
---
```

The body records the stage-specific evidence, assumptions, decisions, checks, and unresolved issues. Skills must recheck important claims against the current repository because an earlier artifact can become stale.

The main sequence has stable filenames. Diagnosis and review results are append-only and numbered within their subdirectories so repeated passes are preserved. The `plan` skill combines investigation findings with user input through probing questions, records the approved design and bounded task sequence in `02-plan.md`, and uses separate approval gates for both. Optional review skills can evaluate it before coding. The `implement` skill follows the ready plan and records execution in `03-implementation.md`, which ends as `implemented`, not `verified`. Only `04-verification-handoff.md` can record final verification.

## Example Ticket

The examples below follow one realistic ticket through the workflow.

> **PAY-1842 — Prevent duplicate card charges during checkout retries**
>
> When the payment provider times out, the checkout service retries the charge request. Some customers have been charged twice because each retry creates a new provider request. Add idempotent payment submission without changing the public checkout API. Existing clients must continue to work. Add regression coverage and document any operational requirements.

## 1. Investigate

Use this before proposing a solution. It extracts requirements, maps the repository, traces affected code, and identifies missing evidence.

```text
/investigate PAY-1842: Prevent duplicate card charges during checkout retries.

Inspect the repository and produce an evidence-backed investigation. Extract the
acceptance criteria and constraints, trace payment submission from the checkout
endpoint to the provider client, identify affected tests and documentation, and
verify the installed payment SDK version. Do not design or modify code yet.
```

Expected result: confirmed requirements, relevant files and symbols, verified build and test commands, likely downstream consumers, risks, assumptions, and questions that could change the design, written to `.claude/results/PAY-1842/01-investigation.md`.

## 2. Plan

Use this after investigation and before implementation. It asks probing questions, compares design alternatives, obtains design approval, and then produces an explicitly approved task sequence.

```text
/plan PAY-1842.

Use .claude/results/PAY-1842/01-investigation.md and my answers to compare
provider idempotency keys, a database-backed request ledger, and an in-memory
deduplication cache. Recommend an approach, select the smallest end-to-end
vertical slice, and stop for design approval. Then break the approved design
into independently verifiable tasks with affected components, invariants, tests,
dependencies, risks, validation commands, and completion conditions. Keep the
public checkout API unchanged. Do not modify source code.
```

The skill first researches repository-answerable questions, then asks one consequential question per message. It does not guess from silence or ambiguous answers. Questions focus on choices that can change scope, priorities, task boundaries, compatibility, migration, rollout, validation, documentation, or completion conditions. Each answer is recorded in the draft artifact.

After resolving material design questions, the skill presents the design and records approval as `design-approved`. It then asks any remaining task-planning questions, presents the complete task sequence, and marks `.claude/results/PAY-1842/02-plan.md` as `ready` only after a second explicit approval.

The `code-review`, `architecture-review`, and `security-review` skills can optionally review this plan. Reinvoke `plan` with the resulting review artifacts to resolve findings, re-present the revision, and obtain approval again before implementation.

## 3. Implement

Use this only after the combined design and task plan is `ready`. It establishes a baseline, changes the smallest coherent slice, and stops on plan conflicts.

```text
/implement PAY-1842 task 1 from the ready implementation plan.

First add a regression test that reproduces duplicate provider submissions when
the first response times out. Then implement only the approved vertical slice.
Preserve the public checkout API and unrelated retry behavior. Run the focused
tests after each meaningful change and stop if the installed SDK cannot support
the approved plan or if persistence becomes necessary.
```

Expected result: code and tests limited to the selected planned task, with progress and evidence recorded in `.claude/results/PAY-1842/03-implementation.md`. Implementation stops if the plan is missing, not ready, stale relative to blocking reviews, or conflicts with repository evidence.

## 4. Diagnose and Review

This stage contains four independent skills. Invoke only the review or diagnostic activity the situation requires.

### Diagnose

Use this for a failing test, production symptom, intermittent behavior, or regression that needs evidence-driven root-cause analysis.

```text
/diagnose PAY-1842: the concurrency regression test intermittently creates two
provider requests.

Reproduce the failure, separate evidence from hypotheses, and run one
discriminating experiment at a time. If the cause is confirmed, make the
smallest in-scope fix, strengthen the regression test, and rerun the original
reproduction.
```

Expected result: a reproducible symptom, evidence, competing hypotheses, experiment results, a supported root cause, and regression evidence for any authorized fix, written to the next numbered file under `.claude/results/PAY-1842/diagnoses/`.

### Code Review

Use this to review either the combined plan or the completed diff against the ticket, approved decisions, callers, and tests.

```text
/code-review PAY-1842 combined plan.

Review .claude/results/PAY-1842/02-plan.md against the ticket. Check whether its
approved design and tasks cover retry paths, concurrent requests,
idempotency-key stability, error handling, public API compatibility, and
regression coverage. Report findings by severity with file and symbol evidence.
Do not modify code or the plan.
```

Expected result: severity-ordered, evidence-backed correctness findings with concrete impacts and corrections, or a clear statement that no material findings remain plus residual validation gaps, written to the next numbered `reviews/<NN>-code-review.md` file.

### Architecture Review

Use this before a new interface, state model, persistence format, concurrency mechanism, or shared abstraction spreads through the codebase.

```text
/architecture-review PAY-1842 combined plan.

Review .claude/results/PAY-1842/02-plan.md before implementation.
Map the proposed ownership and responsibility boundaries, check coupling to the
payment provider, and evaluate how the planned abstraction handles two payment
operations and one future provider. Identify expensive-to-reverse decisions and
recommend corrections without modifying code or the plan.
```

Expected result: evidence-backed structural findings, consequences, tradeoffs, decisions safe to preserve, and decisions needing approval before the pattern spreads, written to the next numbered `reviews/<NN>-architecture-review.md` file.

### Security Review

Use this when a change touches trust boundaries, authorization, credentials, sensitive data, persistence, logging, or external transmission.

```text
/security-review PAY-1842 combined plan.

Review .claude/results/PAY-1842/02-plan.md. Trace the proposed
idempotency key from checkout input through logs, storage, telemetry, and the
payment provider request. Check whether a user could influence or reuse a key
across accounts, whether it exposes sensitive identifiers, and whether logs or
retries could cross tenant boundaries. Do not modify code, the plan, or
credentials.
```

Expected result: severity-ordered findings tied to assets and trust boundaries, plausible threat scenarios, practical mitigations, and explicit scope limitations, written to the next numbered `reviews/<NN>-security-review.md` file without persisting secrets.

## 5. Verify and Hand Off

Use this after implementation and review corrections. It determines the actual completion state and creates a durable handoff or pull-request summary.

```text
/verify-handoff PAY-1842.

Run the relevant build, unit, integration, lint, and runtime checks. Trace every
ticket acceptance criterion to implementation and evidence. Reconcile payment
setup and operational documentation with the verified behavior. Then prepare a
concise PR description covering intent, implementation, compatibility, risks,
executed checks, remaining uncertainty, and reviewer focus areas.
```

Expected result: reproducible verification evidence, criterion-by-criterion status, synchronized documentation, remaining uncertainty, and a concise handoff or PR description in `.claude/results/PAY-1842/04-verification-handoff.md`. Checks that were not run must remain visibly distinct from successful checks.

## Operating Rules

- Investigation gathers evidence; it does not silently become design or implementation.
- Planning asks one material question at a time, records the answers, and never substitutes assumptions for user intent.
- Planning requires explicit approval of the design before task decomposition and explicit approval of the task plan before becoming ready.
- Planning combines approved design decisions and bounded tasks in one artifact; it does not modify source code.
- Implementation requires a ready plan and stops on unresolved blocking review findings.
- Every skill reads relevant prior artifacts and rechecks them against current repository evidence.
- The skill reports the result path after writing or updating an artifact.
- Repository evidence or scope conflicts return the work to investigation or reopen the applicable planning decision.
- Debugging, code review, and final verification are separate activities with separate evidence.
- A change is not complete merely because code was written or a narrow test passed.
