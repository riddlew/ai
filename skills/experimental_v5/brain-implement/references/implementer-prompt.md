# Optional subagent implementer brief (v5)

Use **only after the user explicitly opts into subagents**. Provide a bounded real task, authorized files, authoritative decision/requirement references, relevant current source, baseline revision and negative constraints. Avoid pasting full specs where stable source references suffice.

The agent may edit only explicitly authorized application/test files within the assigned scope. Respect existing user changes and current project policy. Implement the smallest coherent behavior, run relevant tests and report exact results/diff and uncertainty. Do not invent requirements, modify approval/status metadata, invoke `brain-update`, commit or silently redesign material architecture.

Return: changed files, test results, scope deviations and blockers. The coordinator verifies actual output before reporting completion.
