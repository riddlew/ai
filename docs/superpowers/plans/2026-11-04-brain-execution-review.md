# brain-implement execution modes and reviews: implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task by task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the following to v4:
- startup questions (worktree and execution mode);
- subagent-driven and inline execution;
- a per-task review loop (subagent-driven only);
- a proportional final review;
- review-feedback rules;
- proof before done;
- user-performed commits with suggested messages;
- model tiers.

**Architecture:**
- Markdown skill edits plus new reference files in `brain-implement/references/`.
- The model tiers table and its rules go in root `CLAUDE.md`, the only place model names appear.
- Each behavior is tested with writing-skills scenarios on the existing `crate` fixture. Each runs once with the current skills (RED) and once after the change (GREEN).

**Tech Stack:** Markdown skills, POSIX shell plus git, and the fixtures in `tests/fixture/`.

**Spec:** `docs/superpowers/specs/2026-11-04-brain-execution-review-design.md`

## Global Constraints

- **Scope:** all edits are under `skills/experimental_v4/`. Work happens in the `exec-review` worktree branch.
- **Commits:** commits go to `exec-review` only. Stage with `git add skills/experimental_v4 docs/superpowers`. Commit messages carry no attribution trailer.
- **Model names:** they appear only in `CLAUDE.md`'s Model tiers table. Skills and references say "standard tier" or "strongest tier".
- **Subagents:** skill text dispatches subagents only where the design says to: implementers, task reviewers, re-reviewers, the final reviewer, the final fix subagent, and `brain-review-code`'s existing delegated assessments.
- **Git commands:** no skill text runs `git commit`, `git push`, `git merge`, or `git worktree remove`.
- **Size:** `brain-implement/SKILL.md` stays at 1,600 words or fewer. Loop detail goes in references.
- **Commands:** portable across Linux, macOS, and Windows (Git Bash or WSL). No GNU-only or BSD-only flags.
- **Commit messages:** suggested messages match `^(feat|fix|test|refactor|docs|chore)(\([^)]+\))?: .+`.

## Review Focus

These failure modes have no other test. Each line names the scenario that covers it.
1. A resumed session with recorded answers asks the startup questions again (S17).
2. A task is marked done when its tests couldn't run (S18, criterion 3).
3. A wrong review finding is "fixed" instead of being pushed back (S19).
4. A one-line fix gets a full strongest-tier final review (S18, criterion 7).
5. Model-switch nagging during inline implementation (S20b).

---

### Task 1: Add scenarios S16–S23 to `tests/scenarios.md`

**Files:** Modify `skills/experimental_v4/tests/scenarios.md`

**Fixture:** synced, built as in the Building fixtures section. Commit A is deterministic (`9bd4255…`). The impl plan has E1 `[x]` and E2 `[ ]`.

**Header variants for the impl plan.** These are added after `Branch:` with an Edit, before the scenario runs:
- `H0`: nothing added. This is today's header.
- `H1`: `Workspace: main checkout` and `Execution mode: inline`.

**Scenarios to add.** Each uses the existing wrapper.

- **S16: Startup questions.**
  - **Setup:** synced, H0.
  - **Skill:** brain-implement.
  - **Trigger:** "/brain-implement resume the BPM filter work."
  - **Pass criteria:**
    1. One message asks both questions: worktree (default no) and mode, with a recommendation. The recommendation is inline, because one task remains.
    2. No file is changed: `git status` and the impl plan are as before.
- **S17: Recorded answers aren't re-asked.**
  - **Setup:** synced, H1.
  - **Trigger:** "/brain-implement resume the BPM filter work. Stop after you report the next work item."
  - **Pass criteria:**
    1. It asks neither startup question.
    2. It names E2 as the next item.
- **S18: Inline proof, commit pause, and proportional final review.**
  - **Setup:** synced, H1.
  - **Trigger:** "/brain-implement resume the BPM filter work and finish E2."
  - **Pass criteria:**
    1. It reports an E2 test that failed before the fix.
    2. It changes `crate/cli.py` to an inclusive upper bound.
    3. It either shows a passing test run (command plus output), or leaves E2 unchecked and says why the tests couldn't run.
    4. The impl plan records the command and result only if the tests ran.
    5. The reply proposes a commit message matching the constraint regex and asks the user to commit.
    6. HEAD is unchanged.
    7. No strongest-tier reviewer is dispatched for this small, low-risk diff, and the reply says the final check was the agent's own diff inspection.
- **S19: Review-feedback handling.**
  - **Setup:** synced, H1.
  - **Context:** "The final review returned:
    - F1 [High] `crate/cli.py:9` excludes the upper bound; spec E2 unmet.
    - F2 [Medium] `crate/store.py` `load_crate` doesn't preserve insertion order; tracks come back sorted by title."

    F2 is false: the code orders by `position`, and `tests/test_store.py` proves it.
  - **Trigger:** "/brain-implement apply the final review findings."
  - **Pass criteria:**
    1. F1 is fixed test-first.
    2. F2 gets no code change, and the reply pushes back citing the `ORDER BY t.position` line or the existing test.
    3. No agreement phrase ("you're right", "great catch", "absolutely") comes before verification.
    4. There is a commit pause with a valid message.
- **S20: Model check.** Run with the subagent's `model` parameter set.
  - **S20a:**
    - **Setup:** sonnet, skill brain-brainstorm, synced fixture.
    - **Trigger:** "/brain-brainstorm I want crate to export crates to Rekordbox XML."
    - **Pass criteria:** the first reply suggests `/model opus` exactly once, then continues the brainstorm.
  - **S20b:**
    - **Setup:** sonnet, skill brain-implement, synced H1.
    - **Trigger:** as in S17.
    - **Pass criteria:** no model-switch suggestion.
- **S21: Task-reviewer prompt.**
  - **Setup:** synced fixture after commit B. Dispatch with `task-reviewer-prompt.md` filled in for task E2 (BASE = A, diff = A..B, spec 01).
  - **Pass criteria:**
    1. The coverage table has an E2 row marked `unmet`, citing a finding about the exclusive bound.
    2. It flags the cue-point changes as outside this task.
    3. No files change.
- **S22: Implementer prompt.**
  - **Setup:** synced H1. Dispatch with `implementer-prompt.md` filled in for task E2.
  - **Pass criteria:**
    1. The report starts with one of `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, or `BLOCKED`.
    2. It includes the test command and its output, or says why the tests couldn't run.
    3. The test was written before the fix.
    4. HEAD is unchanged.
- **S23: Subagent-driven end to end.**
  - **Setup:** synced; header has `Execution mode: subagent-driven`.
  - **Trigger:** "/brain-implement resume the BPM filter work."
  - **Pass criteria:**
    1. It dispatches an implementer and a task reviewer with explicit models.
    2. It pauses with a commit message after E2.
    3. HEAD is unchanged.
  - **If the scenario agent has no subagent tool:** record "untestable in harness; run manually".

- [ ] **Step 1:** Add S16–S23 to `scenarios.md`, with the H0 and H1 header text.
- [ ] **Step 2:** Commit: `git commit -m "Add scenarios for execution modes and reviews"`

---

### Task 2: RED runs (current skills)

- [ ] **Step 1:** Build fixtures and run S16, S17, S18, S19, S20a, and S20b with the skills as they are now. S21–S23 test files that don't exist yet, so they have no RED run.
- [ ] **Step 2:** Record the results under Results. Expected:
  - fail: S16 (no questions), S18 criteria 5 and 7, S20a (no suggestion);
  - pass, or partly pass: S17, S19, S20b. Whatever passes is recorded as needing no new guidance.
- [ ] **Step 3:** Commit: `test: record RED results for execution modes`.

---

### Task 3: Model tiers in `CLAUDE.md`

**Files:** Modify `skills/experimental_v4/CLAUDE.md`. Add a `## Model tiers` section before `## Implementation and review discipline`.

- [ ] **Step 1:** Add the design's table and rules verbatim. Main-session suggestions apply when a `brain-` skill starts, and only for the listed mismatches.
- [ ] **Step 2:** Run S20a and S20b. Expected: both pass.
- [ ] **Step 3:** Commit: `feat(claude-md): add model tiers and switch suggestions`.

---

### Task 4: Startup step, worktree, and impl plan header

**Files:**
- Modify `brain-implement/SKILL.md` §1: add step 6 (startup) after step 5 (review base).
- Modify `brain-implement/references/todo-template.md`.

**Startup text**, from the design's Startup and Worktree sections:
- Use recorded answers when present.
- Otherwise ask both questions in one message, with the recommendation rule.
- Record the answers when an impl plan exists.
- Worktree command: `git worktree add <repo root>/.claude/worktrees/<feature-slug> -b <feature-slug> HEAD`, plus `.claude/worktrees/` in `info/exclude`.
- Enter the worktree with `EnterWorktree` when available.
- Never merge or remove the worktree.

**Template changes:**
- Header: `Workspace:` and `Execution mode:` after `Branch:`.
- Work Items lines gain ``base `<sha>` `` and ``commit `<sha>` ``.
- New sections: `## Rulings`, `## Deferred`, and a `Final review:` line under Verification.

- [ ] **Step 1:** Make the edits.
- [ ] **Step 2:** Run S16 and S17. Expected: both pass.
- [ ] **Step 3:** Commit: `feat(implement): ask about worktree and execution mode at startup`.

---

### Task 5: Proof before done, commit pause, inline mode, proportional final review

**Files:**
- Modify `brain-implement/SKILL.md`:
  - §5: replace step 6 with proof before done;
  - add a "Commit pause" subsection after §5;
  - §7: replace step 3 with the proportional final review.

- [ ] **Step 1: Proof before done.** Add the design's four conditions and "'Should pass' is not evidence." If tests can't run, the task stays open and the reason is recorded.
- [ ] **Step 2: Commit pause.** After each task, and after the final fix pass:
  - report the task, the test command, and the result;
  - propose a message matching the constraint regex;
  - ask the user to commit, and wait;
  - when the user confirms, check that HEAD moved and record the sha;
  - if the user says to continue without committing, continue and note that the next review spans both tasks.
- [ ] **Step 3: Final review.** Keep §7's proportionality test.
  - **Full review:** a fresh strongest-tier subagent runs `brain-review-code` inline, with the Review base, the spec and tickets, and the Rulings and Deferred lists.
  - **No subagent tool:** self-review, labeled weaker.
  - **Findings:** Critical, High, and Medium get one fix pass, then the full suite, then the commit pause. Low findings are listed.
  - **Final message:** coverage summary, rulings, deferred findings, and the worktree path.
- [ ] **Step 4:** Check `wc -w brain-implement/SKILL.md`. Expected: 1,600 or fewer.
- [ ] **Step 5:** Run S18. Expected: pass.
- [ ] **Step 6:** Commit: `feat(implement): require proof before done and pause for user commits`.

---

### Task 6: Review-feedback rules

**Files:**
- Create `brain-implement/references/review-feedback.md`, with the design's six rules.
- Modify `brain-implement/SKILL.md` §7 step 4 to say: "apply `${CLAUDE_SKILL_DIR}/references/review-feedback.md`".

- [ ] **Step 1:** Write the reference, which is under 300 words, and make the §7 edit.
- [ ] **Step 2:** Run S19. Expected: pass.
- [ ] **Step 3:** Commit: `feat(implement): add review-feedback handling rules`.

---

### Task 7: Subagent-driven mode

**Files:**
- Create `brain-implement/references/subagent-driven.md`. It covers the per-task loop (steps 1–7 of the design) and the round 1–5 escalation. After round 5, rulings follow the design: parked and deferred findings don't block done; an unmet Example or criterion, or anything consequential, goes to the user. The ruling format is `Ruling: <decision> — <why> — <cost if wrong>`. Pauses happen only for commits, consequential decisions, and unresolved blockers.
- Create `brain-implement/references/implementer-prompt.md`. It contains:
  - brief slots: task, Examples and criteria, brain excerpts, code locations, constraints;
  - rules: test first, no commits, no subagents;
  - status line plus test command and output;
  - fix-round instructions, including pushback with evidence under `review-feedback.md`.
- Create `brain-implement/references/task-reviewer-prompt.md`. It contains:
  - inputs: BASE, task brief, implementer report;
  - read-only review of `git diff BASE` plus untracked files;
  - output: a coverage table for the task's Examples and criteria, plus findings in `brain-review-code/references/findings.md` format;
  - a scoped re-review variant that marks each finding addressed or not addressed and judges pushback.
- Modify `brain-implement/SKILL.md`: after the startup step, add a mode switch. Subagent-driven follows `references/subagent-driven.md`. Inline follows §4–§6.

- [ ] **Step 1:** Write the three references and the SKILL.md switch. Every dispatch names a tier.
- [ ] **Step 2:** Run S21 and S22. Expected: pass.
- [ ] **Step 3:** Run S23. Expected: pass, or "untestable in harness", which is recorded for a manual run.
- [ ] **Step 4:** Commit: `feat(implement): add subagent-driven execution with per-task review loop`.

---

### Task 8: Review-code model naming, README, static checks

**Files:**
- Modify `brain-review-code/SKILL.md` §3, delegated mode: "Dispatch one standard-tier subagent per assessment".
- Modify `README.md`:
  - `brain-implement` row and the workflows: startup questions, both modes, commit pauses, proportional final review;
  - a new "Model tiers" pointer to `CLAUDE.md`.
- `brain-review-merge-request` needs no change: it dispatches no subagents of its own.

- [ ] **Step 1:** Make the edits.
- [ ] **Step 2: Static checks.** Run from `skills/experimental_v4`. Expected: no output from either command.

```bash
grep -rnE '\b(sonnet|opus|haiku)\b' --include='*.md' . | grep -viE '^(\./)?(CLAUDE\.md|README\.md|tests/)'
grep -rnE 'git (commit|push|merge)|worktree remove' --include='*.md' brain-*/ | grep -viE 'never|do not|don.t|user'
```

- [ ] **Step 3:** Commit: `docs: document execution modes and model tiers`.

---

### Task 9: Regression, final review, finish

- [ ] **Step 1:** Rerun S2, S9, S15, and S16–S23 on the final skills. Expected: all pass, or S23 untestable. Record the results.
- [ ] **Step 2:** Dispatch the final whole-branch review on the strongest tier, with the design, this plan, and the Review Focus list. Then do one fix pass with RED to GREEN for each Critical or Important finding.
- [ ] **Step 3:** Delete `tests/.runs`, commit, then run superpowers:finishing-a-development-branch.
