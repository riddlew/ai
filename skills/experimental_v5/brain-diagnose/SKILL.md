---
name: brain-diagnose
description: Diagnose bugs and test failures with evidence; apply focused fixes only on explicit authorization.
---

# Diagnose

Investigate expected versus observed behavior, actual code and tests, Git state, relevant project contracts and reproducible failures. Form and discriminate causal hypotheses before modifying code. Do not repeat equivalent fixes or rerun unchanged failing tests without new evidence. Make a focused root-cause repair and regression test only when the user authorized a fix; risk-sensitive decisions require user consultation.

Stop when the cause is supported and the repair verified, or when no materially new diagnostic approach remains. Report symptoms, evidence, changed files, tests and uncertainty concisely. A persistent multi-session problem may warrant an optional diagnosis report; do not automatically call `brain-update`. Detailed techniques in `references/diagnose-details.md`, `flaky-failures.md` and `tracing.md`.
