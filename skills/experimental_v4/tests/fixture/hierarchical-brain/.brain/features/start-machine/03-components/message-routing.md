---
id: CMP-001
kind: component
status: approved
parents: [SPEC-001]
requirements: [SPEC-001#REQ-001, SPEC-001#REQ-003]
depends_on: []
parent_hashes: [SPEC-001@577aa6f3076b9a3118c11bff50e43745c297243b]
---
# Message routing

Routes StartMachine requests through the established TCP dispatcher and ensures the caller receives a formatted response. Does not own the machine lifecycle.
