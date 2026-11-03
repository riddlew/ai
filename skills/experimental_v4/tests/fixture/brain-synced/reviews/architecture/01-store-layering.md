# Store Layering Review

Scope: `crate/store.py`.

Finding: schema creation runs on every `connect()` call, alongside query helpers. At the current size this is acceptable; no change recommended.

Decisions Safe to Preserve: keep all SQL in `store.py`.
Decisions Requiring Approval: none.
