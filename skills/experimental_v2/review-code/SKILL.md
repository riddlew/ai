---
name: review-code
description: Independently review a bounded Git change set for repository fit and requirement fit, emphasizing evidence and actionable impact over speculative refactoring.
---

# Code Review

Review a bounded change set against repository rules and established requirements, with or without a standalone written specification. Follow root `CLAUDE.md` for decision authority.

Produce two **independent** assessments:

- **Repository fit:** compliance with repository rules and material maintainability concerns.
- **Requirement fit:** fidelity to the applicable specification and approved decisions.

Keep the evidence and conclusions isolated until both assessments are finished. A review may recommend changes, but **does not authorize an architectural redesign**. Consequential design alternatives require user consultation before implementation.

## Preparation

### Resolve the comparison

Choose the base in this order:

1. base explicitly given by the user;
2. base recorded by the invoking workflow **before changes began**;
3. otherwise ask the user for the base and stop.

Do not guess the base. Verify that it resolves.

For committed branch changes, review the merge-base equivalent of:

```bash
git diff <base>...HEAD
git log <base>..HEAD --oneline
```

When the requested review also covers uncommitted changes, include staged, unstaged, and relevant untracked files explicitly. Identify their scope separately so no implementation is silently omitted or counted twice. A `git diff <base>...HEAD` alone does **not** include working-tree changes.

If no changes are present within the established review scope, report that and stop.

### Locate authoritative material

Inspect applicable repository guidance and tooling configuration. Include domain records (`CONTEXT-MAP.md`, relevant `CONTEXT.md`) and applicable root/context ADRs. Avoid findings for properties already guaranteed by automated tooling.

Resolve the requirement basis in this order:

1. specification or approved ticket explicitly supplied by the user;
2. governing specification/ticket recorded by the invoking workflow;
3. unambiguous relevant specification under `docs/` or `specs/`;
4. explicitly established requirements from the current task or approved discussion.

Do not invent a specification or guess among several conflicting ones. Ask only when materially ambiguous governing requirements prevent a faithful review. If no reliable basis exists, skip requirement-fit assessment and explain why; routine changes do not require creating a spec.

## Build independent evidence packets

### Repository-fit packet

Provide the range and working-tree scope, changed files and commits, applicable repository rules with locations, relevant changed code, and automated-tooling guarantees.

Evaluate:

- **Cohesion:** unrelated responsibilities, or one behavior spread across needless locations.
- **Coupling:** deep knowledge of other objects, pass-through layers with no useful ownership.
- **Domain representation:** repeated groups of primitive values that obscure important invariants.
- **Control structure:** complexity or duplicated dispatch with a **demonstrable** maintenance cost; conditionals alone do not imply an abstraction is needed.
- **Duplication:** behavior that must be changed in multiple places to stay correct.
- **Abstraction discipline:** new managers, services, interfaces, dependencies, or indirection without a current requirement or concrete advantage; misleading inheritance relationships.
- **Change scope:** unrelated refactors or displaced responsibilities not needed for the task.

These are heuristics, not independent repository rules. Documented rules take precedence.

For a proposed architectural correction, assess whether the simpler existing-architecture approach would work. Do not recommend extra layers merely because they are a familiar pattern or might help future use cases.

### Requirement-fit packet

Provide the same reviewed scope, the authoritative specification and approved decisions, and code showing required behavior.

Trace each applicable requirement to implementation. Report:

- missing or incomplete required behavior;
- behavior contradicting the spec;
- additional **material observable behavior or contract changes** not authorized by the spec;
- an implementation that changes an explicitly approved responsibility or architectural boundary.

Do not treat every undocumented local implementation detail as unsupported behavior. Do not inject generic code-style preferences into requirement fit.

## Reviewer contracts

Run reviewers concurrently when both assessments are available; neither receives the other's conclusions.

### Repository-fit reviewer

Report an issue only when supported by concrete evidence of a repository-rule conflict or meaningful current maintenance consequence. Do not manufacture findings to satisfy a checklist.

For each issue provide:

- **Location:** affected code.
- **Severity:** blocker / significant / minor, based on actual impact.
- **Basis:** exact repository rule or clearly labeled advisory maintainability heuristic.
- **Evidence:** what the change demonstrably does.
- **Impact:** concrete failure, complexity, or maintenance consequence.
- **Smallest correction:** the least disruptive reasonable fix; identify architectural changes as requiring approval.

Cite documented rules by location. Exclude unchanged preexisting issues unless essential to explain an introduced problem, and exclude speculative refactors without a concrete benefit.

Report all substantiated **actionable** findings, ordered by consequence. Do not pad the report with low-confidence aesthetic objections.

### Requirement-fit reviewer

For every mismatch provide:

- **Requirement:** relevant specification text/location or approved decision.
- **Implementation:** changed code or observable behavior.
- **Mismatch:** exact difference.
- **Impact:** consequence for required behavior.

Report all substantiated mismatches, ordered by consequence. Do not offer general maintainability advice here.

## Final report

Keep the two assessments independent:

```markdown
## Repository Fit

<findings, or "No supported findings">

## Requirement Fit

<findings, or "No supported findings">
```

If no reliable requirement basis applies, write:

```markdown
## Requirement Fit

Skipped — no reliable governing requirements were established for this change.
```

Avoid combining or deduplicating distinct findings across the two assessments, even when they concern the same code. Editing for clarity is fine; do not change substantive reviewer conclusions.

Finish with:

```text
Repository fit: <N> findings
Requirement fit: <N> findings | skipped
```

Do not derive an overall pass/fail verdict from the two assessments. If a proposed correction requires an architectural choice, identify the decision to take back to the user; do not silently choose or implement it.
