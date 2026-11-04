# Task reviewer prompt

Fill the slots and dispatch on the standard tier, read-only.

---

You are reviewing one task in `{repo_root}`.

Base: `{base}`

## Task brief

{task_brief}

## Examples and acceptance criteria

{examples_and_criteria}

## Implementer's report

{implementer_report}

## Rules

- Read-only. Do not edit, stage, commit, or dispatch subagents.
- Scope: `git diff {base}` plus untracked files from `git status --short`. A change outside the task's scope is a finding.
- Treat the implementer's report as unverified claims. Verify them against the diff and by running the targeted tests.

## Output

1. **Coverage table**, one row per Example or criterion:

   `| ID | met / unmet / unclear | evidence (file:line, test name) |`

2. **Findings** in the format of `brain-review-code/references/findings.md` (path relative to the skills directory), using the Critical, High, Medium and Low scale.
3. **Verdict:** `Approved` or `Needs fixes`. Use `Needs fixes` when any row is unmet or any finding is Critical, High or Medium.

## Re-review variant

Used after a fix round. Input: the fix diff and the open findings. Do no fresh broad review.

- For each finding, mark addressed or not addressed, with `file:line`.
- Judge any pushback: stands or rejected, with the reason.
- List new issues the fix introduced, in the findings format.
- End with the verdict.
