---
name: investigate
description: Investigate a software request and repository before design or implementation, then write a durable investigation artifact. Use for problem framing, acceptance criteria, repository onboarding, change-impact analysis, unknowns, risks, or dependency and API verification.
argument-hint: "[optional: problem-frame|repository-map|impact-map|risk-scan|dependency-check] [description]"
---

# Investigate

Build an evidence-backed understanding of the request and relevant repository state. Do not design or implement the change unless the user explicitly expands the task.

Use `$ARGUMENTS` as the request or investigation focus when provided.

## Result Artifact

Before investigating, locate the nearest project `.claude/` directory from the working directory up to the repository root. Do not use the personal `~/.claude/` directory.

- If no project `.claude/` directory exists, ask the user where to save the result before continuing. Do not create `.claude/`, choose another location, or skip the artifact without their answer.
- Use `.claude/results/<ISSUE-ID>/` when the request contains a ticket or issue ID such as `PAY-1842`.
- Without an issue ID, use `.claude/results/<NNN>-<short-slug>/`, where `NNN` is the next unused three-digit sequence.
- Write the final result to `01-investigation.md`. Replace that file only when updating the same work item; preserve unrelated artifacts.
- Put the work-item key, stage, status, updated date, repository revision or working-tree state, and input artifact paths in YAML frontmatter. Put the source request, evidence, assumptions, and unresolved questions in the body.
- Report the artifact path to the user.

## Modes

Select only the modes needed for the request:

- **problem-frame**: Extract intended behavior, acceptance criteria, constraints, non-goals, and unresolved questions.
- **repository-map**: Detect languages, frameworks, build and test entry points, conventions, CI, and important directories.
- **impact-map**: Map the request to files, symbols, tests, documentation, APIs, and downstream consumers.
- **risk-scan**: Identify unknowns, expensive assumptions, compatibility risks, and missing evidence.
- **dependency-check**: Verify installed versions and current official documentation for version-sensitive dependencies or APIs.

## Workflow

1. Read repository instructions and inspect the working tree before drawing conclusions.
2. Search broadly enough to find entry points, callers, tests, configuration, and documentation; inspect file contents rather than inferring responsibility from names.
3. Trace important behavior through symbols and call paths. Record evidence as file paths, symbols, commands, or authoritative documentation.
4. Run safe, read-only discovery commands when they materially reduce uncertainty. Report commands as verified only when actually executed successfully.
5. Separate:
   - confirmed requirements from the user or authoritative project material;
   - repository facts supported by evidence;
   - assumptions and inferences;
   - unresolved questions that could change the solution.
6. Assign confidence to non-obvious impact mappings. Explain low-confidence mappings and what would verify them.
7. Stop when the request is sufficiently understood to make a design decision. Do not turn investigation into speculative implementation planning.

## Output

Write a concise investigation report to the result artifact containing only relevant sections:

- Intended behavior and acceptance criteria
- Constraints and non-goals
- Repository map and verified commands
- Impact map with evidence and confidence
- Risks and unknowns
- Assumptions
- Open questions that block or materially alter design

If evidence conflicts with the request or existing documentation, state the conflict directly. Do not silently choose one source.
