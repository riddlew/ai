---
id: TASK-001
kind: task
status: approved
parents: [PLAN-002]
requirements: [SPEC-001#REQ-001, SPEC-001#REQ-002]
depends_on: []
parent_hashes: [PLAN-002@d5d402099b012b2d5c5cc9206b4e36574a3359b7]
---
# Implement machine execution

Extend the existing machine owner. Given a valid eligible request, start the machine; otherwise return failure without state change. Verify specification examples E1 and E2.
