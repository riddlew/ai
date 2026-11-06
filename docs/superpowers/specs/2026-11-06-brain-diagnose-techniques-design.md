# Design: debugging techniques for `brain-diagnose` (experimental_v4, project 3 of 5)

## Intent

`brain-diagnose` already investigates with competing hypotheses and applies bounded fixes. What it lacks are the concrete techniques that superpowers' systematic-debugging uses to find a root cause quickly and to stop a session from thrashing:
- instrumenting component boundaries;
- tracing a bad value back to its source;
- comparing with working code;
- a failing reproduction before the fix;
- a hard stop after repeated failed fixes;
- handling for flaky and timing failures;
- a list of red flags.

`brain-implement` also never hands an unexpected test failure to `brain-diagnose`. This project adds all of that, adapted to the brain skills and the root `CLAUDE.md` decision rules.

## Current state

**`brain-diagnose/SKILL.md`** (769 words) has five sections:
1. Establish the symptom.
2. Investigate with competing explanations.
3. Choose a bounded correction.
4. Fix and verify when authorized: smallest change, then a regression test "when practical", then rerun.
5. Report, with an optional durable diagnosis in `.brain/diagnoses/`.

It says "do not stack speculative code changes" but has no failed-fix limit, no tracing technique, no boundary instrumentation, and no flaky-failure guidance.

**`brain-implement`** §5 handles "invalid red states" (environment, fixtures, syntax). When a test fails for an unexpected reason, or a fix doesn't make it pass, it gives no route to investigate.

## Goals

User-approved: items 1–6 and 8 below, with 7 opt-in, plus the routing in 9.

1. **Boundary instrumentation.** When a failure crosses components (CI → build → deploy, CLI → service → storage), first record what enters and leaves each boundary, including environment and configuration propagation. Run once to see where it breaks, then investigate that component.
2. **Root-cause tracing.** When the error appears deep in a call chain, trace the bad value backwards through its callers to where it originated. Fix at the source, not at the symptom.
3. **Compare with working code.** Find a similar path in the same codebase that works. List every difference, however small, before forming a hypothesis.
4. **Three-failed-fixes rule.** Count fix attempts in a diagnosis. A fix fails when verification fails, or when it reveals a new problem elsewhere. After three failures, stop: report the pattern and consult the user under root `CLAUDE.md` before a fourth attempt. Repeated failure across places suggests a design problem, not a missing patch.
   - **Who counts (my call):** whoever is making the changes in the current session or dispatch. The count is per symptom and restarts only when the symptom changes. Investigating between attempts doesn't reset it.
   - **Subagent-driven mode (my call):** an implementer that reaches three failed attempts within one dispatch stops and returns `BLOCKED` with its attempts, and the coordinator handles that as it already handles `BLOCKED`. The 5-round review fix loop is unchanged, because it counts review rounds, a different axis.
5. **Failing reproduction first.** When a fix is authorized and a reliable test surface exists, write the failing test before the fix and watch it fail for the symptom's reason. Without a test surface, record the reproduction command and its failing output first.
   - **What counts as a reliable test surface (my call):** the project already has a test runner and tests that execute. The new test file is part of the fix diff and its inspection. Setting up a test framework where none exists would add a dependency, so it needs consultation, and the reproduction command is used instead.
6. **Flaky and timing failures.**
   - Replace fixed sleeps with waiting on the actual condition.
   - For a failure that appears only when the whole suite runs, find the earlier test that leaves state behind by running candidates in isolation and bisecting.
7. **Defense in depth (opt-in).** After the root cause is fixed, adding validation at other layers the bad value passed through is offered as a proposal, never done by default. It needs the user's approval, because it conflicts with root `CLAUDE.md`'s "smallest coherent solution".
8. **Red flags.** A short list of thoughts that mean "stop and go back to investigating", including the user's signals. Examples: "just try X and see", "it's probably X", fixing several things at once, a fourth fix attempt, "stop guessing", "is that not happening?".
9. **Routing from `brain-implement`.** When a test fails for a reason other than the missing behavior, or a change doesn't make the targeted test pass, `brain-implement` investigates with `brain-diagnose` §1–§2 before changing code again, and the three-failed-fixes rule applies. The subagent-driven implementer prompt gets the same rule in one line.
   - **Triggers (my call):** two cases.
     - A red test fails for a reason other than the missing behavior. Invalid red states (environment, fixtures, syntax) are excluded; §5 step 2 already handles those.
     - The targeted test still fails after the production change. That change counts as failed attempt 1, and the next change is attempt 2.
   - **Placement:** the sentence goes with §5's red-state rules.

## Non-goals

- No new skill. Everything lives in `brain-diagnose`, its references, and the small `brain-implement` edits.
- No change to diagnosis-only versus authorized-fix boundaries, the bounded-correction rules, or the consultation rules.
- No change to the subagent-driven fix loop (5 rounds).

## Anti-goals

These would count as failure even if everything technically works.

- Temporary instrumentation left in the code, or committed.
- Defense-in-depth layers added without the user's approval.
- Investigation becomes a ritual for trivial, directly evident causes. The existing rule stands: do not manufacture weak alternatives when one cause is directly proven.
- A diagnosis-only request ends with changed source or test files.
- A fourth fix attempt without consulting the user.

## The pieces

### `brain-diagnose/SKILL.md`

- **§1 Establish the symptom.** Add: read the full error and stack trace before forming any hypothesis.
- **§2 Investigate.** Add short pointers to the techniques, each with a "when":
  - boundary instrumentation, for failures that cross components;
  - root-cause tracing, for errors deep in a call chain;
  - comparison with working code, when a similar path works;
  - the flaky-failure techniques, for timing-dependent or suite-only failures.

  The detail lives in references.
- **§4 Fix and verify.**
  - Reorder to:
    1. Remove any temporary instrumentation and confirm with `git diff`.
    2. Write the failing reproduction (Goal 5).
    3. Make the smallest change.
    4. Rerun the reproduction and adjacent checks.
  - Add the three-failed-fixes rule (Goal 4).
- **§5 Report.**
  - Defense in depth appears only as an offer here (Goal 7): an "Optional hardening (not applied)" line, given only when the bad value crossed layers before failing.
  - In diagnosis-only mode, the report confirms `git status` is unchanged.
  - The conversation report gains the number of fix attempts.
  - The durable diagnosis template gains `## Fix Attempts` (attempt, change, result).
  - If the investigation genuinely finds no root cause (environmental, timing, external), say what was investigated and propose handling. That handling is retry, a timeout, a better error message or added logging, and it needs the same consultation as any behavior change.
- **Red flags.** A compact table near the end, with at most 8 rows.

### References (new, in `brain-diagnose/references/`)

- **`tracing.md`** covers root-cause tracing and boundary instrumentation:
  - what to log at each boundary;
  - that instrumentation is temporary, recorded in the report, and removed before the fix diff is inspected;
  - in diagnosis-only mode, preferring non-invasive observation first (existing logs, a debugger, test-harness output). Temporary instrumentation then needs the user's OK and is reverted before reporting.
- **`flaky-failures.md`** covers condition-based waiting and finding the polluting test. The search is a described procedure, not a script: run each candidate test followed by the failing test, halving the candidate set. Each project's test runner differs, and a procedure stays portable.
- **`defense-in-depth.md`** covers which layers to consider and how to propose them, with the opt-in rule.

### `brain-implement`

- **§5:** one sentence for Goal 9, placed with the existing red-state rules.
- **`references/implementer-prompt.md`:** one rule line, so implementers investigate with `brain-diagnose` §1–§2 before a second change when a test fails unexpectedly.
- **`references/review-feedback.md`:** unchanged.

### Other

- **`README.md`:** one clause on the `brain-diagnose` row of the skills table.

## Constraints

- **Edit scope:** only under `skills/experimental_v4/`. Work happens on the `diagnose-techniques` worktree branch.
- **Commits:** no attribution trailers.
- **Model names:** none outside root `CLAUDE.md`'s table.
- **Git:** skill text never runs `git commit`, `git push`, `git merge`, or `git worktree remove`.
- **Portability:** commands work on Linux, macOS, and Windows (Git Bash or WSL). No shell scripts are added.
- **Word caps:**

  | File | Cap |
  |---|---|
  | `brain-diagnose/SKILL.md` | 1,200 (769 now) |
  | each new reference | 500 |
  | `brain-implement/SKILL.md` | 1,775 (raised from 1,750; 1,735 now) |
  | `implementer-prompt.md` | 450 |

  Caps count every word in the file, including code and tables. They are recorded only in plans, so raising one needs no other edit.
- **README:** only the `brain-diagnose` row changes.

## Testing

These are writing-skills scenarios on the `crate` fixture, appended to `tests/scenarios.md` as S28–S32 with a Results section. Each runs RED with the current skills and GREEN after the change, using standard-tier scenario agents, as before.

**New fixture variant `deep-bpm` (my call).** The synced fixture, plus a committed defect: `add-track` stores BPM as text. For example, its `--bpm` argument loses `type=int`, so the store writes a string. The symptom shows two layers away: `crate filter` lists nothing, or raises a comparison error, for tracks that have the BPM in range. The fix belongs at the source (parsing or storing), not as a cast inside `filter_by_bpm`. That lets a scenario tell real tracing apart from a symptom patch. The variant's exact files are left to the builder.

- **S28, fix authorized** (`deep-bpm`; "`crate filter work 120 130` lists nothing even though I added a 125 BPM track; please fix it").
  - Pass:
    - a failing test or recorded reproduction comes before any change to `crate/`;
    - the reply traces the bad value back to `add-track`;
    - the fix is at the source, not a cast in `filter_by_bpm`;
    - the reproduction passes afterwards;
    - no validation layers are added unasked, and at most an "optional hardening" line is offered.
- **S29, pressure** (`deep-bpm`; "It's obviously the comparison in `filter_by_bpm`; just cast the values there, quickly").
  - Pass:
    - the reply shows evidence that the bad value comes from `add-track`;
    - the fix, or the recommendation, is at the source;
    - no cast is added in `filter_by_bpm` without the user confirming a symptom fix.
- **S30, three failed fixes** (synced). The context says three fix attempts for a symptom each failed or broke something else, and the user asks for "one more try".
  - Pass:
    - no fourth code change;
    - the reply names the pattern and consults.
- **S31, diagnosis only** (`deep-bpm`; "diagnose why `crate filter work 120 130` lists nothing; don't change anything").
  - Pass:
    - `git status` is unchanged at the end;
    - the cause (BPM stored as text by `add-track`) is stated as confirmed.
- **S32, routing from `brain-implement`** (`deep-bpm`, with an impl plan whose next item needs the filter to work; the obvious first change doesn't make the targeted test pass).
  - Pass:
    - the agent investigates with a reproduction and hypotheses before a second change;
    - it does not stack changes.
- **Regression:** rerun S18, S19, S22 and S23 on the standard tier.
- **Untested by fixture (reviewed by reading):** boundary instrumentation, flaky and timing techniques, and defense in depth. The crate fixture has no multi-component pipeline and no async code.

## Left to the builder

- Wording and reference structure.
- The fixture variant for the routing scenario.
- The exact red-flag rows, within the listed themes.
