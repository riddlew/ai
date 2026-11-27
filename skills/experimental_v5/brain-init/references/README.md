# Brain experimental_v5

Brain v5 is opt-in and independent of `experimental_v4`. The selected project's `CLAUDE.local.md` contains `Brain workflow version: experimental_v5`. Do not silently switch a v4 project or rewrite existing historical document metadata.

## Workflow

**Default:** `/brain-brainstorm` (when needed) → `/brain-implement`. A direct `/brain-implement` also works. Specs, plans, tasks, `execution.md`, and `handoff.md` are optional and **never prerequisites**. The user may invoke `/brain-update` once before implementation and once after, but no skill automatically invokes it. No document approval states or mandatory per-increment approval.

Inline execution is default; subagents are opt-in. Preserve AI-led, developer-led and Learning Mode pair programming. Use risk-based verification and stop at requested scope. Only the user decides consequential unresolved behavior and architecture.

## Skills (22 Brain skills and write-human)

| Purpose | Skills |
|---|---|
| Core | brain-brainstorm, brain-implement, brain-pair-program |
| Optional planning | brain-write-spec, brain-design-implementation, brain-decompose-feature, brain-write-tasks, brain-plan |
| Brain knowledge | brain-init, brain-update (manual), brain-compact (manual), brain-next |
| Quality and review | brain-diagnose, brain-review-code, brain-review-architecture, brain-review-security, brain-review-merge-request, brain-test-skill |
| Other workflows | brain-distill-content, brain-explain-changes, brain-refine-backlog, brain-retro, write-human |

Review actual source before relying on older Brain knowledge. Preserve `.brain/.notes/` privacy. One authoritative source per decision; handoffs and execution records reference it. Explicit focused amendments supersede only named anchors; conflicting amendments are errors.

See [USAGE.md](USAGE.md), [feature-document-contract.md](feature-document-contract.md), and [deterministic-tooling.md](deterministic-tooling.md).
