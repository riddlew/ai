# Optional subagent execution (v5)

This reference applies **only with explicit user opt-in to subagents**; default inline is sufficient for every Brain skill. Before delegation, inspect Git/worktree state and current requirements, preserve user edits and select narrowly bounded tasks with dependencies. Give each agent authorized files/ownership, code and test references, applicable decisions and verification requirements.

The coordinator should inspect returned files, actual diffs and test results. Do not treat subagent claims as verification. Parallelize only safely independent work; avoid duplicate context and needless extra reviews. No mandatory builder/final multi-agent approval ceremony. Material unresolved architecture or behavior goes to user consultation; no automatic `brain-update`.

If subagent tooling is unavailable, report the limitation and continue inline only when the user has not prohibited it. Never infer delegation authority from task size.
