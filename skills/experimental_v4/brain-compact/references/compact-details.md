# Preview-first compaction procedure

The shared policy, `compact-writing.md` and feature-document contract govern. Minimize words **only if information and authority remain equivalent**.

## Procedure

1. Select a single file by default, or one feature-sized batch for explicit wide scope. Never access `.brain/.notes/`.
2. Identify owner, status, current text, traceability, authoritative parents and potential affected children. Preserve original content for a before/after comparison; preview only.
3. Show a readable diff plus a preservation checklist: actor, date, work ID, exact choice/waiver, reason when given, consequential exceptions, source/version, accepted scope, statuses, approval, commands and observed outcomes, review base, blockers and **distinct** historical events. Do not eliminate information solely because two tests look alike.
4. Obtain explicit approval of that diff. If proposed wording changes the spec or approved binding meaning, stop for the producing skill's substantive revision process instead.
5. Invoke only the producing skill to apply the reviewed, documentation-only changes. For an unavailable Skill tool, provide the exact `/owner` command and the approved excerpt/diff, and stop. Do not edit on an owner's behalf.
6. Verify the resulting file, parent hashes and impacted child fingerprints with owners. **Formatting-only** changes to an approved parent still change its Git-blob fingerprint and can block approved children. Ask the child owner to review; do not silently update `parent_hashes` or approvals. Validation passes only after required reconciliations.
7. Report applied versus merely proposed changes, real checks and remaining dependencies; do not report invented token savings or validation.

## Example: execution ruling

**Before:**
`- Ruling(user, 2026-11-20): PLAN-001's stale runner wording (\`compose down\`, old helper names, moved line anchors) is ignored: "ignore". \`brain-design-implementation\` is not asked to refresh it. INC-7 is built from this record's 2026-11-20 second refresh and the current \`run.sh\`, not the plan's line numbers.`

**Preview:**
`- **2026-11-20 · user · INC-7:** Decision: "ignore" stale PLAN-001 runner notes (\`compose down\`, old helpers, moved line refs); no design-plan refresh requested. Basis: this record's second 2026-11-20 refresh + current \`run.sh\` (not PLAN-001 line refs).`

This retains decision, actor, date, scope, rejected stale notes, no plan refresh, and current implementation basis. **If PLAN-001 contains binding technical constraints**, don't declare them irrelevant: route that conflict to `brain-design-implementation` for approval.

## Producer routing

| File | Owner |
|---|---|
| `01-brief/` | `brain-brainstorm` |
| `02-specifications/` | `brain-write-spec` |
| `03-components/` | `brain-decompose-feature` |
| `04-implementation-plans/` | `brain-design-implementation` |
| `05-tasks/` | `brain-write-tasks` |
| `features/<feature>/execution.md` | `brain-implement`, documentation-only |
| Root docs, `adrs/`, `sources/`, `knowledge/` | `brain-update` |
| `planning/` and reviews/diagnoses | Their respective producing skill |

A denied Brain write or absent owner invocation is a **blocker**, not permission to use a shell workaround. Preserve approved semantics, editor authority, and user checkpoints.
