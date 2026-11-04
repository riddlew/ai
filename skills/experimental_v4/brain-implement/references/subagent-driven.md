# Subagent-driven mode

For the coordinator (the main session). Per task, in order:

1. **Base.** `BASE=$(git rev-parse HEAD)`. Record it in the impl plan's work item.
2. **Implementer.** Dispatch on the standard tier with `${CLAUDE_SKILL_DIR}/references/implementer-prompt.md`. Fill only the task text, its Examples and acceptance criteria, the relevant brain excerpts and code locations, and the constraints. Never send the whole `.brain`. Keep the implementer's agent id for rounds 1-3. Handle its status:
   - `NEEDS_CONTEXT`: answer and resume it.
   - `BLOCKED`: resolve it. If the choice is consequential under root `CLAUDE.md`, consult the user.
3. **Task reviewer.** Dispatch on the standard tier, read-only, with `${CLAUDE_SKILL_DIR}/references/task-reviewer-prompt.md`: BASE, the brief, and the implementer's report.
4. **Fix loop.** Run it when an Example or criterion is unmet, or any finding is Critical, High or Medium. Low findings go to the impl plan's `## Deferred` list and never to a fix round. Each round is one fix plus one scoped re-review (standard tier, the re-review variant in the reviewer prompt) of the fix's diff:
   - Rounds 1-3: resume the same implementer with the open findings (in Claude Code, `SendMessage` to its agent id).
   - Rounds 4-5: dispatch a fresh implementer on the strongest tier with the brief, the prior report and the open findings.
   - The implementer may push back with evidence under `${CLAUDE_SKILL_DIR}/references/review-feedback.md`. The next re-reviewer judges the pushback. A disputed finding still uses up a round.
5. **After round 5.** Rule on each open finding, applying `review-feedback.md`:
   - Reviewer wrong or point contestable: park it with the reason.
   - Real but not blocking: defer it.
   - Unmet Example or criterion, or anything consequential: take it to the user. The task is not done.

   Record each ruling under `## Rulings` as `Ruling: <decision> — <why> — <cost if wrong>`. Parked and deferred findings do not block done.
6. **Proof before done.** Rerun the task's targeted tests yourself and read the output. Check scope with `git diff --stat "$BASE"`. Rely on the reviewer's coverage rows for the Examples. Record the result in the impl plan. The full suite runs at the final review (§7).
7. **Commit pause** as in SKILL.md. After the user confirms, also check that `git status --short` shows no uncommitted changes in the task's files.

## Rules

- Never edit code in this mode, including fixes. Fixes go through implementers.
- Pause only for commit pauses, consequential decisions, and blockers you cannot resolve. Do not ask "should I continue?".
- Never dispatch two implementers at once.
- If no subagent tool is available, say so once and switch to inline for the rest of the run. Record `Execution mode: inline (no subagent tool)` in the impl plan header.
