---
name: brain-review-security
description: Read-only trust-boundary security assessment grounded in actual code.
---

# Security review

Default inline. Trace relevant entry points, trust assumptions, auth checks, sensitive data and output sinks using actual code/config/tests. Develop realistic threat hypotheses, attempt to disprove them, and report verified risks and mitigation with residual uncertainty. Do not access live secrets or run disruptive tests. Consult user before material security-boundary changes; no document approval workflow. Reports optional unless requested. Never automatically invoke `brain-update`. See `references/security-review-details.md` for specialized threats.
