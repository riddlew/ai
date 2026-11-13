# Durable Review Reports

Shared by `brain-review-architecture`, `brain-review-code`, `brain-review-merge-request`, and `brain-review-security`. Each skill determines **when** a report is saved; these rules determine **where and how**.

## Layout

Save each review in its own folder:

```text
.brain/reviews/<type>/<NN>-<short-slug>/review.md
```

`<type>` is `architecture`, `code`, `merge-request`, or `security`, matching the skill. Use a short, descriptive slug for the reviewed scope; number folders by incrementing the highest existing review number **within that type**, including legacy flat `<NN>-<slug>.md` reports. Keep existing zero-padding (two digits by default). If the folder name already exists, choose the next available number. Only review folders, not loose report files, belong directly under `.brain/reviews/<type>/` for new reports. Never overwrite or relocate previous reviews; legacy flat reports remain valid history.

Put the report in `review.md`. Related review artifacts, if explicitly needed, belong in that same review folder, not its parent. Do not create empty supporting files or speculative artifacts.

## Evidence and continuity

Record the review scope, current branch and Git `HEAD` SHA (or explain when unavailable), any material uncommitted state, evidence, limitations, and the date where time or version matters. Describe the findings as observations at review time, not accepted decisions or permanent facts.

For a repeat review of the same or overlapping scope, consult the most relevant previous saved reports, **including legacy flat reports**. Verify their findings against current code and classify them as still supported, resolved, no longer applicable, or unverified; do not blindly carry them forward. Identify newly discovered findings separately from newly introduced defects. If the comparison cannot be made, say what is missing. Previous reports are baselines, not authoritative evidence or proof of completeness.

After saving, invoke `brain-update` to index the new report. Do not promote unapproved review recommendations to ADRs or settled architecture. If the brain is unavailable or cannot be written, deliver the review in the conversation and disclose that no durable baseline was saved.
