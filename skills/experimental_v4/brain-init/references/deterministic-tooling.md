# Deterministic Brain tooling

Use the bundled CLI for mechanical operations; AI still owns project facts, requirements, design, semantic coverage, approvals and reviews. This reference applies to experimental_v4 Brain skills.

Run `sh "${CLAUDE_SKILL_DIR}/../brain-init/scripts/brain-tool"` from sibling skills or `sh "${CLAUDE_SKILL_DIR}/scripts/brain-tool"` from brain-init. The launcher prefers Python 3, then Node.js, then POSIX shell and awk. Set `BRAIN_RUNTIME=python|node|sh` to override. Python uses only its standard library, Node only built-ins, and shell only POSIX utilities; Git is required for Git operations and fingerprints. No pip/npm packages or network are used.

All writes preview by default. After confirming the Brain path and **authorized** write scope, use `--apply --authorized-root PATH`. The root must actually cover every destination; don't choose a broad ancestor just to defeat workspace restrictions. For separate external Brain and repository locations, or an existing customized policy/index that cannot be automatically reconciled, use the skill's existing narrower safe operations or ask the user. Never bypass denied writes with another runtime or tool.

| Family | Deterministic operation |
|---|---|
| `init` | `init --repo <repo> --brain <brain> --tracking ignored|tracked`; create index, install bundled guides and absent policy; preserve conflicting files |
| `doc` | `doc new --brain <brain> --feature <slug> --kind brief|specification|component|plan|task --slug <slug> [--parent ID]`; stable IDs, canonical metadata, draft status |
| `doc` | `--kind execution|planning-index|planning-ticket|diagnosis|review`; optional record; review requires `--report-type architecture|code|merge-request|security` |
| `validate` | `validate --brain <brain> [--check-coverage]`, `--affected ID`, or `--show-parent-hashes <file>`; reports only, no writes |
| `git` | `git --repo <repo> [--since SHA]` lists changes; `git --brain <brain> --pending --branch <branch> --at YYYY-MM-DD` creates an empty pending scaffold, not branch facts |
| `record` | `record --brain <brain> --feature <slug> --event <slug> --detail <one-line fact>` appends a unique factual execution checkpoint |
| `context` | `context --brain <brain> [--branch <branch>] [--feature <slug>]` lists document paths, byte sizes and statuses; it is not a semantic summary |

Guardrails: preview before applying; never overwrite existing user content or silently assign approvals; never update approved child hashes simply because a parent changed; do not generate unrequested feature stages. Branch-only changes remain provisional in `pending/<branch>.md` pending verification on main. The CLI does not apply semantic pending entries, write root project facts, infer completion, or decide whether a design is valid.

The existing `validate_feature_docs.py` remains available for compatibility. The CLI is exercised with identical fixtures under Python, Node and shell; report unsupported formats rather than silently weakening validation. `context` does **not** replace the policy's mandatory root read until a separately approved quality and token-usage assessment.

Implementations: `brain-init/scripts/brain-tool`, `brain-tool.py`, `brain-tool.mjs`, `brain-tool.sh`, `brain-tool-scan.awk`, `brain-tool-validate.awk`, and `scaffolds/`. Tests: `tests/test_deterministic_tool_contract.py`.
