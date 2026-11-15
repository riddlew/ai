---
id: SPEC-001
kind: specification
status: approved
parents: [BRF-001]
requirements: []
depends_on: []
parent_hashes: [BRF-001@aafabfb7aae01896e0d03c1963d1552b81e8e1d0]
---
# StartMachine specification

## Requirements
- REQ-001: A valid StartMachine message reaches the correct machine execution path.
- REQ-002: A StartMachine request for an ineligible machine is rejected without changing machine state.
- REQ-003: Every processed request returns a protocol-conformant success or failure response.

## Examples
- E1: Given an eligible stopped machine, when a valid StartMachine message arrives, then the machine is started and success returned.
- E2: Given an ineligible machine, when a StartMachine message arrives, then its state remains unchanged and failure returned.
