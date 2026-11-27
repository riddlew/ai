# Deterministic Brain v5 tooling

Use `sh "${CLAUDE_SKILL_DIR}/../brain-init/scripts/brain-tool"` for deterministic operations; Python, Node and POSIX shell fallback are available. V5 tools scaffold **optional** documents without `status` or `parent_hashes` metadata, and validate IDs, actual references, amendment supersession and cycles, without approval gates. Existing v4 `status`/hashes are accepted as archival only.

- `init --brain ...`: install version-marked Brain policy, index and guides.
- `doc new --brain ... --feature ... --kind brief|specification|component|plan|task --slug ... [--parent ID]`: optional stage, no parent prerequisite.
- `doc new --kind execution|planning-index|planning-ticket|diagnosis|review`: optional auxiliary record.
- `validate --brain ... [--check-coverage]`: structural checks; `--affected ID` reports linked docs. Historical `--show-parent-hashes` is compatibility-only.
- `record ...`: append verified execution evidence when an execution record exists.
- `context ...`: optional discovery; a context list is not an exclusion list.
- `git ...`: Git inventory and branch pending entry.

Always preview writes, honor worktree scope and `.brain/.notes/`, preserve user data, and never treat scaffolding or validation as approval/authorization. No tool automatically calls `brain-update`.
