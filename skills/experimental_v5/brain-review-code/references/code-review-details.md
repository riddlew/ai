# Scoped code review procedure (v5)

Default inline; subagents only on explicit opt-in. Determine true target branch/merge base, head and actual staged, unstaged and relevant untracked changes. Read authoritative requirements/ADRs/amendments where present, relevant source, callers and tests. Requirements may be established by the current user request without a formal specification or approved task.

Assess correctness, requirement fit and repository fit against observable evidence. Inspect meaningful normal, edge, failure and compatibility behavior proportionate to risk. An undemonstrated risk is a question or limitation, not a verified bug. Preserve exact changed locations, severity, impact and test evidence. Never label tests passed without running or seeing trustworthy execution results.

Routine implementation does not automatically invoke this skill as a gate. No approval statuses, per-increment checkpoints or automatic `brain-update`. Save a durable report only when requested or materially useful. Do not edit production code in review-only mode.
