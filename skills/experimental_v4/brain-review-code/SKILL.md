---
name: brain-review-code
description: Review a bounded Git change set for correctness, requirement fit, and repository fit, reporting only evidence-backed findings. Use when the user asks for a code review of a branch, commit range, or working-tree change, or when implementation of a substantial or consequential change is complete.
---

# Code Review

**Project brain:** If `.brain/00_index.md` exists (at this worktree's root, or in the main checkout when working in a linked git worktree) and you have not read its root files in this session (or they were lost to context compaction), read every root `.md` file in that `.brain/` now. On a branch other than the brain's `Main branch:`, also read `pending/<branch>.md` (a `/` in the branch name is written `--`) when it exists. Read subfolders only when a root file links to them or the task needs them. Do not load `.brain` into subagents wholesale; pass only what their task needs. Write any `.brain/` document into that same `.brain/`. If no brain exists, proceed without one and mention once that `/brain-init` can create it.

Review a bounded change set in three assessments: **Correctness**, **Requirement fit**, and **Repository fit**. Follow `CLAUDE.local.md` for decision authority; a finding may recommend a change but does not authorize a redesign.

Format every finding as defined in `${CLAUDE_SKILL_DIR}/references/findings.md`.

## 1. Resolve the comparison

Choose the base in this order:

1. base explicitly given by the user;
2. base recorded by the invoking workflow before changes began (for example, `Review base` in the impl plan in `.brain/impl_plans/`), if it resolves and is an ancestor of `HEAD`;
3. target branch of a verified PR/MR for the current branch (for example, from `gh pr view` or `glab mr view`);
4. unambiguous repository evidence, such as documented branch conventions naming a single integration branch, or a repository with only one long-lived branch;
5. otherwise ask the user for the base and stop.

Never treat the upstream tracking branch (`@{upstream}`) as the target; it usually tracks the source branch itself.

For committed changes, review the equivalent of:

```bash
git diff <base>...HEAD
git log <base>..HEAD --oneline
```

When the requested scope covers uncommitted work, include staged, unstaged, and relevant untracked files, and list them separately so nothing is omitted or counted twice. If the scope contains no changes, report that and stop.

## 2. Establish the requirement basis

Use the first that applies:

1. specification or approved ticket supplied by the user;
2. governing specification or ticket recorded by the invoking workflow;
3. an unambiguous relevant specification under `.brain/specs/`;
4. requirements explicitly established in the current task or approved discussion.

Do not invent a specification or choose among conflicting ones. Ask only when ambiguity prevents a faithful review. If no reliable basis exists, skip Requirement fit and say why.

Also read applicable repository guidance, tooling configuration, `.brain/glossary.md`, `.brain/03_architecture.md`, and relevant ADRs in `.brain/adrs/`. Do not report properties that automated tooling already guarantees.

## 3. Choose the execution mode

- **Delegated:** when the change spans more than one component (top-level module, package, or service) or about 300 or more changed lines, excluding generated files and lockfiles. Dispatch one standard-tier subagent per assessment in parallel. Give each only its own packet (below) and the path to `references/findings.md`; none receives another's conclusions.
- **Inline:** otherwise, or when subagents are unavailable. Complete each assessment in turn without revising earlier conclusions to match later ones. State in the report that the assessments did not run in separate contexts.

Every packet contains the resolved base, the commit range and any working-tree files, and the changed files. Separate contexts reduce shared assumptions; they do not guarantee correctness. Step 5 applies in both modes.

## 4. Assessments

### Correctness

**Packet:** the change set, plus relevant callers and tests.

Look for defects the change introduces or exposes:

- **Edge cases:** empty, boundary, absent/null, duplicate, and oversized inputs.
- **Failure paths:** swallowed errors, partial failure, cleanup and rollback, retries.
- **Concurrency and lifecycle:** races, ordering, resource leaks, use after close or shutdown.
- **Data integrity:** lost updates, invalid states, migration and serialization compatibility.
- **Regressions in callers:** changed signatures, semantics, defaults, or error behavior that existing callers depend on.

For each candidate, trace the path in current code and try to disprove it: a guard elsewhere, an invariant, a test that covers it. When safe, run targeted existing tests or a minimal non-destructive reproduction. Report only candidates that survive. Category: the bullet heading above.

Do not report style, maintainability, or specification mismatches here.

### Requirement fit

**Packet:** the change set, the governing requirements and approved decisions, and the code implementing the required behavior.

Trace each applicable requirement and specification Example to the implementation. Report:

- missing or incomplete required behavior;
- behavior contradicting the specification;
- material observable behavior or contract changes the specification does not authorize;
- changes to an explicitly approved responsibility or architectural boundary.

Undocumented local implementation details are not unsupported behavior. Category: `Requirement`. Give no maintainability advice here.

Also build a coverage table: one row for each specification Example, and one for each acceptance criterion of the tickets in scope, plus one per Review Focus item (`RF<n>`) when provided. An unmet RF row is a finding graded by its effect, and the summary counts include RF rows. Mark a `blocked` RF item `unverifiable`, naming its pending decision. It is not a finding and never enters a fix pass. Mark each row:

- **met** — cite the test that verifies it, or the file:line that implements it and "no test" when no test does;
- **unmet** — cite the finding that reports it (every unmet row has one);
- **unverifiable** — say what evidence is missing.

### Repository fit

**Packet:** the change set, applicable repository rules with their locations, and what tooling guarantees.

Evaluate as heuristics, subordinate to documented rules:

- **Cohesion:** unrelated responsibilities together, or one behavior spread across needless locations.
- **Coupling:** deep knowledge of other objects; pass-through layers that own nothing.
- **Domain representation:** repeated groups of primitives that obscure invariants.
- **Control structure:** complexity or duplicated dispatch with a demonstrable maintenance cost.
- **Duplication:** behavior that must change in several places to stay correct.
- **Abstraction discipline:** new managers, services, interfaces, dependencies, or indirection without a current requirement; misleading inheritance.
- **Change scope:** unrelated refactors or displaced responsibilities.

Report an issue only when it conflicts with a documented rule (cite its location) or has a concrete current maintenance consequence (label it an advisory heuristic). Exclude unchanged pre-existing issues unless the change worsens them. For a structural correction, first check whether a simpler fix within the existing architecture works, and mark structural changes as requiring approval. Category: the heuristic name or `Repository rule`.

## 5. Consolidate and validate

1. Re-check every finding against the current code. Drop any that is disproven or rests on a misreading.
2. Merge only findings that describe the same defect; keep the merged finding in the most relevant assessment and note the overlap. Keep distinct findings separate even when they touch the same code.
3. Order findings within each assessment by severity.

Edit for clarity, but do not otherwise change an assessment's substantive conclusions.

## 6. Report

```markdown
**Base:** `<sha>` (<how it was chosen>) · **Scope:** <range, plus working-tree files if included> · **Mode:** delegated | inline (assessments did not run in separate contexts)

## Correctness

<findings, or "No supported findings">

## Requirement Fit

| Requirement | Status | Evidence |
|---|---|---|
| E1 | met | `tests/test_filter.py::test_e1_range` |
| E2 | unmet | R1 |
| Ticket 02 AC 2 | met | `crate/cli.py:41` (no test) |

<findings, "No supported findings", or "Skipped — <reason>">

## Repository Fit

<findings, or "No supported findings">
```

Finish with:

```text
Correctness: <N> findings
Requirement fit: <met>/<total> met, <N> findings | skipped
Repository fit: <N> findings
```

Do not derive an overall pass/fail verdict. If a correction requires a consequential choice, name the decision to take back to the user.
