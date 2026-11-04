# Design: Execution modes and reviews for `brain-implement` (experimental_v4, project 1 of 5)

## Intent

Give `brain-implement` the execution discipline superpowers has:
- an independent review after each task, with a bounded fix loop;
- a final review in a fresh context on the strongest model, for any change that isn't small and low-risk;
- explicit rules for handling review feedback;
- proof before any task is called done;
- a model tier for each role;
- an optional git worktree.

The user keeps control of commits. The skill proposes a Conventional Commits message after each task, and the user commits.

The other four projects are separate: spec and ticket review, debugging techniques, a skill-testing skill, and browser mockups.

## Current state (v4)

- **`brain-implement`:**
  - It implements inline, in test-first increments.
  - It tracks progress in `.brain/impl_plans/<feature>.md`, which records a `Review base`.
  - §7 runs `brain-review-code` only for substantial or consequential changes, in the same session.
  - It invokes `brain-update` on completion, and at session end unless nothing has changed since.
  - It never commits.
- **`brain-review-code`:** produces Correctness, Requirement fit (with a coverage table), and Repository fit. It delegates to subagents for large diffs.
- **Root `CLAUDE.md`:** requires consulting the user before consequential choices.
- **Subagents:** v4 skills avoid them unless the user specifies them. The user has specified them for the implementers and reviewers in this design.

## Goals

1. **Two startup questions, on every run.** Before the first change, `brain-implement` asks whether to use a git worktree and which execution mode to use, unless the impl plan already records the answers. Untracked work has no impl plan, so it asks on every run.
2. **Subagent-driven mode:**
   - A fresh implementer subagent builds each task, and a fresh reviewer checks it.
   - Failed reviews go through a fix loop of up to 5 rounds, escalating to a stronger model in rounds 4–5.
   - After round 5, the main session rules on whatever is still open.
   - All tasks run in one session, pausing only for the user's commits and for decisions that need the user.
3. **Inline mode:** the main session implements each task itself. There is no per-task reviewer.
4. **Final review in both modes, proportional to the change.**
   - **Substantial or consequential changes:** reviewed in a fresh context on the strongest model. When that is impossible, the review falls back to a self-review labeled as weaker.
   - **Small, low-risk changes, such as a one-line fix:** keep today's own diff inspection and checks.
   - **A small diff with material consequences:** still gets the full review.
5. **Review feedback handling:** each finding is checked before anything is changed, wrong findings are pushed back with evidence, and the skill never agrees just to please.
6. **Proof before done:** a task is done only after its tests ran and passed in this session and a self-review of the task passed.
7. **Model tiers:** each role gets a tier. When the session model is a poor fit for the work, the skill says so once and suggests switching.
8. **Commits:** after each task, and after the final fix pass, the skill proposes a Conventional Commits message, asks the user to commit, and waits.

## Non-goals

- No reviewer after each task in inline mode.
- The skill never runs `git commit`, `git push`, `git merge`, or worktree removal.
- No autonomous rulings on consequential choices. The `CLAUDE.md` consultation rules still apply, including after the fix loop.
- No tier below Sonnet. Only Sonnet and Opus are available to the user.
- Projects 2–5.

## Startup (new step in `brain-implement` §1, before the first change)

1. If the impl plan header already records `Workspace:` and `Execution mode:`, use those values. A resumed session never asks again. Untracked work has no impl plan, so ask on every run.
2. Otherwise, ask both questions in one message:
   - **Worktree:** "Work in a git worktree for this feature?" The default is no.
   - **Execution mode:** "Subagent-driven or inline?", with a one-sentence recommendation:
     - recommend **subagent-driven** when there are several tasks with few shared interfaces;
     - recommend **inline** for one or two tasks, for tightly coupled tasks, or for untracked work.
3. Record both answers in the impl plan header, when there is one.
4. Then run the model check (see Model tiers).

### Worktree

If the user chooses a worktree:
- Create it from the current `HEAD`, so unpushed work is included: `git worktree add <repo root>/.claude/worktrees/<feature-slug> -b <feature-slug> HEAD`.
- Work inside it. In Claude Code, enter it with `EnterWorktree` (path) when that tool is available.
- Make sure `.claude/worktrees/` is listed in the repository's `info/exclude`.
- An untracked `.brain` is still found in the main checkout, under the existing rule.
- At the end, report the worktree path and branch. Merging, opening a PR, and removing the worktree are the user's to do or request.

## Tasks

A task is one work item in the impl plan, which means one ticket when tickets exist. For untracked work, a task is one behavioral increment of the request, listed in the conversation.

**Commits are a gate between tasks.** The next task starts only after the user confirms the commit. If the user says to continue without committing, continue, and say in the report that the next task's review covers both tasks' changes.

The impl plan records the following for each task:
- the base sha (`HEAD` at task start);
- status;
- the commit sha once the user commits.

It also records `Ruling:` lines, `Deferred:` findings, and a `Final review:` line.

## Subagent-driven mode

For each task:

1. **Record the base.** `BASE = git rev-parse HEAD`.
2. **Dispatch the implementer** (standard tier). Its brief contains:
   - the task text;
   - the spec Examples and acceptance criteria it covers;
   - only the relevant brain excerpts and code locations;
   - the constraints.

   Its instructions:
   - work test-first;
   - do not commit;
   - do not dispatch subagents;
   - report one of `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, or `BLOCKED`, with the test command it ran and the output.

   The coordinator answers `NEEDS_CONTEXT` and resolves `BLOCKED`, consulting the user if the blocker is consequential.
3. **Dispatch the task reviewer** (standard tier, read-only):
   - Its input is the task diff: `git diff BASE` plus any untracked files.
   - It checks spec compliance against the task's Examples and acceptance criteria, with coverage rows like `brain-review-code`'s table, and checks quality.
   - It returns findings on the shared severity scale.
4. **Run the fix loop** when the review shows an unmet Example or criterion, or any Critical, High, or Medium finding. Low findings go to `Deferred:` and never enter the loop. The implementer may push back on a finding with evidence instead of fixing it. The next re-reviewer decides whether the pushback stands, and a disputed finding still uses up a round. Each round is one fix plus one scoped re-review (standard tier) of that fix's diff:
   - **Rounds 1–3:** resume the same implementer (`SendMessage`) with the open findings.
   - **Rounds 4–5:** dispatch a fresh implementer on the strongest tier, with the brief, the prior report, and the open findings.
5. **After round 5, if findings remain open**, the main session rules on each one, using the review-feedback rules:
   - **Reviewer wrong, or the point is contestable:** park it with the reason.
   - **Real but not blocking later tasks:** defer it.
   - **An Example or acceptance criterion still unmet, or anything consequential under `CLAUDE.md`:** take it to the user. The task can't honestly be called done.

   Every ruling goes into the impl plan as `Ruling: <decision> — <why> — <cost if wrong>`. Parked and deferred findings don't block "done".
6. **Prove it's done** (see Proof before done), then record it in the impl plan. The coordinator reruns the task's targeted tests itself, checks `git diff --stat BASE` for scope, and relies on the reviewer's coverage rows for the Examples. The full suite runs at the final review.
7. **Commit pause:** report "Task N done", the test command and result, and a proposed message such as `feat(filter): make the BPM upper bound inclusive`. Ask the user to commit, and wait. When the user says it's committed, check that `HEAD` moved and that the task's files are clean, record the commit sha, and continue.

The coordinator never edits code itself in this mode. It stops only for commit pauses, consequential decisions, and blockers it can't resolve.

## Inline mode

- The main session implements each task test-first, as §5 does today.
- There is no task reviewer.
- Proof before done and the commit pause apply as in subagent-driven mode.

## Final review (both modes, replaces §7 step 3)

The review stays proportional, using §7's existing test:
- **Small, low-risk changes, such as a one-line fix:** your own diff inspection and checks are enough.
- **Substantial or consequential changes:** get the full review below. Consequential means ownership, public contracts, persistence, security, or broad cross-component behavior. A small diff with material consequences counts.

The full review:

1. When every task is done, dispatch a fresh reviewer on the strongest tier that runs `brain-review-code` inline inside the subagent. Give it:
   - the impl plan's `Review base`;
   - the governing spec and tickets;
   - the impl plan's `Ruling:` and `Deferred:` lines, so it can weigh them.
2. If subagents are unavailable, run `brain-review-code` in the main session instead. Record and report `Final review: self-review (no fresh reviewer), weaker than an independent review`.
3. Apply the review-feedback rules to the findings:
   - **Critical, High, and Medium:** these enter one fix pass, with each fix done test-first and the full suite run afterward. In subagent-driven mode, one fix subagent on the strongest tier gets the complete list. In inline mode, the main session fixes them.
   - **Low:** listed for the user.

   There is no second review pass.
4. Run the commit pause for the fix pass, if it changed anything.
5. Send the final message:
   - the coverage summary;
   - every `Ruling:` line;
   - the deferred findings;
   - the worktree path and branch, if one was used.

   Then invoke `brain-update` as today.

## Handling review feedback (shared reference)

`brain-implement/references/review-feedback.md` is used by the main session (for inline fixes and rulings) and handed to implementers in fix rounds:

1. Read all findings before changing anything.
2. Verify each finding against the code and the spec.
3. Then act on it:
   - **Correct:** fix it.
   - **Wrong:** push back with evidence, such as file:line or test output.
   - **Unclear:** ask the reviewer, or ask the user if it is consequential.
4. Never agree just to please. Don't say "you're right" without having checked; state what changed or why not.
5. Before adding capability a reviewer suggested but no requirement asks for, check that something actually needs it (YAGNI).
6. Fix in severity order, and rerun the covering tests after each fix.

## Proof before done

A task is done only when all of the following are true in this session:
- its tests ran and passed, and the output was read;
- each Example and acceptance criterion it covers was compared against real output;
- a self-review of the task diff passed: in scope, no unrelated edits, no debug leftovers, consistent with the spec;
- the impl plan records the test command and its result.

"Should pass" is not evidence.

## Model tiers (root `CLAUDE.md`, the one place that names models)

| Role | Tier | Model today |
|---|---|---|
| Task implementer, task reviewer, scoped re-review | standard | Sonnet |
| Fix-round 4–5 implementer, final reviewer, final fix pass | strongest | Opus |
| Main session: brainstorming, writing specs, architecture review | strongest | Opus |
| Main session: coordinating subagent-driven mode | standard | Sonnet |
| `brain-review-code` delegated assessment subagents | standard | Sonnet |

**Rules** (in `CLAUDE.md`, so they apply to every `brain-` skill):
- Every subagent dispatch names its model explicitly.
- When a skill starts, suggest switching only on a clear mismatch, say so once, and continue either way:
  - Sonnet while brainstorming, writing a spec, or reviewing architecture → suggest `/model opus`.
  - Opus while coordinating subagent-driven mode → suggest `/model sonnet`.
- Inline implementation gets no suggestion, because task difficulty varies. The inline final fix pass runs on whatever the session model is.

## Files

- **`brain-implement/SKILL.md`:**
  - the startup step;
  - a mode switch pointing to the references;
  - proof before done;
  - the commit pause;
  - the final review replacing §7 step 3.
- **New files in `brain-implement/references/`:**
  - `subagent-driven.md` (the per-task loop and rulings);
  - `implementer-prompt.md`;
  - `task-reviewer-prompt.md`;
  - `review-feedback.md`.
- **`brain-implement/references/todo-template.md`:**
  - header fields `Workspace:` and `Execution mode:`;
  - per-task base and commit shas;
  - `Ruling:`, `Deferred:`, and `Final review:` lines.
- **`CLAUDE.md`:** a Model tiers section.
- **`README.md`:** the workflow and skills table.
- **`brain-review-code`:** its delegated assessment subagents name the standard tier. Its delegated mode already falls back to inline when subagents are unavailable, which is the case inside the final-review subagent.
- **`brain-review-merge-request`:** name the model for any subagent it dispatches.

## Testing

Use the writing-skills scenarios in `tests/scenarios.md`:
- startup questions are asked once and not again on resume;
- inline proof before done and the commit pause;
- review-feedback handling, with a planted wrong finding;
- the model-check message.

Scenario agents are themselves subagents and may not be able to dispatch subagents. So the full subagent-driven loop may need a real session the user runs. In that case, test the implementer and reviewer prompts separately on fixtures.

## Left to the builder

- Prompt wording.
- Exact impl plan line formats.
- The wording of the recommendation heuristic.
- How the content is split between `SKILL.md` and the references.
