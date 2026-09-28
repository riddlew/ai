---
name: verify-handoff
description: Verify whether software work is complete and write the final durable verification and handoff artifact. Use for build and test verification, acceptance-criteria checks, documentation synchronization, continuation summaries, PR descriptions, or implementation retrospectives.
argument-hint: "[optional: verify|acceptance|docs-sync|continuation|pr-prep|retrospective] [description]"
---

# Verify and Hand Off

Determine the actual completion state of a change and leave evidence that another engineer can trust and resume from.

Use `$ARGUMENTS` as the change, requirements, or handoff scope when provided.

## Result Artifact

Before verification, locate the nearest project `.claude/` directory from the working directory up to the repository root. Do not use the personal `~/.claude/` directory.

- If no project `.claude/` directory exists, ask the user where to save the result before continuing. Do not create `.claude/`, choose another location, or skip the artifact without their answer.
- Resolve the work-item directory as `.claude/results/<ISSUE-ID>/` from an explicit ticket or issue ID. Without one, use the matching existing work-item directory; if none exists, ask which work item to verify.
- Read `01-investigation.md`, `02-plan.md`, `03-implementation.md`, and all relevant diagnosis and review artifacts. Recheck their claims against the current repository and execution evidence. Treat missing required artifacts as a verification gap rather than inventing their contents.
- Write or update `04-verification-handoff.md`. Use status **verified** only when required acceptance criteria and checks pass; otherwise use **not-verified** or **blocked**.
- Put the work-item key, stage, status, updated date, verified revision or working-tree state, and all input artifact paths in YAML frontmatter. Put commands and results, criterion status, residual risk, and exact resume information when incomplete in the body.
- Report the artifact path and completion status to the user.

## Modes

Select only the modes needed:

- **verify**: Run relevant build, test, lint, static-analysis, API, and runtime checks.
- **acceptance**: Trace every acceptance criterion to implementation and evidence.
- **docs-sync**: Reconcile specifications, decisions, examples, setup instructions, and stale references with the implemented behavior.
- **continuation**: Capture exact state, blockers, remaining tasks, and resume commands.
- **pr-prep**: Prepare a change-set or pull-request description with risks and reviewer focus.
- **retrospective**: Record lessons that materially improve the next change without turning one incident into a universal rule.

## Workflow

1. Re-read the requirements, approved combined plan, diff, and relevant repository instructions.
2. Determine the validation surface from the actual change and risk. Run the strongest practical checks available; do not substitute a narrow unit test for required integration or runtime evidence.
3. Record each command exactly enough to reproduce it, its result, and relevant environment limitations.
4. Trace acceptance criteria individually. Classify each as **verified**, **partially verified**, **not verified**, or **not applicable**, with evidence.
5. Distinguish:
   - checks executed successfully;
   - checks executed and failed;
   - checks not run;
   - conclusions based only on inspection or inference.
6. Update documentation only when it is part of the authorized change. Keep examples and setup commands consistent with verified behavior.
7. Do not declare completion while required checks fail, required criteria remain unverified, or material scope conflicts remain unresolved.

## Handoff Contract

For a completed change, include:

- intent and implemented behavior;
- changed files or components;
- verification evidence;
- compatibility and operational impact;
- risks and residual uncertainty;
- reviewer focus areas when preparing a PR.

For incomplete or paused work, include:

- current state and completed work;
- evidence gathered;
- remaining tasks in dependency order;
- blockers and unresolved decisions;
- exact commands and locations needed to resume;
- working-tree state and any uncommitted changes that must be preserved.

Keep the final handoff concise, but never collapse executed and suggested verification into the same claim.
