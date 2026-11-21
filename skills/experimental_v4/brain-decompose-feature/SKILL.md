---
name: brain-decompose-feature
description: Decompose approved specifications into coherent functional components with complete, traceable requirement coverage before code-level design.
---

# Decompose

Create **functional components** only when a feature benefits from explicit responsibility and requirement-coverage boundaries. Do not invent new services, architectures or extra levels to satisfy a ceremony.

## Workflow

1. Read confirmed specifications, requirements/examples, decisions, current owners, callers, tests and relevant source/ADRs.
2. Partition functionality into the smallest coherent responsibility groups. Preserve existing ownership unless the user approved a change; identify interfaces and cross-component coverage without prescribing unapproved implementation architecture.
3. When useful, scaffold drafts under `.brain/features/<feature-slug>/03-components/` with `brain-tool doc new --kind component`; supply actual approved parents, requirement references, dependencies and evidence. Skip this level when unnecessary.
4. Verify the participating specification's requirement coverage and missing/overlapping ownership. Validate structural references and status; seek approval for consequential ownership changes before approving.
5. Report component IDs, coverage, exclusions and the appropriate blueprint handoff; invoke `brain-update` when documents changed.

Use `${CLAUDE_SKILL_DIR}/../brain-init/references/feature-document-contract.md`. **Read on demand:** `${CLAUDE_SKILL_DIR}/references/decompose-details.md` for multi-parent/split features, overlap analysis and detailed review procedure; `../brain-init/references/deterministic-tooling.md` for CLI.


**Writing:** Follow `${CLAUDE_SKILL_DIR}/../brain-init/references/compact-writing.md` when recording Brain facts: concise, evidence-complete entries without duplicated narrative. Do not reformat unrelated existing files solely for style.

**Recommended next step:** End the final user-facing reply with one concise, evidence-based next action, naming the appropriate skill or command when useful. If blocked, identify the missing information, prerequisite, or approval instead of advancing; if complete, say no further action is needed. A recommendation is not authorization to execute another step. Keep it outside copy-ready deliverables.
