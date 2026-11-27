# Optional executable tasks (v5)

Only create task documents when dependency coordination, parallelization or cross-session resumability materially justifies them. Direct implementation from a clear user request or brainstorming needs no tasks, spec or implementation plan.

If tasks are warranted, inspect actual code/tests, established behavior, applicable plans and amendments, and scope. Split into small independently verifiable behavior increments with real prerequisite links and concise acceptance evidence. Preserve qualified requirement IDs when a specification exists; don't fabricate placeholder parent plans. Use `brain-tool doc new --kind task` for optional new task files and stable TASK IDs.

Check dependencies for cycles, requirement references for validity, and user changes for scope. No document approval statuses, parent fingerprints, builder approval ceremony or automatic `brain-update`. Unresolved consequential decisions require consultation, not a task document gate.
