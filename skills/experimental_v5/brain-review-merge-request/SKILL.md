---
name: brain-review-merge-request
description: Read-only PR/MR review against actual changes and applicable requirements.
disable-model-invocation: true
---

# PR / MR review

Read-only. Inspect exact target/source SHAs, merge base, changes, relevant tests, CI and authoritative decisions/requirements/amendments. Verify prior comments against current code, distinguish findings from unanswered questions, and report material bugs with evidence, severity, locations and merge-blocking rationale. Do not edit, approve, comment, merge, or invoke `brain-update`. Save a report only when requested/useful. Default inline; see `references/mr-review-details.md` for remote-platform edge cases.
