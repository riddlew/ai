---
id: CMP-002
kind: component
status: approved
parents: [SPEC-001]
requirements: [SPEC-001#REQ-001, SPEC-001#REQ-002]
depends_on: []
parent_hashes: [SPEC-001@577aa6f3076b9a3118c11bff50e43745c297243b]
---
# Machine execution

Invokes the existing machine start owner only for eligible targets. Rejects ineligible targets without state changes; returns an execution outcome for the response path.
