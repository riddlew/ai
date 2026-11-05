# Subagent-driven mode

For the coordinator (the main session). When filling any template, fill every slot. Path slots are absolute paths: `{review_feedback_path}` is `${CLAUDE_SKILL_DIR}/references/review-feedback.md`, and `{findings_path}` is `findings.md` in `brain-review-code/references/` beside this skill's folder.

Per task, in order:

1. **Base.** Run `git rev-parse HEAD` and `git status --short`. Record the sha as the task's base and the status output as its pre-existing changes in the impl plan's work item, and use them in later commands. Shell variables do not persist. If the previous task was not committed, keep its base and pre-existing changes, and give the reviewer both tasks' briefs, Examples, and criteria.
2. **Implementer.** Dispatch on the standard tier with `${CLAUDE_SKILL_DIR}/references/implementer-prompt.md`. Fill only the task text, Examples and criteria, relevant brain excerpts and code locations, and constraints. Never send the whole `.brain`. Keep its agent id for rounds 1-3. Handle its status:
   - `NEEDS_CONTEXT`: answer and resume it.
   - `BLOCKED`: resolve it. If the choice is consequential under root `CLAUDE.md`, consult the user.
3. **Task reviewer.** Dispatch on the standard tier, read-only, with `${CLAUDE_SKILL_DIR}/references/task-reviewer-prompt.md`: the base sha, the pre-existing changes (`{preexisting}`), the brief, and the implementer's report.
4. **Fix loop.** Before any fix round, drop findings that target a pre-existing change. Never ask an implementer to delete, revert, or edit the user's pre-existing work. Run the loop when an Example or criterion is unmet or unclear, or any remaining finding is Critical, High or Medium. Low findings go to the impl plan's `## Deferred` list and never to a fix round. Each round is one fix plus one scoped re-review (standard tier, re-review variant). Nothing is committed between rounds, so the re-review input is the cumulative `git diff <base>` plus untracked files, the pre-existing changes, the open findings, and the implementer's fix-round report.
   - Rounds 1-3: resume the same implementer (in Claude Code, `SendMessage` to its agent id) with the open findings in findings format and "apply the Fix round section".
   - Rounds 4-5: dispatch a fresh implementer on the strongest tier. Fill the template, including `{open_findings}` and `{prior_report}`.
   - The implementer may push back with evidence under `review-feedback.md`. The next re-reviewer judges the pushback. A disputed finding still uses up a round.
   - The loop ends when a review or re-review has no unmet or unclear row and no remaining Critical, High or Medium finding.
5. **After round 5.** Rule on each open finding, applying `review-feedback.md`:
   - Reviewer wrong or point contestable: park it with the reason.
   - Real but not blocking: defer it.
   - Unmet Example or criterion, or anything consequential: take it to the user. The task is not done.

   Record each ruling under `## Rulings` as `Ruling: <decision> — <why> — <cost if wrong>`. Parked and deferred findings do not block done.
6. **Proof before done.** This applies SKILL.md §5 step 6 in this mode: (a) rerun the task's targeted tests yourself and read the output; (b) the reviewer's coverage rows are the Example evidence; (c) the task review plus a `git diff --stat <base>` scope check are the self-review; (d) record the command and result in the impl plan. §7 step 1 decides whether the full suite runs.
7. **Commit pause.** Apply SKILL.md's Commit pause unchanged. When the user confirms a commit, also check that `git status --short` shows no uncommitted changes in the task's files.

## Final review

§7 step 3 decides whether a full review runs; per-task reviews and the execution mode do not make a change substantial. When it does run, it uses the impl plan header's `Review base`, not the per-task bases; its fix pass is one fresh strongest-tier implementer, using the implementer prompt's Fix round section with the final findings. Then run the full suite and the commit pause. Inline mode: the main session fixes, as §7 says.

## Rules

- Never edit code in this mode, including fixes. Fixes go through implementers.
- Pause only for commit pauses, consequential decisions, and blockers you cannot resolve.
- Never dispatch two implementers at once.
- If no subagent tool is available, say so once and switch to inline for the rest of the run. Record `Execution mode: inline (no subagent tool)` in the impl plan header.
