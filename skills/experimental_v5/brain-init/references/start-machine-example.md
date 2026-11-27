# StartMachine example — Brain v5 (illustrative)

A user requests a TCP server operation to start an eligible stopped machine and send a protocol-compliant response. The existing server, machine lifecycle and authoritative protocol contract must be inspected before changing code.

## Minimal workflow

`/brain-brainstorm` resolves eligibility, state transition semantics, message shape and failure outcomes using actual contracts. The user may then say `/brain-implement` and Claude implements and verifies directly. **No approved brief, specification, implementation blueprint, tasks, or `brain-update` call is required.**

If the feature is unusually complex, optional `SPEC-001` may declare `REQ-001` start eligibility and `REQ-002` response semantics with concrete examples. Optional `PLAN-001` may detail verified dispatcher and state owners. No approval status or parent fingerprint metadata is generated. Source contract remains authoritative.

If implementation begins and the user changes a significant design choice (e.g. transport response ownership), create a small `PLAN-002` with explicit `amends: [PLAN-001]` and `supersedes: [PLAN-001#response-owner]` only when the existing plan contains that anchor; preserve the rest of the plan. Minor method changes need no new document.

Run focused normal, failure and compatibility tests based on the actual protocol. Stop when verified; do not automatically invoke `brain-update`. The older v4 feature fixtures remain historical compatibility inputs, not v5 procedural guidance.
