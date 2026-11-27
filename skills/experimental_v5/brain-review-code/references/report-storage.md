# Optional review report storage (v5)

Reviews normally report findings in the conversation; store `.brain/reviews/<type>/<NN>-<slug>/review.md` only when the user requests persistence or substantial cross-session value justifies one. Use `brain-tool doc new --kind review --report-type architecture|code|merge-request|security` for safe scaffolding.

Keep scope, reviewed Git revisions, actual changed files, verified findings, severity, source references, limitations and executed test evidence. Review proposals are not authoritative product requirements; capture user-established decisions in their proper home separately. Never automatically invoke `brain-update` after saving a report. Do not duplicate normative specs or migrate historical review approvals.
