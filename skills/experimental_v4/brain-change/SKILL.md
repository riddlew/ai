---
name: brain-change
description: Reconcile a change to an existing Brain feature by coordinating only the affected specification, component, implementation-plan, and task skills. Use after brainstorming or an ordinary discussion; never implement code.
disable-model-invocation: true
---

# Change — Reconcile Feature Documents

Given a proposed or agreed change, determine the **smallest necessary documentation revision path**, coordinate the owning skills, and preserve approvals. This is a **user-invoked, documentation-only** workflow. It never implements production changes.

## Workflow

1. **Establish the change.** Read the user's request and confirmed discussion outcome, then follow `CLAUDE.local.md` for Brain loading. Locate the feature's relevant approved brief, specifications, components, binding plans, tasks, decisions and `execution.md`, plus applicable code/tests. Do not assume previous chat sessions are accessible: if the decision was not recorded, ask for its confirmed summary. Never access `.brain/.notes/` by default.
2. **Classify and scope.** Distinguish changed observable behavior, functional component coverage, binding implementation design, executable tasks, root knowledge, and mere local illustrative implementation details. Identify affected IDs, requirement references and parent/descendant chains; do not automatically invalidate independent documents. Unresolved consequential decisions go to `brain-brainstorm` (or a focused question) before proceeding.
3. **Show the route.** Present a concise current → proposed change, source of the decision, affected artifacts, the smallest ordered skill sequence, preserved artifacts, and approval blockers. A request to update docs is not approval of an as-yet-unwritten revised specification or design.
4. **Invoke owning skills.** Use Claude Code's **Skill tool** to run the affected producer skills **sequentially** in dependency order with the feature, decision, IDs and scope: `brain-write-spec` → `brain-decompose-feature` (if affected) → `brain-design-implementation` (if affected) → `brain-write-tasks` (if affected). A design-only change starts at `brain-design-implementation`. Each owner validates and writes its own files; **`brain-change` does not write or approve producer-owned documents.** Pause and wait for required user approval at each stage before continuing with dependent stages. Do not silently refresh `parent_hashes` or assume an unchanged plan is current after its parent changed.
5. **Protect execution.** Preserve `execution.md`, existing code, uncommitted edits, tests and verified increments. Stop affected implementation while its documents are being revised; unrelated authorized work may continue. Do not invoke `brain-implement`, edit production code or commit changes. Approval of documents is not authorization to implement; resuming requires an explicit user request.
6. **Verify the handoff.** Check owner-reported approvals, requirement coverage, document references and fingerprints with the feature-document validator when possible. Invoke `brain-update` for shared root knowledge/index synchronization as appropriate, never to rewrite a producer's docs. Report completed, blocked and skipped stages, including the exact next command for any blocker.

**If the Skill tool cannot invoke a producer:** give the user the exact `/skill-name` command with a context-specific prompt and **stop before that stage**. Do not edit that skill's documents as a workaround, run a shell command to simulate invocation, or claim a printed command was executed.

Use `${CLAUDE_SKILL_DIR}/../brain-init/references/feature-document-contract.md` for owner/approval rules. **Read on demand:** `${CLAUDE_SKILL_DIR}/references/change-routing.md` for the routing matrix, examples and revision safety.

**Recommended next step:** End the final user-facing reply with one concise, evidence-based next action, naming the appropriate skill or command when useful. If blocked, identify the missing information, prerequisite, or approval instead of advancing; if complete, say no further action is needed. A recommendation is not authorization to execute another step. Keep it outside copy-ready deliverables.
