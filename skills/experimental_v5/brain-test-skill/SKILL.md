---
name: brain-test-skill
description: Test skill behavior against observable scenarios and explicit criteria when agent runner available.
---

# Test a skill

Define actual observable criteria, then compare baseline and modified behavior in isolated disposable fixtures using the same model, wrapper and inputs. Default inline; never auto-dispatch subagents. Running fresh-agent behavioral tests requires an explicitly authorized subagent mode and available agent runner. When not available, report **No behavioral test run** and perform clearly labeled static contract review if useful. Grade actual files, replies and code evidence; never invent run results or claim general reliability from one sample. No automatic `brain-update`. See `references/skill-testing-details.md`.
