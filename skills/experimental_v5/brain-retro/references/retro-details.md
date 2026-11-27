# Brain retro — evidence and reporting guide

This reference is conditional; load for a complex retrospective or when assessing whether a suggestion is warranted. `brain-retro` is **manual and read-only**. A session is not a problem merely because it was long, a code review had findings, or a user revised a design.

## Sources: use the narrowest useful evidence

- Start with the user's observed friction and the relevant currently visible session context. Check whether an existing `.brain/features/<slug>/execution.md` actually records repeated failed checks, stalled approvals, design revisions or expensive context recovery.
- Inspect relevant Git/diffs, observed tool errors and review findings when those clarify whether a process problem repeated. Read the particular skill/policy passage that might have caused it before suggesting a rule change.
- Never imply access to past chat transcripts, model internal reasoning, unrecorded subagent actions, token accounting or timings. An absent record means `unverified`, not that the event did not occur. Ask for a concrete excerpt if essential; otherwise state the limit.
- Respect `CLAUDE.local.md`'s `.brain/.notes/` exclusion and bounded project-context rules. Review evidence only; do not execute code or change files.

## Distinguish types of problem

| Finding | Appropriate outcome |
|---|---|
| Project architecture or code fact missing from shared knowledge | Suggest `/brain-update` with the specific missing fact; retro does **not** synchronize it |
| Approved requirement not found or contradictory | Identify the governing document and owning skill; no silent rewrite or approval |
| Skill instructions caused repeated, avoidable wrong steps | Suggest the narrowest wording/decision-rule change plus a regression/behavior test |
| Same preventable bug repeatedly escaped tests | Suggest a focused automated check without turning retro into code review |
| Large review used subagents despite missing opt-in | Report the actual execution mode evidence and check current policy before proposing changes |
| Single ordinary defect, no structural cause | No process change needed |

Favor mechanisms that plausibly prevent recurrence, not additional documents or mandatory stages. Distinguish one costly, clearly preventable event from unsupported speculation. Check whether the proposed rule already exists and was merely ignored.

## Compact output (max 3)

`**Scope:** <feature/session/PR and evidence inspected>`

`**Observed friction:** <specific repetition or avoidable cost, with reference>`

`1. **Change:** <named skill/file/check and precise adjustment>`
`   - **Why:** <observed evidence; root-cause hypothesis and confidence>`
`   - **Expected benefit / validation:** <what improves; observable future test>`
`   - **Tradeoff:** <only if material>`

`**Limits:** <missing session logs/metrics or other uncertainty>`

If the evidence does not justify a durable improvement, write `No justified workflow change` with a short reason. Do not force three findings or a follow-up recommendation. Any suggested owner action is **optional and must be explicitly requested** before execution; never run it as part of the retrospective.
