---
name: brain-decompose
description: Decompose approved specifications into coherent functional components with complete, traceable requirement coverage before code-level design.
disable-model-invocation: true
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
