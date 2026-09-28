---
name: implement
description: Implement one approved software change by following a ready combined design and implementation plan. Use after planning when code plus tests should be changed with test-driven evidence, invariant preservation, and explicit stop conditions.
argument-hint: "[optional: baseline|vertical-slice|bounded-change|scope-check] [description]"
---

# Implement

Execute one approved change within a bounded scope. Do not redesign the task silently when repository evidence conflicts with the plan.

Use `$ARGUMENTS` to identify the approved work item, planned task, or permitted subset of the implementation plan.

## Result Artifact

Before editing code, locate the nearest project `.claude/` directory from the working directory up to the repository root. Do not use the personal `~/.claude/` directory.

- If no project `.claude/` directory exists, ask the user where to save the result before continuing. Do not create `.claude/`, choose another location, or skip the artifact without their answer.
- Resolve the work-item directory as `.claude/results/<ISSUE-ID>/` from an explicit ticket or issue ID. Without one, use the matching existing work-item directory; if none exists, ask which work item to use rather than creating a disconnected implementation record.
- Read `01-investigation.md` and `02-plan.md`. Require the plan to have status **ready**, record both design and task-plan approval, contain no blocking open questions, and include the requested task.
- Read plan-review artifacts when present. Stop if a material finding remains unresolved or the plan is older than a review that requires changes.
- Before code changes, create or update `03-implementation.md` with status **in-progress** and an execution checklist derived from the selected planned task. The combined plan remains authoritative; the implementation artifact is the live progress and evidence log.
- Follow the checklist and update it after meaningful milestones with completed steps, changed files, commands and results, decisions, and deviations. Record a scope or evidence conflict as **blocked** before stopping.
- At the end, mark the artifact **implemented**, not verified. Final completion belongs to `verify-handoff`.
- Put the work-item key, stage, status, updated date, starting and current repository revision or working-tree state, and input artifact paths in YAML frontmatter. Report the artifact path to the user.

## Modes

Select only the modes needed:

- **baseline**: Reproduce current behavior or establish a failing test before changing implementation.
- **vertical-slice**: Implement the smallest approved end-to-end path.
- **bounded-change**: Make a narrowly scoped correction or enhancement within named files, behaviors, and invariants.
- **scope-check**: Compare new evidence with the approved plan and decide whether to continue or stop.

## Entry Gate

Before editing, identify from the implementation plan:

- approved behavior and acceptance criteria;
- allowed files or components and allowed behavior changes;
- invariants, compatibility requirements, and non-goals;
- validation commands and the stop condition.

If a material design decision is unresolved, stop and return it to the user or the plan workflow. Infer routine implementation details only when they do not alter the approved behavior or architecture.

## Workflow

1. Read repository instructions and inspect existing changes. Preserve unrelated user work.
2. Establish a reproducible baseline. Prefer an acceptance-level failing test before implementation when practical; otherwise record why another baseline is more appropriate.
3. Make the smallest coherent change that satisfies the selected planned task. Follow existing local patterns unless the approved plan intentionally changes them.
4. Keep tests tied to observable behavior and relevant regressions. Avoid tests that merely restate implementation details.
5. Run focused validation after meaningful increments. Distinguish executed checks from checks that remain suggested.
6. Re-check scope before touching additional files, altering a public contract, introducing a dependency, changing persisted data, or adding an abstraction.
7. Stop implementation and report the conflict if:
   - repository evidence contradicts the plan;
   - an acceptance criterion cannot be met within scope;
   - a new expensive-to-reverse decision appears and requires reopening the plan;
   - required access, dependency, environment, or user authority is missing;
   - validation reveals a broader defect outside the approved change.

## Output

Write and report:

- implemented behavior;
- changed files;
- tests and checks actually executed with results;
- any unresolved issue or scope conflict.

Do not claim completion based on code inspection alone. Leave broader refactoring, cleanup, and unrelated defects out of the change unless separately approved.
