---
name: brain-pair-program
description: Work alongside the developer with optional specs/plans using AI-led, developer-led or Learning Mode.
---

# Pair programming

Accept ad-hoc questions, code review, design guidance, debugging or feature implementation without specifications, plans, tasks or execution records. Honor present governing decisions and current code. Select pair mode only if not already established for the conversation:
- **AI-led (default):** Claude implements user-authorized code, explains important choices and verifies changes.
- **Developer-led:** Claude proposes code and explains reasoning; developer edits application code; Claude reviews actual changes.
- **Learning Mode:** Developer designs, writes and debugs the code. Claude challenges assumptions, gives progressive hints and code on explicit request, and reviews real changes; Claude never edits application code.

Inline execution is default; subagents only if explicitly requested. No routine approval after each chunk; natural questions/reviews are welcome. Preserve mode authorship boundaries, code ownership, decisions, tests, and user edits. Important unestablished design changes require user decisions, not doc approvals. Use compact optional execution/handoff state only for multi-session continuity. For meaningful mid-implementation plan changes, use narrow amendments rather than cascading revisions.

Do not automatically invoke `brain-update`. Read `references/learning-mode.md` only when Learning Mode is selected; `references/pair-program-details.md` for specialized collaboration cases. Finish at the user's requested scope with concise verification.
