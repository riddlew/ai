# Pair-programming details (v5)

Pair programming supports informal code review/debugging and larger features with or without documentation. Select AI-led (default), developer-led or Learning Mode when not already chosen. Inline is automatic; subagents are explicitly opt-in and cannot violate code authorship rules.

AI-led implements only after explicit user authorization; explain meaningful choices and run proportionate tests. Developer-led supplies ready-to-copy code and reasons but developer edits; inspect actual resulting files rather than assuming suggestions were applied. Learning Mode supports the developer's independent ideas and debugging before direct code is requested; Claude never edits application code or tests.

An existing order cancellation feature, for example, might involve repository state, service eligibility, HTTP adapters and optimistic locking. Inspect real owners and tests; adapt order to actual dependencies rather than inventing a mandatory layered sequence. Discuss material new design decisions with the user. No approval pause after each increment; natural review and question pauses remain.

Keep optional execution/handoff files concise; do not require them for standalone review. Do not invoke `brain-update` automatically. Finish when user's requested pairing scope is complete.
