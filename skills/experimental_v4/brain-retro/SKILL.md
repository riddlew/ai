---
name: brain-retro
description: Inspect evidence from an implementation or review session to propose targeted improvements to Brain instructions, context retrieval, tests or tooling. Read-only, manually invoked, never an automatic post-review step.
disable-model-invocation: true
argument-hint: "[feature | PR | session] [--focus <workflow friction>]"
---

# Retro — Improve the Development Workflow

Use `/brain-retro` **only when explicitly invoked**. Identify avoidable process friction and recommend a few durable improvements. Unlike `brain-update` (which synchronizes project facts) and `brain-review-code` (which evaluates code quality and requirements), this skill evaluates **how the work was done**. It does not review or fix code, synchronize Brain knowledge, edit instructions, create reports, or open PRs.

## Workflow

1. **Confirm mode and scope.** Follow `CLAUDE.local.md` `Execution mode selection`; inline is recommended, but do not silently choose it or dispatch subagents. Use `$ARGUMENTS`, the active conversation, or an unambiguous named feature/PR to bound the retrospective. If several targets match, ask. Exclude `.brain/.notes/` from all discovery, reading and reporting unless the user explicitly authorizes specific notes. Do not load the entire Brain or all project history by default.
2. **Collect actual evidence.** Use relevant user-provided observations, currently available conversation context, a feature's `execution.md`, completed review findings, Git/diffs, and available test or tool outcomes. Read governing instructions only when needed to understand a plausible cause. **Never assume old chat transcripts, hidden agent logs, token counts, or tool timings are accessible.** Distinguish observed facts, user reports, inferences and missing evidence. Ask for a missing log or example only if it would materially change the conclusion.
3. **Find preventable causes, not just symptoms.** Look for repeated failed fixes, misunderstood contracts, duplicated investigation, hard-to-find Brain context, unnecessary tool calls, avoidable subagent/token use, and confusing or contradictory instructions. Separate a missing project fact (`brain-update`), an unclear workflow rule, a missing automated check, and an isolated one-off mistake. Trace each proposed improvement to the evidence; do not blame a skill without verifying the relevant instruction.
4. **Select at most 1–3 improvements.** Prefer small, actionable, maintainable changes to a named skill, policy file, knowledge entry, tool, or test. For each, state **evidence → likely cause (with confidence) → targeted change → expected benefit → how to verify**, including meaningful tradeoffs. No speculative process ceremony, duplicate records, artificial token-savings numbers, or recommendations to relax code-quality/approval checks. If evidence does not support a repeatable improvement, say **"No justified workflow change"**.
5. **Report only; do not execute.** Deliver a concise retrospective in the conversation with sources/limitations. Never edit source, tests, skills, `CLAUDE.local.md` or `.brain`; invoke `brain-update` or another skill; write a retrospective file; create an issue or PR; or schedule a recurring retro. A recommendation is **not** authorization to act. If the user later requests changes, route them explicitly to the appropriate owner without treating that later request as part of this read-only invocation.

**Read on demand:** `${CLAUDE_SKILL_DIR}/references/retro-details.md` for evidence thresholds, example reporting, distinctions from `brain-update` and how to avoid low-value recommendations.

**Recommended next step:** End the final user-facing reply with one concise, evidence-based next action, naming the appropriate skill or command when useful. If blocked, identify the missing information, prerequisite, or approval instead of advancing; if complete, say no further action is needed. A recommendation is not authorization to execute another step. Keep it outside copy-ready deliverables.
