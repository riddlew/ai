# Compact writing rules for Brain Markdown

All Brain document producers use this standard for **new** content and the passages they revise. The separate, user-invoked `brain-compact` skill previews changes to **existing** records. Reducing word count is secondary to accuracy.

- **Write atomic, information-dense statements.** Prefer `decision → effect → basis` to narrating a conversation. Use concise bullets for isolated events, tables for repeated fields, and clear headings when needed. Avoid filler, duplicate background and cryptic shorthand.
- **Use grounded references, not copied context.** Reuse stable IDs, `SPEC-ID#REQ-ID` and source/ADR links to avoid repetition, but keep normative requirements, acceptance examples, binding constraints and exclusions **self-contained** where necessary. Don't replace an essential rule with only a reference.
- **Preserve all relevant facts.** Keep actor, date, scope, explicit wording of decisions/rulings, supplied rationale or risks, approval, status, dependencies, negative constraints, provenance/versions, commands and **actual results with revision**. Keep unresolved uncertainty visible. Never silently merge different events, erase checkpoints, or turn a reported outcome into a verified test.
- **Record deltas, not repeated histories.** Put each decision and verification in its owning document. Later updates can cite the earlier entry if its evidence remains accessible and complete; avoid repeating whole sessions. A linked summary is not authority to discard unique evidence.
- **No arbitrary word or token limits.** Longer text is justified for an exact protocol, failure path, API contract, or consequential rationale. Do not trade clarity for abbreviations.
- **Keep approval structure stable.** Preserve `id`, `status`, `parents`, `requirements`, `depends_on` and valid `parent_hashes`. A stylistic edit to an approved parent changes its Git-blob hash and may require child-owner review. `execution.md` records facts; it does not override a binding plan. Never silently update approval or fingerprints.

## Compact examples

**Ruling and basis:**
`- **2026-11-20 · user · INC-7:** Decision: "ignore" stale PLAN-001 runner notes (\`compose down\`, old helpers/line refs); no plan refresh requested. Basis: second 2026-11-20 execution refresh + current \`run.sh\` (not PLAN-001 line refs).`

Check whether ignored text is illustrative. If it is binding plan content, seek `brain-design-implementation` approval instead of editing away the conflict.

**Requirement and example:**
`- REQ-004: Unknown YAML fields produce warnings; exit 0 if no other error.`
`- E3: Given one unknown YAML field, running the CLI reports that key on stderr and exits 0.`

**Verified increment:**
`- **INC-7 · 2026-11-20 · verified, awaiting user review:** \`test_yaml_warning.py -q\` PASS at `<revision>` (E3).`

Never merge independent later test runs or approvals into this checkpoint.
